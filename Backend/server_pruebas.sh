#!/bin/bash
# echo levantar servidor python
source venv/bin/activate
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5063
