import unittest

from resume_kit.corpus import load_corpus


class CorpusTests(unittest.TestCase):
    def test_load_corpus_has_required_sources(self):
        corpus = load_corpus()
        keys = {source.key for source in corpus.sources}
        self.assertIn("fact_baseline", keys)
        self.assertIn("resume_ai_agent", keys)

    def test_extract_evidence_contains_agent_project(self):
        corpus = load_corpus()
        ids = {item.id for item in corpus.evidence}
        self.assertIn("personal-content-distribution-agent", ids)
