# data-accessor-weaviate-web
Under Construction
This is a WEB API that works as a microservice within the Toposoid project.
Toposoid is a knowledge base construction platform.(see [Toposoid Root Project](https://github.com/toposoid/toposoid.git))
This microservice is a CUID wrapper for Weaviate (https://github.com/weaviate/weaviate).


## Requirements
* Docker version 20.10.x, or later
* docker-compose version 1.22.x
* The following microservices must be running
> semitechnologies/weaviate:1.21.2


## Setup
```bssh
docker-compose up -d
```

## Usage
http://localhost:9011/docs

# Note
* This microservice uses 9011 as the default port.
* This microservice uses [Weaviate](https://github.com/weaviate/weaviate)

## License
toposoid/data-accessor-weaviate-web is Open Source software released under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).

## Author
* Makoto Kubodera([Linked Ideal LLC.](https://linked-ideal.com/))

Thank you!