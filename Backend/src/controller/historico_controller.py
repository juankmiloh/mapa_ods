import json

from flask import request

from ..controller import controller
from ..service import HistoricoService
from ..repository import HistoricoRepository
from ..util.constants import API_ROOT_PATH

# -------------------------------------------------------
# ----------- OPERACIONES HISTORICO GENERAL -------------
# -------------------------------------------------------

# Obtener documento PDF del historico general
@controller.route(API_ROOT_PATH + 'historico/document', methods=['GET'])
def historicoPdf(historico_service: HistoricoService, historico_repository: HistoricoRepository):
    root = request.args.get('root', default='', type=str)
    year = request.args.get('year', default='', type=str)
    folder = request.args.get('folder', default='', type=str)
    document = request.args.get('document', default='', type=str)
    return historico_service.historico_pdf(historico_repository, root, year, folder, document)

# Obtener listado de historico GENERAL
@controller.route(API_ROOT_PATH + 'historico_general', methods=['GET'])
def historicoGeneral(historico_service: HistoricoService, historico_repository: HistoricoRepository):
    return json.dumps(historico_service.get_historico_general(historico_repository))

# Crear un registro de historico GENERAL
@controller.route(API_ROOT_PATH + 'historico_general', methods=['POST'])
def createHistoricoGeneral(historico_service: HistoricoService, historico_repository: HistoricoRepository):
    historico = request.json
    return json.dumps(historico_service.historico_general_insert(historico_repository, historico))

# -------------------------------------------------------
# ----------- OPERACIONES HISTORICO GENERAL -------------
# -------------------------------------------------------

# Obtener listado de historico ESPECIFICO
@controller.route(API_ROOT_PATH + 'historico_especifico', methods=['GET'])
def historicoEspecifico(historico_service: HistoricoService, historico_repository: HistoricoRepository):
    return json.dumps(historico_service.get_historico_especifico(historico_repository))

# Crear un registro de historico ESPECIFICO
@controller.route(API_ROOT_PATH + 'historico_especifico', methods=['POST'])
def createHistoricoEspecifico(historico_service: HistoricoService, historico_repository: HistoricoRepository):
    historico = request.json
    return json.dumps(historico_service.historico_especifico_insert(historico_repository, historico))