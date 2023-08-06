# kf_utils v2.0.2

This repository provides the utils package used in all **Knowledge Factory** microservices.

**Table of contents:**
- [Use this package in your code](#use-this-package-in-your-code)
- [Available modules and methods](#available-modules-and-methods)
- [Add new features, hotfixes or bugfixes](#add-new-features,-hotfixes-or-bugfixes)
- [Run automatic tests](#run-automatic-tests)
- [Build kf_utils as a PyPi package](#build-kf_utils-as-a-pypi-package)
- [Project changelog](#project-changelog)



## Use this package in your code

First of all, to install this package using `pip`, use the following command:

```shell
# To download it from a PyPi repository
pip install kf-utils-package

# Go to the kf_utils folder and execute this command
# to install the package using setup.py config
pip install -e .
```

To use this package in your code just import `kf_utils`:

```python
# Import the whole kf_utils package
import kf_utils

# Import just the package/method you want to use
from kf_utils import graphs             # graphs package
from kf_utils.files import to_file      # to_file method from files package
```

We really encourage you to import **just the module/method you want to use**, because it will always be more optimal 
than importing the entire `kf_utils` package.



## Available modules and methods

All the different packages, modules and methods available in this `kf_utils` are listed here:

- [char_codec module](#char_codec-module)
  - [CharCodec class](#charcodec-class)
    - [extract_bracketed method](#extract_bracketed-method)
    - [extract_quoted method](#extract_quoted-method)
    - [quoted method](#quoted-method)
    - [angled method](#angled-method)
    - [bracketed method](#bracketed-method)
    - [pointers method](#pointers-method)
    - [properties method](#properties-method)
    - [sequence method](#sequence-method)
- [dicts module](#dicts-module)
  - [clean_dict method](#clean_dict-method)
  - [merge_dicts method](#merge_dicts-method)
- [extractors module](#extractors-module)
  - [extract_angled method](#extract_angled-method)
  - [extract_between_parenthesis method](#extract_between_parenthesis-method)
  - [extract_between_delimiters method](#extract_between_delimiters-method)
  - [extract_quoted method](#extract_quoted-method-v2)
  - [extract_double_quoted method](#extract_double_quoted-method)
  - [extract_single_quoted method](#extract_single_quoted-method)
- [files module](#files-module)
    - [base64_ method](#base64_-method)
    - [base64_decode method](#base64_decode-method)
    - [copy_file method](#copy_file-method)
    - [count_occurrences_in_file method](#count_occurrences_in_file-method)
    - [delete_line_number method](#delete_line_number-method)
    - [to_file method](#to_file-method)
    - [delete method](#delete-method)
    - [get_file_name_from_path method](#get_file_name_from_path-method)
    - [file_split_name_ext method](#file_split_name_ext-method)
    - [get_file method](#get_file-method)
    - [get_file_content method](#get_file_content-method)
    - [get_file_extension method](#get_file_extension-method)
    - [remove_extension_from_file_path method](#remove_extension_from_file_path-method)
    - [get_directory_and_file_name_and_extension_from_path method](#get_directory_and_file_name_and_extension_from_path-method)
    - [get_file_name method](#get_file_name-method)
    - [get_file_root_path method](#get_file_root_path-method)
    - [to_json method](#to_json-method)
    - [exist method](#exist-method)
    - [drop_dir method](#drop_dir-method)
    - [drop_file method](#drop_file-method)
    - [from_json method](#from_json-method)
    - [from_yaml method](#from_yaml-method)
    - [path_exists method](#path_exists-method)
    - [grep method](#grep-method)
    - [head method](#head-method)
    - [tail method](#tail-method)
    - [import_library method](#import_library-method)
    - [make_dirs method](#make_dirs-method)
    - [remove_file_protocol method](#remove_file_protocol-method)
    - [to_file_line method](#to_file_line-method)
    - [xst_file method](#xst_file-method)
    - [extract_files_from_zip_folder method](#extract_files_from_zip_folder-method)
    - [get_file_name_length method](#get_file_name_length-method)
    - [get_file_size method](#get_file_size-method)
    - [get_file_name_and_extension method](#get_file_name_and_extension-method)
- [graphs module](#graphs-module)
  - [load_graph method](#load_graph-method)
  - [convert_response_query_graph_to_df method](#convert_response_query_graph_to_df-method)
- [hashers module](#hashers-module)
  - [HashAlgorithm class](#hashalgorithm-class)
  - [crc method](#crc-method)
  - [scrc method](#scrc-method)
  - [hash method](#hash-method)
  - [md5 method](#md5-method)
  - [hashbin method](#hashbin-method)
  - [md5int method](#md5int-method)
  - [uuids method](#uuids-method)
- [lang module](#lang-module)
  - [alpha2 method](#alpha2-method)
- [lists module](#lists-module)
  - [duplicated method](#duplicated-method)
  - [index method](#index-method)
  - [ordered_set method](#ordered_set-method)
  - [remove_duplicates method](#remove_duplicates-method)
- [replacers module](#replacers-module)
  - [replace_chars method](#replace_chars-method)
  - [replace_substrings method](#replace_substrings-method)
  - [replace_match_boundaries method](#replace_match_boundaries-method)
  - [replace_quoted method](#replace_quoted-method)
  - [un_pad_fixed_locations method](#un_pad_fixed_locations-method)
  - [replace method](#replace-method)
  - [replace_angled method](#replace_angled-method)
  - [replace_delimited method](#replace_delimited-method)
- [strings module](#strings-module)
  - [indices method](#indices-method)
  - [is_get_list method](#is_get_list-method)
  - [json_str_to_dict method](#json_str_to_dict-method)
  - [mask_quoted method](#mask_quoted-method)
  - [unmask_quoted method](#unmask_quoted-method)
  - [nnl method](#nnl-method)
  - [remove_comments method](#remove_comments-method)
  - [slash method](#slash-method)
  - [tokenize method](#tokenize-method)
  - [unaccent method](#unaccent-method)
  - [url_tail method](#url_tail-method)
  - [url_head method](#url_head-method)
  - [regex method](#regex-method)
- [timers module](#timers-module)
  - [now method](#now-method)
  - [str_to_datetime method](#str_to_datetime-method)
  - [Timer class](#timer-class)
    - [now method](#now-method-v2)
    - [trig method](#trig-method)
    - [console method](#console-method)
    - [delta method](#delta-method)
    - [deltas method](#deltas-method)
- [data_types package](#data_types-package)
    - [uri module](#uri-module)
      - [URI class](#uri-class)
      - [URL class](#url-class)
    - [persistor_type module](#persistor_type-module)
      - [PersistorType class](#persistortype-class)


### `char_codec` module

```python
import kf_utils.char_codec
from kf_utils import char_codec
```

Class `CharCodec` is a helper to code and decode characters or strings of characters.

> **Note** Main use cases: parsers, compiler, and text analysers in general that need to find patterns and replace 
> portions of text that match the patterns with another text or symbol.

#### `CharCodec` class

String coder and decoder.

Attributes:
- **code:** The code taking the place of the substring to be replaced.
- **to_replace:** The substring that is being replaced.
- **text:** The text containing the substring to be replaced.
- **exclude:** A text NOT to replace if found inside the substring being replaced.

##### `extract_bracketed` method

Extracts string between left and right delimiters.

- **Params:**
  - **text: str** – string to be analysed.
  - **left: str** – left delimiter.
  - **right: str** – right delimiter.
- **Returns: list** – extracted parts listed as strings.

##### `extract_quoted` method

Extracts text between double or single quotes unless it equals the 'exclude' text.

- **Params:**
  - **text: str** – string to be analysed.
  - **exclude: str** – text to exclude. By default, it is set to None.
- **Returns: list** – extracted parts listed as strings.

##### `quoted` method

Replaces a substring inside a double or single quoted text with the code.

- **Returns: str** – the text with the replaced substring.

##### `angled` method

Replaces everything between &lt;&gt;, uses a special pattern that avoids problems with statements containing operators 
like &lt; and &gt;.

- **Params:**
  - **exclude: str** – text to exclude. By default, it is set to None.
- **Returns: str** – the text with angled chars replaced.

##### `bracketed` method

Replaces a substring inside parenthesis, square brackets, curly brackets, angles or disparate delimiters with the code.

- **Params:**
  - **left: str** – left delimiter.
  - **right: str** – right delimiter.
  - **exclude: str** – text to exclude. By default, it is set to None.
- **Returns: str** – the text with bracketed chars replaced.

##### `pointers` method

Replaces pointers to functions (e.g., the dot in "class.function_name(*args, **kwargs))" with the code.
 
- **Returns: list** – function with pointers replaced.

##### `properties` method

Replaces invocation to method or class properties.

- **Returns: list** – function with pointers replaced.

**Example:**
```python
md5 = "self.io().hash"

# Returns
md5 = "self.io()<code>hash"
```

##### `sequence` method

Replaces each inner 'x' char with the code in a sequence of words separated with 'x'. E.g., with '.' as the 
separator and &lt;code&gt; representing whatever code you choose, e.g. &lt;&#95;&#95;DOT&#95;&#95;&gt;

Notice that the tokenizer is able to remove comments, which in this case is highly convenient.

> **Note**
> `remove_comments` defaults to **True**, thus this argument here is superfluous, but we keep it for the 
> sake of clarity and documentation.

- **Returns: list** – function with pointers replaced.

**Example:**
```python
from kf_utils.char_codec import CharCodec

text: str = "com.nttdata.dgi.crud.Compiler. t1 = sequence.of.dots.here # comment"
code: str = "<__DOT__>"
to_replace: str = "."
replacer: CharCodec = CharCodec(text=text, to_replace=to_replace, code=code)

new_text: str = replacer.sequence()
print(new_text)         # "com<__DOT__>nttdata<__DOT__>dgi<__DOT__>crud<__DOT__>Compiler<__DOT__>"
```

***

### `dicts` module

```python
import kf_utils.dicts
from kf_utils import dicts
```

Methods related with dicts management.

#### `clean_dict` method

Delete key from a dict where value is None.

- **Params:**
  - **data_dict: dict** – dictionary to clean.
- **Returns: dict** – dictionary with cleaned key-values.

**Example:**
```python
from kf_utils.dicts import clean_dict

dict_with_none_values: dict = {"id": "123", "field": None}      # GIVEN a dict with None values

new_clean_dict: dict = clean_dict(dict_with_none_values)        # RETURNS a new dict without None values
print(new_clean_dict)                                           # {"id": "123"}
```

#### `merge_dicts` method

Merges several dictionaries in one.

- **Params:**
  - **args: dict** – dictionaries to be merged.
- **Returns: dict** – a new dictionary with the previous dictionaries merged.

**Example:**
```python
from kf_utils.dicts import merge_dicts

# GIVEN several dictionaries
dic1 = {"a": 1, "b": 2}
dic2 = {"b": 3, "c": 4}
dic3 = {"d": 5, "e": 6, "f": 8}

new_merged_dict: dict = merge_dicts(dic1, dic2, dic3)   # RETURNS a new dict containing the original items
print(new_merged_dict)                                  # {"a": 1, "b": 3, "c": 4, "d": 5, "e": 6, "f": 8}
```

***

### `extractors` module

```python
import kf_utils.extractors
from kf_utils import extractors
```

Helpers for advance extraction of substrings.

#### `extract_angled` method

Extracts text between &lt; and &gt;. 

Copes with the situation: `var_name = 1 > 2`.

- **Params:**
  - **txt: str** – txt to be analysed.
- **Returns: list** – extracted parts listed.

#### `extract_between_parenthesis` method

Extracts text between '(' and ')'.

- **Params:**
  - **txt: str** – txt to be analysed.
- **Returns: list** – extracted parts listed.

#### `extract_between_delimiters` method

Extracts text between any left char and right car.

**BEWARE THAT** the last right char is included and needs to be removed.

- **Params:**
  - **txt: str** – txt to be analysed.
  - **left: str** – left delimiter.
  - **right: str** – right delimiter.
- **Returns: list** – extracted parts listed.

#### `extract_quoted` method<a name="extract_quoted-method-v2"></a>

Extracts text between double or single quotes unless it equals the 'exclude' text.

- **Params:**
  - **quoted_txt: str** – quoted text to be analysed.
  - **exclude: str** – text to exclude. By default, it is set to None.
- **Returns: list** – extracted parts listed.

#### `extract_double_quoted` method

Extracts text between double quotes unless it equals the 'exclude' text.

- **Params:**
  - **quoted_txt: str** – double-quoted text to be analysed.
  - **exclude: str** – text to exclude. By default, it is set to None.
- **Returns: list** – extracted parts listed.

#### `extract_single_quoted` method

Extracts text between single quotes unless it equals the 'exclude' text.

- **Params:**
  - **quoted_txt: str** – single-quoted text to be analysed.
  - **exclude: str** – text to exclude. By default, it is set to None.
- **Returns: list** – extracted parts listed.

***

### `files` module

```python
import kf_utils.files
from kf_utils import files
```

Methods related with files and directories management

#### `base64_` method

Returns the content of a file as a Base64 string

- **Params:**
  - **file_path: str** – path to the file.
- **Returns: str** – content of the file encoded as Base64 string.

#### `base64_decode` method

Decodes a Base64 string back into the original content in bytes

- **Params:**
  - **encoded_str: str** – base64 coded string.
- **Returns: bytes** – decoded content in bytes

#### `copy_file` method

Copies source file to target file.

- **Params:**
  - **source_file_path: str** – file to be copied.
  - **target_file_path: str** – file that will be created containing the source file content.

#### `count_occurrences_in_file` method

Returns the number of times that the text occurs in the file.

- **Params:**
  - **txt: str** – text to find in the file content.
  - **file_path: str** – path to the file.
  - **case_sensitive: bool** – whether the search is case-sensitive. By default, it is set to True.
- **Returns: int** – the number of times that the text occurs in the file.

#### `delete_line_number` method

Removes a line from a file.

- **Params:**
  - **file_path: str** – file to edit.
  - **line: int** – number of the line to be removed.

#### `to_file` method

Writes a text into a file.

- **Params:**
  - **txt: str** – text to be written into the file.
  - **path: str** – path where the file will be created.

#### `delete` method

Removes all occurrences of a text from inside a file.

- **Params:**
  - **txt: str** – text to be removed in the file.
  - **file_path: str** – path to the file.

#### `get_file_name_from_path` method

> **Deprecated** since `v2.0.1`. It's replaced by `get_file_name()` method.

Given a full file path name, returns just the filename.

- **Params:**
  - **path: str** – full file path name.
- **Returns: str** – filename extracted from the path.

#### `file_split_name_ext` method

> **Deprecated** since `v2.0.1`. It's replaced by `get_file_name_and_extension()` method.

Given a complete file path name, it separates the name from the extension.

- **Params:**
  - **file_name: str** – complete file path name.
- **Returns: (str, str)** – filename, extension.

#### `get_file` method

> **Deprecated** since `v2.0.1`. It's replaced by `get_file_name_and_extension()` method

Given the full file path name, it returns the name and the extension of the file.

- **Params:**
  - **path_filename: str** – full file path name.
- **Returns: (str, str)** – name, extension.

**Example:**
```python
from kf_utils.files import get_file

windows_file_path: str = 'C:\\utils\\README.md'
linux_file_path: str = '/home/README.md'
folder_path: str = 'C:\\folder'

windows: tuple[str, str] = get_file(windows_file_path)
linux: tuple[str, str] = get_file(linux_file_path)
folder: tuple[str, str] = get_file(folder_path)

print(windows)      # ('README', 'md')
print(linux)        # ('README', 'md)
print(folder)       # ('folder', '')
```

#### `get_file_content` method

Returns the content of a file as a string.

- **Params:**
  - **path: str** – the path filename.
  - **encoding: str** – the encoding of the content if known, otherwise defaults to `'utf-8'`.
  - **bytes_number: int** – the number of bytes to read; if '0' the entire file is read.
- **Returns: str** – the file content as a string.

**Example:**
```python
from kf_utils.files import get_file_content

file_path: str = 'C:\\files\\test.txt'

file_content: str = get_file_content(file_path)

print(file_content)     # I'm the test file content
```

#### `get_file_extension` method

Returns the file extension from a path.

- **Params:**
  - **file_path: str** – absolute or relative path of the file.
- **Returns: str** – string with the extension of the file.

**Example:**
```python
from kf_utils.files import get_file_extension

file: str = "/home/test.txt"                # GIVEN a file path

extension: str = get_file_extension(file)   # RETURNS the extension of the file
print(extension)                            # "txt"
```

#### `remove_extension_from_file_path` method

Given the complete file path, remove the file extension.

- **Params:**
  - **file_path: str** – path where the file is.
- **Returns: str** – the entire file path without extension of the file.

#### `get_file_extension` method

Returns the file extension from a path.

- **Params:**
  - **file_path: str** – absolute or relative path of the file.
- **Returns: str** – string with the extension of the file.

**Example:**

```python
from kf_utils.files import get_file_extension

windows_file_path: str = 'C:\\utils\\README.md'
linux_file_path: str = '/home/README.md'
folder_path: str = 'C:\\folder'

windows: str = get_file_extension(windows_file_path)
linux: str = get_file_extension(linux_file_path)
folder: str = get_file_extension(folder_path)

print(windows)      # 'md'
print(linux)        # 'md'
print(folder)       # ''
```

#### `get_directory_and_file_name_and_extension_from_path` method

Given the complete file path, remove the entire file path and preserve the file name.

- **Params:**
  - **path: str** – path where the file is.
- **Returns: (str, str, str)** – directory of the file, file name and extension.

**Example:**
```python
from kf_utils.files import get_directory_and_file_name_and_extension_from_path

windows_file_path: str = 'C:\\utils\\README.md'
linux_file_path: str = '/home/README.md'
folder_path: str = 'C:\\folder'

windows: tuple[str, str, str] = get_directory_and_file_name_and_extension_from_path(windows_file_path)
linux: tuple[str, str, str] = get_directory_and_file_name_and_extension_from_path(linux_file_path)
folder: tuple[str, str, str] = get_directory_and_file_name_and_extension_from_path(folder_path)

print(windows)      # ('C:\\utils', 'README', 'md')
print(linux)        # ('/home', 'README', 'md)
print(folder)       # ('C:', '', 'folder)
```

#### `get_file_name` method

Extracts the file name and extension from a path.

- **Params:**
  - **file_path: str** – absolute or relative path of the file.
- **Returns: str** – file 'name.extension'.

**Example:**
```python
from kf_utils.files import get_file_name

file_path: str = "/home/test.txt"           # GIVEN an absolute path to a file

file_name: str = get_file_name(file_path)   # RETURNS the file name and extension
print(file_name)                            # "test.txt"
```

#### `get_file_root_path` method

Given the complete file path, remove the file name from the path.

- **Params:**
  - **file_path: str** – path where the file is.
- **Returns: str** – path to the directory in which a file is located without the file name.

#### `to_json` method

Save a dictionary to a JSON file.

- **Params:**
  - **dict_data: dict** – dictionary to save to json file.
  - **path: str** – absolute or relative path where the json will be saved.

**Example:**
```python
from kf_utils.files import to_json, exist

employee_file_path: str = '/home/employee.json'
employee: dict = {
  "employee": {
    "name": "John", 
    "age": 30, 
    "city": "New York"
  }
}

to_json(employee, employee_file_path)

# Does employee.json file exist?
print(exist(employee_file_path))       # True
```

#### `exist` method

Check if the file exists.

- **Params:**
  - **file_path: str** – absolute or relative path of the file.
- **Returns: bool** – boolean indicating if the file exists.

**Example:**
```python
from kf_utils.files import exist

existing_file_path: str = '/home/this_file_exists.txt'
not_existing_file_path: str = '/home/this_file_does_not_exists.txt'

existing_file_exist: bool = exist(existing_file_path)
not_existing_file_exist: bool = exist(not_existing_file_path)

print(existing_file_exist)          # True
print(not_existing_file_exist)      # False
```

#### `drop_dir` method

Recursively removes a directory tree from the file system.

- **Params:**
  - **dir_path: str** – path to the directory.

#### `drop_file` method

Removes a file from the file system.

- **Params:**
  - **file_path: str** – absolute or relative path of the file.

**Example:**
```python
from kf_utils.files import drop_file, exist

file_path: str = '/home/test.txt'

drop_file(file_path)

# Does test.txt file exist?
print(exist(file_path))        # False
```

#### `from_json` method

Returns the Python dictionary out of a JSON file.

- **Params:**
  - **file_path: str** – absolute or relative path of the json file to load.
- **Returns: dict** – file content as a Python dict.

**Example:**
```python
from kf_utils.files import from_json

employee_file_path: str = '/home/employee.json'

employee: dict = from_json(employee_file_path)

print(employee)     # {"employee":{"name":"John", "age":30, "city":"New York"}}
```

#### `from_yaml` method

Returns the Python dictionary out of a YAML file.

- **Params:**
  - **file_path: str** – absolute or relative path of the YAML file to load.
- **Returns: dict** – file content as a Python dict.

**Example:**
```python
from kf_utils.files import from_yaml

employee_file_path: str = '/home/employee.yaml'

employee: dict = from_yaml(employee_file_path)

print(employee)     # {"employee":{"name":"John", "age":30, "city":"New York"}}
```


#### `path_exists` method

> **Deprecated** since `v2.0.1`. It's replaced by `exist()` method.

Checks whether a file or directory exists or not.

- **Params:**
  - **path: str** – the path to the dir or file.
- **Returns: bool** – the result of the checking.

#### `grep` method

Checks whether a file or directory exists or not.

- **Params:**
  - **file: str** – the file containing the text to grep.
  - **text: str** – the string to find in the file content.
  - **case_sensitive: bool** – if False, the comparison is insensitive to the letter casing. By default, it is set 
    to True.
- **Returns: Iterator[str]** – the result of the checking.

#### `head` method

Returns the first **n** lines of a text file. If the number of lines is negative or the forwards flag is set to 
False, the lines are reversed.

- **Params:**
  - **file_path: str** – path to the file containing the text.
  - **lines: int** – number of lines to be returned.
  - **encoding: str** – the encoding of the content if known, otherwise defaults to 'utf-8'.
  - **forwards: bool** – whether the lines should be reversed. By default, it is set to True.
- **Returns: Iterator[str]** – the extracted lines from the file content.

#### `tail` method

Returns the last **n** lines of a text file. If the number of lines is negative or the forwards flag
is set to False, the lines are reversed.

- **Params:**
  - **file_path: str** – path to the file containing the text.
  - **lines: int** – number of lines to be returned.
  - **encoding: str** – the encoding of the content if known, otherwise defaults to 'utf-8'.
  - **forwards: bool** – whether the lines should be reversed. By default, it is set to True.
- **Returns: Iterator[str]** – the extracted lines from the file content.

#### `import_library` method

Imports a library dynamically if installed.

> **Note** Use Case: control the installation of different libraries based on the Operating System, the version of 
> the library, the dynamical installation of one library or another (e.g., install NLTK or spaCy?), etc.
> 
> See the DGI/SEMBU `FilePersistor.select()` method for a Use Case where the content of the file is returned as a 
> spaCy Doc if spaCy is installed or as a string if not installed.

> **Warning** Make sure the library `iadn` is installed.

- **Params:**
  - **package: str** – package to be installed.
- **Returns: Distribution** – the import statement as a Distribution object.

#### `make_dirs` method

Given the complete path to a file, creates the directories preceding the name of the file.

- **Params:**
  - **file_path: str** – a relative or absolute path or path file name.

**Example:**
```python
from kf_utils.files import make_dirs, exist

file_directory: str = '/home/testing'

# Does file_directory exist?
print(exist(file_directory))       # False

file_to_create: str = file_directory + '/test.txt'

make_dirs(file_to_create)

# Does file_directory exist?
print(exist(file_directory))       # True
```

#### `remove_file_protocol` method

Removes `file:` and `file://` from an url string, like in `'file:../test/files/eDeclaration.xsd'` or `'file:///home/paula/.
bashrc'`.

- **Params:**
  - **url: str or URL** – url to be modified.
- **Returns: str or None** – url without `'file://'` protocol.

#### `to_file_line` method

Inserts a line in a file containing multiple lines.

- **Params:**
  - **txt: str** – text to add in the file.
  - **file_path: str** – path to the file.
  - **index: int** – number of the line where the text will be inserted.

#### `xst_file` method

Checks whether a file or directory exists or not.

- **Params:**
  - **path: str** – the path to the dir or file.
- **Returns: bool** – the result of the checking.

#### `extract_files_from_zip_folder` method

Given the complete zip file path, unzip the documents zipped.

- **Params:**
  - **save_file_path: str** – path where the zip file is.
  - **temporal_folder: str** – path where the zip object will be temporally extracted.
- **Returns: list[str]** – list with the path to each unzipped file.

#### `get_file_name_length` method

Return the length of the file name.

- **Params:**
  - **file_path: str** – absolute or relative path of the file.
- **Returns: int** – int with the length of the file name.

**Example:**
```python
from kf_utils.files import get_file_name_length

file_name: str = "/home/test.txt"

file_name_length: int = get_file_name_length(file_name)
print(file_name_length)     # 4
```

#### `get_file_size` method

Return the file size.

- **Params:**
  - **file_path: str** – absolute or relative path of the file.
- **Returns: int** – bytes value of the file size.

**Example:**
```python
from kf_utils.files import get_file_size

file_name: str = "/home/test.txt"

file_size: int = get_file_size(file_name)
print(file_size)        # 10769322
```

***

#### `get_file_name_and_extension` method

Given a complete file path name, it separates the name of the file (including the path) from the extension.

- **Params:**
  - **file_path: str** – path to the file.
- **Returns: tuple(str, str)** – file name and extension.

**Example:**
```python
from kf_utils.files import get_file_name_and_extension

file_path: str = "home/test.txt"

file_name: str = get_file_name_and_extension(file_path)[0]
file_extension: str = get_file_name_and_extension(file_path)[1]
print(file_name)             # 'home/test_file'
print(file_extension)        # 'txt'
```

***

### `graphs` module

```python
import kf_utils.graphs
from kf_utils import graphs
```

Methods related with graphs management

#### `load_graph` method

Returns an instance of Graph from a file.

- **Params:**
  - **file_path: str** – absolute or relative path of the graph.
- **Returns: Graph** – Graph loaded.

**Example:**
```python
from kf_utils.graphs import load_graph

graph = load_graph('home/test.ttl') # -> Graph()
```

#### `convert_response_query_graph_to_df` method

Transforms the result of an rdf query using the rdflib library to a dataframe.

- **Params:**
  - **result_query: rdflib.query.Result** – rdflib query result.
- **Returns: pandas.DataFrame** – transformed query result to a dataframe.

***



### `hashers` module

```python
import kf_utils.hashers
from kf_utils import hashers
```

Helpers for custom hashing

#### `HashAlgorithm` class

Hashing methods enum.

It contains:
1. md5
2. sha1
3. sha256

#### `crc` method

Returns the CRC of a text as an int. Uses `zlib`.

- **Params:**
  - **value** – the value to hash.
- **Returns: int** – the CRC of the text as int.

#### `scrc` method

Returns the CRC of a text as a string. Uses `zlib`.

- **Params:**
  - **value** – the value to hash.
- **Returns: int** – the CRC of the text as string.

#### `hash` method

Returns the hash of a file content.

- **Params:**
  - **file: str** – the name of the file.
  - **algorithm: HashAlgorithm** – the type of hash. By default, it is set to md5.
- **Returns: str** – the hash of a file as string.

#### `md5` method

Returns the MD5 hash as a string.

- **Params:**
  - **text: str** – text to hash.
- **Returns: str** – MD5 of the text as string.

#### `hashbin` method

Returns the hash of a binary file content.

- **Params:**
  - **file: str** – path to the file.
  - **algorithm_type: HashAlgorithm** – algorithm to use to hash the file content. By default, is set to md5.
- **Returns: str** – the file content hashed using a specific algorithm as string.
- **Raises:**
  - **NotImplemented** – if the algorithm type is not implemented

**Example:**
```python
from kf_utils.hashers import hashbin, HashAlgorithm

file_path: str = '/home/test.txt'

md5_hash_content: str = hashbin(file_path)
sha256_hash_content: str = hashbin(file_path, HashAlgorithm.sha256)

print(md5_hash_content)         # dd18bf3a8e0a2a3e53e2661c7fb53534
print(sha256_hash_content)      # a6ed0c785d4590bc95c216bcf514384eee6765b1c2b732d0b0a1ad7e14d3204a
```

#### `md5int` method

Returns the MD5 hash as an int.

- **Params:**
  - **text** – text to hash.
- **Returns: int** – MD5 hash as integer.

#### `uuids` method

Returns a standard 4-UUID as a string.

- **Returns: str** – standard 4-UUID as a string.




***

### `lang` module

```python
import kf_utils.lang
from kf_utils import lang
```

Language functools

#### `alpha2` method

Returns the alpha-2 version of an expanded idb lang, like from 'en-US' into 'en'.

- **Params:**
  - **lang: str** – idb version of the lang.
- **Returns: str** – alpha-2 version of the lang.

***

### `lists` module

```python
import kf_utils.lists
from kf_utils import lists
```

Manipulation of lists

#### `duplicated` method

Returns True if an element of a list contains duplicated elements, or False otherwise.

- **Params:**
  - **elements: list** – list to be analysed.
- **Returns: bool** – whether the list contains duplicate elements.

#### `index` method

Returns the position of an string element in a list or None if not found.

- **Params:**
  - **list&#95;: list** – the list to look up into.
  - **pattern: str** – the string to find within the list.
  - **case_insensitive: bool** – if True the search does not care about the case of the pattern. By default, it is 
    set to True.
- **Returns: int** – the position of the pattern, an integer, or None if not found.

#### `ordered_set` method

Removes duplicate items from a list without altering the occurrence order. Faster than OrderedDict.

- **Params:**
  - **items: list** – list of items to order and remove duplicate.
- **Returns: list** – the given list without duplicate items.

#### `remove_duplicates` method

Removes duplicated elements from a list.

- **Params:**
  - **vector: list** – list of items.
- **Returns: list** – list without duplicate items.

***

### `replacers` module

```python
import kf_utils.replacers
from kf_utils import replacers
```

Helpers for advanced string replacement

#### `replace_chars` method

Returns a str where mapped `{'char': 'replacer', ...}` are replaced.

- **Params:**
  - **txt: str** – text where to replace specific chars.
  - **trans: dict** – dict that maps specific characters and its replacer. E.g.: `{'char': 'replacer', 'prod': 
    'test', 'author': 'SEMBU'}`.
- **Returns: str** – replaced text as string.

#### `replace_substrings` method

Replaces multiples substrings in a text with the pairs (`source_substring`, `target_substring`).

- **Params:**
  - **txt: str** – text where to replace specific substrings.
  - **tuple_list: list[tuple[str, str]]** – list of pairs (`source_substring`, `target_substring`).
- **Returns: str** – replaced text as string.

**Example:**
```python
from kf_utils.replacers import replace_substrings

text: str = "The quick brown fox jumps over the lazy dog"                   # GIVEN the text "The quick brown fox jumps over the lazy dog"
replacer: list[tuple[str, str]] = [("brown", "red"), ("lazy", "quick")]     # AND the list of pairs [("brown", "red"), ("lazy", "quick")]

new_text: str = replace_substrings(text, replacer)                          # RETURNS "The quick red fox jumps over the quick dog"
print(new_text)                                                             # "The quick red fox jumps over the quick dog"
```

#### `replace_match_boundaries` method

Replaces a word in a string but not other words containing that word.

- **Params:**
  - **to_replace: str** – text with substrings to be replaced.
  - **tuples: list[tuple[str, str]]** –  a list of tuples containing the substring to match and the replacer substring: 
    (`source_substring`, `target_substring`).
  - **escape_chars: dict** – a list of tuples containing special chars that need to be coded before the replacement. 
    By default, it is set to None.
  - **mask_quoted: bool** – if False, quoted substrings inside the `to_replace` will not be masked. Masking is used to 
    avoid unwanted boundaries inside the `to_replace` string. By default, it is set to False.
- **Returns: str** – replaced text as string.

**Example:**
```python
from kf_utils.replacers import replace_match_boundaries

text: str = "allowedX and allowed and allowedXX"                # GIVEN the string "allowedX and allowed and allowedXX"
replacer: list[tuple[str, str]] = [("allowed", "ALLOWED")]      # AND the list of pairs [("allowed", "ALLOWED")]

new_text: str = replace_match_boundaries(text, replacer)        # RETURNS "allowedX and ALLOWED and allowedXX"
print(new_text)                                                 # "allowedX and ALLOWED and allowedXX"
```

#### `replace_quoted` method

Replaces a portion of text (the `to_replace`) enclosed with double or single quotes (the `text_to_replace`) with an 
alternative text, unless it equals the `exclude` text.

> **Note**
> See the Compiler class within the Persistor package to see an example of how this is used to code and decode dots 
> (.) occurring between quotes.

- **Params:**
  - **quoted_txt: str** – the text containing quoted words and possibly unquoted words.
  - **to_replace: str** –  the text inside the quotes to be replaced.
  - **replacer: str** – the text used to swap the to_replace var with.
  - **exclude: str** – do not apply the replacement if the quoted text contains this text. By default, it is set to 
    None.
- **Returns: str** – replaced text as string.

**Example:**
```python
from kf_utils.replacers import replace_quoted
from kf_utils.hashers import hash

text: str = ''' a text with "double quoted dots ." and a p.function('.') call'''

new_text: str = replace_quoted(text, '.', hash('.'), '.')
print(new_text)                                             # ''' a text with "double quoted dots 5058f1af8388633f609cadb75a75dc9d and a p.function('.') call'''

# In the new_text all quoted text has been replaced with the dot hash, except in p.function('.'), since:
#   1. The dot between p and function is not double or single quoted.
#   2. The argument of the function contains the string to exclude.
```

#### `un_pad_fixed_locations` method

Given a text padded with padding_char, and a list with `(substring, start, end)` tuples, it replaces the portions that 
had been padded with the original text.

- **Params:**
  - **quoted_txt: str** – the text containing the substrings that are to be replaced with the masker.
  - **to_replace: list[tuple]** –  the list of tuples containing the `(masked_substrings, start, end)`.
- **Returns: str** – replaced text as string.

#### `replace` method

Replaces a text with the items in a list, except if the item is to be excluded.

- **Params:**
  - **original_txt: str** – the text original text to be analysed.
  - **to_replace: str** –  the text to be replaced.
  - **replacer: str** – the text used to swap the to_replace var with.
  - **listed_terms: list[str]** – list of terms to replace.
  - **exclude: str** – do not apply the replacement if the substring contains this text.
- **Returns: str** – replaced text as string.

#### `replace_angled` method

Treats differently the <> than when using replace_between_delimiters. Copes with the case where the line contains 
just one angle, like in exec statements with <, >, <=, and >= operators.

- **Params:**
  - **angled_txt: str** – the text containing angled words and possibly non-angled words.
  - **to_replace: str** –  the text inside the angled to be replaced.
  - **replacer: str** – the text used to swap the to_replace var with.
  - **exclude: str** – do not apply the replacement if the angled text contains this text. By default, it is set to 
    None.
- **Returns: str** – replaced text as string.

#### `replace_delimited` method

Ibidem to replace quoted, but with different delimiters to the left and right sides.

Replaces a portion of text (the `to_replace`) enclosed with specific delimiters (the `text_to_replace`) with an 
alternative text, unless it equals the `exclude` text.

- **Params:**
  - **delimited_txt: str** – the text containing delimited words and possibly non-delimited words.
  - **left: str** –  left delimiter.
  - **right: str** – right delimiter.
  - **to_replace: str** – the text inside the delimiters to be replaced.
  - **replacer: str** – the text used to swap the to_replace var with.
  - **exclude: str** – do not apply the replacement if the delimited text contains this text. By default, it is set 
    to None.
- **Returns: str** – replaced text as string.

***

### `strings` module

```python
import kf_utils.strings
from kf_utils import strings
```

Functools for the manipulation of strings

#### `indices` method

Searches a string (the `key`) in a text and returns a list with all the positions where the key occurs.

- **Params:**
  - **txt: str** – text where to search.
  - **key: str** –  substrings to search inside the text.
  - **case_sensitive: bool** – whether the search is case-sensitive. By default, it is set to True.
- **Returns: list** – list with all the positions where the key occurs in the given text.

#### `is_get_list` method

Determines whether a text is a valid Python's list.

> **Note**
> `is_get_` methods have a twofold mission:
> 1. they check that a condition is met, and
> 2. f the condition is met then return a value.
> 
> In this case, the condition to be met is that the text is a valid Python list expressed as a text. The value 
> returned is the Python's list.

- **Params:**
  - **o: list or str** – list or list-style string.
  - **dic: dict** – a dictionary with all the variables needed for the Python interpreter to execute the code; if 
    not provided, the presumption is that the statement to be executed is a primitive of the type x = 1 + 2, b = 
    True, h = "Hello World", or similar. By default, it is set to None.
- **Returns: list** – list with the `o` param content.

#### `json_str_to_dict` method

Used to read JSON objects expressed as texts and transform them into Python's dictionaries.

One usage of this method is to read JSONL files and process the contents, e.g. to store these contents into NO-SQL 
databased, such as in an Elasticsearch index as Elastic documents.

- **Params:**
  - **json_line: str** – json-style string.
- **Returns: dict** – Python's dictionary with the json content.

#### `mask_quoted` method

Extracts quoted substrings from a quoted text, masks (i.e., codes) the substrings and returns the masked text and a 
list of tuples with the pairs `[(original substring, masked substring), ...]`

- **Params:**
  - **quoted_txt: str** – text that contains quoted substrings.
- **Returns: (str, list[tuple[str, str]])** – masked text and a list of tuples with the pairs `[(original substring, masked substring), ...]`.

#### `unmask_quoted` method

For a given text, and a list of pairs `(substring, crc(substring))`, replaces previously masked substrings into their 
original forms.

- **Params:**
  - **masked_txt: str** – masked text returned by mask_quoted method. _Please refer to `mask_quoted` method 
    documentation._
  - **tuples: list[tuple[str, str]]** – list of tuples with the pairs `[(original substring, masked substring), ...]`.
- **Returns: str** – original text with its previously masked substrings replaced into their original forms.

#### `nnl` method

Replaces all new lined `'\n'` with `' '`

- **Params:**
  - **text: str** – text with new lines
- **Returns: str** – text without new lines.

#### `remove_comments` method

Removes C-like `/*...*/` block and `//` or `#` line comments.

- **Params:**
  - **txt: str** – the string containing comments.
  - **include_double_slash: bool** – include_double_slash: if True, line comments starting with '//' will be removed.
    By default, it is set to False, because strings containing 'http://whatever.org' would be reduced to 'http:'.
- **Returns: str** – text without comments.

#### `slash` method

Will add the trailing slash if it's not already there.

- **Params:**
  - **path: str** – path file name.
- **Returns: str** – slashed path file name.

#### `tokenize` method

Very elementary tokenizer totally oriented to parse Query strings. It implements at least some interesting features:
1. It is able to remove C-like comments (both block and line comments);
2. The list of punctuation signs can be customised, so one can decide what signs to isolate as tokens; and
3. It is fast and language-independent.

- **Params:**
  - **txt: str** – the string to be tokenized.
  - **punctuation_tokens: str** – a string with punctuation signs to be split. If None, a default list is provided. 
    By default, it is set to None.
- **Returns: list[str]** – the list of tokens.

#### `unaccent` method

Removes the diacritics and character symbols of a text.

- **Params:**
  - **text: str** – text with diacritics and character symbols.
- **Returns: str** – text without diacritics and character symbols.

#### `url_tail` method

Returns the element id of an url. If instead of sep being `'/'` it is a different one, this function can be used for 
many other purposes, e.g. getting the last element after `'#}'` in `'{blahblahblah.blablhablah#}type'`, which would 
return `'type'` if `sep = '#}'`.

- **Params:**
  - **url: str** – url where to find the id.
  - **sep: str** – url delimiter. By default, it is set to `'/'`.
- **Returns: str** – element id of the url as string.

#### `url_head` method

> **Note**
> See `url_tail`. Same comments

Returns the element id of an url. If instead of sep being `'/'` it is a different one, this function can be used for 
many other purposes, e.g. getting the last element after `'#}'` in `'{blahblahblah.blablhablah#}type'`, which would 
return `'{blahblahblah.blablhablah'` if `sep = '#}'`.

- **Params:**
  - **url: str** – url where to find the id.
  - **sep: str** – url delimiter. By default, it is set to `'/'`.
- **Returns: str** – head of the url as string.

#### `regex` method

Returns the result of the search regex.

- **Params:**
  - **content: str** – text where to search.
  - **regex_condition: str** – regex expression to search in the text.
- **Returns: str** – head of the url as string.

***

### `timers` module

```python
import kf_utils.timers
from kf_utils import timers
```

Helpers for custom timers

#### `now` method

Returns the current timestamp with timezone

- **Returns: datetime** – Current timestamp with Spain timezone.

**Example:**
```python
from datetime import datetime
from kf_utils.timers import now

now: datetime = now()

print(now)      # 2022-08-16 09:30:06.466873+02:00
```

#### `str_to_datetime` method

Given a string with a datetime in format **YYYY-mm-dd HH:MM:SS.f+Z** (e.g.: `2022-07-13 10:00:00.21324+00:02`), convert 
this string in a datetime object.

- **Params:**
  - **string_datetime: str** – string with a properly formatted datetime.
- **Returns: datetime** – datetime object.

**Example:**
```python
from datetime import datetime
from kf_utils.timers import str_to_datetime

date_str: str = '2022-08-16 09:30:06.466873+02:00'

date: datetime = str_to_datetime(date_str)

print(date)     # 2022-08-16 09:30:06.466873+02:00
```

#### `Timer` class

Class for capturing and display timedelta.

Attributes:
- **n:** datetime that represents the current instant
- **d:** Timedelta or None
- **out:** Output of the class

##### `now` method<a name="now-method-v2"></a>

This moment.

- **Returns: datetime** – the current instant as datetime.

##### `trig` method

Triggers `now()`, and returns `self`.

- **Returns: Timer** – the self object with n attribute updated with the current datetime instant.

##### `console` method

Prints the delta.

- **Returns: str** – the delta as string. _Please refer to `delta` method documentation for more information._

##### `delta` method

Difference between now and the last now.

If `reset = True` **n** is set to 0, thus being able to use consecutive deltas without having to re-now().

- **Params:**
  - **reset: bool** – if it is True, n attribute is set to 0. By default, it is set to False.
- **Returns: timedelta** – difference between now and the last now as timedelta object.

**Example:**
```python
from kf_utils.timers import Timer

t: Timer = Timer()
now = t.now()

print(t.delta(True))
print(t.delta(True))
```

##### `deltas` method

Returns the timedelta as a string. Please, refer to delta method documentation for more information.

- **Returns: str** – the timedelta as string.

***

### `data_types` package

```python
import kf_utils.data_types
from kf_utils import data_types
```

Custom data types used by the `kf_utils` modules and functions

#### `uri` module

```python
import kf_utils.data_types.uri
from kf_utils.data_types import uri
```

Core classes URL and URI

##### `URI` class

URI data type. Accepts the following protocols:
- file:../dir/dir/file.ext
- http://example.org
- ftp://repo.example.org/dir
- ftps://repo.example.org/dir
- mailto:username@server.org
- urn:zone:domain:host:etc

Attributes:
- **host:** URI's host part (e.g.: `'example.org'`).
- **uri_str:** URI stored as plain string.
- **protocol:** URI's protocol (e.g.: `'file:'`, `'http:'`, `'ftp:'`).

###### `validate` method

Checks whether the uri has a valid URI syntax, including the protocol `"file:"`

- **Params:**
  - **uri: str** – uri to validate.
- **Raises:**
  - **ArgumentException** – if uri has not a valid format.

###### `get_protocol` method

Returns the protocol of the URL (`"http:"`, `"ftp:"`, `"ftps:"`, `"file:"`). No need to verify if url is None, since this is taken 
care of at construction time.

- **Returns: str** – the protocol of the url.

###### `get_host` method

Returns the host of the URI (`"example.org"`). No need to verify if url is None, since this is taken care of at 
construction time.

- **Returns: str** – the protocol of the url.

##### `URL` class

Specialisation of `URI` class, for back-wards compatibility with previous NTT-DGI developments. _Please refer to 
`URI` class documentation._


#### `persistor_type` module 

```python
import kf_utils.data_types.persistor_type
from kf_utils.data_types import persistor_type
```

Enumeration of persistors used by the Knowledge Factory, and beyond.

##### `PersistorType` class

Defines the persistor types.


## Add new features, hotfixes or bugfixes

Please, refer to [CONTRIBUTING](./CONTRIBUTING.md), there is explained the methodolofy used to add new **features**, 
**hotfixes** and **bugfixes**.



## Run automatic tests

All the automatic tests are stored in [test](./test) folder. 
They can be run by both, executing [test.sh](./test.sh) script or executing the following command:

```shell
pip install --no-cache-dir --user --upgrade coverage unittest-xml-reporting && \
python -m coverage erase && \
python -m coverage run -m xmlrunner discover -o ./xunit_reports && \
python -m coverage report && \
python -m coverage xml -i
```

It will execute all the automatic tests, and it will create a new folder called *xunit_reports* and a new xml file 
called *coverage.xml*, that will contain the tests results and reports.



## Build `kf_utils` as a PyPi package

To build the **kf_utils** pip package you'll need to upgrade and use `setuptools` and `wheel` packages.

You can do both, execute [build.sh](./build.sh) script or execute the following commands in the repo root folder:

```shell
# Upgrade setuptools library
pip install --no-cache-dir --user --upgrade setuptools wheel && \

# Build the package
python -m setup sdist bdist_wheel
```

It will build the PyPi package, and will create several folders and files, the folders names will be: *build*, *dist* 
and *kf_utils.egg-info*. The most important folder is **dist**, there will be the distribution files of the kf_utils 
PyPi package.



## Project changelog

All notable changes to this project will be documented in [CHANGELOG](./CHANGELOG.md) file. So if you want to know 
about all the changes included in each release, check out this file.
