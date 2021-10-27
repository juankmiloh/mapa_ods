import json

from flask import request

from ..controller import controller
from ..service import DivipolaService
from ..repository import DivipolaRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'divipola', methods=['GET'])
def divipola(divipola_service: DivipolaService, divipola_repository: DivipolaRepository):
    # ARGS 
    optionDpto = request.args.get('optiondpto', default='', type=str)
    optionMpio = request.args.get('optionmpio', default='', type=str)
    optionCpoblado = request.args.get('optioncpoblado', default='', type=str)
    dpto = request.args.get('dpto', default='', type=str)
    mpio = request.args.get('mpio', default='', type=str)
    cpoblado = request.args.get('cpoblado', default='', type=str)
    return json.dumps(divipola_service.get_divipola(divipola_repository, optionDpto, optionMpio, optionCpoblado, dpto, mpio, cpoblado))
