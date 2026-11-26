"""Render compact review sections from evidence and the current diff."""
from collections import defaultdict
from html import escape
from pathlib import Path


def coverage_rows(root, target, coverage, added, file_ids):
    if coverage is None:
        return '<p>No added-line coverage measurement.</p>'
    path = (root / coverage['path']).resolve()
    if Path(coverage['path']).is_absolute() or not path.is_relative_to(root) or coverage['revision'] != target['head']:
        raise ValueError('Coverage must come from the reviewed head and record folder.')
    measured = defaultdict(dict)
    source = None
    for row in path.read_text(encoding='utf-8').splitlines():
        if row.startswith('SF:'):
            source = row[3:].removeprefix('./')
        elif row == 'end_of_record':
            source = None
        elif row.startswith('DA:') and source in added:
            line, hits, *_ = row[3:].split(',')
            line, hits = int(line), int(hits)
            if line in added[source]:
                measured[source][line] = measured[source].get(line, False) or hits > 0
    total = sum(map(len, measured.values()))
    if not total:
        raise ValueError('LCOV has no measured added lines. Use repository-relative source paths.')
    covered = sum(sum(lines.values()) for lines in measured.values())
    rows = ''.join(
        f'<li><a href="#{file_ids[file]}" title="{escape(file)}">{escape(Path(file).name)}</a>'
        f'<span>{sum(lines.values())}/{len(lines)} lines</span></li>'
        for file, lines in sorted(measured.items()) if lines
    )
    return (
        f'<p><strong>{covered / total:.0%}</strong> · {covered}/{total} measured added lines</p>'
        f'<p class="section-note">{escape(coverage["scope"])}</p>'
        '<details><summary>Coverage by file</summary><ul class="evidence-rows">'
        + rows + '</ul></details>'
    )


def extra_sections(root, record, copy, findings, index, file_ids, added, line_ids):
    def source_link(item):
        path = item.get('path')
        if path is None:
            return ''
        line = item.get('line')
        target = file_ids[path] if line is None else line_ids[(path, line)]
        label = Path(path).name + (f':{line}' if line is not None else '')
        return f' <a class="code-link" href="#{target}" title="{escape(path)}">{escape(label)}</a>'

    def panel(identity, title, content, style=''):
        return f'<section class="report-panel {style}" id="{identity}"><h2>{title}</h2>{content}</section>'

    requirements = {r['id']: r for r in record['requirements']}
    lookup = {f['id']: i for i, f in enumerate(findings, 1)}
    plan_items = copy.get('plan', [])
    plan_states = {'done': 'Done', 'issue': 'Issue found', 'partial': 'Partial',
                   'unverified': 'Unverified', 'outside': 'Outside plan'}
    plan_rows = []
    for item in plan_items:
        status = item['status']
        req = requirements.get(item.get('requirement'))
        if status != 'outside' and req is None:
            raise ValueError('Link each plan item to a requirement ID.')
        if status in ('done', 'issue') and not item.get('evidence'):
            raise ValueError('Describe the evidence for this plan result.')
        if status == 'done' and req.get('gap'):
            raise ValueError('A requirement with a recorded gap cannot be marked done.')
        note = item.get('evidence') or (req.get('gap') if req else '') or ''
        plan_rows.append(
            f'<li><span class="check-state {status}">{plan_states[status]}</span>'
            f'<span>{escape(item["title"])}{source_link(item)}'
            + (f'<small>{escape(note)}</small>' if note else '') + '</span></li>'
        )
    planned = sum(i['status'] != 'outside' for i in plan_items)
    done = sum(i['status'] == 'done' for i in plan_items)
    plan = panel('plan', 'Plan check',
                 f'<p class="section-note">{done}/{planned} done</p><ul class="status-rows">{"".join(plan_rows)}</ul>'
                 if plan_rows else '<p>No plan results recorded.</p>')

    merge_ids = dict.fromkeys([f['id'] for f in findings if f['priority'] <= 1] + copy.get('merge_findings', []))
    merge_rows = []
    for identifier in merge_ids:
        number = lookup[identifier]
        tag, title, *_ = index[number - 1]
        merge_rows.append(f'<li>{tag} <a href="#comment-{number}">{title}</a></li>')
    for item in copy.get('merge_notes', []):
        merge_rows.append(f'<li>{escape(item["text"])}{source_link(item)}</li>')
    merge = panel('merge', 'Before you merge', f'<ul>{"".join(merge_rows)}</ul>', 'merge') if merge_rows else ''

    target = record['target']
    flows = []
    for flow in copy.get('flows', []):
        steps = []
        for item in flow['steps']:
            state = {'new': 'New', 'changed': 'Changed', 'existing': 'Unchanged'}[item['state']]
            steps.append(f'<li><span class="check-state">{state}</span>'
                         f'<span>{escape(item["text"])}{source_link(item)}</span></li>')
        flows.append(f'<div class="flow"><h3>{escape(flow["title"])}</h3>'
                     f'<ol class="status-rows">{"".join(steps)}</ol></div>')
    flow_panel = panel('flows', 'How it works', ''.join(flows)) if flows else ''

    coverage = coverage_rows(root, target, copy.get('coverage'), added, file_ids)
    gaps = ''.join(f'<li>{escape(gap)}</li>' for gap in copy.get('test_gaps', []))
    tests = panel('coverage', 'Tests', coverage + (f'<h3>Test gaps</h3><ul>{gaps}</ul>' if gaps else ''))
    return {'plan': plan, 'merge': merge, 'flows': flow_panel, 'coverage': tests}


def check_sections(record, copy, findings):
    checks = record['checks']
    notes = copy.get('check_notes', {})
    project = copy.get('project_checks', {})
    history = copy.get('check_history', {})
    check_ids = {check['id'] for check in checks}
    if (notes.keys() | project.keys() | history.keys()) - check_ids:
        raise ValueError('Check presentation refers to an unknown check ID.')
    states = {'passed': 'Passed', 'failed': 'Failed', 'blocked': 'Blocked',
              'not_run': 'No run', 'timeout': 'Time limit'}
    history_states = {'setup': 'Setup error', 'observation': 'Observation'}

    review_runs = [
        check for check in checks
        if (check['status'] != 'passed' if check['id'] in project else check['id'] in notes)
    ]
    review_ids = {check['id'] for check in review_runs}
    other_runs = [check for check in checks if check['id'] not in review_ids]
    if history.keys() - {check['id'] for check in other_runs}:
        raise ValueError('Run history presentation must refer to an additional run.')

    findings_by_check = defaultdict(list)
    for number, finding in enumerate(findings, 1):
        for key in finding['checks']:
            findings_by_check[key].append(number)

    def row(check, archived=False):
        key, status = check['id'], check['status']
        presentation = project.get(key, {})
        entry = history.get(key, {}) if archived else {}
        kind = entry.get('kind')
        label = entry.get('label') or presentation.get('label') or notes.get(key, key)
        detail = f'<small>{escape(notes[key])}</small>' if presentation and key in notes else ''
        if archived:
            detail += f'<small><code>{escape(key)}</code>'
            if kind:
                detail += f' · Run status {states[status]}'
            detail += '</small>'
        if presentation and check.get('command'):
            detail += (
                '<details class="check-command"><summary>Command</summary>'
                f'<code>{escape(check["command"])}</code></details>'
            )
        if presentation.get('duration'):
            detail += f'<small>{escape(presentation["duration"])}</small>'
        state = history_states[kind] if kind else states[status]
        label = escape(label)
        linked = findings_by_check[key]
        if not archived and status == 'failed' and len(linked) == 1:
            label = f'<a href="#comment-{linked[0]}">{label}</a>'
        return (
            f'<li class="check-row"><span class="check-state {kind or status}">{state}</span>'
            f'<div class="check-copy">{label}{detail}</div></li>'
        )

    def rows(runs, archived=False):
        return '<ul class="check-rows">' + ''.join(row(check, archived) for check in runs) + '</ul>'

    review_counts = ' · '.join(
        f'{count} {label.lower()}' for state, label in states.items()
        if (count := sum(check['status'] == state for check in review_runs))
    )
    review_panel = (
        '<section class="check-panel" aria-labelledby="review-checks-title">'
        '<div class="check-heading"><h3 id="review-checks-title">Review checks</h3>'
        f'<span class="check-count">{review_counts}</span></div>{rows(review_runs)}</section>'
    ) if review_runs else ''
    run_count = len(other_runs)
    run_word = 'run' if run_count == 1 else 'runs'
    archive_link = f'<a href="#more-runs">{run_count} more {run_word}</a>' if other_runs else ''
    verification = (
        '<section id="verification" aria-labelledby="verification-title">'
        '<div class="section-heading"><h2 id="verification-title">Verification</h2>'
        f'{archive_link}</div>{review_panel}</section>'
    ) if checks else ''
    evidence = '<section id="checks"><h2>Test results</h2>'
    evidence += rows(review_runs) if review_runs else ''
    if other_runs:
        evidence += (
            '<details class="other-checks" id="more-runs">'
            f'<summary>Run history <span>{run_count} {run_word}</span></summary>'
            f'{rows(other_runs, archived=True)}</details>'
        )
    return verification, evidence + '</section>' if checks else ''
