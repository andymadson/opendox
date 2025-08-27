# `main` Module

**Source:** `src\opendox\cli\main.py`

Module containing 7 functions and 0 classes

## Overview

This module contains **5** functions and **0** classes.

### Functions

- [`version_callback()`](#version_callback)
- [`callback()`](#callback)
- [`init()`](#init)
- [`generate()`](#generate)
- [`serve()`](#serve)

---

## Functions

### `version_callback()`

```python
version_callback(value: bool)
```

#### Description

*No documentation available*

**Source:** Lines 19-24

---

### `callback()`

```python
callback(version: Optional[bool])
```

**Decorators:**
- `@app.callback()`

#### Description

*No documentation available*

**Source:** Lines 27-34

---

### `init()`

```python
init(repo: str, output: Path, config: Optional[Path])
```

**Decorators:**
- `@app.command()`

#### Description

*No documentation available*

**Source:** Lines 37-66

---

### `generate()`

```python
generate(path: Path, output: Path, model: str, max_files: int, no_incremental: bool)
```

**Decorators:**
- `@app.command()`

#### Description

Here is a Python docstring for your function:

**Source:** Lines 69-89

---

### `serve()`

```python
serve(port: int, host: str)
```

**Decorators:**
- `@app.command()`

#### Description

*No documentation available*

**Source:** Lines 92-98

---


*Generated on 2025-08-27 14:32:53 by OPENDOX*
