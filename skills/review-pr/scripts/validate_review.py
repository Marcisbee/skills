#!/usr/bin/env python3
"""Validate a private review record against local Git objects. Read operations only."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def validate(record, repo, artifact_root):
    errors, limits = [], []

    def error(where, message):
        errors.append(f'{where}: {message}')

    def text(value, where):
        if not isinstance(value, str) or not value.strip():
            error(where, 'use nonempty text')
            return False
        return True

    def path(value, where, dot=False):
        if not text(value, where):
            return False
        parts = PurePosixPath(value)
        if parts.is_absolute() or '..' in parts.parts or (value == '.' and not dot):
            error(where, 'use a relative path without ..')
            return False
        return True

    def rows(name):
        value = record.get(name)
        if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
            error(name, 'use an array of objects')
            return []
        return value

    def names(items, name, key='id'):
        result = set()
        for item in items:
            value = item.get(key)
            if text(value, f'{name}.{key}'):
                if value in result:
                    error(name, f'duplicate {key}: {value}')
                result.add(value)
        return result

    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.PIPE)

    target = record.get('target', {})
    if not isinstance(target, dict):
        error('target', 'use an object')
        target = {}
    revisions = {}
    for key in ['base', 'head', 'merge_base']:
        value = target.get(key)
        if not isinstance(value, str) or not re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', value):
            error(f'target.{key}', 'use a full Git commit ID')
            continue
        try:
            if git('rev-parse', f'{value}^{{commit}}').decode().strip() != value:
                raise ValueError()
            revisions[key] = value
        except (subprocess.CalledProcessError, ValueError):
            error(f'target.{key}', 'commit is not in this repository')
    for key in ['base_repo', 'head_repo', 'base_ref']:
        text(target.get(key), f'target.{key}')

    blobs = {}

    def blob(revision, name):
        identity = (revision, name)
        if identity not in blobs:
            if git('cat-file', '-t', f'{revision}:{name}').strip() != b'blob':
                raise ValueError('use a source file: ' + name)
            blobs[identity] = git('show', f'{revision}:{name}')
        return blobs[identity]

    def reference(ref, where, changed=False):
        if not isinstance(ref, dict):
            error(where, 'use a code reference object')
            return
        name, side = ref.get('path'), ref.get('side', 'new')
        if not path(name, where + '.path'):
            return
        if side not in ['new', 'old']:
            error(where + '.side', 'use new or old')
            return
        revision = revisions.get('head' if side == 'new' else 'merge_base')
        if not revision:
            return
        try:
            content = blob(revision, name)
        except ValueError as exc:
            error(where, str(exc))
            return
        except subprocess.CalledProcessError:
            error(where, f'{name} does not exist on side {side}')
            return
        line = ref.get('line')
        if line is None:
            text(ref.get('note'), where + '.note')
        elif type(line) is not int or not 1 <= line <= len(content.splitlines()) or b'\0' in content:
            error(where + '.line', f'use a source line in {name} on side {side}')
            return
        if changed:
            primary = next((p for p, pair in changed_paths.items() if name == pair[side]), None)
            if primary is None:
                error(where, f'{name} is not a changed path on side {side}')
                return
            pair = changed_paths[primary]
            diff = git('diff', '--no-ext-diff', '--no-textconv', '--unified=0', '--find-renames',
                       revisions['merge_base'], revisions['head'], '--',
                       *sorted({':(literal)' + value for value in pair.values() if value}))
            hunks = re.findall(rb'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', diff, re.M)
            if hunks:
                ranges = [(int(h[0 if side == 'old' else 2]), int(h[1 if side == 'old' else 3] or b'1')) for h in hunks]
                if line is None or not any(start <= line < start + count for start, count in ranges):
                    error(where + '.line', 'anchor must use a changed line')

    changed_paths = {}
    if 'merge_base' in revisions and 'head' in revisions:
        tokens = iter(git('diff', '--name-status', '-z', '--find-renames', revisions['merge_base'], revisions['head']).decode().rstrip('\0').split('\0'))
        for status in tokens:
            if not status:
                continue
            first = next(tokens)
            old, new = (first, next(tokens)) if status[0] in 'RC' else (first, first)
            changed_paths[new] = {'old': old if status[0] != 'A' else '',
                                  'new': new if status[0] != 'D' else ''}
    files = rows('files')
    file_names = names(files, 'files', 'path')
    for name in sorted(set(changed_paths) - file_names):
        error('files', 'missing changed file: ' + name)
    for name in sorted(file_names - set(changed_paths)):
        error('files', 'not a changed file: ' + name)
    for item in files:
        if item.get('status') not in ['read', 'blocked']:
            error('files', 'use status read or blocked')
        text(item.get('note'), 'files.note')
        if item.get('status') == 'blocked':
            limits.append('file: ' + str(item.get('path')))

    def strings(value, where, empty=False):
        if not isinstance(value, list) or (not value and not empty):
            error(where, 'use an array of text values')
            return []
        for item in value:
            text(item, where)
        return [item for item in value if isinstance(item, str) and item.strip()]

    def artifact(name, where, digest=None):
        if not path(name, where):
            return
        file = (artifact_root / name).resolve()
        try:
            file.relative_to(artifact_root)
            value = file.read_bytes()
        except (ValueError, OSError):
            error(where, 'artifact must exist in the record folder')
            return
        if digest is not None and hashlib.sha256(value).hexdigest() != digest:
            error(where, 'artifact hash does not agree')

    checks = rows('checks')
    check_ids = names(checks, 'checks')
    check_by_id = {c.get('id'): c for c in checks if isinstance(c.get('id'), str)}

    def check_links(value, where):
        linked = strings(value, where, empty=True)
        for identity in linked:
            if identity not in check_ids:
                error(where, 'unknown check: ' + identity)
        return linked

    statuses = ['passed', 'failed', 'timeout', 'blocked', 'not_run']
    for item in checks:
        where = 'checks.' + str(item.get('id'))
        for key in ['command', 'result']:
            text(item.get(key), where + '.' + key)
        path(item.get('cwd'), where + '.cwd', dot=True)
        strings(item.get('paths'), where + '.paths')
        status, exit_code = item.get('status'), item.get('exit_code')
        if status not in statuses:
            error(where + '.status', 'use passed, failed, timeout, blocked or not_run')
        if item.get('revision') != revisions.get('head'):
            error(where + '.revision', 'test revision does not agree with target.head')
        if status == 'passed' and (type(exit_code) is not int or exit_code != 0):
            error(where + '.exit_code', 'passed result must have exit code 0')
        if status == 'failed' and (type(exit_code) is not int or exit_code == 0):
            error(where + '.exit_code', 'failed result must have a nonzero exit code')
        if status in ['blocked', 'not_run', 'timeout']:
            limits.append(where)
        sources = item.get('sources', {})
        if not isinstance(sources, dict) or not sources:
            error(where + '.sources', 'record the source files and SHA-256 hashes for this plan')
        else:
            for name, digest in sources.items():
                if not path(name, where + '.sources') or 'head' not in revisions:
                    continue
                try:
                    observed = hashlib.sha256(blob(revisions['head'], name)).hexdigest()
                    if observed != digest:
                        error(where + '.sources', 'plan source hash does not agree: ' + name)
                except ValueError as exc:
                    error(where + '.sources', str(exc))
                except subprocess.CalledProcessError:
                    error(where + '.sources', 'plan source is missing: ' + name)
        if status in ['passed', 'failed', 'timeout']:
            if not text(item.get('log_sha256'), where + '.log_sha256'):
                continue
            artifact(item.get('log'), where + '.log', item['log_sha256'])
        elif item.get('log'):
            artifact(item['log'], where + '.log', item.get('log_sha256'))

    requirements = rows('requirements')
    names(requirements, 'requirements')
    if not requirements:
        text(record.get('requirements_note'), 'requirements_note')
    for item in requirements:
        where = 'requirements.' + str(item.get('id'))
        for key in ['text', 'source']:
            text(item.get(key), where + '.' + key)
        paths = strings(item.get('paths'), where + '.paths', empty=True)
        for name in paths:
            reference({'path': name, 'note': 'requirement mapping'}, where + '.paths')
        linked = check_links(item.get('checks', []), where + '.checks')
        if not paths or not linked or any(check_by_id.get(c, {}).get('status') != 'passed' for c in linked):
            text(item.get('gap'), where + '.gap')
        if item.get('gap'):
            limits.append(where)

    findings = rows('findings')
    names(findings, 'findings')
    for item in findings:
        where = 'findings.' + str(item.get('id'))
        if type(item.get('priority')) is not int or item['priority'] not in range(4):
            error(where + '.priority', 'use an integer from 0 to 3')
        for key in ['trigger', 'effect', 'evidence', 'counterevidence', 'fix']:
            text(item.get(key), where + '.' + key)
        reference(item.get('location'), where + '.location', changed=True)
        refs = item.get('references')
        if not isinstance(refs, list) or not refs:
            error(where + '.references', 'include source references for the evidence')
        else:
            for ref in refs:
                reference(ref, where + '.references')
        check_links(item.get('checks', []), where + '.checks')

    browser = rows('browser')
    names(browser, 'browser')
    for item in browser:
        where = 'browser.' + str(item.get('id'))
        for key in ['route', 'expected', 'fixtures', 'result']:
            text(item.get(key), where + '.' + key)
        strings(item.get('paths'), where + '.paths')
        strings(item.get('actions'), where + '.actions')
        viewport = item.get('viewport')
        if not isinstance(viewport, list) or len(viewport) != 2 or any(type(n) is not int or n <= 0 for n in viewport):
            error(where + '.viewport', 'use two positive integer dimensions')
        if item.get('revision') != revisions.get('head'):
            error(where + '.revision', 'browser revision does not agree with target.head')
        if item.get('status') not in ['passed', 'failed', 'blocked', 'not_run']:
            error(where + '.status', 'use passed, failed, blocked or not_run')
        if item.get('status') in ['passed', 'failed']:
            identity = item.get('check')
            if not isinstance(identity, str) or identity not in check_ids:
                error(where + '.check', 'unknown check: ' + str(identity))
            elif check_by_id[identity].get('status') != item['status']:
                error(where + '.check', 'browser and check status do not agree')
        else:
            limits.append(where)
        for name in strings(item.get('artifacts', []), where + '.artifacts', empty=True):
            artifact(name, where + '.artifacts')
    return errors, limits, len(findings)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--repo', required=True, type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding='utf-8'))
        if not isinstance(record, dict):
            raise ValueError('record must be an object')
        errors, limits, count = validate(record, args.repo.resolve(), args.record.resolve().parent)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f'Cannot validate record: {exc}\n')
    for error in errors:
        print(error)
    if errors:
        return 1
    print(f'Record structure and code references agree: {count} findings.')
    if limits:
        print('Scope limits: ' + ', '.join(limits))
    print('A reviewer must examine the evidence. This tool does not show defect correctness or test execution.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
