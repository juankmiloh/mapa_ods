from ..repository import DivipolaRepository

class DivipolaService:

    def get_divipola(self, divipola_repository: DivipolaRepository, optionDpto, optionMpio, optionCpoblado, dpto, mpio, cpoblado):
        divipola = []
        data = divipola_repository.get_divipola_bd(optionDpto, optionMpio, optionCpoblado, dpto, mpio, cpoblado)
        for result in data:
            divipola.append(
                {
                    'cod': result[0],
                    'nombre': result[1],
                }
            )
        return divipola