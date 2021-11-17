import json

from flask import request

from ..controller import controller
from ..service import EstratificacionService
from ..repository import EstratificacionRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'estratificacion', methods=['GET'])
def estratificacion(estratificacion_service: EstratificacionService, estratificacion_repository: EstratificacionRepository):
    # ARGS
    servicio = request.args.get('servicio', default=0, type=int)
    anio = request.args.get('anio', default=0, type=str)
    mes = request.args.get('mes', default=0, type=str)
    empresa = request.args.get('empresa', default=0, type=str)
    dpto = request.args.get('dpto', default=0, type=str)
    mpio = request.args.get('mpio', default=0, type=str)
    cpoblado = request.args.get('cpoblado', default=0, type=str)
    opcion = request.args.get('opcion', default=0, type=int)
    # return json.dumps(estratificacion_service.get_estratificacion(estratificacion_repository, servicio, anio, mes, empresa, dpto, mpio, cpoblado, opcion))
    return estratificacion_service.get_estratificacion(estratificacion_repository, servicio, anio, mes, empresa, dpto, mpio, cpoblado, opcion)
