from .....services.tarifarito.revisor.TarifasService import TarifasService
from flask import request
from flask_restful import Resource
import time


class rTarifas(Resource):

    def get(self, anio=0, mes=0, empresa=0, mercado=0, ntprop=""):
        self.__ANIO_ARG = anio if anio != 0 else 0
        self.__PERIODO_ARG = 0 if mes <= 0 else mes
        self.__EMPRESA_ARG = empresa if empresa != 0 else 0
        self.__MERCADO_ARG = mercado if mercado != 0 else 0
        self.__NTPROP_ARG = ntprop if ntprop != "" else "TODOS"
        tarifasService = TarifasService(self.__ANIO_ARG, self.__PERIODO_ARG, self.__EMPRESA_ARG, self.__MERCADO_ARG, self.__NTPROP_ARG)
        dataCU = tarifasService.getTarifas()
        jsonValues = tarifasService.get_model_tarifas(dataCU)
        print(f"finished at {time.strftime('%X')}")
        return jsonValues