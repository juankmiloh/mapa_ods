from ..repository import TercerosRepository
from ..util.web_util import add_wrapper

class TercerosService:

    def get_terceros(self, terceros_repository: TercerosRepository):
        terceros = []
        data = terceros_repository.get_terceros_bd()
        for result in data:
            terceros.append(
                {
                    'idtercero': result[0],
                    'idproceso': result[1],
                    'persona': result[2],
                    'documento': result[3],
                    'nombre': result[4],
                    'direccion': result[5],
                    'email': result[6],
                }
            )
        return terceros

    def get_terceros_proceso(self, terceros_repository: TercerosRepository, idproceso):
        terceros = []
        data = terceros_repository.get_terceros_proceso_bd(idproceso)
        for result in data:                
            terceros.append(
                {
                    'idtercero': result[0],
                    'persona': result[1],
                    'documento': result[2],
                    'nombre': result[3],
                    'direccion': result[4],
                    'email': result[5],
                }
            )
        return terceros

    def terceros_insert(self, terceros_repository: TercerosRepository, terceros):
        terceros_repository.terceros_insert_bd(terceros)
        return add_wrapper(['terceros registrada con éxito!'])

    def terceros_update(self, terceros_repository: TercerosRepository, dataterceros):
        terceros_repository.terceros_update_bd(dataterceros)
        return add_wrapper(['terceros actualizada con éxito!'])

    def terceros_delete(self, terceros_repository: TercerosRepository, idtercero):
        terceros_repository.terceros_delete_bd(idtercero)
        return add_wrapper(['terceros borrada con éxito!'])