# TO PUSH

`rm -rf dist/*`
`python3 setup.py bdist_wheel --universal`
`python3 -m pip install twine`
`twine upload dist/*`
