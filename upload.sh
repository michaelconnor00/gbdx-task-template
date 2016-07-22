echo "[pypi]" > ~/.pypirc
echo "repository=https://pypi.python.org/pypi" >> ~/.pypirc
echo "username:" $PYPI_USERNAME >> ~/.pypirc
echo "password:" $PYPI_PASSWORD >> ~/.pypirc
cat ~/.pypirc
python setup.py sdist upload
