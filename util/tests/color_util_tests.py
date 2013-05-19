import unittest
import numpy as np
from util.color_util import hex_to_rgb, rgb_to_hex, create_color_references, get_color

num_X11_colors = 140
white_hex = "FFFFFF"
white_dec = (255, 255, 255)
black_hex = "000000"
black_dec = (0, 0, 0)

tomato_hex = "FA6940"
teal_hex = "087585"


class TestColorUtil(unittest.TestCase):

    def test_hex_to_dec_rgb(self):
        self.assertEqual(white_dec, hex_to_rgb(white_hex))
        self.assertEqual(black_dec, hex_to_rgb(black_hex))

    def test_dec_to_hex_rgb(self):
        self.assertEqual(white_hex.upper(), rgb_to_hex(*white_dec).upper())
        self.assertEqual(black_hex.upper(), rgb_to_hex(*black_dec).upper())

    def test_color_references(self):
        color_list, rgb_np_array = create_color_references()
        self.assertEqual(num_X11_colors, len(color_list))
        self.assertEqual(num_X11_colors, np.shape(rgb_np_array)[0])
        for color in color_list:
            self.assertIsNotNone(color['name'])
            self.assertIsNotNone(color['group'])
            self.assertIsNotNone(color['hex'])

    def test_get_color(self):
        should_be_tomato = get_color(*hex_to_rgb(tomato_hex))
        self.assertEqual("tomato", should_be_tomato['name'].lower())
        should_be_teal = get_color(*hex_to_rgb(teal_hex))
        self.assertEqual("teal", should_be_teal['name'].lower())


if __name__ == '__main__':
    unittest.main()