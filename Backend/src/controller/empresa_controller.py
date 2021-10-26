import json

from flask import request

from ..controller import controller
from ..repository import EmpresaRepository
from ..service import EmpresaService
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'empresas', methods=['GET'])
def empresas(empresa_service: EmpresaService, empresa_repository: EmpresaRepository):
    # params servicio
    servicio = request.args.get('servicio', default=0, type=str)
    return json.dumps(empresa_service.get_empresas(empresa_repository, servicio))
