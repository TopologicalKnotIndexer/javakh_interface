# javakh_interface
use python to solve khovanov homology with javakh (jre needed).

## Install

```bash
pip install javakh-interface
```

## Usage

```python
import javakh_interface

pd_code = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
print(javakh_interface.solve_khovanov(pd_code))
```
