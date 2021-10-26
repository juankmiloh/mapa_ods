from ..repository import TiposancionRepository

class TiposancionService:

    def get_tiposancion(self, tiposancion_repository: TiposancionRepository):
        tiposancion = []
        data = tiposancion_repository.get_tiposancion_bd()
        for result in data:
            tiposancion.append(
                {
                    'idtiposancion': result[0],
                    'nombre': result[1],
                }
            )
        return tiposancion