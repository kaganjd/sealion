## Server

Uses Python 3.6, aiohttp

For first-time setup with virtualenv:

1. `$ cd server`
2. `$ virtualenv venv`
3. `$ source venv/bin/activate`
4. `$ pip install -r requirements.txt` to install dependencies (`pip install NEW_PACKAGE && pip freeze > requirements.txt` to save new dependencies)

Start server:

3. `$ python main.py` from `server/` directory starts a server on port 8080

## Client

Uses Javascript, webpack

- `$ npm install` installs dependencies
- `$ npm run build` creates `client/dist/main.js`

## Tests

Uses pytest

- `$ pytest` from `server/` directory runs tests
- add tests to `server/tests/` directory with the naming convention `test_*.py`

## Use

There's a sample p5.js project with `main.js` included. To view the sample project:

- in one Terminal window, go to the `server/` directory, follow the server setup steps, and start the server
- in another Terminal window, go to the `client/` directory and run `npm run build` to create `dist/main.js`
- open `index.html` in your browser
- open devtools so you can see the console
