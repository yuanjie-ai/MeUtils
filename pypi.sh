#!/usr/bin/env bash
python setup.py sdist bdist_wheel && twine upload ./dist/*

pip install ./dist/*.whl -U
rm -rf ./build ./dist ./*.egg* ./.eggs
exit

# twine upload -r pypi dist/*
# twine upload -r pypitest dist/*

# vim ~/.pypirc
#[distutils] # this tells distutils what package indexes you can push to
#index-servers =
#  pypi
#  pypitest
#
#[pypi]
#repository: https://pypi.python.org/pypi
#username: myuser
#password: mypwd
#
#[pypitest]
#repository: https://testpypi.python.org/pypi
#username: myuser
#password: mypwd
