# pylogger_unified

A python wrapper that handles web logging, standard application logging to different format: json (gelf), colored text, raw, gnome notifications

## Build manually (testing env for the moment)

Install testing envrionment here: <https://packaging.python.org/en/latest/tutorials/packaging-projects/>.

```bash
cd pylogger-unified/
python3 -m build
python3 -m twine upload --repository testpypi ./dist/*
```

## Install the lib (testing env for the moment)

```bash
pip3 install -i https://test.pypi.org/simple/ pylogger_unified
```

## Start Using the lib

```python3
from pylogger_unified import logger as pylogger_unified
logger=pylogger_unified.init_logger()
logger.info("this is a test")
```
