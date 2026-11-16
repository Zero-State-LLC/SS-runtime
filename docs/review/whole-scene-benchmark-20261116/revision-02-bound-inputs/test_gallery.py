#!/usr/bin/env python3
"""Portable gallery structure/link checks, separate from retained real-browser sizing."""
import json
from pathlib import Path
from html.parser import HTMLParser
import unittest
import build_gallery as g

class Tags(HTMLParser):
    def __init__(self): super().__init__(); self.tags=[]
    def handle_starttag(self, tag, attrs): self.tags.append((tag,dict(attrs)))

class GalleryTests(unittest.TestCase):
    def testAll54SelectionsExistAndOrdinaryIsPrimary(self):
        g.build(); text=(g.HERE/'index.html').read_text(); parsed=Tags(); parsed.feed(text)
        names=[a['value'] for t,a in parsed.tags if t=='option' and a.get('value','').startswith('r02-')]
        self.assertEqual(len(names),18); self.assertEqual(len(set(names)),18)
        self.assertIn('-ordinary-',names[0])
        for name in names:
            for sheet in ('native','half','grayscale'): self.assertTrue((g.HERE/f'capture/{name}-{sheet}.png').is_file())
        for t,a in parsed.tags:
            if t=='a': self.assertTrue((g.HERE/a['href']).is_file(),a['href'])
    def testHonestSizingAndStatus(self):
        text=(g.HERE/'index.html').read_text()
        for phrase in ('NOT visual acceptance','STAGED is secondary','not a renderer output','different aspect','overflow:auto','352:704','163:326','grayscale(1)'):
            self.assertIn(phrase.lower(),text.lower())
    def testRetainedRealBrowserMeasurements(self):
        proof=json.loads((g.HERE/'browser-validation.json').read_text())
        self.assertEqual(proof['checked'],54); self.assertEqual(proof['errors'],[])
        self.assertEqual(proof['nativeCSS'],[704,326]); self.assertEqual(proof['halfCSS'],[352,163])
        self.assertEqual(proof['benchmarkNatural'],[1672,941])

if __name__=='__main__': unittest.main()
