from sqlalchemy.sql import text


class EstratificacionRepository:
    def __init__(self, db):
        self.db = db

    def get_estratificacion_bd(self, servicio, anio, mes, empresa, sector, dpto, mpio, cpoblado):
        if servicio == 4:
            print('SERVICIO --> ', servicio)
            sql = '''
                SELECT TC2.CAR_CARG_ANO, TC2.CAR_CARG_PERIODO, TC2.IDENTIFICADOR_EMPRESA, CONVERT(ESP.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250') ARE_ESP_NOMBRE, CODIGO_CENTRO_POBLADO, NOMBRE_CENTRO_POBLADO, LONGITUD, LATITUD, COUNT(*) AS CANTIDAD_ESTRATOS FROM 
                (
                SELECT CAR_T1732_DANE_NIU, CAR_T1743_INFO_PRED_UTIL, TC2.CAR_T1743_CEDULA_CAT_NPN, TC1.CAR_T1732_DIRECCION, TC1.CAR_T1732_ESTRATO_SECTOR, TC1.CAR_T1732_NIU, TC1.CAR_T1732_ID_MERCADO, TC2.CAR_CARG_PERIODO, TC2.CAR_CARG_ANO, TC2.IDENTIFICADOR_EMPRESA FROM ENERGIA_CREG_015.CAR_T1743_TC2FACTURACION_USU TC2, ENERGIA_CREG_015.CAR_T1732_TC1_INV_USUARIOS TC1
                WHERE TC2.CAR_CARG_ANO = TC1.CAR_CARG_ANO
                AND TC2.CAR_CARG_PERIODO = TC1.CAR_CARG_PERIODO
                AND TC2.IDENTIFICADOR_EMPRESA = TC1.IDENTIFICADOR_EMPRESA
                AND TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)) = TC1.CAR_T1732_ID_MERCADO
                AND SUBSTR(CAR_T1743_MERCADO_NIU, INSTR(CAR_T1743_MERCADO_NIU, '-')+1) = TC1.CAR_T1732_NIU
                AND TC2.CAR_CARG_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                AND TC2.CAR_CARG_PERIODO = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                AND (TC2.IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 2103 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,1,2)=LPAD(:DPTO_ARG,2,'0') OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 8 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,3,3)=LPAD(:MPO_ARG,3,'0') OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,6,3)=LPAD(:CPOBLADO_ARG,3,'0') OR 'TODOS' = :CPOBLADO_ARG) --CODCPOBLADO (REMPLAZAR EL 0 POR LA VARIABLE DEL FRONT)
                ) TC2,
                (
                SELECT CAR_T1549_DANE_DEPTO, CAR_T1549_DANE_MPIO, CAR_T1549_ESTRATO_ALCALDIA, CAR_T1549_PREDIAL_UTILIZADO, CAR_T1549_NPN_INFO_PRED_CAT, CAR_T1549_DIRECCION_CAT, CAR_CARG_ANO FROM ESTRATIFICACION_2016.CAR_T1549_ESTRATIFICA_COBERT
                WHERE CAR_CARG_ANO = :ANIO_ARG
                ) ALCALDIA,
                JHERRERAA.GIS_CENTRO_POBLADO DIVIPOLA,
                RUPS.ARE_ESP_EMPRESAS ESP
                WHERE 
                1 = :ESTRATO_SELECT
                AND TC2.CAR_CARG_ANO = ALCALDIA.CAR_CARG_ANO
                AND TC2.CAR_T1743_CEDULA_CAT_NPN = ALCALDIA.CAR_T1549_NPN_INFO_PRED_CAT
                AND TC2.CAR_T1743_INFO_PRED_UTIL = ALCALDIA.CAR_T1549_PREDIAL_UTILIZADO
                AND TC2.CAR_T1732_ESTRATO_SECTOR = ALCALDIA.CAR_T1549_ESTRATO_ALCALDIA -- CUANDO EL ESTRATO ES IGUAL
                AND TC2.CAR_T1732_DANE_NIU = DIVIPOLA.CODIGO_CENTRO_POBLADO
                AND TC2.IDENTIFICADOR_EMPRESA = ESP.ARE_ESP_SECUE
                GROUP BY TC2.CAR_CARG_ANO, TC2.CAR_CARG_PERIODO, TC2.IDENTIFICADOR_EMPRESA, CONVERT(ESP.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250'), CODIGO_CENTRO_POBLADO, NOMBRE_CENTRO_POBLADO, LONGITUD, LATITUD
                UNION
                SELECT TC2.CAR_CARG_ANO, TC2.CAR_CARG_PERIODO, TC2.IDENTIFICADOR_EMPRESA, CONVERT(ESP.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250') ARE_ESP_NOMBRE, CODIGO_CENTRO_POBLADO, NOMBRE_CENTRO_POBLADO, LONGITUD, LATITUD, COUNT(*) AS CANTIDAD_ESTRATOS FROM 
                (
                SELECT CAR_T1732_DANE_NIU, CAR_T1743_INFO_PRED_UTIL, TC2.CAR_T1743_CEDULA_CAT_NPN, TC1.CAR_T1732_DIRECCION, TC1.CAR_T1732_ESTRATO_SECTOR, TC1.CAR_T1732_NIU, TC1.CAR_T1732_ID_MERCADO, TC2.CAR_CARG_PERIODO, TC2.CAR_CARG_ANO, TC2.IDENTIFICADOR_EMPRESA FROM ENERGIA_CREG_015.CAR_T1743_TC2FACTURACION_USU TC2, ENERGIA_CREG_015.CAR_T1732_TC1_INV_USUARIOS TC1
                WHERE TC2.CAR_CARG_ANO = TC1.CAR_CARG_ANO
                AND TC2.CAR_CARG_PERIODO = TC1.CAR_CARG_PERIODO
                AND TC2.IDENTIFICADOR_EMPRESA = TC1.IDENTIFICADOR_EMPRESA
                AND TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)) = TC1.CAR_T1732_ID_MERCADO
                AND SUBSTR(CAR_T1743_MERCADO_NIU, INSTR(CAR_T1743_MERCADO_NIU, '-')+1) = TC1.CAR_T1732_NIU
                AND TC2.CAR_CARG_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                AND TC2.CAR_CARG_PERIODO = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                AND (TC2.IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 2103 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,1,2)=LPAD(:DPTO_ARG,2,'0') OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 8 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,3,3)=LPAD(:MPO_ARG,3,'0') OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,6,3)=LPAD(:CPOBLADO_ARG,3,'0') OR 'TODOS' = :CPOBLADO_ARG) --CODCPOBLADO (REMPLAZAR EL 0 POR LA VARIABLE DEL FRONT)
                ) TC2,
                (
                SELECT CAR_T1549_DANE_DEPTO, CAR_T1549_DANE_MPIO, CAR_T1549_ESTRATO_ALCALDIA, CAR_T1549_PREDIAL_UTILIZADO, CAR_T1549_NPN_INFO_PRED_CAT, CAR_T1549_DIRECCION_CAT, CAR_CARG_ANO FROM ESTRATIFICACION_2016.CAR_T1549_ESTRATIFICA_COBERT
                WHERE CAR_CARG_ANO = :ANIO_ARG
                ) ALCALDIA,
                JHERRERAA.GIS_CENTRO_POBLADO DIVIPOLA,
                RUPS.ARE_ESP_EMPRESAS ESP
                WHERE
                TC2.CAR_CARG_ANO = ALCALDIA.CAR_CARG_ANO
                AND 2 = :ESTRATO_SELECT
                AND TC2.CAR_T1743_CEDULA_CAT_NPN = ALCALDIA.CAR_T1549_NPN_INFO_PRED_CAT
                AND TC2.CAR_T1743_INFO_PRED_UTIL = ALCALDIA.CAR_T1549_PREDIAL_UTILIZADO
                AND TC2.CAR_T1732_ESTRATO_SECTOR <> ALCALDIA.CAR_T1549_ESTRATO_ALCALDIA -- CUANDO LOS ESTRATOS SON DIFERENTES A LOS REGISTRADOS POR LA ALCALDIA
                AND TC2.CAR_T1732_DANE_NIU = DIVIPOLA.CODIGO_CENTRO_POBLADO
                AND TC2.IDENTIFICADOR_EMPRESA = ESP.ARE_ESP_SECUE
                GROUP BY TC2.CAR_CARG_ANO, TC2.CAR_CARG_PERIODO, TC2.IDENTIFICADOR_EMPRESA, CONVERT(ESP.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250'), CODIGO_CENTRO_POBLADO, NOMBRE_CENTRO_POBLADO, LONGITUD, LATITUD
                UNION
                SELECT ESTRATOS.CAR_CARG_ANO, ESTRATOS.CAR_CARG_PERIODO, ESTRATOS.IDENTIFICADOR_EMPRESA, CONVERT(ESP.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250') ARE_ESP_NOMBRE, CODIGO_CENTRO_POBLADO, NOMBRE_CENTRO_POBLADO, LONGITUD, LATITUD, COUNT(*) AS CANTIDAD_ESTRATOS FROM 
                (
                SELECT * FROM 
                (
                SELECT TC2.CAR_CARG_ANO, TC2.CAR_CARG_PERIODO, TC2.IDENTIFICADOR_EMPRESA, CAR_T1732_DANE_NIU, CAR_T1743_INFO_PRED_UTIL, TC2.CAR_T1743_CEDULA_CAT_NPN, TC1.CAR_T1732_DIRECCION, TC1.CAR_T1732_ESTRATO_SECTOR, TC1.CAR_T1732_NIU, TC1.CAR_T1732_ID_MERCADO FROM ENERGIA_CREG_015.CAR_T1743_TC2FACTURACION_USU TC2, ENERGIA_CREG_015.CAR_T1732_TC1_INV_USUARIOS TC1
                WHERE TC2.CAR_CARG_ANO = TC1.CAR_CARG_ANO
                AND TC2.CAR_CARG_PERIODO = TC1.CAR_CARG_PERIODO
                AND TC2.IDENTIFICADOR_EMPRESA = TC1.IDENTIFICADOR_EMPRESA
                AND TO_NUMBER(SUBSTR(CAR_T1743_MERCADO_NIU, 1, INSTR(CAR_T1743_MERCADO_NIU, '-')-1)) = TC1.CAR_T1732_ID_MERCADO
                AND SUBSTR(CAR_T1743_MERCADO_NIU, INSTR(CAR_T1743_MERCADO_NIU, '-')+1) = TC1.CAR_T1732_NIU
                AND TC2.CAR_CARG_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                AND TC2.CAR_CARG_PERIODO = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                AND (TC2.IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 2103 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,1,2)=LPAD(:DPTO_ARG,2,'0') OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 8 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,3,3)=LPAD(:MPO_ARG,3,'0') OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                AND (SUBSTR(TC1.CAR_T1732_DANE_NIU,6,3)=LPAD(:CPOBLADO_ARG,3,'0') OR 'TODOS' = :CPOBLADO_ARG) --CODCPOBLADO (REMPLAZAR EL 0 POR LA VARIABLE DEL FRONT)
                ) TC2
                LEFT JOIN
                (
                SELECT CAR_T1549_DANE_DEPTO, CAR_T1549_DANE_MPIO, CAR_T1549_ESTRATO_ALCALDIA, CAR_T1549_PREDIAL_UTILIZADO, CAR_T1549_NPN_INFO_PRED_CAT, CAR_T1549_DIRECCION_CAT, CAR_CARG_ANO ANO_ALCALDIA FROM ESTRATIFICACION_2016.CAR_T1549_ESTRATIFICA_COBERT
                WHERE CAR_CARG_ANO = :ANIO_ARG
                ) ALCALDIA
                ON
                TC2.CAR_CARG_ANO = ALCALDIA.ANO_ALCALDIA
                AND TC2.CAR_T1743_CEDULA_CAT_NPN = ALCALDIA.CAR_T1549_NPN_INFO_PRED_CAT
                AND TC2.CAR_T1743_INFO_PRED_UTIL = ALCALDIA.CAR_T1549_PREDIAL_UTILIZADO
                WHERE CAR_T1549_PREDIAL_UTILIZADO IS NULL -- CUANDO NO HAY INFORMACION DE ESTRATOS REGISTRADOS EN LA ALCALDIA
                ) ESTRATOS,
                JHERRERAA.GIS_CENTRO_POBLADO DIVIPOLA,
                RUPS.ARE_ESP_EMPRESAS ESP
                WHERE
                3 = :ESTRATO_SELECT
                AND ESTRATOS.CAR_T1732_DANE_NIU = DIVIPOLA.CODIGO_CENTRO_POBLADO
                AND ESTRATOS.IDENTIFICADOR_EMPRESA = ESP.ARE_ESP_SECUE
                GROUP BY ESTRATOS.CAR_CARG_ANO, ESTRATOS.CAR_CARG_PERIODO, ESTRATOS.IDENTIFICADOR_EMPRESA, CONVERT(ESP.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250'), CODIGO_CENTRO_POBLADO, NOMBRE_CENTRO_POBLADO, LONGITUD, LATITUD
            '''
        elif servicio == 5:
            sql = '''
                SELECT 
                    T.CAR_CARG_ANO,
                    T.CAR_CARG_PERIODO,
                    T.COD_DANE,
                    T.IDENTIFICADOR_EMPRESA,
                    CONVERT(ESP.ARE_ESP_NOMBRE, 'US7ASCII', 'EE8MSWIN1250') ARE_ESP_NOMBRE,
                    T.RES_NORES, --USO
                    GIS.DANE_NOM_DPTO,
                    GIS.DANE_NOM_MPIO,
                    GIS.DANE_NOM_POBLAD,
                    GIS.LONGITUD,
                    GIS.LATITUD,
                    SUM(T.CONSUMO) CONSUMO,
                    SUM(T.FACXCON) FACXCON
                FROM (--B1
                    SELECT B1.CAR_CARG_ANO, B1.CAR_CARG_PERIODO, B1.IDENTIFICADOR_EMPRESA, (CASE WHEN B1.CAR_T1555_SECTOR_CONSUMO IN ('1','2','3','4','5','6') THEN 1 ELSE 2 END) RES_NORES, B1.CAR_T1555_DANE COD_DANE
                        , SUM(B1.CAR_T1555_CONSUMO) CONSUMO, SUM(B1.CAR_T1555_FACTU_CONSUMO) FACXCON
                    FROM CARG_COMERCIAL_G.CAR_T1555_FACTURA_GAS_REGULA B1
                    WHERE B1.IDENTIFICADOR_EMPRESA < 99800
                        AND B1.CAR_CARG_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                        AND B1.CAR_CARG_PERIODO = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (B1.IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 2103 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(B1.CAR_T1555_DANE,1,2)=LPAD(:DPTO_ARG,2,'0') OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 8 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(B1.CAR_T1555_DANE,3,3)=LPAD(:MPO_ARG,3,'0') OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(B1.CAR_T1555_DANE,6,3)=LPAD(:CPOBLADO_ARG,3,'0') OR 'TODOS' = :CPOBLADO_ARG) --CODCPOBLADO (REMPLAZAR EL 0 POR LA VARIABLE DEL FRONT)
                        AND (CASE WHEN B1.CAR_T1555_SECTOR_CONSUMO IN ('1','2','3','4','5','6') THEN 1 ELSE 2 END) = 1 --1= RESIDENCIAL; 2=NO RESIDENCIAL; (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                    GROUP BY B1.CAR_CARG_ANO, B1.CAR_CARG_PERIODO, B1.IDENTIFICADOR_EMPRESA, (CASE WHEN B1.CAR_T1555_SECTOR_CONSUMO IN ('1','2','3','4','5','6') THEN 1 ELSE 2 END), B1.CAR_T1555_DANE
                    UNION
                    --B2
                    SELECT C.CAR_CARG_ANO, C.CAR_CARG_PERIODO, C.IDENTIFICADOR_EMPRESA, 2 RES_NORES, B2.CAR_T1556_CODIGODANE
                        , SUM(NVL(B2.CAR_T1556_VOLUMENM3,0)) CONSUMO,SUM(NVL(B2.CAR_T1556_FACTCARGOVBLE,0)) FACXCON
                        --, SUM(B2.CAR_T1556_VOLUMENM3) CONSUMO,SUM(B2.CAR_T1556_FACTCARGOVBLE) FACXCON
                    FROM CARG_ARCH.CAR_CARG_CARGUES C
                        INNER JOIN CARG_COMERCIAL_G.CAR_T1556_FACGASNOREGULADO B2 ON C.CAR_CARG_SECUE=B2.CAR_CARG_SECUE
                    WHERE C.CAR_TIAR_CODIGO= 1556 
                        AND C.CAR_CARG_ESTADO= 'C'
                        AND C.IDENTIFICADOR_EMPRESA < 99800
                        AND C.CAR_CARG_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                        AND C.CAR_CARG_PERIODO = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (C.IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 2103 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(B2.CAR_T1556_CODIGODANE,1,2)=LPAD(:DPTO_ARG,2,'0') OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 8 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(B2.CAR_T1556_CODIGODANE,3,3)=LPAD(:MPO_ARG,3,'0') OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(B2.CAR_T1556_CODIGODANE,6,3)=LPAD(:CPOBLADO_ARG,3,'0') OR 'TODOS' = :CPOBLADO_ARG) --CODCPOBLADO (REMPLAZAR EL 0 POR LA VARIABLE DEL FRONT)
                        AND 1 = :SECTOR_ARG --1= RESIDENCIAL; 2=NO RESIDENCIAL; (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                    GROUP BY C.CAR_CARG_ANO, C.CAR_CARG_PERIODO, C.IDENTIFICADOR_EMPRESA, 2, B2.CAR_T1556_CODIGODANE
                    UNION
                    --F100
                    SELECT F100.CAR_CARG_ANO, F100.CAR_CARG_MES, F100.ARE_ESP_SECUE, (CASE WHEN F100.CAR_T100_SECTORCONSUMO IN ('1','2','3','4','5','6') THEN 1 ELSE 2 END) RES_NORES, F100.CAR_T100_CODIGODANE
                        , SUM(NVL(F100.CAR_T100_CONSUMO,0)) CONSUMO, SUM(NVL(F100.CAR_T100_FACTCONSUMO,0)) FACXCON
                    FROM CARG_COMERCIAL_G.CAR_T100_FACGASREGULADO F100
                    WHERE F100.ARE_ESP_SECUE < 99800
                        AND F100.CAR_CARG_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                        AND F100.CAR_CARG_MES = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (F100.ARE_ESP_SECUE = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 2103 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(F100.CAR_T100_CODIGODANE,1,2)=LPAD(:DPTO_ARG,2,'0') OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 8 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(F100.CAR_T100_CODIGODANE,3,3)=LPAD(:MPO_ARG,3,'0') OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(F100.CAR_T100_CODIGODANE,6,3)=LPAD(:CPOBLADO_ARG,3,'0') OR 'TODOS' = :CPOBLADO_ARG) --CODCPOBLADO (REMPLAZAR EL 0 POR LA VARIABLE DEL FRONT)
                        AND (CASE WHEN F100.CAR_T100_SECTORCONSUMO IN ('1','2','3','4','5','6') THEN 1 ELSE 2 END) = :SECTOR_ARG --1= RESIDENCIAL; 2=NO RESIDENCIAL; (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                    GROUP BY F100.CAR_CARG_ANO, F100.CAR_CARG_MES, F100.ARE_ESP_SECUE, (CASE WHEN F100.CAR_T100_SECTORCONSUMO IN ('1','2','3','4','5','6') THEN 1 ELSE 2 END), F100.CAR_T100_CODIGODANE
                    UNION
                    --F101
                    SELECT C.CAR_CARG_ANO, C.CAR_CARG_PERIODO, C.IDENTIFICADOR_EMPRESA, 2 RES_NORES, F101.CAR_T101_CODIGODANE
                        , SUM(NVL(F101.CAR_T101_VOLUMENM3,0)) CONSUMO,SUM(NVL(F101.CAR_T101_FACTCARGOVBLE,0)) FACXCON
                        --, SUM(F101.CAR_T101_VOLUMENM3) CONSUMO,SUM(F101.CAR_T101_FACTCARGOVBLE) FACXCON
                    FROM CARG_ARCH.CAR_CARG_CARGUES C
                        INNER JOIN CARG_COMERCIAL_G.CAR_T101_FACGASNOREGULADO F101 ON C.CAR_CARG_SECUE=F101.CAR_CARG_SECUE
                    WHERE C.CAR_TIAR_CODIGO= 101 
                        AND C.CAR_CARG_ESTADO= 'C'
                        AND C.IDENTIFICADOR_EMPRESA < 99800
                        AND C.CAR_CARG_ANO = :ANIO_ARG --ANIO (REMPLAZAR EL 2021 POR LA VARIABLE DEL FRONT)
                        AND C.CAR_CARG_PERIODO = :MES_ARG --MES (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (C.IDENTIFICADOR_EMPRESA = :EMPRESA_ARG OR 0 = :EMPRESA_ARG) --ID_ESP (REMPLAZAR EL 2103 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(F101.CAR_T101_CODIGODANE,1,2)=LPAD(:DPTO_ARG,2,'0') OR 'TODOS' = :DPTO_ARG) --CODDEPTO (REMPLAZAR EL 8 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(F101.CAR_T101_CODIGODANE,3,3)=LPAD(:MPO_ARG,3,'0') OR 'TODOS' = :MPO_ARG) --CODMPIO (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                        AND (SUBSTR(F101.CAR_T101_CODIGODANE,6,3)=LPAD(:CPOBLADO_ARG,3,'0') OR 'TODOS' = :CPOBLADO_ARG) --CODCPOBLADO (REMPLAZAR EL 0 POR LA VARIABLE DEL FRONT)
                        AND 2 = :SECTOR_ARG --1= RESIDENCIAL; 2=NO RESIDENCIAL; (REMPLAZAR EL 1 POR LA VARIABLE DEL FRONT)
                    GROUP BY C.CAR_CARG_ANO, C.CAR_CARG_PERIODO, C.IDENTIFICADOR_EMPRESA, 2, F101.CAR_T101_CODIGODANE
                    ) T
                    INNER JOIN RUPS.ARE_ESP_EMPRESAS ESP ON T.IDENTIFICADOR_EMPRESA=ESP.ARE_ESP_SECUE
                    INNER JOIN (SELECT D.DANE_COD_DEPTO, D.DANE_NOM_DPTO, D.DANE_COD_MPIO, D.DANE_NOM_MPIO, D.DANE_COD_CTP, D.DANE_NOM_POBLAD, D.DANE_DIVIPOLA
                                    , G.LATITUD, G.LONGITUD
                                FROM CARG_ARCH.DANE_DIVIPOLA D
                                    LEFT JOIN JHERRERAA.GIS_CENTRO_POBLADO G ON TO_NUMBER(D.DANE_DIVIPOLA)=G.CODIGO_CENTRO_POBLADO
                                ) GIS ON T.COD_DANE=GIS.DANE_DIVIPOLA
                GROUP BY  T.CAR_CARG_ANO, T.CAR_CARG_PERIODO
                , T.COD_DANE, GIS.DANE_NOM_DPTO, GIS.DANE_NOM_MPIO, GIS.DANE_NOM_POBLAD, GIS.LONGITUD, GIS.LATITUD
                , T.IDENTIFICADOR_EMPRESA, ESP.ARE_ESP_NOMBRE
                , T.RES_NORES --USO
            '''
        return self.db.engine.execute(text(sql), ANIO_ARG=anio, MES_ARG=mes, EMPRESA_ARG=empresa, SECTOR_ARG=sector, DPTO_ARG=dpto, MPO_ARG=mpio, CPOBLADO_ARG=cpoblado, ESTRATO_SELECT='1').fetchall()
