from flask import abort
from ..repository import CausalRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class CausalService:

    def get_causal(self, causal_repository: CausalRepository):
        causal = []
        data = causal_repository.get_causal_bd()
        for result in data:
            causal.append(
                {
                    'id': result[0],
                    'nombre': result[1],
                }
            )
        return causal

    def get_causal_proceso(self, causal_repository: CausalRepository, idproceso):
        causal = []
        data = causal_repository.get_causal_proceso_bd(idproceso)
        for result in data:                
            causal.append(
                {
                    'idproceso': result[0],
                    'idcausal': result[1],
                    'f_hechos': str(result[2]),
                    'descripcion': result[3],
                    'fecha_registro': str(result[4]),
                    'nombrecausal': result[5]
                }
            )
        return causal
    
    def get_cantidad_causal_proceso(self, causal_repository: CausalRepository, idproceso):
        causal = []
        data = causal_repository.get_cantidad_causal_proceso_bd(idproceso)
        for result in data:                
            causal.append(
                {
                    'idproceso': result[0],
                    'idcausal': result[1],
                    'nombrecausal': result[2],
                    'cantidad': result[3]
                }
            )
        return causal

    def causal_insert(self, causal_repository: CausalRepository, causal):
        causal_repository.causal_insert_bd(causal)
        return add_wrapper(['causal registrada con éxito!'])

    def causal_update(self, causal_repository: CausalRepository, datacausal):
        causal_repository.causal_update_bd(datacausal)
        return add_wrapper(['causal actualizada con éxito!'])

    def causal_delete(self, causal_repository: CausalRepository, idcausal):
        causal_repository.causal_delete_bd(idcausal)
        return add_wrapper(['causal borrada con éxito!'])