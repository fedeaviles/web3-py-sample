# Interact with Products contract

## Setup

clone repo

```
pipenv shell
pipenv install
```

## Functions

```
pipenv run ipython
from functions import *
```

then run the function you want to

## Events

use another console to listen the events

```
pipenv run ipython
from events import *
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
