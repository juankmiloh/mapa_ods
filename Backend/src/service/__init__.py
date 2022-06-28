from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton

from .prueba_service import PruebaService
from .empresa_service import EmpresaService
from .procesos_service import ProcesosService
from .servicios_service import ServiciosService
from .usuarios_service import UsuariosService
from .divipola_service import DivipolaService
from .tiposancion_service import TiposancionService
from .anios_service import AniosService
from .causal_service import CausalService
from .etapa_service import EtapaService
from .informe_service import InformeService
from .terceros_service import TercerosService
from .consumos_service import ConsumosService
from .notificacion_service import NotificacionService
from .historico_service import HistoricoService
from .estratificacion_service import EstratificacionService
from .visitas_service import VisitasService

class ServiceModule(Module):
    def configure(self, binder):
        prueba_service = PruebaService()
        empresa_service = EmpresaService()
        procesos_service = ProcesosService()
        servicios_service = ServiciosService()
        usuarios_service = UsuariosService()
        divipola_service = DivipolaService()
        tiposancion_service = TiposancionService()
        anios_service = AniosService()
        causal_service = CausalService()
        etapa_service = EtapaService()
        informe_service = InformeService()
        terceros_service = TercerosService()
        consumos_service = ConsumosService()
        notificacion_service = NotificacionService()
        historico_service = HistoricoService()
        estratificacion_service = EstratificacionService()
        visitas_service = VisitasService()

        binder.bind(PruebaService, to=prueba_service, scope=singleton)
        binder.bind(EmpresaService, to=empresa_service, scope=singleton)
        binder.bind(ProcesosService, to=procesos_service, scope=singleton)
        binder.bind(ServiciosService, to=servicios_service, scope=singleton)
        binder.bind(UsuariosService, to=usuarios_service, scope=singleton)
        binder.bind(DivipolaService, to=divipola_service, scope=singleton)
        binder.bind(TiposancionService, to=tiposancion_service, scope=singleton)
        binder.bind(AniosService, to=anios_service, scope=singleton)
        binder.bind(CausalService, to=causal_service, scope=singleton)
        binder.bind(EtapaService, to=etapa_service, scope=singleton)
        binder.bind(InformeService, to=informe_service, scope=singleton)
        binder.bind(TercerosService, to=terceros_service, scope=singleton)
        binder.bind(ConsumosService, to=consumos_service, scope=singleton)
        binder.bind(NotificacionService, to=notificacion_service, scope=singleton)
        binder.bind(HistoricoService, to=historico_service, scope=singleton)
        binder.bind(EstratificacionService, to=estratificacion_service, scope=singleton)
        binder.bind(VisitasService, to=visitas_service, scope=singleton)
