# syntax=docker/dockerfile:1
# check=error=true

ARG GITHUB_TOKEN=none_token
ARG GITHUB_USER=none_user

ARG APP_NAME=fastapi-template
ARG UBUNTU_VERSION=22.04
ARG USR_NAME=oceanos
ARG GRP_NAME=ihcantabria

ARG UV_VERSION=0.6.8
ARG RUFF_VERSION=0.9.7


### BASE stage
## - Ubuntu base image
## - misc: cdo curl git perl sudo vim
## - user creation
FROM ubuntu:${UBUNTU_VERSION} AS base
LABEL maintainer="German Aragon <german.aragon@unican.es>"
ARG USR_NAME
ARG GRP_NAME

RUN apt-get update --fix-missing
RUN apt-get install --fix-broken -y
# RUN apt-get install -y gfortran gcc g++ make
# RUN apt-get install -y hdf5-tools libhdf5-dev libhdf5-doc libhdf5-fortran-102 libhdf5-hl-100 libhdf5-hl-cpp-100 libhdf5-hl-fortran-100
# RUN apt-get install -y netcdf-bin netcdf-doc libnetcdf-dev libnetcdf-c++4 libnetcdf-c++4-dev libnetcdff7 libnetcdff-dev libnetcdff-doc
# RUN apt-get install -y pnetcdf-bin libpnetcdf-dev libnetcdf-pnetcdf-dev 
# RUN apt-get install -y openmpi-bin openmpi-common openmpi-doc libopenmpi3 libopenmpi-dev libhdf5-openmpi-dev
RUN apt-get install -y curl perl sudo vim git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends cdo 
RUN apt-get clean

# Install QT dependencies to allow QtAgg from PySide6 as matplotlib backend
RUN apt-get install -y libxcb-xinerama0 libxcb-cursor0 libx11-xcb1 libxrender1
RUN apt-get install -y libxi6 libxkbcommon-x11-0 libglu1-mesa libegl1-mesa libxcb1 libxcb-icccm4
RUN apt-get install -y libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0
RUN apt-get install -y libxcb-sync1 libxcb-xfixes0


# create user under `ihcantabria` group (or whaever is set under `GRP_NAME` arg)
RUN groupadd -g 1000 ${GRP_NAME} && \
    useradd -m -u 1000 -g ${GRP_NAME} ${USR_NAME}
# add user to sudo group, without sudo password
RUN usermod -aG sudo ${USR_NAME} && \
    echo "${USR_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER ${USR_NAME}
ENV HOME=/home/${USR_NAME}
WORKDIR ${HOME}


### Local development stage (development, made for devcontainer)
## - uv + ruff (Python tools)
FROM base AS local_development
ARG UV_VERSION
ARG RUFF_VERSION
RUN curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh
ENV PATH=${HOME}/.local/bin:$PATH
RUN uv tool install ruff@${RUFF_VERSION}


### Deployment stage (production)
## - all from OPERATIONAL_DEV stage
## - python code
FROM local_development AS deployment
ARG USR_NAME
ARG GRP_NAME
ARG GITHUB_TOKEN
ARG GITHUB_USER
ENV WORK_DIR=${HOME}/${APP_NAME}
RUN mkdir -p ${WORK_DIR}
WORKDIR ${WORK_DIR}
COPY --chown=${USR_NAME}:${GRP_NAME} .python-version pyproject.toml uv.lock ./
# see https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment

# Configure git to use the provided GitHub token
RUN echo ${GITHUB_USER}
RUN git config --global url."https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com".insteadOf "https://github.com"
RUN uv sync --frozen --no-dev

ENV PATH=${WORK_DIR}/.venv/bin:$PATH
COPY --chown=${USR_NAME}:${GRP_NAME} ${APP_NAME} ${APP_NAME}

### Deployment stage (production + cerrts and binary)
FROM deployment AS deployment_final

ADD teseo ${WORK_DIR} 
COPY cert.crt /certificados/cert.crt
COPY cert.key /certificados/cert.key

# Run the service
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile=/certificados/cert.key", "--ssl-certfile=/certificados/cert.crt"]

