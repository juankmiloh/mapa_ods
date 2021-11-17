from flask import Blueprint
from flask_cors import CORS

controller = Blueprint('controller', __name__, url_prefix='/')
# src.controller

from . import \
front_controller, \
prueba_controller, \
empresa_controller, \
procesos_controller, \
servicios_controller, \
usuarios_controller, \
divipola_controller, \
tiposancion_controller, \
anios_controller, \
causal_controller, \
etapa_controller, \
informe_controller, \
terceros_controller, \
consumos_controller, \
notificacion_controller, \
historico_controller, \
estratificacion_controller
