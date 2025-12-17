#!/bin/sh


# Daca gasim pe disk fisierele de certificat pentru domeniu adaugam configuratia SSL in nginx
include_certificates_config() {
    domein=$1
    if [ -f /etc/letsencrypt/live/$domein/fullchain.pem ] || [ -f /etc/letsencrypt/live/$domein/privkey.pem ]; then
        echo "Certificate files for $domein are present."
        echo "Add $domein.conf in nginx."
        cp /tmp/nginx/conf.d/$domein.conf /etc/nginx/conf.d/$domein.conf
    else
        echo "Certificate files for $domein are NOT present."
    fi
}

include_certificates_config "itschool.org.ro"
include_certificates_config "dev.itschool.org.ro"
include_certificates_config "stage.itschool.org.ro"
include_certificates_config "amihai.ro"