import unittest

from pycerializer.pycerializer import (
    pack_list_num, 
    unpack_list_num,
    pack_list_2d_num,
    unpack_list_2d_num,
    pack_dict,
    unpack_dict,
    pack_list_dict,
    unpack_list_dict
)

class TestStringMethods(unittest.TestCase):

    def test_pack_list_num(self):
        original = (1, 123, 24323, 21)
        packed = pack_list_num(original, 'int16_t', 'little')
        unpacked = unpack_list_num(*packed, 'int16_t', 'little')
        self.assertEqual(original, unpacked[0])

    def test_pack_list_2d_num(self):
        original = ((1, 123), (243234, 21))
        packed = pack_list_2d_num(original, 'int32_t', 'little')
        unpacked = unpack_list_2d_num(packed[0], (2, 2), 'int32_t', 'little')
        self.assertEqual(original, unpacked[0])

    def test_pack_dict(self):
        original = {
            'name': b'name 1',
            'age': 34,
            'height': 177,
            'surname': b'surname 1',
            'weight': 86
        }

        d_map = {
            'name': 'string',
            'age': 'int8_t',
            'height': 'int32_t',
            'surname': 'string',
            'weight': 'int8_t'
        }

        packed = pack_dict(original, d_map)
        unpacked = unpack_dict(packed[0], d_map)
        self.assertEqual(original, unpacked[0])

    def test_pack_list_dict(self):

        original = [{
            'name': b'name 1',
            'age': 34,
            'height': 177,
            'surname': b'surname 1',
            'weight': 86
        }, 
        {
            'name': b'name 2',
            'age': 43,
            'height': 187,
            'surname': b'surname 2',
            'weight': 67
        }, {
            'name': b'name 3',
            'age': 38,
            'height': 189,
            'surname': b'surname 3',
            'weight': 99
        }]

        d_map = {
            'name': 'string',
            'age': 'int8_t',
            'height': 'int32_t',
            'surname': 'string',
            'weight': 'int8_t'
        }


        packed = pack_list_dict(original, d_map)
        unpacked = unpack_list_dict(packed[0], d_map, packed[1])
        self.assertEqual(original, unpacked[0])


if __name__ == '__main__':
    unittest.main()
