# javakh-interface

Compute integral Khovanov homology through the corrected, high-performance cppkh backend.

## Installation

```bash
pip install javakh-interface
```

## Quick start

`from javakh_interface import solve_khovanov` then `solve_khovanov(pd_code)`.

PD codes are lists of four-entry crossings. Each arc label must occur exactly twice. Functions validate their inputs and do not mutate caller-owned PD-code lists unless explicitly documented.

## Development

Use Python 3.10 or newer for Python packages. Build distributions with `poetry build`. Run the package's tests or examples before publishing. C++ projects require a modern standards-compliant compiler.

## License

MIT. See `LICENSE`.
