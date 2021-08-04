<p align="center">
    <img src="https://github.com/rsusik/pycerializer/raw/master/pycerializer.png" alt="PyCerializer" />
</p>
<p align="center">
    <em>Lightweight serialization module for Python.</em>
</p>
<p align="center">
<a href="https://pypi.org/project/pycerializer" target="_blank">
    <img src="https://img.shields.io/pypi/v/pycerializer?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://github.com/rsusik/pycerializer/blob/master/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/rsusik/pycerializer" alt="Package version">
</a>
</p>


PyCerializer is a lightweight serialization module for Python. 
The aim of PyCerializer is to produce serialized data that 
can be easily read in other programming languages such 
as C/C++ and others.

## Requirements
There are no external dependencies.
The package is based on standard python module `struct`
that is available in all supported python versions, but
the PyCerializer use also `typing` module that was introduced 
in Python 3.5.

## Supported types:

- Numbers
    - [u]int64_t
    - [u]int32_t
    - [u]int16_t
    - [u]int8_t
- Strings
- Structures

## Endianess:
- little,
- big.

## Installation
```
pip install pycerializer
```

## Examples

### Serialize the Python list and save to file:
```python
original = (1, 123, 4321)
packed = pack_list_num(original, 'int16_t', 'little')
with open('file.bin', 'wb') as f:
    f.write(packed)
```

### Deserialize the list using Python:
```python
with open('file.bin', 'rb') as f:
    packed = f.read()
    unpacked = unpack_list_num(*packed, 'int16_t', 'little')
```

### Deserialize the list using C/C++:
```cpp
FILE *f = fopen("file.bin", "rb");
const int n = 3;
int16_t buff[n];
fread(buff, sizeof(int16_t), n, f);
for (int i = 0; i < n; i++) printf("%d ", buff[i] );
```

### Serialize and deserialize the list of dictionaries:
```python
    # data
    data = [{
        'name': b'John',
        'age': 34,
        'height': 177,
        'surname': b'Smith',
        'weight': 86
    }, 
    {
        'name': b'Andrew',
        'age': 43,
        'height': 187,
        'surname': b'Bluebaum',
        'weight': 67
    }, {
        'name': b'Michael',
        'age': 38,
        'height': 189,
        'surname': b'Brown',
        'weight': 99
    }]

    # data field:type mapping
    data_map = {
        'name': 'string',
        'age': 'int8_t',
        'height': 'int32_t',
        'surname': 'string',
        'weight': 'int8_t'
    }

    # packing
    data_bytes, data_elements, _, data_elements_size = pack_list_dict(data, data_map)

    # unpacking
    data_unpacked = unpack_list_dict(data_bytes, data_map, data_elements)

    # metadata
    meta = {
        'number_of_elements': data_elements,
    }

    # metadata field:type mapping
    meta_map = {
        'number_of_elements': 'uint64_t'
    }

    meta_bytes, _ = pack_dict(meta, meta_map)
    elements_size_bytes, _ = pack_list_num(data_elements_size, 'int64_t')

    # write bytes to a file
    with open('list_of_dicts.bin', 'wb') as f:
        f.write(meta_bytes)
        f.write(elements_size_bytes)
        f.write(data_bytes)

    # Get the C struct to use it later in C code
    print(get_c_struct(meta_map, name='meta_t'))
    print(get_c_struct(data_map, name='data_t'))
```

### Deserialize and print the data from file using C/C++:
```cpp
// Copied from Python output
typedef struct _meta_t {
    uint64_t number_of_elements;
} meta_t;


typedef struct _data_t {
    char * name;
    int8_t age;
    int32_t height;
    char * surname;
    int8_t weight;
} data_t;

// Read the data from buffer
size_t data_t_read(data_t *obj, uint8_t *bytes) {
    int64_t *name_size = (int64_t *)bytes;           bytes += sizeof(int64_t);
    obj->name = (char*)calloc(*name_size + 1, sizeof(char));

    memcpy(obj->name, bytes, *name_size);            bytes += *name_size;
    memcpy(&(obj->age), bytes, sizeof(uint8_t));     bytes += sizeof(uint8_t);
    memcpy(&(obj->height), bytes, sizeof(uint32_t)); bytes += sizeof(uint32_t);

    int64_t *surname_size = (int64_t *)bytes;        bytes += sizeof(int64_t);
    obj->surname = calloc(*surname_size + 1, sizeof(char));

    memcpy(obj->surname, bytes, *surname_size);      bytes += *surname_size;
    memcpy(&(obj->weight), bytes, sizeof(int8_t));   bytes += sizeof(int8_t);

    return 0;
}

// Never forget to deallocate the memory
void data_t_free(data_t obj) {
    free(obj.name);
    free(obj.surname);
}


int main() {
    FILE *f = fopen("list_of_dicts.bin", "rb");
    meta_t meta;
    fread(&meta, sizeof(meta_t), 1, f);

    data_t *data = (data_t*)malloc(sizeof(data_t) * meta.number_of_elements);
    int64_t* sizes = (int64_t*)malloc(meta.number_of_elements * sizeof(int64_t*));
    fread(sizes, meta.number_of_elements, sizeof(int64_t), f);
    printf("Number of elements: %lu\n", meta.number_of_elements);

    for (uint64_t i = 0; i < meta.number_of_elements; i++) {
        uint8_t *buff = (uint8_t*)malloc(sizes[i]);
        fread(buff, sizes[i], 1, f);
        data_t_read(data + i, buff);
        printf("%lu. %s %s, age: %d, height: %d, weight: %d\n", i, data[i].name, data[i].surname, data[i].age, data[i].height, data[i].weight);
        data_t_free(data[i]);
        free(buff);
    }
    fclose(f);
    free(sizes);
    free(data);

    return 0;
}
```

## Limitation
This module works well for flat data, and definitely, there is much more effort needed to store and read data than using, for example, `pickle`. 
On the other hand, it may take much more effort to read pickled data in C++.
Pycerializer was written ad-hoc for another project and was used for prototyping in Python, where there was a need to read the output in C++, which is the case where this module works quite well.
The number of supported types is very limited but can be easily extended.
Any contribution is welcome.
