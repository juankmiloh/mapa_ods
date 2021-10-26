from ..repository import AniosRepository


class AniosService:

    def get_anios(self, anios_repository: AniosRepository, anio):
        anios = []
        data = anios_repository.get_anios_bd(anio)
        anio = 0
        for result in data:
            if anio != result[0]:
                    anios.append(
                        {
                            'anio': result[0]
                        }
                    )
            anio = result[0]
        return anios
