from ..repository import InformeRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class InformeService:

    def get_cantidad_procesos(self, informe_repository: InformeRepository, idservicio, iddependencia):
        print('------------ SERVICIO SELECCIONADO ----', idservicio, '----------------')
        procesos = {}
        data = informe_repository.get_cantidad_procesos_bd(idservicio, iddependencia)
        for result in data:
            print('------------ CANTIDAD DE PROCESOS ----', result, '----------------')
            procesos[result[1]] = {
                'cantidad': result[0],
                'fase': result[1]
            }
        return procesos

    def get_cantidad_procesos_empresa(self, informe_repository: InformeRepository, idservicio, iddependencia):
        
        pieChartData = {}

        empPactivos = []
        pactivos = []
        empPterminados = []
        pterminados = []
        empPeliminados = []
        peliminados = []

        columnsTable = [
            {
                'label': '#',
                'prop': 'idproceso'
            },
            {
                'label': 'Expediente',
                'prop': 'expediente'
            },
            {
                'label': 'Empresa',
                'prop': 'empresa'
            },
            {
                'label': 'Fase',
                'prop': 'fase'
            }
        ]

        dataActivos = []
        dataTerminados = []
        dataEliminados = []

        # PROCESOS ACTIVOS

        data = informe_repository.get_cantidad_procesos_empresa_bd(1, idservicio, iddependencia)
        for result in data:
            empPactivos.append(result[1].capitalize())
            pactivos.append(
                {
                    'value': result[0],
                    'name': result[1].capitalize()
                }
            )

        data = informe_repository.get_procesos_empresa_bd(1, idservicio, iddependencia)
        for result in data:
            dataActivos.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'empresa': result[2].capitalize(),
                    'fase': 'Activo'
                }
            )

        # PROCESOS TERMINADOS

        data = informe_repository.get_cantidad_procesos_empresa_bd(2, idservicio, iddependencia)
        for result in data:
            empPterminados.append(result[1].capitalize())
            pterminados.append(
                {
                    'value': result[0],
                    'name': result[1].capitalize()
                }
            )

        data = informe_repository.get_procesos_empresa_bd(2, idservicio, iddependencia)
        for result in data:
            dataTerminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'empresa': result[2].capitalize(),
                    'fase': 'Terminado'
                }
            )
        
        # PROCESOS Eliminados

        data = informe_repository.get_cantidad_procesos_empresa_bd(3, idservicio, iddependencia)
        for result in data:
            empPeliminados.append(result[1].capitalize())
            peliminados.append(
                {
                    'value': result[0],
                    'name': result[1].capitalize()
                }
            )

        data = informe_repository.get_procesos_empresa_bd(3, idservicio, iddependencia)
        for result in data:
            dataEliminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'empresa': result[2].capitalize(),
                    'fase': 'Eliminado'
                }
            )
        
        # SE ESTRUCTURA EL OBJETO JSON DE RESPUESTA

        pieChartData = {
            'activos': {
                'title': 'Procesos activos',
                'leyenda': empPactivos,
                'datos': pactivos,
                'columns': columnsTable,
                'data': dataActivos
            },
            'terminados': {
                'title': 'Procesos terminados',
                'leyenda': empPterminados,
                'datos': pterminados,
                'columns': columnsTable,
                'data': dataTerminados
            },
            'eliminados': {
                'title': 'Procesos eliminados',
                'leyenda': empPeliminados,
                'datos': peliminados,
                'columns': columnsTable,
                'data': dataEliminados
            }
        }

        print(pieChartData)
        return pieChartData

    def get_cantidad_procesos_causal(self, informe_repository: InformeRepository, idservicio, iddependencia):
        pieChartData = {}

        empPactivos = []
        pactivos = []
        empPterminados = []
        pterminados = []
        empPeliminados = []
        peliminados = []

        columnsTable = [
            {
                'label': '#',
                'prop': 'idproceso'
            },
            {
                'label': 'Expediente',
                'prop': 'expediente'
            },
            {
                'label': 'Causa',
                'prop': 'causa'
            },
            {
                'label': 'Fase',
                'prop': 'fase'
            }
        ]

        dataActivos = []
        dataEliminados = []
        dataTerminados = []

        # PROCESOS ACTIVOS

        data = informe_repository.get_cantidad_procesos_causal_bd(1, idservicio, iddependencia)
        for result in data:
            empPactivos.append(result[1])
            pactivos.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_causal_bd(1, idservicio, iddependencia)
        for result in data:
            dataActivos.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'causa': result[2].capitalize(),
                    'fase': 'Activo'
                }
            )

        # PROCESOS TERMINADOS

        data = informe_repository.get_cantidad_procesos_causal_bd(2, idservicio, iddependencia)
        for result in data:
            empPterminados.append(result[1])
            pterminados.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_causal_bd(2, idservicio, iddependencia)
        for result in data:
            dataTerminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'causa': result[2].capitalize(),
                    'fase': 'Terminado'
                }
            )

        # PROCESOS ELIMINADOS

        data = informe_repository.get_cantidad_procesos_causal_bd(3, idservicio, iddependencia)
        for result in data:
            empPeliminados.append(result[1])
            peliminados.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_causal_bd(3, idservicio, iddependencia)
        for result in data:
            dataEliminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'causa': result[2].capitalize(),
                    'fase': 'Eliminado'
                }
            )

        # SE ESTRUCTURA EL OBJETO JSON DE RESPUESTA
        
        pieChartData = {
            'activos': {
                'title': 'Procesos activos',
                'leyenda': empPactivos,
                'datos': pactivos,
                'columns': columnsTable,
                'data': dataActivos
            },
            'terminados': {
                'title': 'Procesos terminados',
                'leyenda': empPterminados,
                'datos': pterminados,
                'columns': columnsTable,
                'data': dataTerminados
            },
            'eliminados': {
                'title': 'Procesos eliminados',
                'leyenda': empPeliminados,
                'datos': peliminados,
                'columns': columnsTable,
                'data': dataEliminados
            }
        }
        return pieChartData
    
    def get_cantidad_procesos_estado(self, informe_repository: InformeRepository, idservicio, iddependencia):
        pieChartData = {}

        empPactivos = []
        pactivos = []
        empPterminados = []
        pterminados = []
        empPeliminados = []
        peliminados = []

        columnsTable = [
            {
                'label': '#',
                'prop': 'idproceso'
            },
            {
                'label': 'Expediente',
                'prop': 'expediente'
            },
            {
                'label': 'Estado',
                'prop': 'estado'
            },
            {
                'label': 'Fase',
                'prop': 'fase'
            }
        ]

        dataActivos = []
        dataTerminados = []
        dataEliminados = []

        # PROCESOS ACTIVOS

        data = informe_repository.get_cantidad_procesos_estado_bd(1, idservicio, iddependencia)
        for result in data:
            empPactivos.append(result[1])
            pactivos.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_estado_bd(1, idservicio, iddependencia)
        for result in data:
            dataActivos.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'estado': result[3].capitalize(),
                    'fase': 'Activo'
                }
            )

        # PROCESOS TERMINADOS

        data = informe_repository.get_cantidad_procesos_estado_bd(2, idservicio, iddependencia)
        for result in data:
            empPterminados.append(result[1])
            pterminados.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_estado_bd(2, idservicio, iddependencia)
        for result in data:
            dataTerminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'estado': result[3].capitalize(),
                    'fase': 'Terminado'
                }
            )

        # PROCESOS ELIMINADOS

        data = informe_repository.get_cantidad_procesos_estado_bd(3, idservicio, iddependencia)
        for result in data:
            empPeliminados.append(result[1])
            peliminados.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_estado_bd(3, idservicio, iddependencia)
        for result in data:
            dataEliminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'estado': result[3].capitalize(),
                    'fase': 'Eliminado'
                }
            )

        # SE ESTRUCTURA EL OBJETO JSON DE RESPUESTA
        
        pieChartData = {
            'activos': {
                'title': 'Procesos activos',
                'leyenda': empPactivos,
                'datos': pactivos,
                'columns': columnsTable,
                'data': dataActivos
            },
            'terminados': {
                'title': 'Procesos terminados',
                'leyenda': empPterminados,
                'datos': pterminados,
                'columns': columnsTable,
                'data': dataTerminados
            },
            'eliminados': {
                'title': 'Procesos eliminados',
                'leyenda': empPeliminados,
                'datos': peliminados,
                'columns': columnsTable,
                'data': dataEliminados
            }
        }
        return pieChartData
    
    def get_cantidad_procesos_usuario(self, informe_repository: InformeRepository, idservicio, iddependencia):
        pieChartData = {}

        empPactivos = []
        pactivos = []
        empPterminados = []
        pterminados = []
        empPeliminados = []
        peliminados = []

        columnsTable = [
            {
                'label': '#',
                'prop': 'idproceso'
            },
            {
                'label': 'Expediente',
                'prop': 'expediente'
            },
            {
                'label': 'Usuario',
                'prop': 'usuario'
            },
            {
                'label': 'Fase',
                'prop': 'fase'
            }
        ]

        dataActivos = []
        dataTerminados = []
        dataEliminados = []

        # PROCESOS ACTIVOS

        data = informe_repository.get_cantidad_procesos_usuario_bd(1, idservicio, iddependencia)
        for result in data:
            empPactivos.append(result[1])
            pactivos.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_usuario_bd(1, idservicio, iddependencia)
        for result in data:
            dataActivos.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'usuario': result[2].capitalize(),
                    'fase': 'Activo'
                }
            )

        # PROCESOS TERMINADOS

        data = informe_repository.get_cantidad_procesos_usuario_bd(2, idservicio, iddependencia)
        for result in data:
            empPterminados.append(result[1])
            pterminados.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_usuario_bd(2, idservicio, iddependencia)
        for result in data:
            dataTerminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'usuario': result[2].capitalize(),
                    'fase': 'Terminado'
                }
            )

        # PROCESOS ELIMINADOS

        data = informe_repository.get_cantidad_procesos_usuario_bd(3, idservicio, iddependencia)
        for result in data:
            empPeliminados.append(result[1])
            peliminados.append(
                {
                    'value': result[0],
                    'name': result[1]
                }
            )

        data = informe_repository.get_procesos_usuario_bd(3, idservicio, iddependencia)
        for result in data:
            dataEliminados.append(
                {
                    'idproceso': result[0],
                    'expediente': result[1],
                    'usuario': result[2].capitalize(),
                    'fase': 'Eliminado'
                }
            )

        # SE ESTRUCTURA EL OBJETO JSON DE RESPUESTA
        
        pieChartData = {
            'activos': {
                'title': 'Procesos activos',
                'leyenda': empPactivos,
                'datos': pactivos,
                'columns': columnsTable,
                'data': dataActivos
            },
            'terminados': {
                'title': 'Procesos terminados',
                'leyenda': empPterminados,
                'datos': pterminados,
                'columns': columnsTable,
                'data': dataTerminados
            },
            'eliminados': {
                'title': 'Procesos eliminados',
                'leyenda': empPeliminados,
                'datos': peliminados,
                'columns': columnsTable,
                'data': dataEliminados
            }
        }
        return pieChartData