FROM python:3.9.16

WORKDIR /app
ARG TARGET_BRANCH
ENV DEPLOYMENT=local

SHELL ["/bin/bash", "-c"]

RUN apt-get update \
&& apt-get -y install git unzip \
&& curl -LsSf https://astral.sh/uv/install.sh | sh \
&& source ${HOME}/.local/bin/env \
&& git clone https://github.com/toposoid/data-accessor-weaviate-web.git \
&& cd data-accessor-weaviate-web \
&& git fetch origin ${TARGET_BRANCH} \
&& git checkout ${TARGET_BRANCH} \
&& sed s/__##GIT_BRANCH##__/${TARGET_BRANCH}/g pyproject.toml.template > pyproject.toml \
&& uv sync
#&& sed -i s/__##GIT_BRANCH##__/${TARGET_BRANCH}/g requirements.txt \
#&& pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt


COPY ./docker-entrypoint.sh /app/
ENTRYPOINT ["/app/docker-entrypoint.sh"]
