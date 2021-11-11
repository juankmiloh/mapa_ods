from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton

from .prueba_repository import PruebaRepository
from .empresa_repository import EmpresaRepository
from .procesos_repository import ProcesosRepository
from .servicios_repository import ServiciosRepository
from .usuarios_repository import UsuariosRepository
from .divipola_repository import DivipolaRepository
from .tiposancion_repository import TiposancionRepository
from .anios_repository import AniosRepository
from .causal_repository import CausalRepository
from .etapa_repository import EtapaRepository
from .informe_repository import InformeRepository
from .terceros_repository import TercerosRepository
from .interrupciones_repository import InterrupcionesRepository
from .notificacion_repository import NotificacionRepository
from .historico_repository import HistoricoRepository
from .estratificacion_repository import EstratificacionRepository


class RepositoryModule(Module):
    def __init__(self, db):
        self.db = db

    def configure(self, binder):
        prueba_repository = PruebaRepository(self.db)
        empresa_repository = EmpresaRepository(self.db)
        procesos_repository = ProcesosRepository(self.db)
        servicios_repository = ServiciosRepository(self.db)
        usuarios_repository = UsuariosRepository(self.db)
        divipola_repository = DivipolaRepository(self.db)
        tiposancion_repository = TiposancionRepository(self.db)
        anios_repository = AniosRepository(self.db)
        causal_repository = CausalRepository(self.db)
        etapa_repository = EtapaRepository(self.db)
        informe_repository = InformeRepository(self.db)
        terceros_repository = TercerosRepository(self.db)
        interrupciones_repository = InterrupcionesRepository(self.db)
        notificacion_repository = NotificacionRepository(self.db)
        historico_repository = HistoricoRepository(self.db)
        estratificacion_repository = EstratificacionRepository(self.db)

        binder.bind(PruebaRepository, to=prueba_repository, scope=singleton)
        binder.bind(EmpresaRepository, to=empresa_repository, scope=singleton)
        binder.bind(ProcesosRepository, to=procesos_repository, scope=singleton)
        binder.bind(ServiciosRepository, to=servicios_repository, scope=singleton)
        binder.bind(UsuariosRepository, to=usuarios_repository, scope=singleton)
        binder.bind(DivipolaRepository, to=divipola_repository, scope=singleton)
        binder.bind(TiposancionRepository, to=tiposancion_repository, scope=singleton)
        binder.bind(AniosRepository, to=anios_repository, scope=singleton)
        binder.bind(CausalRepository, to=causal_repository, scope=singleton)
        binder.bind(EtapaRepository, to=etapa_repository, scope=singleton)
        binder.bind(InformeRepository, to=informe_repository, scope=singleton)
        binder.bind(TercerosRepository, to=terceros_repository, scope=singleton)
        binder.bind(InterrupcionesRepository, to=interrupciones_repository, scope=singleton)
        binder.bind(NotificacionRepository, to=notificacion_repository, scope=singleton)
        binder.bind(HistoricoRepository, to=historico_repository, scope=singleton)
        binder.bind(EstratificacionRepository, to=estratificacion_repository, scope=singleton)