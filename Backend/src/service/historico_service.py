from ..repository import HistoricoRepository
from ..util.web_util import add_wrapper
from flask import send_file

class HistoricoService:

    # -------------------------------------------------------
    # ----------- OPERACIONES HISTORICO GENERAL -------------
    # -------------------------------------------------------

    def historico_pdf(self, historico_repository: HistoricoRepository,  root, year, folder, document):
        # path = "assets\\"+folder+"\\"+document
        path = "sources/"+root+"/"+year+"/"+folder+"/"+document
        return send_file(path)

    def get_historico_general(self, historico_repository: HistoricoRepository):
        historico = []
        data = historico_repository.get_historico_general_bd()
        for result in data:
            historico.append(
                {
                    'idhistorico': result[0],
                    'expediente': result[1],
                    'empresa': result[2],
                    'servicio': result[3],
                    'devuelto': result[4],
                    'r_memorado_devolucion_ig': result[5],
                    'f_memorando_devolucion_ig': str(result[6]),
                    'archivado': result[7],
                    'acto_administrativo_archivo_preliminar': result[8],
                    'f_acto_administrativo_archivo_preliminar': str(result[9]),
                    'acumulacion_procesos': result[10],
                    'acto_administrativo_acumulacion': result[11],
                    'f_acto_administrativo_acumulacion': str(result[12]),
                    'otros': result[13],
                    'en_firme': result[14],
                    'f_firmeza': str(result[15]),
                    'resolucion_decision': result[16],
                    'f_decision': str(result[17]),
                    'tipo_decision': result[18],
                    'valor_sancion': result[19],
                    'resolucion_recurso': result[20],
                    'f_resolucion_recurso': str(result[21]),
                    'decision_recurso': result[22],
                    'valor_sancion_recurso': result[23],
                    'n_servicio': result[24],
                    'n_empresa': result[25],
                    'nit_empresa': result[26],
                    'n_tipo_decision': result[27],
                    'n_decision_recurso': result[28],

                    'CAUSA1': result[30],
                    'CAUSA2': result[31],
                    'CAUSA3': result[32],
                    'CAUSA4': result[33],
                    'CAUSA5': result[34],
                    'CAUSA6': result[35],
                    'CAUSA7': result[36],
                    'CAUSA8': result[37],
                    'CAUSA9': result[38],
                    'CAUSA10': result[39],
                }
            )
        return historico

    def historico_general_insert(self, historico_repository: HistoricoRepository, historico):
        historico_repository.historico_general_insert_bd(historico)
        return add_wrapper(['Historico general registrado con éxito!'])

    # -------------------------------------------------------
    # ----------- OPERACIONES HISTORICO ESPECIFICO ----------
    # -------------------------------------------------------

    def get_historico_especifico(self, historico_repository: HistoricoRepository):
        historico = []
        data = historico_repository.get_historico_especifico_bd()
        for result in data:
            historico.append(
                {
                    'expediente': result[0],
                    'empresa': result[1],
                    'servicio': result[2],
                    'cargo': result[3],
                    'norma_infringida': result[4],
                    'causal': result[5],
                    'sub_causal': result[6]
                }
            )
        return historico

    def historico_especifico_insert(self, historico_repository: HistoricoRepository, historico):
        historico_repository.historico_especifico_insert_bd(historico)
        return add_wrapper(['Historico especifico registrado con éxito!'])