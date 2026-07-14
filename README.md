# javakh-interface

Provide a stable Python API for integral Khovanov homology computation.

## Installation

```bash
pip install javakh-interface
```

## Usage example

```python
from javakh_interface import solve_khovanov

pd = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
print(solve_khovanov(pd))
```

## Algorithm

The compatibility wrapper forwards the historical `solve_khovanov` options to `cppkh-interface`. That backend validates the PD code, optionally simplifies Reidemeister-I and nugatory crossings, and evaluates the normalized diagram with its integer Khovanov engine. Batch and explicit crossing-sign APIs are forwarded without silently changing arguments, so downstream link-orientation enumeration can share one native process.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

- A C++14 compiler such as GCC or Clang is required the first time the backend is compiled.
- A Java runtime is not required by the current implementation.

## Development

Python 3.10 or newer is required. Contract tests use a mock native backend and therefore do not compile C++:

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of repository maintenance.

## License

MIT. See `LICENSE`.

## Citation

If you use this repository in academic work, please cite it as:

```bibtex
@software{topologicalknotindexer_javakh_interface,
  author = {{GGN\_2015}},
  title = {{javakh\_interface}},
  year = {2026},
  url = {https://github.com/TopologicalKnotIndexer/javakh_interface}
}
```
