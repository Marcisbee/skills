#!/usr/bin/env python3
"""Render the reviewed commits and final comments as one offline HTML file."""
import argparse
import base64
from html import escape
import json
from pathlib import Path
import re
import subprocess

from validate_review import validate
from report_sections import check_sections, extra_sections


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def section(title, items, identity, ordered=False):
    items = list(items)
    if not items:
        return ''
    tag = 'ol' if ordered else 'ul'
    return f'<section id="{identity}"><h2>{title}</h2><{tag}>' + ''.join(
        f'<li>{item}</li>' for item in items
    ) + f'</{tag}></section>'


def prose(value):
    return re.sub(r"`([^`\n]+)`", r"<code>\1</code>", escape(value))


def render(repo, record, copy, root):
    target = record['target']
    diff_args = ['diff', '--no-ext-diff', '--no-textconv', '--no-color', '--find-renames',
                 '--submodule=short',
                 target['merge_base'], target['head'], '--']
    names = iter(git(repo, *diff_args[:1], '--name-status', '-z', *diff_args[1:]).decode().split('\0'))
    files = []
    for status in names:
        if not status:
            break
        first = next(names)
        second = next(names) if status[0] in 'RC' else first
        files.append((status, first, second))
    patch = git(repo, *diff_args[:1], '--patch', '--unified=3', *diff_args[1:]).decode('utf-8', 'replace')
    patches = re.split(r'^diff --git ', patch, flags=re.M)[1:]
    if len(files) != len(patches):
        raise ValueError('The patch and file list differ.')

    findings = sorted(record['findings'], key=lambda f: f['priority'])
    comments = copy['comments']
    if set(comments) != {f['id'] for f in findings}:
        raise ValueError('Supply one comment for each finding ID in the record.')
    by_line = {}
    index = []
    for number, finding in enumerate(findings, 1):
        comment = comments[finding['id']]
        if not all(isinstance(comment.get(key), str) and comment[key].strip() for key in ('title', 'body')):
            raise ValueError(f'Missing title or body for {finding["id"]}.')
        path = finding['location']['path']
        side = finding['location'].get('side', 'new')
        line = finding['location']['line']
        priority = finding['priority']
        tag = f'<span class="priority p{priority}">P{priority}</span>'
        title = prose(comment['title'])
        site = ''
        if comment.get('thread'):
            url = comment['thread']
            if not re.fullmatch(r'https://[^\s\\"<>]+', url):
                raise ValueError('Use an HTTPS URL for the previous comment.')
            site = f'<p><a rel="noreferrer" href="{escape(url)}">Previous comment</a></p>'
        card = (
            f'<article class="comment" id="comment-{number}" tabindex="-1">'
            f'<h3>{tag} {title}</h3><p class="body">{prose(comment["body"])}</p>{site}'
            f'<a href="#finding-{number}">Back to comment</a></article>'
        )
        by_line.setdefault((path, side, line), []).append(card)
        index.append((tag, title, prose(comment['body']), path, line, priority))

    review_files = {row['path']: row['status'] for row in record['files']}
    file_ids = {new: f'file-{n}' for n, (_, _, new) in enumerate(files, 1)}
    groups = []
    assigned = set()
    for group in copy.get('change_groups', []):
        paths = group['paths']
        if not paths or len(paths) != len(set(paths)) or set(paths) & assigned or set(paths) - file_ids.keys():
            raise ValueError('Each review group must list changed paths once.')
        assigned.update(paths)
        groups.append((group['title'], group.get('summary', ''), paths))
    remainder = [path for path in file_ids if path not in assigned]
    if remainder:
        commented = {finding['location']['path'] for finding in findings}
        priority_paths = [new for _, old, new in files if new in remainder and (new in commented or old in commented)]
        if priority_paths:
            groups.append(('Files with comments', '', priority_paths))
        other = [path for path in remainder if path not in priority_paths]
        if other:
            groups.append(('Other changed files' if groups else 'Changed files', '', other))
    ordered_paths = [path for _, _, paths in groups for path in paths]
    neighbors = {
        path: (ordered_paths[i - 1] if i else None, next_path)
        for i, (path, next_path) in enumerate(zip(ordered_paths, ordered_paths[1:] + [None]))
    }
    group_names = {path: title for title, _, paths in groups for path in paths}
    file_aliases = {old: new for _, old, new in files}
    nav = []
    blocks = {}
    removed = {}
    added = {}
    line_ids = {}
    for number, ((status, old, new), patch) in enumerate(zip(files, patches), 1):
        label = escape(new if old == new else f'{old} → {new}')
        file_id = f'file-{number}'
        folder, _, name = new.rpartition('/')
        nav.append((new,
            f'<li><a href="#{file_id}" title="{label}"><span class="file-state">{escape(status[0])}</span>'
            f'<span><strong>{escape(name or new)}</strong><small>{escape(folder)}</small></span></a></li>'
        ))
        rendered = []
        added[new] = set()
        removed[new] = 0
        old_line = new_line = None
        for row in patch.split('\n')[1:-1]:
            if old_line is None and row.startswith(('index ', '--- ', '+++ ')):
                continue
            hunk = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', row)
            before = after = None
            kind = 'meta'
            if hunk:
                old_line, new_line = map(int, hunk.groups())
            elif old_line is not None and row[:1] in (' ', '-', '+'):
                kind = {' ': 'context', '-': 'remove', '+': 'add'}[row[0]]
                if kind == 'remove':
                    removed[new] += 1
                if kind != 'add':
                    before = old_line
                    old_line += 1
                if kind != 'remove':
                    after = new_line
                    new_line += 1
            if after is not None:
                line_ids[new, after] = f'line-{number}-new-{after}'
                if kind == 'add':
                    added[new].add(after)
            ids = []
            cards = []
            for path, side, line in [(old, 'old', before), (new, 'new', after)]:
                if line is not None:
                    line_id = f'line-{number}-{side}-{line}'
                    cards.extend(by_line.pop((path, side, line), []))
                    ids.append(line_id)
                else:
                    ids.append('')
            columns = []
            for identity, line in zip(ids, (before, after)):
                attr = f' id="{identity}"' if identity else ''
                columns.append(f'<span class="number"{attr}>{line if line is not None else ""}</span>')
            rendered.append(f'<div class="row {kind}">{"".join(columns)}<code>{escape(row)}</code></div>')
            rendered.extend(cards)
        for path, side in [(old, 'old'), (new, 'new')]:
            rendered.extend(by_line.pop((path, side, None), []))
        marker = ' · Scope limit' if review_files[new] == 'blocked' else ''
        prev, next_path = neighbors[new]
        links = ''.join(
            f'<a href="#{file_ids[path]}">{caption}</a>'
            for path, caption in [(prev, 'Previous file'), (next_path, 'Next file')] if path
        )
        file_nav = (f'<nav class="file-step" aria-label="Review order"><strong>{escape(group_names[new])}</strong>'
                    f'<label><input type="checkbox" class="viewed" value="{file_id}"> Mark as viewed</label>{links}</nav>')
        totals = (f'<span class="diff-totals"><span>+{len(added[new])}</span> '
                  f'<span>−{removed[new]}</span></span>')
        blocks[new] = (
            f'<details class="file" id="{file_id}"><summary>'
            f'<span class="file-caption"><span class="file-status">{escape(status)}</span> {label}{marker}</span>'
            f'{totals}</summary>{file_nav}<div class="diff">{"".join(rendered)}</div></details>'
        )
    if by_line:
        raise ValueError(f'Comment locations missing from the patch: {list(by_line)}')
    cards = []
    file_comments = {}
    for number, (tag, title, body, path, line, priority) in enumerate(index, 1):
        label = escape(path.rsplit('/', 1)[-1]) + (f':{line}' if line is not None else '')
        cards.append(
            f'<article class="finding" id="finding-{number}" tabindex="-1">'
            f'<details{" open" if priority <= 1 else ""}><summary>{tag} '
            f'<span>{title}<small title="{escape(path)}">{label}</small></span></summary>'
            f'<p class="body">{body}</p></details>'
            f'<a class="action" href="#comment-{number}">View diff <span aria-hidden="true">↗</span></a>'
            '</article>'
        )
        side = findings[number - 1]['location'].get('side', 'new')
        file_path = file_aliases.get(path, path) if side == 'old' else path
        file_comments.setdefault(file_path, []).append(number)
    comment_section = (
        '<section id="comments"><h2>Comments</h2>'
        + (''.join(cards) or '<p class="empty-state">No code defects found.</p>')
        + '</section>'
    )

    group_cards = []
    path_links = []
    for number, (title, summary, paths) in enumerate(groups, 1):
        comments_here = sorted(number for path in paths for number in file_comments.get(path, []))
        notes = []
        for n in comments_here:
            tag, title_text, _, path, line, _ = index[n - 1]
            location = escape(path.rsplit('/', 1)[-1]) + (f':{line}' if line is not None else '')
            notes.append(f'<li>{tag}<a href="#inline-comment-{n}">{title_text}</a>'
                         f'<code title="{escape(path)}">{location}</code></li>')
        notes_html = f'<ul class="group-notes">{"".join(notes)}</ul>' if notes else ''
        slots = ''.join(f'<div class="file-slot">{blocks[path]}</div>'
                        for path in paths)
        file_total = f'{len(paths)} file' + ('s' if len(paths) != 1 else '')
        totals = (f'<span class="diff-totals"><span>+{sum(len(added[p]) for p in paths)}</span> '
                  f'<span>−{sum(removed[p] for p in paths)}</span></span>')
        group_id = f'change-group-{number}'
        ids = ' '.join(file_ids[path] for path in paths)
        progress = f'<span class="group-progress" data-files="{ids}">0/{len(paths)}</span>'
        path_links.append(f'<li><span class="path-number" aria-hidden="true">{number}</span>'
                          f'<a href="#{group_id}">{escape(title)}</a>{progress}</li>')
        priority = {'focus': 'Read first', 'skim': 'Skim', '': ''}.get(
            copy.get('group_focus', {}).get(title, ''), ''
        )
        badge = f' <span class="priority">{priority}</span>' if priority else ''
        group_cards.append(
            f'<details class="review-group" id="{group_id}"><summary><span class="step">{number:02}</span>'
            f'<span><strong>{escape(title)}</strong>{badge}'
            + (f'<small>{escape(summary)}</small>' if summary else '') + '</span>'
            f'<span class="group-count">{file_total} {totals} {progress}</span></summary>'
            f'<div class="group-content">{notes_html}<div class="inline-files">{slots}</div></div></details>'
        )
    order = ('<section id="review-order"><h2>Changes in review order</h2>'
             + ''.join(group_cards) + '</section>') if groups else ''

    checks, evidence_checks = check_sections(record, copy, findings)

    extras = extra_sections(root, record, copy, findings, index, file_ids, added, line_ids)
    path_nav = (
        '<nav id="review-path" aria-label="Review path"><h2>Review path</h2>'
        f'<span id="viewed-total">0/{len(files)}</span>'
        f'<progress id="viewed-meter" aria-label="Files viewed" value="0" max="{len(files) or 1}"></progress>'
        '<ol>' + ''.join(path_links) + '</ol>'
        + ('<a href="#verification">Verification</a>' if checks else '')
        + ('<a href="#flows">How it works</a>' if extras['flows'] else '')
        + '<a href="#coverage">Tests</a></nav>'
    )

    screenshots = []
    for screenshot in copy.get('screenshots', []):
        path = (root / screenshot['path']).resolve()
        if not path.is_relative_to(root) or Path(screenshot['path']).is_absolute():
            raise ValueError('Use screenshot paths relative to the record folder.')
        payload = path.read_bytes()
        if path.suffix.lower() == '.png' and payload.startswith(b'\x89PNG\r\n\x1a\n'):
            mime = 'image/png'
        elif path.suffix.lower() in ('.jpg', '.jpeg') and payload.startswith(b'\xff\xd8\xff'):
            mime = 'image/jpeg'
        else:
            raise ValueError(f'Use a PNG or JPEG screenshot: {path.name}')
        data = base64.b64encode(payload).decode('ascii')
        caption = escape(screenshot['caption'])
        screenshots.append(f'<figure><img loading="lazy" src="data:{mime};base64,{data}" alt="{caption}">'
                           f'<figcaption>{caption}</figcaption></figure>')
    template = Path(__file__).resolve().parents[1] / 'assets' / 'review.html'
    title = escape(copy['title'])
    facts = ''.join(
        f'<dt>{label}</dt><dd><code>{escape(target[key])}</code></dd>'
        for label, key in [('Head repository', 'head_repo'), ('Head commit', 'head'),
                           ('Base repository', 'base_repo'), ('Base branch', 'base_ref'),
                           ('Base commit', 'base'), ('Merge base', 'merge_base')]
    )
    blocked = sum(status == 'blocked' for status in review_files.values())
    nav_by_path = dict(nav)
    parts = {
        **extras,
        'pathnav': path_nav,
        'title': title,
        'summary': ''.join(f'<p>{escape(p)}</p>' for p in copy.get('summary', [])),
        'commentcount': str(len(findings)),
        'filecount': str(len(files)),
        'repo': escape(target['head_repo']),
        'revision': escape(target['head']),
        'head': escape(target['head'][:8]),
        'label': escape(copy['label']) + ' · ' if copy.get('label') else '',
        'limited': f'<small>{blocked} files with scope limits</small>' if blocked else '',
        'facts': facts,
        'nav': ''.join(nav_by_path[path] for path in ordered_paths),
        'order': order,
        'checks': checks,
        'comments': comment_section,
        'details': evidence_checks
        + section('Scope limits', map(escape, copy.get('limits', [])), 'limits')
        + section('Questions and suggestions', map(escape, copy.get('notes', [])), 'notes')
        + ('<section><h2>Browser screenshots</h2><div class="screenshots">' + ''.join(screenshots)
           + '</div></section>' if screenshots else ''),
        'files': '' if files else '<p>No changed files.</p>',
    }
    return re.sub(r'@@([a-z]+)@@', lambda m: parts[m[1]], template.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('record', type=Path)
    parser.add_argument('copy', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        record_path = args.record.resolve()
        record = json.loads(record_path.read_text(encoding='utf-8'))
        errors, _, _ = validate(record, args.repo.resolve(), record_path.parent)
        if errors:
            raise ValueError('\n'.join(errors))
        copy = json.loads(args.copy.read_text(encoding='utf-8'))
        html = render(args.repo.resolve(), record, copy, record_path.parent)
        with args.output.open('x', encoding='utf-8') as output:
            output.write(html)
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
