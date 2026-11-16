#!/usr/bin/env python3
"""Portable HTML/CSS/path checks. Not browser or native-test evidence."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

HERE=Path(__file__).resolve().parent

class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids={}
        self.references=[]
        self.options={}
        self.select=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                raise ValueError('Duplicate HTML id')
            self.ids[attrs['id']]=(tag,attrs)
        if tag=='select':
            self.select=attrs['id']
            self.options[self.select]=[]
        if tag=='option':
            self.options[self.select].append(attrs['value'])
        for name in ('href','src'):
            if name in attrs:
                self.references.append(attrs[name])
    def handle_endtag(self,tag):
        if tag=='select':
            self.select=None

class GalleryStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(HERE/'index.html').read_text()
        cls.css=(HERE/'gallery.css').read_text()
        cls.js=(HERE/'gallery.js').read_text()
        cls.page=Markup()
        cls.page.feed(cls.html)

    def test_01_controls_and_accessible_labels(self):
        self.assertEqual(self.page.options,{'capture':['1040','1030','1020'],'zoom':['1','1.25','1.4'],'arm':['paired','control','candidate'],'size':['native','half']})
        for name in ('capture','zoom','arm','size','grayscale'):
            self.assertIn(f'for="{name}"',self.html)
        self.assertEqual(self.page.ids['grayscale'][1]['type'],'checkbox')

    def test_02_initial_missing_evidence_is_fail_closed(self):
        self.assertIn('disabled',self.page.ids['controls'][1])
        self.assertIn('Missing evidence:',self.html)
        self.assertEqual(self.page.ids['error'][1]['role'],'alert')
        self.assertIn("element('captures').replaceChildren()",self.js)
        self.assertNotIn('data:image',self.html+self.js)

    def test_03_native_logical_css_sizes_do_not_shrink(self):
        for size,w,h in [('native',704,326),('half',352,163)]:
            self.assertRegex(self.css,rf'#captures\[data-size="{size}"\].*--logical-width: {w}px; --logical-height: {h}px;')
        rule=re.search(r'\.capture-image\s*\{([^}]+)',self.css).group(1)
        self.assertIn('max-width: none',rule)
        self.assertIn('height: var(--logical-height)',rule)
        self.assertIn('overflow: auto',self.css)

    def test_04_exact_relative_paths_and_no_remote_dependencies(self):
        expected={'gallery.css','gallery.js','../../stone-painted-facade-20261116/inputs/benchmark.png'}
        self.assertEqual(set(self.page.references),expected)
        for reference in self.page.references:
            self.assertNotIn('://',reference)
        self.assertTrue((HERE/'gallery.js').is_file())
        self.assertTrue((HERE/'gallery.css').is_file())
        benchmark=(HERE/'../../stone-painted-facade-20261116/inputs/benchmark.png').resolve()
        self.assertEqual(benchmark,HERE.parent.parent/'stone-painted-facade-20261116/inputs/benchmark.png')
        self.assertTrue(benchmark.is_file())

    def test_05_reference_uniform_fit_and_no_crop(self):
        rule=re.search(r'#benchmark\s*\{([^}]+)',self.css).group(1)
        self.assertIn('height: auto',rule)
        self.assertIn('object-fit: contain',rule)
        self.assertNotIn('object-fit: cover',self.css)

    def test_06_scope_labels_and_no_source_verdict(self):
        for text in ('Quiet presentation-only reposition','Original authority fields and solids retained','not encounter','owner-acceptance','does not assign a source verdict'):
            self.assertIn(text,self.html)
        self.assertIn('Structure tests are not browser',self.html)

    def test_07_importer_status_version_and_census_contract(self):
        for constant in ('NATIVE_QUIET_SOURCE_COMPARISON_NOT_ACCEPTANCE','source-scene-continuation-002-three-zooms','source-scene-continuation-003-upright-census','source-scene-continuation-004-depth-order'):
            self.assertIn(constant,self.js)
        self.assertIn('value="1040" selected',self.html)
        self.assertIn('hidden',self.page.ids['evidence-links'][1])
        for guard in ('verification.nativeTests === 1','verification.captures === 6','verification.images === 18','record.captures.length === 6'):
            self.assertIn(guard,self.js)
        self.assertIn("capture.name + suffix + '.png'",self.js)
        self.assertIn("grayscale ? '-grayscale'",self.js)
        self.assertNotIn('-half-grayscale',self.js)

    def test_08_png_hash_and_size_checked_before_enabling(self):
        self.assertIn("hash(recordBytes)",self.js)
        self.assertIn('hash(bytes) === file.digest',self.js)
        self.assertIn('image.naturalWidth === file.pixels[0]',self.js)
        self.assertLess(self.js.index('image.naturalWidth === file.pixels[0]'),self.js.index("element('controls').disabled = false"))
        self.assertNotIn('.decode()',self.js)

if __name__=='__main__':
    unittest.main(verbosity=2)
