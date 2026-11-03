"""Negative and positive tests for the SVG security/structure gate."""
import tempfile
import unittest
from pathlib import Path
from scripts.validate_profile import validate_svg

SVG = """<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 900 240" role="img" aria-labelledby="t d">
  <title id="t">Card title</title><desc id="d">Useful summary</desc>
  <rect width="900" height="240" fill="#0B1020"/>
</svg>"""


class SVGValidatorTests(unittest.TestCase):
    def check(self, contents):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / "card.svg"
            file.write_text(contents, encoding="utf-8")
            return validate_svg(file)

    def test_accepts_pure_accessible_svg(self):
        self.assertEqual([], self.check(SVG))

    def test_rejects_missing_description(self):
        self.assertTrue(self.check(SVG.replace("<desc id=\"d\">Useful summary</desc>", "")))

    def test_rejects_duplicate_ids(self):
        self.assertTrue(self.check(SVG.replace('fill="#0B1020"', 'id="t" fill="#0B1020"')))

    def test_rejects_raster_embedding(self):
        self.assertTrue(self.check(SVG.replace("</svg>", '<image href="data:image/png;base64,AAAA"/></svg>')))

    def test_rejects_external_dependency(self):
        self.assertTrue(self.check(SVG.replace("</svg>", '<a href="https://example.org"/></svg>')))

    def test_rejects_event_handlers(self):
        self.assertTrue(self.check(SVG.replace('<rect width=', '<rect onmouseover="go()" width=')))


if __name__ == "__main__":
    unittest.main()
