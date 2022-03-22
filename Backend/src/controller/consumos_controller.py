import json

from flask import request

from ..controller import controller
from ..service import ConsumosService
from ..repository import ConsumosRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'consumos', methods=['GET'])
def consumos(consumos_service: ConsumosService, consumos_repository: ConsumosRepository):
    # ARGS
    servicio = request.args.get('servicio', default=0, type=int)
    anio = request.args.get('anio', default=0, type=int)
    mes = request.args.get('mes', default=0, type=int)
    empresa = request.args.get('empresa', default=0, type=int)
    sector = request.args.get('sector', default=0, type=int)
    dpto = request.args.get('dpto', default='TODOS', type=str)
    mpio = request.args.get('mpio', default='TODOS', type=str)
    cpoblado = request.args.get('cpoblado', default='TODOS', type=str)
    return consumos_service.get_consumos(consumos_repository, servicio, anio, mes, empresa, sector, dpto, mpio, cpoblado)
