#!/bin/bash
# echo run server mapa de ODS
# -- COMANDOS PARA LEVANTAR SERVIDOR
source ~/.bashrc # Comando para actualizar la configuracion de nvm
nvm use v14.18.2 # Comando para indicar la version de node a utilizar
ng serve --host 0.0.0.0 --port 5059 --disableHostCheck true
