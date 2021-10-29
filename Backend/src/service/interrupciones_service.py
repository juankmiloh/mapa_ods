from ..repository import InterrupcionesRepository
import csv
from flask import send_file  # descargar archivos

class InterrupcionesService:

    def get_interrupciones(self, interrupciones_repository: InterrupcionesRepository, servicio, anio, mes, empresa, sector, dpto, mpio, cpoblado):
        interrupciones = []
        data = interrupciones_repository.get_interrupciones_bd(servicio, anio, mes, empresa, sector, dpto, mpio, cpoblado)
        for result in data:
            interrupciones.append(
                {
                    'ano': result[0],
                    'mes': result[1],
                    'cod_dane': result[2],
                    'cod_empresa': result[3],
                    'nom_empresa': result[4],
                    'res_nores': result[5],
                    'dane_nom_dpto': result[6],
                    'dane_nom_mpio': result[7],
                    'dane_nom_poblad': result[8],
                    'longitude': result[9],
                    'latitude': result[10],
                    'consumo': result[11],
                    'consumo_mod': result[11] / 1000,
                    'facxcon': result[12],
                    'chrome': 1 # Esto se coloca para que renderice el mapa en chrome
                }
            )
        return self.__getCSV(interrupciones)

    def __getCSV(self, arrayInterrupciones):
        with open('src/assets/file_consumo.csv', 'w', newline='') as csvfile:
            fieldnames = ['ano','mes','cod_dane','cod_empresa','nom_empresa','res_nores','dane_nom_dpto','dane_nom_mpio','dane_nom_poblad','longitude', 'latitude','consumo','consumo_mod','facxcon', 'chrome']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(arrayInterrupciones)
        return send_file('assets/file_consumo.csv', as_attachment=True)