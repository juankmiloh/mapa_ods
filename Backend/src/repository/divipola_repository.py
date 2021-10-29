from sqlalchemy.sql import text


class DivipolaRepository:
    def __init__(self, db):
        self.db = db

    def get_divipola_bd(self, optionDpto, optionMpio, optionCpoblado, dpto, mpio, cpoblado):
        sql = '''
            SELECT * FROM
            (
            SELECT D.DANE_COD_DEPTO, D.DANE_NOM_DPTO, 1 AS DANE_COD_MPIO, 'DANE_NOM_MPIO'  AS DANE_NOM_MPIO
            FROM CARG_ARCH.DANE_DIVIPOLA D
            LEFT JOIN JHERRERAA.GIS_CENTRO_POBLADO G ON TO_NUMBER(D.DANE_DIVIPOLA)=G.CODIGO_CENTRO_POBLADO
            WHERE 'depto' = :DEPTO_ARG
            GROUP BY D.DANE_COD_DEPTO, D.DANE_NOM_DPTO
            UNION
            SELECT D.DANE_COD_MPIO, D.DANE_NOM_MPIO, D.DANE_COD_DEPTO, D.DANE_NOM_DPTO
            FROM CARG_ARCH.DANE_DIVIPOLA D
            LEFT JOIN JHERRERAA.GIS_CENTRO_POBLADO G ON TO_NUMBER(D.DANE_DIVIPOLA)=G.CODIGO_CENTRO_POBLADO
            WHERE 'mpio' = :MPIO_ARG
            AND (D.DANE_COD_DEPTO = :COD_DEPTO_ARG OR 0 = :COD_DEPTO_ARG)
            AND (D.DANE_COD_MPIO = :COD_MPIO_ARG OR 0 = :COD_MPIO_ARG)
            GROUP BY D.DANE_COD_MPIO, D.DANE_NOM_MPIO, D.DANE_COD_DEPTO, D.DANE_NOM_DPTO
            UNION
            SELECT D.DANE_COD_CTP, D.DANE_NOM_POBLAD, D.DANE_COD_DEPTO, D.DANE_NOM_DPTO
            FROM CARG_ARCH.DANE_DIVIPOLA D
            LEFT JOIN JHERRERAA.GIS_CENTRO_POBLADO G ON TO_NUMBER(D.DANE_DIVIPOLA)=G.CODIGO_CENTRO_POBLADO
            WHERE 'cpoblado' = :CPOBLADO_ARG
            AND (D.DANE_COD_DEPTO = :COD_DEPTO_ARG OR 0 = :COD_DEPTO_ARG)
            AND (D.DANE_COD_MPIO = :COD_MPIO_ARG OR 0 = :COD_MPIO_ARG)
            AND (D.DANE_COD_CTP = :COD_CTP_ARG OR 0 = :COD_CTP_ARG)
            GROUP BY D.DANE_COD_CTP, D.DANE_NOM_POBLAD, D.DANE_COD_DEPTO, D.DANE_NOM_DPTO
            )
            ORDER BY 2
        '''
        return self.db.engine.execute(text(sql),DEPTO_ARG=optionDpto, MPIO_ARG=optionMpio, CPOBLADO_ARG=optionCpoblado, COD_DEPTO_ARG=dpto, COD_MPIO_ARG=mpio, COD_CTP_ARG=cpoblado).fetchall()