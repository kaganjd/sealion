## Client

Uses Javascript, webpack

- `npm run build` creates `dist/main.js`
- `npm run precommit` to prettify before making commits. This will automatically `git add` the files you run it on.

## Server

Uses Python 3.6, aiohttp

For first-time setup with virtualenv:

1. `cd p5.packets-server`
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install pipenv`
5. `pipenv install` installs the dependencies listed in Pipfile

Start server:

3. `python3 main.py` starts a server on port 8080
