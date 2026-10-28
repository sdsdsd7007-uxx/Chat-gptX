import csv
import json
import os
import tempfile
import unittest
from pathlib import Path

from project_q.inventory_scanner import InventoryError, create_inventory


class InventoryScannerTests(unittest.TestCase):
    def make_tree(self, base):
        root = Path(base) / "source"
        (root / "nested").mkdir(parents=True)
        (root / "nested" / "a.txt").write_text("alpha", encoding="utf-8")
        (root / "b.txt").write_text("beta", encoding="utf-8")
        return root

    def test_records_root_directories_and_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_tree(tmp)
            out = Path(tmp) / "reports" / "inventory.csv"
            manifest = create_inventory(str(root), str(out))
            with out.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            kinds = [row["item_type"] for row in rows]
            self.assertEqual(kinds.count("directory"), 2)
            self.assertEqual(kinds.count("file"), 2)
            self.assertEqual(manifest["directory_count"], 2)
            self.assertEqual(manifest["file_count"], 2)
            self.assertEqual(manifest["source_writes"], 0)
            self.assertTrue(manifest["snapshot_sha256"])

    def test_symlink_file_and_directory_are_rejected_without_following(self):
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "source"
            outside = Path(tmp) / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "secret.txt").write_text("outside", encoding="utf-8")
            (root / "escape-file.txt").symlink_to(outside / "secret.txt")
            (root / "escape-dir").symlink_to(outside, target_is_directory=True)
            out = Path(tmp) / "inventory.csv"
            manifest = create_inventory(str(root), str(out))
            with out.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            rejected = [row for row in rows if row["exception_reason"] == "SYMLINK_REJECTED_NOT_FOLLOWED"]
            self.assertEqual(len(rejected), 2)
            self.assertEqual(manifest["symlink_rejected_count"], 2)
            self.assertNotIn("secret.txt", [row["item_name"] for row in rows])
            self.assertEqual((outside / "secret.txt").read_text(encoding="utf-8"), "outside")

    def test_source_root_symlink_is_rejected(self):
        if not hasattr(os, "symlink"):
            self.skipTest("symlinks unavailable")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "source"
            root.mkdir()
            alias = Path(tmp) / "alias"
            alias.symlink_to(root, target_is_directory=True)
            with self.assertRaises(InventoryError):
                create_inventory(str(alias), str(Path(tmp) / "out.csv"))

    def test_output_inside_source_root_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_tree(tmp)
            with self.assertRaises(InventoryError):
                create_inventory(str(root), str(root / "inventory.csv"))

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_tree(tmp)
            out = Path(tmp) / "inventory.csv"
            out.write_text("preserve", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                create_inventory(str(root), str(out))
            self.assertEqual(out.read_text(encoding="utf-8"), "preserve")

    def test_snapshot_digest_is_reproducible_for_unchanged_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_tree(tmp)
            first = create_inventory(str(root), str(Path(tmp) / "one.csv"))
            second = create_inventory(str(root), str(Path(tmp) / "two.csv"))
            self.assertEqual(first["snapshot_sha256"], second["snapshot_sha256"])

    def test_manifest_records_scope_and_unknown_permissions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.make_tree(tmp)
            out = Path(tmp) / "inventory.csv"
            manifest = create_inventory(str(root), str(out), source_system="synthetic-test")
            self.assertEqual(manifest["source_system"], "synthetic-test")
            self.assertFalse(manifest["cloud_permissions_reviewed"])
            self.assertEqual(manifest["source_writes"], 0)


if __name__ == "__main__":
    unittest.main()
