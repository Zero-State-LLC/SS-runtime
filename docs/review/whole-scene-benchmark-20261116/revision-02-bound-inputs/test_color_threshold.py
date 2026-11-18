import unittest
from PIL import Image
from verify_capture import has_more_than_64_colors

class ExactColorThresholdTests(unittest.TestCase):
    def test_exactly64_rejected(self):
        image = Image.new('RGB', (64, 1))
        image.putdata([(i, i, i) for i in range(64)])
        self.assertFalse(has_more_than_64_colors(image))

    def test_exactly65_accepted(self):
        image = Image.new('RGB', (65, 1))
        image.putdata([(i, i, i) for i in range(65)])
        self.assertTrue(has_more_than_64_colors(image))

    def test_last_pixel_counted_not_sampled(self):
        image = Image.new('RGB', (1024, 64))
        for i in range(64):
            image.putpixel((i, 0), (i, i, i))
        self.assertFalse(has_more_than_64_colors(image))
        image.putpixel((1023, 63), (64, 64, 64))
        self.assertTrue(has_more_than_64_colors(image))

if __name__ == '__main__':
    unittest.main()
