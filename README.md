## Server

Uses Python 3.6, aiohttp

For first-time setup with virtualenv:

1. `cd p5.packets-server`
2. `virtualenv venv`
3. `source venv/bin/activate`
4. `pip install pipenv`
5. `pipenv install` installs the dependencies listed in Pipfile

Start server:

3. `python main.py` starts a server on port 8080

## Client

Uses Javascript, webpack

- `npm install` installs dependencies
- `npm run build` creates `dist/main.js`

## Use

There's a sample p5.js project with `main.js` included. To view the sample project:

- in one Terminal window, go to the `p5.packets-server` directory, follow the server setup steps, and start the server
- in another Terminal window, go to the `p5.packets-client` directory and run `npm run build` to create `dist/main.js`
- open `index.html` in your browser
- open devtools so you can see the console
