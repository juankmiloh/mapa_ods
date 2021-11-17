from ..repository import ConsumosRepository
import csv
from flask import send_file  # descargar archivos

class ConsumosService:

    def get_consumos(self, consumos_repository: ConsumosRepository, servicio, anio, mes, empresa, sector, dpto, mpio, cpoblado):
        consumos = []
        data = consumos_repository.get_consumos_bd(servicio, anio, mes, empresa, sector, dpto, mpio, cpoblado)
        consumo = 0
        for result in data:
            if servicio == 4:
                consumo = result[11] / 1000
            elif servicio == 5:
                consumo = result[11] / 100

            consumos.append(
                {
                    'ano': result[0],
                    'mes': result[1],
                    'cod_dane': result[2],
                    'dane_nom_dpto': result[3],
                    'dane_nom_mpio': result[4],
                    'dane_nom_poblad': result[5],
                    'longitude': result[6],
                    'latitude': result[7],
                    'cod_empresa': result[8],
                    'nom_empresa': result[9],
                    'res_nores': result[10],
                    'consumo': result[11],
                    'consumo_mod': consumo,
                    'facxcon': result[12],
                    'chrome': 1 # Esto se coloca para que renderice el mapa en chrome
                }
            )
        return self.__getCSV(consumos)

    def __getCSV(self, arrayConsumos):
        with open('src/assets/file_consumo.csv', 'w', newline='') as csvfile:
            fieldnames = ['ano','mes','cod_dane','cod_empresa','nom_empresa','res_nores','dane_nom_dpto','dane_nom_mpio','dane_nom_poblad','longitude', 'latitude','consumo','consumo_mod','facxcon', 'chrome']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(arrayConsumos)
        return send_file('assets/file_consumo.csv', as_attachment=True)