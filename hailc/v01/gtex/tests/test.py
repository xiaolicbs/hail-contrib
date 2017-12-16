"""
Unit tests for gtex hail modules
"""

import unittest
# import filecmp

from hail import *
import methods

hc = None


def setUpModule():
    global hc
    hc = HailContext()
    methods.patch()


def tearDownModule():
    global hc
    hc.stop()
    hc = None


def create_vds(rows, schema, types):
    return (VariantDataset.from_table(KeyTable.from_py(hc,
                                                       rows,
                                                       TStruct(schema, types),
                                      key_names=['v'])))


class GTExFilteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rows1 = [
            {'v': Variant.parse('1:100:A:T'), 'filters': [], 'expect_filters': []},
            {'v': Variant.parse('1:200:A:T'), 'filters': ['LOWQUAL'], 'expect_filters': ['LOWQUAL']},
            {'v': Variant.parse('1:300:A:T'), 'filters': ['VQSR'], 'expect_filters': ['VQSR']},
            {'v': Variant.parse('1:400:A:T'), 'filters': [], 'expect_filters': ['OTHER']},
            {'v': Variant.parse('1:500:A:T'), 'filters': [], 'expect_filters': ['MonoAfterGTFilter']}
        ]

        rows2 = [
            {'v': Variant.parse('1:100:A:T'), 'filters': [], 'expect_filters': []},
            {'v': Variant.parse('1:400:A:T'), 'filters': [], 'expect_filters': []},
            {'v': Variant.parse('1:500:A:T'), 'filters': [], 'expect_filters': []}
        ]

        rows3 = [
            {'v': Variant.parse('1:100:A:T'), 'filters': [], 'expect_filters': []},
            {'v': Variant.parse('1:400:A:T'), 'filters': [], 'expect_filters': []}
        ]

        rows4 = [
            {'v': Variant.parse('1:100:A:T'), 'filters': [], 'expect_filters': []}
        ]

        rows5 = [
            {'v': Variant.parse('1:100:A:T'), 'filters': ['VQSR'], 'expect_filters': []},
            {'v': Variant.parse('1:100:A:T'), 'filters': ['VQSR', 'LCR'], 'expect_filters': ['LCR']},
            {'v': Variant.parse('1:100:A:T'), 'filters': [], 'expect_filters': []},
            {'v': Variant.parse('1:100:A:T'), 'filters': ['LOW', 'LCR'], 'expect_filters': ['LOW', 'LCR']},
            {'v': Variant.parse('1:100:A:T'), 'filters': ['LOW'], 'expect_filters': ['LOW']}
        ]
        schema = ['v', 'filters', 'expect_filters']
        types = [TVariant(), TSet(TString()), TSet(TString())]
        cls.vds1 = create_vds(rows1, schema, types)
        cls.vds2 = create_vds(rows2, schema, types)
        cls.vds3 = create_vds(rows3, schema, types)
        cls.vds4 = create_vds(rows4, schema, types)
        cls.vds5 = create_vds(rows5, schema, types)


    def test_flag_removed_sites(self):
        result_vds = (self.vds1
                      .flag_removed_sites(self.vds2, self.vds3,
                                          'MonoAfterGTFilter')
                      .flag_removed_sites(self.vds3, self.vds4, "OTHER"))
        correct = self.vds1.query_variants('variants.map(v => va.filters == va.expect_filters).count()')
        self.assertEqual(correct, self.vds1.count_variants())


    def test_remove_va_filter(self):
        result_vds = (self.vds5.remove_va_filter('VQSR'))
        print(result_vds.variants_table().show(5))
        correct = self.vds5.query_variants('variants.map(v => va.filters == va.expect_filters).count()')



if __name__ == '__main__':
    unittest.main()
