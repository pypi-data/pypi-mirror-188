To publish to PyPi you have to pass the creds for pypi
- increment the version number in pyproject.toml
- poetry build
- poetry publish --username(not email) --password

# Rivertils
Scripts that are imported by packages you've deployed to pypi