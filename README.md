# PyDumper

PyDumper is lightweight module for python serialization. 
The aim of PyDumper is to produce serialized data that 
can be easily read in other programming languages such 
as C/C++ and others.

## Requirements
There are no external dependencies.
The package is based on standard python module `struct`
that is available in all supported python versions, but
the pydumper use also `typing` module that was introduced 
in Python 3.5.

## Supported types:
- [u]int64_t
- [u]int32_t
- [u]int16_t
- [u]int8_t
- string
- structures

## Endianess:
- little
- big

## Installation
```
pip install pydumper
```

## A simple example

Pack and save to file python list:
```python
original = (1, 123, 24323, 21)
packed = pack_list_num(original, 'int16', 'little')
with open('file.bin', 'wb') as f:
    f.write(packed)
```

Unpack this list using python:
```python
with open('file.bin', 'rb') as f:
    packed = f.read()
    unpacked = unpack_list_num(*packed, 'int16', 'little')
```

Unpack this list using C/C++:
```cpp
TODO...
```

Generate C/C++ structure from python:
```python
TODO....
```

Pack Python dictionary into bytes and save to file:
```
TODO...
```

Unpack that dictionary using C/C++:
```
TODO...
```

## Limitation
The structure packing supports only Python dictionaries with numeric fields.
