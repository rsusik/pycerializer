import struct
from typing import Dict, Iterable, Tuple, Optional


endianness_map = {
    'little': '<',
    'big': '>',
    '<': '<',
    '>': '>'
}


num_type_map = {
    'int8_t': 'b',
    'uint8_t': 'B',
    'int16_t': 'h',
    'uint16_t': 'H',
    'int32_t': 'i',
    'uint32_t': 'I',
    'int64_t': 'q',
    'uint64_t': 'Q',
}


str_type_map = {
    'string': 's',
}

num_type_map_to_c = {
    'int8_t': 'int8_t',
    'uint8_t': 'uint8_t',
    'int16_t': 'int16_t',
    'uint16_t': 'uint16_t',
    'int32_t': 'int32_t',
    'uint32_t': 'uint32_t',
    'int64_t': 'int64_t',
    'uint64_t': 'uint64_t',
}

str_type_map_to_c = {
    'string': 'char *'
}


def _get_num_type(
    t : str
) -> str:
    '''
    
    '''
    if t in num_type_map:
        return num_type_map[t]
    else:
        raise Exception(f'ERROR: Not supported type {t}')


def _get_str_type(
    t : str
) -> str:
    '''
    
    '''
    if t in str_type_map:
        return str_type_map[t]
    else:
        raise Exception(f'ERROR: Not supported type {t}')


def _get_type(
    t : str
) -> str:
    '''
    
    '''
    all_type_map = {}
    all_type_map.update(num_type_map)
    all_type_map.update(str_type_map)
    if t in all_type_map:
        return all_type_map[t]
    else:
        raise Exception(f'ERROR: Not supported type {t}')


def _get_c_type(
    t : str
) -> str:
    '''
    
    '''
    all_type_map = {}
    all_type_map.update(num_type_map_to_c)
    all_type_map.update(str_type_map_to_c)
    if t in all_type_map:
        return all_type_map[t]
    else:
        raise Exception(f'ERROR: Not supported type {t}')



def _get_endianness(
    e : str
) -> str:
    '''
    
    '''
    if e in endianness_map:
        return endianness_map[e]
    else:
        raise Exception(f'ERROR: Not supported endianness {e}')


def pack_list_num(
    l : Iterable[int], 
    t : Optional[str] = 'int64_t', 
    e : Optional[str] = 'little'
) -> Tuple[bytes, int]:
    '''
    Pack python iterable into bytes.

    Returns a tuple containg:
    - bytes object containing `len(l)` of numbers `l` packed into bytes,
    - number of elements packed.

    Parameters:
    :param l: iterabpe of numbers to be packed,
    :param t: type of the data,
    :param e: endianess.

    Example:
    packed = pack_list_num([1, 2, 3], 'int16_t', 'little')
    '''
    e = _get_endianness(e)
    t = _get_num_type(t)
    number_of_elements = len(l)
    return struct.pack(f'{e}{number_of_elements}{t}', *l), number_of_elements


def unpack_list_num(
    buffer : bytes, 
    n : int, 
    t : Optional[str] = 'int64_t', 
    e : Optional[str] = 'little'
) -> Tuple[int]:
    '''
    Unpack `buffer` bytes into python tuple containing `n` numbers.

    Returns a tuple containg:
    - a python tuple of `n` numbers,
    - number of element `n`.

    Parameters:
    :param buffer: buffer with numbers to be unpacked.
    :param n: number of elements to be unpacked.
    :param t: type of the numeric data.
    :param e: endianess.

    Example:
    unpacked = unpack_list_num(*packed, 'int16_t', 'little')
    print(unpacked) # ( [1, 2, 3], 3 )
    '''
    e = _get_endianness(e)
    t = _get_num_type(t)
    l = struct.unpack(f'{e}{n}{t}', buffer)
    return l, n


def pack_list_2d_num(
    l : Iterable[Iterable[int]], 
    t : Optional[str] = 'int64_t', 
    e : Optional[str] = 'little'
) -> bytes:
    '''
    Pack python two dimmensional array `l` (of shape (a, b)) 
    into bytes object.
    Note: The iterable containing **a** iterables of **b** numbers 
    will be squeezed before packing.

    Returns a tuple containg:
    - bytes object containing **a x b** numbers packed into bytes,
    - number of elements packed.

    Parameters:
    :param l: two dimmensional array of shape (a, b),
    :param t: type of the numeric data,
    :param e: endianess.

    Example:
    packed = pack_list_num([1, 2, 3], 'int16_t', 'little')
    '''
    return pack_list_num([x for y in l for x in y], t, e)


def unpack_list_2d_num(
    buffer : bytes, 
    shape : Tuple[int, int], 
    t : Optional[str] = 'int64_t', 
    e : Optional[str] = 'little'
) -> Tuple[Tuple[Tuple[int]], Tuple[int, int]]:
    '''
    Unpack bytes object `buffer` into python two dimmensional 
    tuple of given `shape` (a, b).

    Returns a tuple containg:
    - unpacked two dimmentional tuple of given `shape`,
    - `shape`.

    Parameters:
    :param buffer: bytes object containing a x b number of size `t`,
    :param shape: shape (a, b) of the data to be returned,
    :param t: type of the numeric data,
    :param e: endianess.

    Example:
    unpacked = unpack_list_2d_num(packed[0], (2, 2), 'int32_t', 'little')
    '''
    first_dim = shape[0]
    second_dim = shape[1]
    l, _ = unpack_list_num(buffer, first_dim*second_dim, t, e)
    return tuple(l[i*second_dim:(i+1)*second_dim] for i in range(first_dim)), shape


def pack_dict(
    d : Dict, 
    key_type_mapping : Dict, 
    e : Optional[str] = 'little', 
    enc : Optional[str] = 'utf-8', 
    size_type : Optional[str] = 'int64_t'
) -> Tuple[bytes, int]:
    '''
    Packs the dictionary into bytes but only those 
    elements that are listed in `key_type_mapping`
    and in given order.

    Returns
    - bytes and 
    - size of the structure.

    Parameters:
    :param d: Python dictionary,
    :param key_type_mapping: a dictionary with key / type mapping,
    :param e: endianess,
    :param enc: encoding (in case of strings),
    :param size_type: type of the number which indicates length of the string (only for strings).

    Example:
    ```
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
    ```
    '''
    e = _get_endianness(e)
    size_type = _get_num_type(size_type)
    frmt = f'{e}'
    data = []
    for key in key_type_mapping.keys():
        t = _get_type(key_type_mapping[key])
        if t == 's':
            number_of_chars = len(d[key])
            frmt += f'{size_type}{number_of_chars}s'
            if type(d[key]) == str:
                val = bytes(d[key], encoding=enc)
            else:
                val = d[key]
            data.extend([number_of_chars, val])
        else:
            frmt += t
            data.append(d[key])
    return struct.pack(f'{frmt}', *data), struct.calcsize(frmt)


def unpack_dict(
    b : bytes, 
    key_type_mapping : Dict, 
    offset : int = None, 
    e : Optional[str] = 'little', 
    enc : Optional[str] = 'utf-8', 
    size_type : Optional[str] = 'int64_t'
) -> Dict:
    '''
    Unpacks the bytes into dictionary.

    Returns a dictionary.

    Parameters:
    :param b: bytes (packed dictionary),
    :param key_type_mapping: a dictionary with key / type mapping that was used for packing,
    :param e: endianess,
    :param enc: encoding (in case of strings),
    :param size_type: type of the number which indicates length of the string (only for strings).

    Example:
    ```
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
    ```
    '''
    e = _get_endianness(e)
    size_type = _get_num_type(size_type)
    d = {}
    if offset is None:
        offset = 0
    else:
        offset = int(offset)
        
    for key in key_type_mapping.keys():
        t = _get_type(key_type_mapping[key])
        if t == 's':
            number_of_chars = struct.unpack_from(f'{e}{size_type}', b, offset=offset)[0]
            offset += struct.calcsize(f'{e}{size_type}')
            val = struct.unpack_from(f'{e}{number_of_chars}{t}', b, offset=offset)[0]
            offset += struct.calcsize(f'{e}{number_of_chars}{t}')
            d[key] = val
        else:
            val = struct.unpack_from(f'{e}{t}', b, offset=offset)[0]
            offset += struct.calcsize(f'{e}{t}')
            d[key] = val
    return d, offset


def pack_list_dict(
    l : Iterable[Dict], 
    key_type_mapping : Dict, 
    e : Optional[str] = 'little', 
    enc : Optional[str] = 'utf-8', 
    size_type : Optional[str] = 'int64_t'
) -> Tuple[bytes, int, int, Iterable[int]]:
    '''
    Packs the list of dictionaries into bytes (only 
    those elements that are listed in `key_type_mapping`
    and in given order).

    Returns a tuple of:
    - bytes,
    - length of `l`,
    - size,
    - size of each dictionary.

    Parameters:
    :param l: iterable containing dictionaries,
    :param key_type_mapping: a dictionary with key / type mapping,
    :param e: endianess,
    :param enc: encoding (in case of strings),
    :param size_type: type of the number which indicates length of the string (only for strings).
    '''
    b = bytearray()
    sizes = []
    for el in l:
        packed = pack_dict(el, key_type_mapping, e, enc, size_type)
        b.extend(packed[0])
        sizes.append(packed[1])
    return b, len(l), len(b), sizes


def unpack_list_dict(
    b : bytes, 
    key_type_mapping : Dict, 
    number_of_elements : int, 
    e : Optional[str] = 'little', 
    enc : Optional[str] = 'utf-8', 
    size_type : Optional[str] = 'int64_t'
) -> Tuple[Iterable[Dict], int, int]:
    '''
    Unpacks the bytes into dictionary.

    Returns a tuple of:
    - tuple of dictionaries,
    - `number_of_elements`,
    - number of bytes.

    Parameters:
    :param b: bytes (packed list of `number_of_elements` dictionaries),
    :param key_type_mapping: a dictionary with key / type mapping that was used for packing,
    :param e: endianess,
    :param enc: encoding (in case of strings),
    :param size_type: type of the number which indicates length of the string (only for strings).

    '''
    offset = 0
    l = []
    for idx in range(number_of_elements):
        unpacked, o = unpack_dict(b, key_type_mapping, offset, e, enc, size_type)
        offset += (o - offset)
        l.append(unpacked)
    return l, len(l), len(b)


def size_of_dict(
    key_type_mapping : Dict, 
    e : Optional[str] = 'little'
) -> int:
    '''Calculates size of dict.

    Note: works only for dict with all numeric types.
    
    Returns size of dict.

    Parameters:
    :param key_type_mapping: a dictionary with key / type mapping that was used for packing,
    :param e: endianess.
    '''
    e = _get_endianness(e)
    frmt = f'{e}'
    for key in key_type_mapping.keys():
        t = _get_type(key_type_mapping[key])
        frmt += t
    return struct.calcsize(frmt)


def get_c_struct(
    key_type_mapping : Dict, 
    name : str, 
    e : Optional[str] = 'little'
) -> str:
    '''
    Returns the C structure.

    Note: Works only for dict with all numeric types

    Parameters:
    :param key_type_mapping: a dictionary with key / type mapping that was used for packing,
    :param name: structure name,
    :param e: endianess.
    '''
    e = _get_endianness(e)
    out = f'typedef struct _{name} {{\n'

    for key in key_type_mapping.keys():
        t = key_type_mapping[key]
        c_type = _get_c_type(t)
        out += f'\t{c_type} {key};\n'
    out += f'}} {name};\n'
    return out
