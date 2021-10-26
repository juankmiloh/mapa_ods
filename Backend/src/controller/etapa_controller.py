import json

from flask import request

from ..controller import controller
from ..service import EtapaService
from ..repository import EtapaRepository
from ..util.constants import API_ROOT_PATH

# Obtener listado de estados (etapas)
@controller.route(API_ROOT_PATH + 'etapas', methods=['GET'])
def etapa(etapa_service: EtapaService, etapa_repository: EtapaRepository):
    return json.dumps(etapa_service.get_etapa(etapa_repository))

# Obtener detalle de las etapas de un proceso
@controller.route(API_ROOT_PATH + 'etapa_proceso', methods=['GET'])
def getEtapaProceso(etapa_service: EtapaService, etapa_repository: EtapaRepository):
    # Id proceso
    idProceso = request.args.get('idproceso', default='', type=str)
    idEtapa = request.args.get('idetapa', default=0, type=str)
    return json.dumps(etapa_service.get_etapa_proceso(etapa_repository, idProceso, idEtapa))

# Crear una etapa
@controller.route(API_ROOT_PATH + 'etapas', methods=['POST'])
def createEtapa(etapa_service: EtapaService, etapa_repository: EtapaRepository):
    etapa = request.json
    return json.dumps(etapa_service.etapa_insert(etapa_repository, etapa))

# Actualizar etapa
@controller.route(API_ROOT_PATH + 'etapas/update', methods=['PUT'])
def updateEtapa(etapa_service: EtapaService, etapa_repository: EtapaRepository):
    # Datos etapa
    dataEtapa = request.json
    return json.dumps(etapa_service.etapa_update(etapa_repository, dataEtapa))

# Eliminar una etapa
@controller.route(API_ROOT_PATH + 'etapas', methods=['DELETE'])
def deleteEtapa(etapa_service: EtapaService, etapa_repository: EtapaRepository):
    # Datos etapa
    dataEtapa = request.json
    return json.dumps(etapa_service.etapa_delete(etapa_repository, dataEtapa))

# Eliminar un acto
@controller.route(API_ROOT_PATH + 'actos', methods=['DELETE'])
def deleteActo(etapa_service: EtapaService, etapa_repository: EtapaRepository):
    # Datos acto
    dataActo = request.json
    return json.dumps(etapa_service.acto_delete(etapa_repository, dataActo))