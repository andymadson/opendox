# `cache` Module

**Source:** `src\opendox\core\cache.py`

Module containing 8 functions and 1 classes

## Overview

This module contains **5** functions and **1** classes.

### Classes

- [`DocumentationCache`](#documentationcache)

### Functions

- [`__init__()`](#__init__)
- [`_load_cache()`](#_load_cache)
- [`get_file_hash()`](#get_file_hash)
- [`needs_update()`](#needs_update)
- [`update()`](#update)

---

## Classes

### `DocumentationCache`

```python
class DocumentationCache
```

#### Description

Class DocumentationCache with 8 methods.

#### Methods

| Method | Description |
|--------|-------------|
| `__init__()` | Initialize the class instance |
| `_load_cache()` | Private method |
| `get_file_hash()` | Method implementation |
| `needs_update()` | Method implementation |
| `update()` | Method implementation |
| `save()` | Method implementation |
| `clear()` | Method implementation |
| `remove_entry()` | Method implementation |

**Source:** Lines 7-68

---

## Functions

### `__init__()`

```python
__init__(self, project_root: Path, output_dir: Path)
```

#### Description

*No documentation available*

**Source:** Lines 8-13

---

### `_load_cache()`

```python
_load_cache(self) -> Dict
```

#### Description

*No documentation available*

**Source:** Lines 15-21

---

### `get_file_hash()`

```python
get_file_hash(self, file_path: Path) -> str
```

#### Description

*No documentation available*

**Source:** Lines 23-29

---

### `needs_update()`

```python
needs_update(self, file_path: Path) -> bool
```

#### Description

*No documentation available*

**Source:** Lines 31-46

---

### `update()`

```python
update(self, file_path: Path)
```

#### Description

*No documentation available*

**Source:** Lines 48-51

---


*Generated on 2025-08-27 14:32:53 by OPENDOX*
