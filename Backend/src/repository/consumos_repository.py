from sqlalchemy.sql import text


class ConsumosRepository:
    def __init__(self, db):
        self.db = db

    def get_consumos_bd(self, servicio, anio, mes, empresa, sector, dpto, mpio, cpoblado):
        
        print('SERVICIO --> ', servicio)
        sql = '''
            SELECT T.CAR_CARG_ANO, T.CAR_CARG_PERIODO
            , T.COD_DANE, GIS.DANE_NOM_DPTO, GIS.DANE_NOM_MPIO, GIS.DANE_NOM_POBLAD, GIS.LONGITUD, GIS.LATITUD
            , T.ID_COMER, ESP.ARE_ESP_NOMBRE
            , T.RES_NORES --USO
            , NVL(SUM(T.CONSUMO), 0) CONSUMO
            , SUM(T.FACXCON) FACXCON
            FROM (--CONSOLIDADOS
                SELECT C.SUM_CON_ANO CAR_CARG_ANO, C.SUM_CON_PERIODO CAR_CARG_PERIODO, C.IDENTIFICADOR_EMPRESA ID_COMER, (CASE WHEN C.SUM_CON_ESTRATO BETWEEN 1 AND 6 THEN 1 ELSE 2 END) RES_NORES
                    , TO_NUMBER(LPAD(C.SUM_CON_DEPTO,2,'0') || LPAD(C.SUM_CON_MUNICIPIO,3,'0') || LPAD(C.SUM_CON_CNRPBLADO,3,'0')) COD_DANE, C.SUM_CON_CONSUMO CONSUMO, C.SUM_CON_FCTRAXCON FACXCON
                FROM SUM_SUI.SUM_CON_CONSOLIDA C
                WHERE C.IDENTIFICADOR_EMPRESA < 99800
                    AND C.SUM_CON_SERVICIO = :SERVICIO_ARG
                    AND C.SUM_CON_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                    AND C.SUM_CON_PERIODO = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                    AND (C.IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 564 POR LA VARIABLE DEL FRONT)
                    AND (C.SUM_CON_DEPTO = :DPTO_ARG OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 5 POR LA VARIABLE DEL FRONT)
                    AND (C.SUM_CON_MUNICIPIO = :MPO_ARG OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                    AND (CASE WHEN C.SUM_CON_ESTRATO BETWEEN 1 AND 6 THEN 1 ELSE 2 END) = :SECTOR_ARG --1= RESIDENCIAL; 2=NO RESIDENCIAL; (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                ) T
                INNER JOIN RUPS.ARE_ESP_EMPRESAS ESP ON T.ID_COMER=ESP.ARE_ESP_SECUE
                INNER JOIN (SELECT D.DANE_COD_DEPTO, D.DANE_NOM_DPTO, D.DANE_COD_MPIO, D.DANE_NOM_MPIO, D.DANE_COD_CTP, D.DANE_NOM_POBLAD, D.DANE_DIVIPOLA
                                , G.LATITUD, G.LONGITUD
                            FROM CARG_ARCH.DANE_DIVIPOLA D
                                LEFT JOIN JHERRERAA.GIS_CENTRO_POBLADO G ON TO_NUMBER(D.DANE_DIVIPOLA)=G.CODIGO_CENTRO_POBLADO
                            ) GIS ON T.COD_DANE=GIS.DANE_DIVIPOLA
            GROUP BY  T.CAR_CARG_ANO, T.CAR_CARG_PERIODO
            , T.COD_DANE, GIS.DANE_NOM_DPTO, GIS.DANE_NOM_MPIO, GIS.DANE_NOM_POBLAD, GIS.LONGITUD, GIS.LATITUD
            , T.ID_COMER, ESP.ARE_ESP_NOMBRE
            , T.RES_NORES --USO
        '''
        return self.db.engine.execute(text(sql), ANIO_ARG=anio, MES_ARG=mes, EMPRESA_ARG=empresa, SECTOR_ARG=sector, DPTO_ARG=dpto, MPO_ARG=mpio, SERVICIO_ARG=servicio).fetchall()