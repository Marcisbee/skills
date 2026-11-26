#!/usr/bin/env python3
"""Small prose gate, not an ASD-STE100 dictionary or compliance certificate."""
import argparse
from pathlib import Path
import re
import sys

# These ordinary uses failed a dictionary audit. This is not a full dictionary.
WORDS = re.compile(
    r'\b(?:now|still|both|needs?|requires?|required|requiring|avoid(?:s|ed|ing)?|'
    r'confirm(?:s|ed|ing)?|valid|wrong|absent|reach(?:es|ed|ing)?|relevant|'
    r'remain(?:s|ed|ing)?|identical|unavailable|every|existing|inconsistent|'
    r'inspect(?:s|ed|ing)?|checked|checking|tested|testing)\b', re.I)
# CHECK and TEST are nouns in STE. Do not reject their noun uses.
COMMAND = re.compile(
    r'(?:^|[.!?;:]\s*|\bthen\s+)(check|test)\s+'
    r'(?=(?:the|a|an|that|whether|all|each|both|two|three|it|this|these|those)\b)', re.I)


def prose_blocks(raw):
    """Keep soft line wraps in one block. Preserve source line numbers."""
    block, start, fence = [], 0, None
    for number, line in enumerate(raw.splitlines(), 1):
        stripped = line.strip()
        marker = re.match(r'^(`{3,}|~{3,})', stripped)
        if marker:
            if block:
                yield start, ' '.join(block)
                block = []
            char = marker[1][0]
            if fence is None:
                fence = char
            elif fence == char:
                fence = None
            continue
        if fence is not None:
            continue
        boundary = re.match(r'^(?:#{1,6}\s|[-*+]\s|\d+\.\s|\|)', stripped)
        if not stripped or boundary:
            if block:
                yield start, ' '.join(block)
                block = []
        if stripped:
            if not block:
                start = number
            block.append(stripped)
    if block:
        yield start, ' '.join(block)


def findings(raw):
    for line, block in prose_blocks(raw):
        # Exact code names count as one unit. They do not enter the vocabulary pass.
        text = re.sub(r'(`+)(.+?)\1', ' CODE ', block)
        text = re.sub(r'\[([^\]]+)\]\([^\n]*?\)', r'\1', text)
        text = re.sub(r'https?://\S+', ' LINK ', text)
        text = re.sub(r'^\s*(?:#{1,6}\s+|\d+\.\s+|[-*+]\s+|>\s*)', '', text)
        text = text.replace('**', '').replace('__', '')
        if ';' in text:
            yield line, 'semicolon in prose'
        for match in WORDS.finditer(text):
            yield line, 'word/form: ' + match[0]
        for match in COMMAND.finditer(text):
            yield line, 'noun used as a command: ' + match[1]
        # A conservative house limit: 20 words in descriptions and instructions.
        for sentence in re.split(r'(?<=[.!?])\s+', text):
            tokens = re.findall(r"[\w]+(?:[-’'][\w]+)*", sentence)
            if len(tokens) > 20:
                yield line, f'{len(tokens)} words in one sentence (limit 20)'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('draft', type=Path)
    args = parser.parse_args()
    try:
        raw = args.draft.read_text(encoding='utf-8')
    except (OSError, UnicodeError) as error:
        parser.exit(2, f'Cannot read draft: {error}\n')
    faults = list(findings(raw))
    for line, message in faults:
        print(f'{args.draft}:{line}: {message}')
    if faults:
        print('Revise the prose. Do the dictionary and meaning audit too.')
        return 1
    print('Mechanical gate passed. Do the dictionary and meaning audit too.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
