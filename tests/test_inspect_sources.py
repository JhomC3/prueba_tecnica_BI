"""Controles de lectura: defectos no ocultos y texto original preservado."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "inspection", Path(__file__).resolve().parents[1] / "scripts/inspect_sources.py"
)
inspection = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspection)


class InspectionTests(unittest.TestCase):
    def inspect(self, content):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.csv"
            path.write_text(content, encoding="utf-8")
            return inspection.inspect_csv(path)

    def test_bom_quotes_and_missing_values(self):
        result = self.inspect('\ufeffID,label\n1,"a,b"\n2,\n2,\n')
        self.assertEqual(result["columns"], ["ID", "label"])
        self.assertEqual(result["samples"][0]["values"], ["1", "a,b"])
        self.assertEqual(result["missing_by_column"], {"ID": 0, "label": 2})
        self.assertEqual(result["duplicate_rows"], 1)

    def test_malformed_and_blank_records_are_visible(self):
        result = self.inspect('ID,amount\n1,0\n2\n,\n3,NaN\n')
        self.assertEqual(result["rows"], 4)
        self.assertEqual(result["malformed_rows"], 1)
        self.assertEqual(result["empty_records"], [3])
        self.assertEqual(result["amount"]["invalid_records"], [4])
        self.assertEqual(result["amount"]["zero_rows"], 1)

    def test_report_escapes_source_text(self):
        self.assertEqual(inspection.cell('<script>'), '&lt;script&gt;')


if __name__ == "__main__":
    unittest.main()
