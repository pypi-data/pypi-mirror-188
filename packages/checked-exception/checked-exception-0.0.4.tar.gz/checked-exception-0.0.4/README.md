# Checked Exception

This is a checked exception library, which tries to implement checked exceptions in Python.

## Publish to test.pypi.org (for testing purpose)

Need to `pip install wheel twine` first

```
python setup.py sdist bdist_wheel
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# And maybe delete this?
rm -rf dist
```

install it with like

```
pip install -i https://test.pypi.org/simple/ checked-exception==0.0.3
```

## Publish

```
python setup.py sdist bdist_wheel
python -m twine upload dist/*
rm -rf dist
```
