"""Verificações de identidade bibliográfica, sem abrir PDFs."""
import unittest
from build_master_corpus import identity, normalize_title, key

class IdentityTests(unittest.TestCase):
    def test_same_doi_different_title(self):
        self.assertEqual(identity({'doi':'https://doi.org/10.123/ABC','title':'Original'}),identity({'doi':'10.123/abc','title':'Tradução'}))

    def test_unicode_is_preserved(self):
        self.assertNotEqual(normalize_title('会话设计'),normalize_title('对话系统'))
        self.assertTrue(normalize_title('대화형 디자인'))

    def test_distinct_identifiers_remain_distinct(self):
        self.assertNotEqual(identity({'source_id':'repository:1','title':'Same'}),identity({'source_id':'repository:2','title':'Same'}))

    def test_document_doi_matching(self):
        self.assertEqual(key({'doi':'10.123/a','title':'A'}),key({'doi':'https://doi.org/10.123/A','title':'B'}))

if __name__=='__main__':
    unittest.main()
