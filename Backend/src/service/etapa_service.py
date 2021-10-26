from ..repository import EtapaRepository
from ..util.web_util import add_wrapper

class EtapaService:

    def get_etapa(self, etapa_repository: EtapaRepository):
        etapa = []
        data = etapa_repository.get_etapa_bd()
        for result in data:
            etapa.append(
                {
                    'id': result[0],
                    'nombre': result[1],
                    'obligatoriedad': result[2],
                    'fecha_final': result[3],
                    'varios_actos': result[4],
                    'observacion': result[5],
                    'siguiente_estado': result[6],
                }
            )
        return etapa

    def get_etapa_proceso(self, etapa_repository: EtapaRepository, idproceso, idEtapa):
        etapas = []
        data = etapa_repository.get_etapa_proceso_bd(idproceso, idEtapa)
        for result in data:
            fechafin = result[4]
            if fechafin is None: 
                fechafin = None # Se reasigna el valor porque no toma el 'None (null)' desde el front
            else:
                fechafin = str(result[4]) # Se convierte a string para poder retornar la fecha
            fechainicio = result[3]
            if fechainicio is None:
                fechainicio = None
            else:
                fechainicio = str(result[3])
            fecharecepcion = result[6]
            if fecharecepcion is None:
                fecharecepcion = None
            else:
                fecharecepcion = str(result[6])
            
            etapas.append(
                {
                    'etapa': result[0],
                    'numeroacto': result[1],
                    'radicado': result[2],
                    'fechaInicio': fechainicio,
                    'fechaFin': fechafin,
                    'observacion': result[5],
                    'fechaRecepcion': fecharecepcion,
                    'nombre': result[7],
                    'nombre_acto': 'Acto # ' + str(result[1]),
                    'obligatoriedad': result[8],
                    'fecha_final': result[9],
                    'varios_actos': result[10],
                    'campo_observacion': result[11],
                    'fecha_recepcion': result[12],
                    'siguiente_estado': result[13]
                }
            )

        return etapas

    def etapa_insert(self, etapa_repository: EtapaRepository, etapa):
        data = etapa_repository.etapa_insert_bd(etapa)
        self.updateNumeroActos(etapa_repository, data, etapa)
        return add_wrapper(['Etapa registrada con éxito!'])

    def etapa_update(self, etapa_repository: EtapaRepository, dataEtapa):
        data = etapa_repository.etapa_update_bd(dataEtapa)
        self.updateNumeroActos(etapa_repository, data, dataEtapa)
        return add_wrapper(['Etapa actualizada con éxito!'])

    def etapa_delete(self, etapa_repository: EtapaRepository, etapa):
        data = etapa_repository.etapa_delete_bd(etapa)
        self.updateNumeroActos(etapa_repository, data, etapa)
        return add_wrapper(['Etapa borrada con éxito!'])

    # Funcion que actualiza el numero de acto de acuerdo al orden de la fecha de inicio (es decir el acto con menor fecha de inicio sera el # 1)
    def updateNumeroActos(self, etapa_repository: EtapaRepository, data, etapa):
        contador = 1
        for result in data:
            idproceso = result[0]
            idetapa = result[1]
            numeroacto = result[2]
            fecharegistro = result[7]
            if contador != numeroacto:
                print('CONTADOR --> ', contador)
                print('REGISTRO --> ', numeroacto)
                etapa_repository.updateNumeroActoEtapa(idproceso, idetapa, numeroacto, fecharegistro, contador)
                contador += 1
            else:
                contador += 1
    
    def acto_delete(self, etapa_repository: EtapaRepository, acto):
        etapa_repository.acto_delete_bd(acto)
        return add_wrapper(['Acto borrada con éxito!'])