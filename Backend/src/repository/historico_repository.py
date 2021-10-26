from itertools import count
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import Null


class HistoricoRepository:
    def __init__(self, db):
        self.db = db

    # -------------------------------------------------------
    # ----------- OPERACIONES HISTORICO GENERAL -------------
    # -------------------------------------------------------

    def get_historico_general_bd(self):
        sql = '''
            SELECT * FROM
            (
                SELECT HISTORICOGRAL.*, DR.TIPODESCISIONRECURSO FROM 
                (
                    SELECT HISTORICO.*, TS.NOMBRETIPOSANCION FROM 
                    (
                        SELECT HG.*, S.NOMBRE AS N_SERVICIO, E.NOMBRE AS N_EMPRESA, E.NIT AS NIT_EMPRESA
                        FROM HISTORICO_INFO_GENERAL HG, EMPRESA E, SERVICIO S
                        WHERE HG.SERVICIO = E.SERVICIO
                        AND HG.EMPRESA = E.IDEMPRESA
                        AND HG.SERVICIO = S.IDSERVICIO
                    ) HISTORICO
                    LEFT JOIN
                    TIPOSANCION TS
                    ON HISTORICO.TIPO_DECISION = TS.IDTIPOSANCION
                ) HISTORICOGRAL
                LEFT JOIN
                DESCISIONRECURSO DR
                ON HISTORICOGRAL.DECISION_RECURSO = DR.IDDESCISIONRECURSO	
            ) INFO_GENERAL,
            (
                SELECT * FROM crosstab($$
                    SELECT EXPEDIENTE, CAUSAL, CAUSAL.NOMBRECAUSAL AS CAUSA
                    FROM HISTORICO_INFO_ESPECIFICA HIE, CAUSAL
                    WHERE HIE.CAUSAL = CAUSAL.IDCAUSAL
                    GROUP BY EXPEDIENTE, CAUSAL, CAUSAL.NOMBRECAUSAL
                    ORDER BY EXPEDIENTE
                    $$,
                    $$ select IDCAUSAL from causal $$)
                    AS t (
                        EXPEDIENTE TEXT,
                        "1" TEXT,
                        "2" TEXT,
                        "3" TEXT,
                        "4" TEXT,
                        "5" TEXT,
                        "6" TEXT,
                        "7" TEXT,
                        "8" TEXT,
                        "9" TEXT,
                        "10" TEXT
                    )
            ) CAUSAS
            WHERE INFO_GENERAL.EXPEDIENTE = CAUSAS.EXPEDIENTE;
        '''
        return self.db.engine.execute(text(sql)).fetchall()

    def historico_general_insert_bd(self, historico):
        print('-------------------------------------')
        print('OBJ HISTORICO_INFO_GENERAL -> ', historico)
        print('-------------------------------------')
        for x in historico:
            if historico[x] == 'None':
                historico[x] = None
        sql = '''
            INSERT INTO HISTORICO_INFO_GENERAL(EXPEDIENTE, EMPRESA, SERVICIO, DEVUELTO, R_MEMORADO_DEVOLUCION_IG, F_MEMORANDO_DEVOLUCION_IG, ARCHIVADO, ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR, F_ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR, ACUMULACION_PROCESOS, ACTO_ADMINISTRATIVO_ACUMULACION, F_ACTO_ADMINISTRATIVO_ACUMULACION, OTROS, EN_FIRME, F_FIRMEZA, RESOLUCION_DECISION, F_DECISION, TIPO_DECISION, VALOR_SANCION, RESOLUCION_RECURSO, F_RESOLUCION_RECURSO, DECISION_RECURSO, VALOR_SANCION_RECURSO)
            VALUES (:EXPEDIENTE_ARG, :EMPRESA_ARG, :SERVICIO_ARG, :DEVUELTO_ARG, :R_MEMORADO_DEVOLUCION_IG_ARG, :F_MEMORANDO_DEVOLUCION_IG_ARG, :ARCHIVADO_ARG, :ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR_ARG, :F_ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR_ARG, :ACUMULACION_PROCESOS_ARG, :ACTO_ADMINISTRATIVO_ACUMULACION_ARG, :F_ACTO_ADMINISTRATIVO_ACUMULACION_ARG, :OTROS_ARG, :EN_FIRME_ARG, :F_FIRMEZA_ARG, :RESOLUCION_DECISION_ARG, :F_DECISION_ARG, :TIPO_DECISION_ARG, :VALOR_SANCION_ARG, :RESOLUCION_RECURSO_ARG, :F_RESOLUCION_RECURSO_ARG, :DECISION_RECURSO_ARG, :VALOR_SANCION_RECURSO_ARG);
        '''
        self.db.engine.execute(text(sql), EXPEDIENTE_ARG=historico["EXPEDIENTE"], EMPRESA_ARG=historico["EMPRESA"], SERVICIO_ARG=historico["SERVICIO"], DEVUELTO_ARG=historico["DEVUELTO"], R_MEMORADO_DEVOLUCION_IG_ARG=historico["R_MEMORADO_DEVOLUCION_IG"], F_MEMORANDO_DEVOLUCION_IG_ARG=historico["F_MEMORANDO_DEVOLUCION_IG"], ARCHIVADO_ARG=historico["ARCHIVADO"], ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR_ARG=historico["ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR"], F_ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR_ARG=historico["F_ACTO_ADMINISTRATIVO_ARCHIVO_PRELIMINAR"], ACUMULACION_PROCESOS_ARG=historico["ACUMULACION_PROCESOS"], ACTO_ADMINISTRATIVO_ACUMULACION_ARG=historico["ACTO_ADMINISTRATIVO_ACUMULACION"], F_ACTO_ADMINISTRATIVO_ACUMULACION_ARG=historico["F_ACTO_ADMINISTRATIVO_ACUMULACION"], OTROS_ARG=historico["OTROS"], EN_FIRME_ARG=historico["EN_FIRME"], F_FIRMEZA_ARG=historico["F_FIRMEZA"], RESOLUCION_DECISION_ARG=historico["RESOLUCION_DECISION"], F_DECISION_ARG=historico["F_DECISION"], TIPO_DECISION_ARG=historico["TIPO_DECISION"], VALOR_SANCION_ARG=historico["VALOR_SANCION"], RESOLUCION_RECURSO_ARG=historico["RESOLUCION_RECURSO"], F_RESOLUCION_RECURSO_ARG=historico["F_RESOLUCION_RECURSO"], DECISION_RECURSO_ARG=historico["DECISION_RECURSO"], VALOR_SANCION_RECURSO_ARG=historico["VALOR_SANCION"])

    # -------------------------------------------------------
    # ----------- OPERACIONES HISTORICO ESPECIFICO ----------
    # -------------------------------------------------------

    def get_historico_especifico_bd(self):
        sql = '''
            SELECT * FROM HISTORICO_INFO_ESPECIFICA;
        '''
        return self.db.engine.execute(text(sql)).fetchall()

    def historico_especifico_insert_bd(self, historico):
        print('-------------------------------------')
        print('OBJ HISTORICO_INFO_ESPECIFICA -> ', historico)
        print('-------------------------------------')
        
        sql = '''
            INSERT INTO HISTORICO_INFO_ESPECIFICA(EXPEDIENTE, EMPRESA, SERVICIO, CARGO, NORMA_INFRINGIDA, CAUSAL, SUB_CAUSAL)
            VALUES (:EXPEDIENTE_ARG, :EMPRESA_ARG, :SERVICIO_ARG, :CARGO_ARG, :NORMA_INFRINGIDA_ARG, :CAUSAL_ARG, :SUB_CAUSAL_ARG);
        '''
        self.db.engine.execute(text(sql), EXPEDIENTE_ARG=historico["expediente"], EMPRESA_ARG=historico["empresa"], SERVICIO_ARG=historico["servicio"], CARGO_ARG=historico["cargo"], NORMA_INFRINGIDA_ARG=historico["norma_infringida"], CAUSAL_ARG=historico["causal"], SUB_CAUSAL_ARG=historico["sub_causal"])