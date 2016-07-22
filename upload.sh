echo "[server-login]" >> ~/.pypirc
echo "username:" $PYPI_USERNAME >> ~/.pypirc
echo "password:" $PYPI_PASSWORD >> ~/.pypirc
python setup.py sdist upload
