# 🌊 Sea Lion

Sea Lion makes network information available as a data source for p5.js sketches.

To do that, Sea Lion relies on a local server talking to the network and serving information it collects to a JavaScript client. From there, you can use p5.js functions to consume and process the network data however you want.

# Getting started

1. Clone this repository

## Server

For first-time setup with virtualenv:

1. Open up Terminal and `$ cd sealion/server/` to get to the server directory
2. `$ virtualenv venv` to create a virtualenv
3. `$ source venv/bin/activate` to activate the virtualenv
4. `$ pip install -r requirements.txt` to install Python dependencies

Then either start the server with a GUI control panel:

5. `$ python main.py --gui`

Or start the server with a CLI:

5. `$ python main.py --cli` starts a server on port 8080

## Client

1. In a separate Terminal tab from the server, `cd` to the `sealion/client/` directory
2. Run `$ npm install` to install Node.js dependencies
3. Open `sealion/client/sample-project/index.html` in your browser

# Development

## Server

From `server/`:

- `pip install NEW_PACKAGE && pip freeze > requirements.txt` to save new dependencies

## Client

From `client/`:

- `$ npm run build` creates `client/dist/main.js`

## Docs

See [docs-specific README](./metadocs/README_docs.md)

## Tests

Uses pytest

- `$ pytest` from `server/` directory runs tests
- `$ pytest --cov=src` from `server/` creates a coverage report
- add tests to `server/tests/` directory with the naming convention `test_*.py`

# GUI troubleshooting

To run the server GUI, you will need [Tk/Tcl](http://www.tcl.tk/) in your virtual environment. Tk/Tcl is bundled with most installations of Python, but if it was not automatically added to your virtual environment, then try reinstalling your virtual environment:

1. `$ cd sealion/server/` to get to the server directory if you're not there already
1. `$ deactivate` to stop your current virtual environment session
1. `$ rm -rf venv` to remove the `venv` directory so you can create a new one
1. `$ virtualenv --system-site-packages venv` to reinstall your virtual environment
1. Re-run steps 3-5 in the [server section](https://github.com/kaganjd/sealion#server) of "Getting started" above.
