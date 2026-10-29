"""Regression checks: accidental renumbering must stop builds, not bless assets."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from icon_identity import validate_identities


class IdentityProtectionTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.ledger = {'schemaVersion': 1, 'icons': [
            {'id': 'first', 'unicode': 'E001', 'fallback': '!'},
            {'id': 'second', 'unicode': 'E002', 'fallback': '"'}]}
        self.save()
        self.entries = [('first', 0xE001, '!'), ('second', 0xE002, '"')]

    def save(self):
        (self.root / 'icon-identities.json').write_text(json.dumps(self.ledger), encoding='utf-8')

    def test_unchanged_and_reordered_records_pass(self):
        self.assertEqual(validate_identities(self.entries, self.root), 2)
        self.assertEqual(validate_identities(list(reversed(self.entries)), self.root), 2)

    def test_renumbering_and_fallback_changes_fail(self):
        for record in [('first', 0xE003, '!'), ('first', 0xE001, '#')]:
            with self.subTest(record=record), self.assertRaisesRegex(ValueError, 'identity changed'):
                validate_identities([record, self.entries[1]], self.root)

    def test_removal_and_rename_fail(self):
        for records in [self.entries[1:], [('renamed', 0xE001, '!'), self.entries[1]]]:
            with self.subTest(records=records), self.assertRaisesRegex(ValueError, 'removed or renamed'):
                validate_identities(records, self.root)

    def test_duplicate_or_reused_codepoint_fails(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate Unicode'):
            validate_identities(self.entries + [('third', 0xE001, '#')], self.root)

    def test_unregistered_addition_fails(self):
        with self.assertRaisesRegex(ValueError, 'Unregistered'):
            validate_identities(self.entries + [('third', 0xE003, '#')], self.root)

    def test_registered_append_passes(self):
        self.ledger['icons'].append({'id': 'third', 'unicode': 'E003', 'fallback': '#'})
        self.save()
        self.assertEqual(validate_identities(self.entries + [('third', 0xE003, '#')], self.root), 3)

    def test_inserting_old_codepoint_fails(self):
        self.ledger['icons'].append({'id': 'third', 'unicode': 'E000', 'fallback': '#'})
        self.save()
        with self.assertRaisesRegex(ValueError, 'strictly above'):
            validate_identities(self.entries + [('third', 0xE000, '#')], self.root)

    def test_missing_ledger_fails_closed(self):
        (self.root / 'icon-identities.json').unlink()
        with self.assertRaisesRegex(ValueError, 'cannot be skipped'):
            validate_identities(self.entries, self.root)


if __name__ == '__main__':
    unittest.main()
