# virtual-glob

Globbing of remote/virtual file systems.

## Motivation

Globbing is a common operation in many programs, but it is not always required to use the local file system, as is the case for `glob.glob` or `pathlib.Path.glob`.
This package provides a way to glob over remote/virtual file systems.

Apart from [python-glob2](https://github.com/miracle2k/python-glob2), which is unmaintained,
I could not find another Python packages that provided this functionality, so I made my own!

## Usage

Install the package:

```bash
pip install virtual-glob
```

Use the `glob` function, which can take a `pathlib.Path` instance, the provided `InMemoryPath` class, or any other class that implements the `VirtualPath` below:

```python
from virtual_glob import glob, InMemoryPath

fs = InMemoryPath.from_list(["a/b/c/my1.txt", "e/f/g/my2.txt", "x/y/z/other.txt"])
matches = {p.path for p in glob(fs, "**/my[0-9].txt")}
assert matches == {"a/b/c/my1.txt", "e/f/g/my2.txt"}
```

See the tests for more examples.

## Virtual file systems

The file system must be accessible via a single class, directly mimicking `pathlib.Path`, with the following protocol:

```python
class VirtualPath(Protocol):
    @property
    def name(self) -> str:
        """Return the name of this path."""

    def is_dir(self) -> bool:
        """Return True if this path is a directory."""

    def iterdir(self: PathType) -> Iterable[PathType]:
        """Iterate over the contents of this directory."""

    def joinpath(self: PathType, *parts: str) -> PathType:
        """Join this path with the given parts."""

    def exists(self) -> bool:
        """Return True if this path exists."""
```

## Rules

- Patterns must be in POSIX format, i.e. `/` is the path separator.
- Patterns must be relative, i.e. they must not start with `/`.
- Patterns are case-sensitive.
- Patterns with a trailing `/` only match directories.
- `**` matches zero or more directories, it must be the only thing in a path segment.
- `*` matches zero or more characters, except `/`.
- `?` matches exactly one character, except `/`.
- `[...]` matches one character in the set, except `/`.
- `[!...]` matches one character not in the set, except `/`.

## Design

Make as few calls to the underlying file system as possible, particularly for `iterdir`.
For example, looking to "short-circuit" when a pattern contains no "magic" characters.
