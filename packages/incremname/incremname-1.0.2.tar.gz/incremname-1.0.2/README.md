# incremname

This Python package, based on `os.path` functions, increments a file or folder name if it already exists.

## Requirements

Python 3.8 or later is required (because [the walrus operator](https://peps.python.org/pep-0572/) is used in the source code). The package is OS independent.

## Installation

`pip install incremname`

## Basic Usage

```python
from incremname import incname

path = r"C:\Documents\file.txt"
with open(incname(path), "w") as f:
    f.write("text")
```

* If `file.txt` does not exist, `incname(path)` returns `file.txt`.

* If `file.txt` exists but `file.01.txt` does not exist, `incname(path)` returns `file.01.txt`.

* If `file.txt` and `file.01.txt` exist but `file.02.txt` does not exist, `incname(path)` returns `file.02.txt`.

* ...and so on.

The same works with folders.

## Advanced Usage

Function `incname(path)` has five keyword arguments with default values:

* `z_fill=2` is an argument of `zfill()` to fill the counter with leading zeros,

* `sep_1="."` is a separator before the counter,

* `sep_2=""` is a separator after the counter,

* `start=1` is the first value of the counter,

* `use_ext=True`: if `True`, then the counter is added before the extension (that is got from `os.path.splitext(path)`); if `False`, then the counter is added after `path` and `os.path.splitext(path)` is not used. The latter might be useful, e.g., for folders that contain `.` in their names.

## Warning

[TOCTOU](https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use) is not controlled here.

## Changelog

* Version 1.0.2 (2023-01-30): add use_ext argument

* Version 1.0.1 (2023-01-15): add long description

* Version 1.0.0 (2023-01-15): initial release

----------

**incremname**

Version 1.0.2 (2023-01-30)

Copyright (c) 2023 Evgenii Shirokov

MIT License
