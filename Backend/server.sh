#!/bin/bash
# echo levantar servidor python
source venv/bin/activate
flask run -h 0.0.0.0 -p 5059
# flask run -h 0.0.0.0 -p 5000 --cert=superservicios.gov.co.crt --key=superservicios.key
# PEM pass=%Abcs011549123.%