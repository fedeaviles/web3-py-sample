[![codecov](https://codecov.io/gh/fedeaviles/web3-py-sample/branch/main/graph/badge.svg?token=AW59LH04G5)](https://codecov.io/gh/fedeaviles/web3-py-sample)

# Interact with Products contract

You will need at least 2 addresses with their respective private keys

## Setup

clone repo

```
pipenv shell
pipenv install
```

## API

### Start server

```
pipenv shell
uvicorn main:app
```

View and interact with the endpoints at http://127.0.0.1:8000/docs

## Sign Service

### Start server

```
pipenv shell
uvicorn service:app --port=8001
```

## Functions

```
pipenv run ipython
from app.functions import *
```

then run the function you want to

## Events

use another console to listen the events

```
pipenv run ipython
from app.events import *
```

to listen the events for new products

```
listen_new_products()
```

or to listen the events for accepted products

```
listen_accepted_products()
```

or to listen the events for delegated products, you need to subscribe to

```
suscribe('newOwnerAddress')
listen_delegated_products()
```

## Tests

```
pipenv run pytest
```
