FROM odoo:18

# Cambiar temporalmente al usuario root
USER root

# Copiar el archivo de configuración de Odoo
COPY ./etc/odoo.conf /etc/odoo.conf

# Crear grupo y usuario "opam" con UID y GID 2000
RUN groupadd -g 2000 opam && \
    useradd -u 2000 -g opam -m -s /bin/bash opam

# Utilizar "opam" como propietario en:
#   - /var/lib/odoo
#   - /mnt/extra-addons
#   - /etc/odoo.conf
RUN chown -R opam:opam /var/lib/odoo && \
    chmod -R 770 /var/lib/odoo

RUN chown -R opam:opam /mnt/extra-addons && \
    chmod -R 770 /mnt/extra-addons

RUN chown opam:opam /etc/odoo.conf && \
    chmod 770 /etc/odoo.conf

# Cambiar al usuario "opam"
USER opam
