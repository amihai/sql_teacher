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

# Observatie: Aici montez unul cate unul fiserele de config doar ca sa fie clar in 
# timpul demo-ului toate locatiile unde trebuie modificat pentru un domeniu now. 
# In productie asta trebuie sa fie automaziata si generica (sa nu depinda de domeniu) 

include_certificates_config "itschool.org.ro"
include_certificates_config "dev.itschool.org.ro"
include_certificates_config "stage.itschool.org.ro"
include_certificates_config "amihai.ro"