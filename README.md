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

The public function validates the PD code, optionally simplifies Reidemeister-I and nugatory crossings, and sends the normalized `PD[X[...]]` document to the high-performance integer Khovanov backend. The backend constructs the cube of resolutions, composes cobordism maps, performs chain-complex reductions, and reports the bigraded free and torsion groups in `q^...*t^...*Z[...]` form. The wrapper preserves the historical `solve_khovanov` signature.

## Input conventions

A PD code is represented as a list of four-entry crossings. Arc labels normally occur exactly twice. Public functions validate inputs and return new values rather than mutating caller-owned data unless their API explicitly says otherwise.

## External software

- A C++14 compiler such as GCC or Clang is required the first time the backend is compiled.
- A Java runtime is not required by the current implementation.

## Development

Run examples and package checks before release. Python packages require Python 3.10 or newer. Build PyPI artifacts with:

```bash
poetry check
poetry build
```

## License

MIT. See `LICENSE`.
