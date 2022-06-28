from ..repository import VisitasRepository
from ..util.web_util import add_wrapper

class VisitasService:

    def get_visitas(self, visitas_repository: VisitasRepository):
        visitas = []
        data = visitas_repository.get_visitas_bd()
        for result in data:
            visitas.append(
                {
                    'idvisita': result[0],
                    'idusuario': result[1],
                    'observacion': result[2],
                    'fecharegistro': str(result[3])
                }
            )
        return add_wrapper(visitas)

    def visitas_insert(self, visitas_repository: VisitasRepository, visitas):
        visitas_repository.visitas_insert_bd(visitas)
        return 'Visita registrada con éxito!'

    def visitas_update(self, visitas_repository: VisitasRepository, datavisitas):
        visitas_repository.visitas_update_bd(datavisitas)
        return 'Visita actualizada con éxito!'

    def visitas_delete(self, visitas_repository: VisitasRepository, visitas):
        visitas_repository.visitas_delete_bd(visitas)
        return 'Visita eliminada con éxito!'
