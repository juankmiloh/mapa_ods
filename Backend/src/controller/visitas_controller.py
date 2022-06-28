import json

from flask import request

from ..controller import controller
from ..service import VisitasService
from ..repository import VisitasRepository
from ..util.constants import API_ROOT_PATH

# Obtener listado de (visitas)
@controller.route(API_ROOT_PATH + 'visitas', methods=['GET'])
def visitas(visitas_service: VisitasService, visitas_repository: VisitasRepository):
    return json.dumps(visitas_service.get_visitas(visitas_repository))

# Crear una visitas
@controller.route(API_ROOT_PATH + 'visitas', methods=['POST'])
def createVisitas(visitas_service: VisitasService, visitas_repository: VisitasRepository):
    visitas = request.json
    return json.dumps(visitas_service.visitas_insert(visitas_repository, visitas))

# Actualizar visitas
@controller.route(API_ROOT_PATH + 'visitas', methods=['PUT'])
def updateVisitas(visitas_service: VisitasService, visitas_repository: VisitasRepository):
    # Datos visitas
    dataVisitas = request.json
    return json.dumps(visitas_service.visitas_update(visitas_repository, dataVisitas))

# Eliminar una visitas
@controller.route(API_ROOT_PATH + 'visitas', methods=['DELETE'])
def deleteVisitas(visitas_service: VisitasService, visitas_repository: VisitasRepository):
    # Datos visitas
    dataVisitas = request.json
    return json.dumps(visitas_service.visitas_delete(visitas_repository, dataVisitas))
