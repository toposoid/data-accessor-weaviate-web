# data-accessor-weaviate-web
Under Construction
This is a WEB API that works as a microservice within the Toposoid project.
Toposoid is a knowledge base construction platform.(see [Toposoid Root Project](https://github.com/toposoid/toposoid.git))
This microservice is a CUID wrapper for Weaviate (https://github.com/weaviate/weaviate).

[![Test And Build](https://github.com/toposoid/data-accessor-weaviate-web/actions/workflows/action.yml/badge.svg)](https://github.com/toposoid/data-accessor-weaviate-web/actions/workflows/action.yml)

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

## Note
* This microservice uses 9011 as the default port.
* This microservice uses [Weaviate](https://github.com/weaviate/weaviate)

## License
This program is offered under a commercial and under the AGPL license.
For commercial licensing, contact us at https://toposoid.com/contact.  For AGPL licensing, see below.

AGPL licensing:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

## Author
* Makoto Kubodera([Linked Ideal LLC.](https://linked-ideal.com/))

Thank you!