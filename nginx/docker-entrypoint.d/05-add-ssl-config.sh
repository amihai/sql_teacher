#!/bin/sh

# Daca gasim pe disk fisierele de certificat pentru itschool.org.ro adaugam configuratia SSL in nginx

if [ -f /etc/letsencrypt/live/itschool.org.ro/fullchain.pem ] || [ -f /etc/letsencrypt/live/itschool.org.ro/privkey.pem ]; then
    echo "Certificate files for itschool.org.ro are present."
    echo "Add itschool.org.ro.conf in nginx."
    cp /tmp/nginx/conf.d/itschool.org.ro.conf /etc/nginx/conf.d/itschool.org.ro.conf
else
    echo "Certificate files for itschool.org.ro are NOT present."
fi