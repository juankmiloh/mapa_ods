#!/bin/bash
# echo levantar servidor python
source venv/bin/activate
flask run -h 0.0.0.0 -p 5057
