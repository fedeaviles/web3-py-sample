# Interact with Products contract

You will need at least 2 addresses with their respective private keys

## Setup

clone repo

```
pipenv shell
pipenv install
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
pipenv run pytest app
```
