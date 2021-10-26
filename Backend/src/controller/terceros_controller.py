import json

from flask import request

from ..controller import controller
from ..service import TercerosService
from ..repository import TercerosRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'terceros', methods=['GET'])
def terceros(terceros_service: TercerosService, terceros_repository: TercerosRepository):
    return json.dumps(terceros_service.get_terceros(terceros_repository))

# Obtener detalle de los terceros de un proceso
@controller.route(API_ROOT_PATH + 'terceros_proceso', methods=['GET'])
def getTercerosProceso(terceros_service: TercerosService, terceros_repository: TercerosRepository):
    # Id proceso
    idProceso = request.args.get('idProceso', default='', type=str)
    return json.dumps(terceros_service.get_terceros_proceso(terceros_repository, idProceso))

# Crear un tercero
@controller.route(API_ROOT_PATH + 'terceros', methods=['POST'])
def createTerceros(terceros_service: TercerosService, terceros_repository: TercerosRepository):
    terceros = request.json
    return json.dumps(terceros_service.terceros_insert(terceros_repository, terceros))

# Actualizar tercero
@controller.route(API_ROOT_PATH + 'terceros', methods=['PUT'])
def updateTerceros(terceros_service: TercerosService, terceros_repository: TercerosRepository):
    # Datos terceros
    dataterceros = request.json
    return json.dumps(terceros_service.terceros_update(terceros_repository, dataterceros))

# Eliminar un tercero
@controller.route(API_ROOT_PATH + 'terceros', methods=['DELETE'])
def deleteTerceros(terceros_service: TercerosService, terceros_repository: TercerosRepository):
    # ID tercero
    idtercero = request.args.get('idtercero', default='', type=str)
    return json.dumps(terceros_service.terceros_delete(terceros_repository, idtercero))