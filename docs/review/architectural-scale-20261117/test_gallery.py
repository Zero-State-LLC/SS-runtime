"""Check every static review link and the complete comparison image census."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.images = []
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'img':
            self.images.append(values)
        if tag == 'a':
            self.links.append(values['href'])


def local_file(href):
    path = (HERE / 'gallery' / href).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Gallery link escapes repository')
    if not path.is_file():
        raise ValueError('Missing gallery dependency: ' + href)
    return path


class GalleryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (HERE / 'gallery/index.html').read_text()
        cls.page = Page(cls.text)

    def test_exact_image_census(self):
        self.assertEqual(len(self.page.images), 8)
        self.assertEqual(len({row['src'] for row in self.page.images}), 8)
        actual = {row['src'] for row in self.page.images if '/source/output/' in row['src']}
        expected = {f'../source/output/{arm}-z{zoom}.png'
                    for arm in ('current', 'proposed') for zoom in (100, 125, 140)}
        self.assertEqual(actual, expected)

    def test_all_images_decode_and_are_described(self):
        for row in self.page.images:
            with self.subTest(src=row['src']):
                self.assertTrue(row.get('alt'))
                with Image.open(local_file(row['src'])) as image:
                    image.load()
                    self.assertGreater(image.width, 0)
                    self.assertGreater(image.height, 0)

    def test_scene_frames_have_retained_aspect(self):
        for row in self.page.images:
            if '/source/output/' in row['src']:
                with Image.open(local_file(row['src'])) as image:
                    self.assertEqual(image.width * 326, image.height * 704)

    def test_all_document_links_exist(self):
        self.assertEqual(len(self.page.links), 4)
        for href in self.page.links:
            local_file(href)

    def test_original_benchmark_not_substituted(self):
        image = next(row for row in self.page.images if row.get('id') == 'benchmark')
        self.assertEqual(image['src'], '../../building-perspective-detail-20261116/kiosk/inputs/benchmark.png')
        self.assertIn('object-fit:contain', self.text)
        self.assertNotIn('object-fit:cover', self.text)

    def test_source_evidence_is_not_called_native(self):
        self.assertIn('synthetic source-scene reconstruction, not native captures', self.text)
        self.assertIn('Owner review required', self.text)
        self.assertIn('This static page does not certify them at runtime', self.text)
        self.assertNotIn('<script', self.text)

    def test_traversal_rejected(self):
        with self.assertRaisesRegex(ValueError, 'escapes'):
            local_file('../../../../../../outside')


if __name__ == '__main__':
    unittest.main(verbosity=2)
