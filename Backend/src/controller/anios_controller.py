import json

from flask import request

from ..controller import controller
from ..service import AniosService
from ..repository import AniosRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'anios', methods=['GET'])
def anios(anios_service: AniosService, anios_repository: AniosRepository):
    # params anio
    anio = request.args.get('anio', default=0, type=str)
    return json.dumps(anios_service.get_anios(anios_repository, anio))
