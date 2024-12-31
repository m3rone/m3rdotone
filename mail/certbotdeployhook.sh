#!/bin/bash

certbot --nginx certonly -d mail.m3r.one -n --force-renewal # --reuse-key?
setfacl -R -m u:maddy:rX /etc/letsencrypt/{live,archive}


systemctl reload maddy
