# `cache_manager` Module

**Source:** `src\opendox\core\cache_manager.py`

Module containing 3 functions and 1 classes

## Overview

This module contains **3** functions and **1** classes.

### Classes

- [`DocumentationCache`](#documentationcache)

### Functions

- [`__init__()`](#__init__)
- [`get_cached_doc()`](#get_cached_doc)
- [`cache_doc()`](#cache_doc)

---

## Classes

### `DocumentationCache`

```python
class DocumentationCache
```

#### Description

Cache documentation with Redis.

#### Methods

| Method | Description |
|--------|-------------|
| `__init__()` | Initialize the class instance |
| `get_cached_doc()` | Method implementation |
| `cache_doc()` | Method implementation |

**Source:** Lines 12-47

---

## Functions

### `__init__()`

```python
__init__(self, redis_url: str)
```

#### Description

*No documentation available*

**Source:** Lines 15-25

---

### `get_cached_doc()`

```python
get_cached_doc(self, code_hash: str) -> Optional[str]
```

#### Description

*No documentation available*

**Source:** Lines 27-35

---

### `cache_doc()`

```python
cache_doc(self, code: str, documentation: str, ttl: int)
```

#### Description

*No documentation available*

**Source:** Lines 37-47

---


*Generated on 2025-08-27 14:32:53 by OPENDOX*
