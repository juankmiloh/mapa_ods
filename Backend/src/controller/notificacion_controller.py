import json

from flask import request

from ..controller import controller
from ..service import NotificacionService
from ..repository import NotificacionRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'notificacion', methods=['GET'])
def notificacion(notificacion_service: NotificacionService, notificacion_repository: NotificacionRepository):
    return json.dumps(notificacion_service.get_notificacion(notificacion_repository))

# Obtener detalle de las notificaciones de un proceso
@controller.route(API_ROOT_PATH + 'notificacion_proceso', methods=['GET'])
def getNotificacionProceso(notificacion_service: NotificacionService, notificacion_repository: NotificacionRepository):
    # Id proceso
    idProceso = request.args.get('idproceso', default='', type=str)
    return json.dumps(notificacion_service.get_notificacion_proceso(notificacion_repository, idProceso))

# Crear una notificacon
@controller.route(API_ROOT_PATH + 'notificacion', methods=['POST'])
def createNotificacion(notificacion_service: NotificacionService, notificacion_repository: NotificacionRepository):
    notificacion = request.json
    return json.dumps(notificacion_service.notificacion_insert(notificacion_repository, notificacion))

# Actualizar notificacion
@controller.route(API_ROOT_PATH + 'notificacion', methods=['PUT'])
def updateNotificacion(notificacion_service: NotificacionService, notificacion_repository: NotificacionRepository):
    # Datos Notificacion
    dataNotificacion = request.json
    return json.dumps(notificacion_service.notificacion_update(notificacion_repository, dataNotificacion))

# Eliminar una notificacion
@controller.route(API_ROOT_PATH + 'notificacion', methods=['DELETE'])
def deleteNotificacion(notificacion_service: NotificacionService, notificacion_repository: NotificacionRepository):
    # ID notificacion
    idNotificacion = request.args.get('idnotificacion', default='', type=str)
    return json.dumps(notificacion_service.notificacion_delete(notificacion_repository, idNotificacion))