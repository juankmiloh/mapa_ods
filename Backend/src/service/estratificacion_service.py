from ..repository import EstratificacionRepository
import csv
from flask import send_file  # descargar archivos

class EstratificacionService:

    def get_estratificacion(self, estratificacion_repository: EstratificacionRepository, servicio, anio, mes, empresa, dpto, mpio, cpoblado, opcion):
        estratificacion = []
        data = estratificacion_repository.get_estratificacion_bd(servicio, anio, mes, empresa, dpto, mpio, cpoblado, opcion)
        for result in data:
            estratificacion.append(
                {
                    'ano': result[0],
                    'mes': result[1],
                    # 'cod_empresa': result[2],
                    # 'nom_empresa': result[3],
                    'cod_dane': result[2],
                    'dane_nom_poblad': result[3],
                    'longitude': result[4],
                    'latitude': result[5],
                    'estrato': result[6],
                    'cantidad_estratos_sui': result[7],
                    'cantidad_estratos_alcaldia': result[8],
                    'chrome': 1 # Esto se coloca para que renderice el mapa en chrome
                }
            )
        # return estratificacion
        return self.__getCSV(estratificacion)

    def __getCSV(self, arrayEstratificacion):
        with open('src/assets/file_estratificacion.csv', 'w', newline='') as csvfile:
            fieldnames = ['ano','mes','cod_dane','dane_nom_poblad','longitude', 'latitude','estrato','cantidad_estratos_sui','cantidad_estratos_alcaldia','chrome']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(arrayEstratificacion)
        return send_file('assets/file_estratificacion.csv', as_attachment=True)