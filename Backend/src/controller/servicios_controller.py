import json

from flask import request

from ..controller import controller
from ..service import ServiciosService
from ..repository import ServiciosRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'servicios', methods=['GET'])
def servicios(servicios_service: ServiciosService, servicios_repository: ServiciosRepository):
    # Id dependencia
    iddependencia = request.args.get('dependencia', default='', type=str)
    return json.dumps(servicios_service.get_servicios(servicios_repository, iddependencia))
