import json

from flask import request

from ..controller import controller
from ..service import ProcesosService
from ..repository import ProcesosRepository
from ..util.constants import API_ROOT_PATH

# Obtener listado de procesos
@controller.route(API_ROOT_PATH + 'procesos', methods=['GET'])
def getListProcesos(procesos_service: ProcesosService, procesos_repository: ProcesosRepository):
    # Id dependencia
    iddependencia = request.args.get('dependencia', default='', type=str)
    return json.dumps(procesos_service.get_procesos(procesos_repository, iddependencia))

# Obtener detalle de un proceso
@controller.route(API_ROOT_PATH + 'proceso/detalle', methods=['GET'])
def getProceso(procesos_service: ProcesosService, procesos_repository: ProcesosRepository):
    # Id proceso
    idProceso = request.args.get('idproceso', default='', type=str)
    return json.dumps(procesos_service.proceso_detalle(procesos_repository, idProceso))

# Crear un proceso
@controller.route(API_ROOT_PATH + 'procesos', methods=['POST'])
def createProceso(procesos_service: ProcesosService, procesos_repository: ProcesosRepository):
    proceso = request.json
    return json.dumps(procesos_service.proceso_insert(procesos_repository, proceso))

# Actualizar usuario asignado al proceso
@controller.route(API_ROOT_PATH + 'procesos/usuarioupdate', methods=['PUT'])
def updateUsuarioProceso(procesos_service: ProcesosService, procesos_repository: ProcesosRepository):
    # Id proceso
    dataProceso = request.json
    return json.dumps(procesos_service.proceso_usuario_update(procesos_repository, dataProceso))

# Actualizar proceso
@controller.route(API_ROOT_PATH + 'procesos/update', methods=['PUT'])
def updateProceso(procesos_service: ProcesosService, procesos_repository: ProcesosRepository):
    # Id proceso
    dataProceso = request.json
    return json.dumps(procesos_service.proceso_update(procesos_repository, dataProceso))

# Eliminar un proceso
@controller.route(API_ROOT_PATH + 'procesos', methods=['DELETE'])
def deleteProceso(procesos_service: ProcesosService, procesos_repository: ProcesosRepository):
    # Id proceso
    idProceso = request.args.get('idProceso', default='', type=str)
    return json.dumps(procesos_service.proceso_delete(procesos_repository, idProceso))
