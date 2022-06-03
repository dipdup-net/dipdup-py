# syntax=docker/dockerfile:1.3-labs
FROM python:3.11.0b3-slim-bullseye
ARG EXTRAS
SHELL ["/bin/bash", "-x", "-v", "-c"]

RUN <<eot
    apt update
    apt install -y --no-install-recommends make git sudo gcc build-essential libffi-dev `if [[ $EXTRAS =~ "pytezos" ]]; then echo pkg-config libsodium-dev libsecp256k1-dev libgmp-dev; fi`
    pip install poetry==1.2.0b1
    useradd -ms /bin/bash dipdup
    mkdir /home/dipdup/source
    rm -r /var/lib/apt/lists/* /var/log/* /tmp/*
eot

COPY --chown=dipdup Makefile pyproject.toml poetry.lock README.md /home/dipdup/source/
COPY --chown=dipdup inject_pyproject.sh /usr/bin/inject_pyproject.sh
WORKDIR /home/dipdup/source

RUN <<eot
    # We want to copy our code at the last layer but not to break poetry's "packages" section
    mkdir -p /home/dipdup/source/src/dipdup
    touch /home/dipdup/source/src/dipdup/__init__.py
    poetry config virtualenvs.create false
    make install DEV=0 EXTRAS="${EXTRAS}"
    # apt purge -y gcc build-essential pkg-config
    echo 'sudo /usr/bin/inject_pyproject.sh' >> /usr/bin/inject_pyproject
    echo 'dipdup ALL = NOPASSWD: /usr/bin/inject_pyproject.sh' >> /etc/sudoers
    chmod +x /usr/bin/inject_pyproject.sh
    chmod +x /usr/bin/inject_pyproject
eot

COPY --chown=dipdup . /home/dipdup/source

USER dipdup
WORKDIR /home/dipdup/
ENTRYPOINT ["dipdup"]
CMD ["run"]
