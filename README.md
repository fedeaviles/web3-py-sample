[![codecov](https://codecov.io/gh/fedeaviles/web3-py-sample/branch/main/graph/badge.svg?token=AW59LH04G5)](https://codecov.io/gh/fedeaviles/web3-py-sample)

# Interact with Products contract

## Docker and Docker Compose installation

Install Docker:

- `https://docs.docker.com/install/`

After install Docker, proceed to install Docker Compose:

- `https://docs.docker.com/compose/install/`

## Setup

Copy the `.env.example` and complete it with your secrets.

```bash
cp .env.example .env
```

### Build image

```bash
docker-compose -f docker-compose.yml build
```

### Run

```bash
docker-compose -f docker-compose.yml up -d
```

### Stop

```bash
docker-compose -f docker-compose.yml down
```

## API

View and interact with the endpoints at

- Main Api: http://localhost:8000/docs
- Sign Service: http://localhost:8001/docs

## Functions

```
docker-compose exec api ipython
from app.functions import *
```

then run the function you want to

## Events

use another console to listen the events

```
docker-compose exec api ipython
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
docker-compose exec api pytest
```
