from ..repository import PruebaRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class PruebaService:

    def prueba_inicial(self, prueba_repository: PruebaRepository):
        return add_wrapper([item[1] for item in prueba_repository.prueba_inicial_bd()])

    def prueba_insert(self, prueba_repository: PruebaRepository, nombre_estado):
        prueba_repository.prueba_insert_bd(nombre_estado)
        return add_wrapper(['Insertado con nami'])
