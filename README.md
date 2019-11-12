# Server

The server code!

## Installation

Environment and dependencies managed using `pipenv`
(considering dockerization)

To enter the environment:

```bash
pipenv shell
```

To install the whole dependencies:

```bash
pipenv install
```

To exit the environment:

```bash
exit
```

## Start the server

first you should install `mongodb` and `redis` on your machine.

- `mongodb`: https://www.mongodb.com/download-center/community
- `redis`: https://redis.io/download
  - windows alternative: https://www.memurai.com/

Once you started `mongodb` and `redis`. Filling the configurations in `config.ini`. Then run the server using following command:

```bash
python app/app.py
```

You can access the Swagger API from `http://localhost:23333/doc/`

## Editor, linting, formatting ... etc

Using the basic configuration of:

- linter: `flake8`
- formatter: `yapf`
- refactoring: `rope`

Recommended environment: `vscode` with official python plugin.

## Architecture

The code has layers from top to bottom:

- `controller`: where to validate a request
- `service`: where there is somea logic
- `datasources`:
  - `model`: mongodb connection
  - `cache`: redis connection
  - `mq`: redis connection (mainly sending messages according to users' actions)

We have to hold the static files for our SPA.
