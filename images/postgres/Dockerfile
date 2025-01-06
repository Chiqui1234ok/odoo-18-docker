FROM postgres:17.2

# Cambiar temporalmente al usuario root
USER root

# Crear grupo y usuario "opam" con UID y GID 2001
RUN groupadd -g 2001 opam && \
    useradd -u 2001 -g opam -m -s /bin/bash opam

# Utilizar "opam" como propietario en:
#   - /var/lib/postgresql/data
RUN chown -R opam:opam /var/lib/postgresql/data && \
    chmod -R 770 /var/lib/postgresql/data

# Cambiar al usuario "opam"
USER opam