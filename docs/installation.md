### Installation instructions


You must currently build ``pyoz`` from source using **Python 3.4+**.
In the near future, ``pip`` and ``conda`` packages will become available.

Until then, we recommend that you install the ``pyoz`` dependencies using
 [``conda``](https://www.continuum.io/downloads) and install ``pyoz`` itself
 directly from its source on github:
 
```bash
conda install scipy numba
pip install git+https://github.com/ctk3b/pyoz.git#egg=pyoz
```

but, in theory, you can also install them via pip:

```bash
pip install scipy numba
pip install git+https://github.com/ctk3b/pyoz.git#egg=pyoz
```
#### Editable install

If you want to make modifications to the source code, you should install 
``pyoz`` in [``editable mode``](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs):

```bash
conda install scipy numba
pip install -e git+https://github.com/ctk3b/pyoz.git#egg=pyoz
cd src/pyoz
```

#### Testing your installation

The test suite uses ``pytest`` which you can install
via ``pip``:

```bash
pip install pytest
```

To run the tests, enter the `pyoz` directory and run:

```bash
py.test -v
```