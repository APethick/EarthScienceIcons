"""Fail-closed validation of the append-only, published icon identity ledger.

This module only reads the ledger. Builds must never regenerate it from sources
or generated assets: doing that could silently approve a renumbered icon.
"""
import json
from pathlib import Path


def validate_identities(entries, root=None):
    """Validate (id, codepoint, fallback) records before writing any assets."""
    root = Path(root) if root is not None else Path(__file__).resolve().parent
    path = root / 'icon-identities.json'
    if not path.is_file():
        raise ValueError('Missing icon-identities.json; identity protection cannot be skipped')
    ledger = json.loads(path.read_text(encoding='utf-8'))
    if ledger.get('schemaVersion') != 1 or not ledger.get('icons'):
        raise ValueError('Invalid icon identity ledger')
    locked = [(item['id'], int(item['unicode'], 16), item['fallback']) for item in ledger['icons']]
    if any(current[1] <= previous[1] for previous, current in zip(locked, locked[1:])):
        raise ValueError('Identity ledger must append codepoints strictly above all previous allocations')
    actual = list(entries)
    for records, label in ((locked, 'ledger'), (actual, 'catalogue')):
        for index, field in enumerate(('ID', 'Unicode codepoint', 'fallback character')):
            values = [row[index] for row in records]
            if len(values) != len(set(values)):
                raise ValueError(f'Duplicate {field} in icon {label}')
        for identifier, codepoint, fallback in records:
            if not 0xE000 <= codepoint <= 0xF8FF or len(fallback) != 1:
                raise ValueError(f'Invalid icon identity: {identifier}')
    by_id = {row[0]: row for row in actual}
    for identifier, codepoint, fallback in locked:
        if identifier not in by_id:
            raise ValueError(f'Published icon removed or renamed: {identifier}; retain its glyph and identity')
        current = by_id[identifier]
        if current[1] != codepoint or current[2] != fallback:
            raise ValueError(f'Published icon identity changed: {identifier}; must remain U+{codepoint:04X} with fallback {fallback!r}')
    unregistered = set(by_id) - {row[0] for row in locked}
    if unregistered:
        raise ValueError('Unregistered icons: ' + ', '.join(sorted(unregistered)) +
                         '; append new identities to icon-identities.json; never edit existing entries')
    return len(locked)


def validate_sources(icons, fallback_keys, root=None):
    if len(icons) > len(fallback_keys):
        raise ValueError('Insufficient stable printable fallback keys')
    return validate_identities(((icon['id'], icon['codepoint'], fallback_keys[index])
                                for index, icon in enumerate(icons)), root)


def validate_manifest(catalog, root=None):
    return validate_identities(((icon['id'], icon['codepoint_int'], icon['ascii_key'])
                                for icon in catalog['icons']), root)
