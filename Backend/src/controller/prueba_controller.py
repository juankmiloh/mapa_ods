import datetime
import json

from flask import request

from ..controller import controller
from ..repository import PruebaRepository
from ..service import PruebaService
from ..util.constants import API_ROOT_PATH
from ..util.web_util import to_date


@controller.route(API_ROOT_PATH + 'pruebas', methods=['GET'])
def pruebas(prueba_service: PruebaService, prueba_repository: PruebaRepository):
    return json.dumps(prueba_service.prueba_inicial(prueba_repository))


@controller.route(API_ROOT_PATH + 'pruebas_insert', methods=['GET'])
def pruebasInsert(prueba_service: PruebaService, prueba_repository: PruebaRepository):
    # Nombre estado
    nombre_estado = request.args.get('estado', default='', type=str)
    return json.dumps(prueba_service.prueba_insert(prueba_repository, nombre_estado))
