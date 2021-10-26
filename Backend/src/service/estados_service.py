from flask import abort
from ..repository import EstadosRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class EstadosService:

    def get_estados(self, estados_repository: EstadosRepository):
        estados = []
        data = estados_repository.get_estados_bd()
        for result in data:
            estados.append(
                {
                    'idestado': result[0],
                    'nombre': result[1],
                }
            )
        return estados