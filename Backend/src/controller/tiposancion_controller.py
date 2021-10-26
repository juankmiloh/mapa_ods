import json

from flask import request

from ..controller import controller
from ..service import TiposancionService
from ..repository import TiposancionRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'tiposancion', methods=['GET'])
def tiposancion(tiposancion_service: TiposancionService, tiposancion_repository: TiposancionRepository):
    return json.dumps(tiposancion_service.get_tiposancion(tiposancion_repository))
