from ..repository import InterrupcionesRepository
import csv
from flask import send_file  # descargar archivos

class InterrupcionesService:

    def get_interrupciones(self, interrupciones_repository: InterrupcionesRepository, anio, mes, empresa, causa):
        interrupciones = []
        data = interrupciones_repository.get_interrupciones_bd(anio, mes, empresa, causa)
        for result in data:
            interrupciones.append(
                {
                    'empresa': result[0],
                    'centro_poblado': result[1],
                    'longitude': result[2],
                    'latitude': result[3],
                }
            )
        return self.__getCSV(interrupciones)

    def __getCSV(self, arrayInterrupciones):
        with open('src/assets/file.csv', 'w', newline='') as csvfile:
            fieldnames = ['empresa', 'centro_poblado', 'longitude', 'latitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(arrayInterrupciones)
        return send_file('assets/file.csv', as_attachment=True)