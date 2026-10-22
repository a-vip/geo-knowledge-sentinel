import unittest
from scripts.geo_engine import score_geo_readiness, build_knowledge_graph

class TestGEOEngine(unittest.TestCase):
    def test_geo_scoring(self):
        sample_content = """
        The V-BAT 5.3 achieves 12 hours of flight time with a heavy fuel engine.
        According to Shield AI, "the Hivemind autonomy operates in GPS-denied contested environments."
        Evaluated under Article 36 of the Geneva Conventions and UNIDIR guidelines.
        """
        metrics = score_geo_readiness("V-BAT MQ-35", sample_content)
        self.assertGreaterEqual(metrics["score"], 70)
        self.assertGreater(metrics["stats_count"], 0)
        self.assertGreater(metrics["quote_count"], 0)
        self.assertGreater(metrics["citation_count"], 0)

    def test_knowledge_graph_structure(self):
        posts = [{"title": {"rendered": "Test"}, "link": "https://aviperera.com/test/", "date_gmt": "2026-10-22"}]
        kg = build_knowledge_graph(posts)
        self.assertEqual(kg["@context"], "https://schema.org")
        self.assertTrue(len(kg["@graph"]) >= 2)
        author = kg["@graph"][0]
        self.assertEqual(author["name"], "Avi Perera")
        self.assertIn("https://www.wikidata.org/wiki/Q140248356", author["sameAs"])

if __name__ == "__main__":
    unittest.main()
