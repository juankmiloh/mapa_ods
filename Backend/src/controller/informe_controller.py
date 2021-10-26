import json

from flask import request

from ..controller import controller
from ..service import InformeService
from ..repository import InformeRepository
from ..util.constants import API_ROOT_PATH

@controller.route(API_ROOT_PATH + 'procesos_empresa', methods=['GET'])
def procesosEmpresa(informe_service: InformeService, informe_repository: InformeRepository):
    # Id servicio
    idservicio = request.args.get('idservicio', default='', type=int)
    # Id dependencia
    iddependencia = request.args.get('iddependencia', default='', type=str)
    return json.dumps(informe_service.get_cantidad_procesos_empresa(informe_repository, idservicio, iddependencia))

@controller.route(API_ROOT_PATH + 'procesos_causal', methods=['GET'])
def procesosCausas(informe_service: InformeService, informe_repository: InformeRepository):
    # Id servicio
    idservicio = request.args.get('idservicio', default='', type=int)
    # Id dependencia
    iddependencia = request.args.get('iddependencia', default='', type=str)
    return json.dumps(informe_service.get_cantidad_procesos_causal(informe_repository, idservicio, iddependencia))

@controller.route(API_ROOT_PATH + 'procesos_estado', methods=['GET'])
def procesosEstado(informe_service: InformeService, informe_repository: InformeRepository):
    # Id servicio
    idservicio = request.args.get('idservicio', default='', type=int)
    # Id dependencia
    iddependencia = request.args.get('iddependencia', default='', type=str)
    return json.dumps(informe_service.get_cantidad_procesos_estado(informe_repository, idservicio, iddependencia))

@controller.route(API_ROOT_PATH + 'procesos_usuario', methods=['GET'])
def procesosUsuario(informe_service: InformeService, informe_repository: InformeRepository):
    # Id servicio
    idservicio = request.args.get('idservicio', default='', type=int)
    # Id dependencia
    iddependencia = request.args.get('iddependencia', default='', type=str)
    return json.dumps(informe_service.get_cantidad_procesos_usuario(informe_repository, idservicio, iddependencia))

@controller.route(API_ROOT_PATH + 'cantidad_procesos', methods=['GET'])
def procesosCantidad(informe_service: InformeService, informe_repository: InformeRepository):
    # Id servicio
    idservicio = request.args.get('idservicio', default='', type=int)
    # Id dependencia
    iddependencia = request.args.get('iddependencia', default='', type=str)
    return json.dumps(informe_service.get_cantidad_procesos(informe_repository, idservicio, iddependencia))