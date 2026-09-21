See @README.md for the general behavior of this tool.

- This project uses static type checking for Python via pyright, configured in
  `pyproject.toml` under `[tool.pyright]` (strict mode). The type-checked code
  is the deployment tooling under `tools/` (`backup.py`, `syscheck.py`,
  `utils.py`) and `traefik/overview-page/generate.py`.
- `praktomat/local.py` is excluded from type checking: it's a Django settings
  fragment that gets copied into the (externally cloned) Praktomat application
  image, and it relies on names defined by that application's
  `settings/defaults.py`, which isn't part of this repo.
- Python dependencies are declared in `requirements.txt` (`libPyshell`, the
  library behind `from shell import *` in the scripts above, and `pyright`
  itself) and installed with `pip` into the virtual environment at `.venv`.
- `./check-ci` type checks the project (runs pyright inside the `.venv`).
- Definition of done: `./check-ci` must pass without errors.
