#!/bin/bash
python -m build
twine upload --repository testpypi dist/*
twine upload --repository pypi dist/*
