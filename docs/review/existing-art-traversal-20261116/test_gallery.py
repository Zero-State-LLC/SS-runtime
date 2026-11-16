#!/usr/bin/env python3
"""Portable gallery checks only, not real browser sizing or visual acceptance."""
from html.parser import HTMLParser
import unittest
from PIL import Image
import build_gallery as g
import verify_capture as v

class Tags(HTMLParser):
    def __init__(self): super().__init__(); self.tags=[]
    def handle_starttag(self,tag,attrs): self.tags.append((tag,dict(attrs)))

class GalleryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        g.build(); cls.text=(g.HERE/'index.html').read_text(); cls.tags=Tags(); cls.tags.feed(cls.text)
    def test_actual_capture_census_and_hashes(self):
        packet=v.load(g.HERE/'capture/eat-records.json')
        captures=[c for a in packet['arms'] for c in a['captures']]
        self.assertEqual(len(captures),52)
        for c in captures:
            path=g.HERE/'capture'/f'{c["name"]}.png'
            self.assertEqual(v.sha(path),c['sha256'])
            with Image.open(path) as image: self.assertEqual(list(image.size),c['nativePixels'])
    def test_links_and_all_keypoint_mapping_combinations(self):
        for tag,attrs in self.tags.tags:
            if tag=='a': self.assertTrue((g.HERE/attrs['href']).is_file())
        packet=v.load(g.HERE/'capture/eat-records.json')
        names={c['name'] for a in packet['arms'] for c in a['captures']}
        for arm in ('normal','reduced'):
            for phase in [n for n,_ in v.LEGS]+['pause']:
                for mapping in v.MAPPINGS:
                    self.assertIn(f'eat-{arm}-{phase}-{mapping}',names)
        self.assertLess(self.text.index('value="shipping"'),self.text.index('value="midpoint-post-action-still"'))
    def test_truthful_controls_and_logical_sizes(self):
        for phrase in ('not coherent repaired scene','not live midpoint display','different framing','not a renderer output','overflow:auto','352:704','163:326','grayscale(1)','max-width:none'):
            self.assertIn(phrase,self.text.lower())
        self.assertIn("style.height='auto'",self.text)

if __name__=='__main__': unittest.main()
