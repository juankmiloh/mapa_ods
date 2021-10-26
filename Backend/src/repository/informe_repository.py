from sqlalchemy.sql import text


class InformeRepository:
    def __init__(self, db):
        self.db = db

    def get_cantidad_procesos_bd(self, idservicio, iddependencia):
        sql = '''
            SELECT (CASE WHEN PROCESO_FASE.CANTIDAD IS NOT NULL THEN PROCESO_FASE.CANTIDAD ELSE 0 END) AS CANTIDAD, FASE.NOMBRE FROM
            (SELECT * FROM FASE) FASE
            LEFT JOIN
            (SELECT F.IDFASE, COUNT(*) AS CANTIDAD, F.NOMBRE FROM PROCESO P, FASE F WHERE (P.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = F.IDFASE AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG) GROUP BY F.IDFASE, F.NOMBRE ORDER BY F.NOMBRE ASC) PROCESO_FASE
            ON FASE.IDFASE = PROCESO_FASE.IDFASE;
        '''
        return self.db.engine.execute(text(sql), IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()

    # DATOS EMPRESA
    
    def get_cantidad_procesos_empresa_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT COUNT(*), EMP.NOMBRE FROM PROCESO P, EMPRESA EMP
            WHERE
                (P.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = :FASE_ARG
                AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
                AND P.EMPRESA = EMP.IDEMPRESA
                AND P.IDSERVICIO = EMP.SERVICIO
            GROUP BY EMP.NOMBRE
            ORDER BY COUNT(*) ASC;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()

    def get_procesos_empresa_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT P.IDPROCESO, P.RADICADOPROCESO, EMP.NOMBRE FROM PROCESO P, EMPRESA EMP
            WHERE
                (P.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = :FASE_ARG
                AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
                AND P.EMPRESA = EMP.IDEMPRESA
                AND P.IDSERVICIO = EMP.SERVICIO;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()

    # DATOS CAUSAL
    
    def get_cantidad_procesos_causal_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT COUNT(*), C.NOMBRECAUSAL FROM PROCESO P, PROCESO_CAUSAL PC, CAUSAL C
            WHERE 
                (P.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = :FASE_ARG
                AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
                AND P.IDPROCESO = PC.IDPROCESO
                AND PC.IDCAUSAL = C.IDCAUSAL
            GROUP BY 
                PC.IDCAUSAL,
                C.NOMBRECAUSAL;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()

    def get_procesos_causal_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT P.IDPROCESO, P.RADICADOPROCESO, C.NOMBRECAUSAL FROM PROCESO P, PROCESO_CAUSAL PC, CAUSAL C
            WHERE 
                (P.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = :FASE_ARG
                AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
                AND P.IDPROCESO = PC.IDPROCESO
                AND PC.IDCAUSAL = C.IDCAUSAL;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()

    # DATOS USUARIO
    
    def get_cantidad_procesos_usuario_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT COUNT(*), U.NOMBRE||' '||U.APELLIDO FROM PROCESO P, USUARIOS U
            WHERE
                (U.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = :FASE_ARG
                AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
                AND P.USUARIOASIGNADO = U.IDUSUARIO
            GROUP BY U.NOMBRE||' '||U.APELLIDO;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()
    
    def get_procesos_usuario_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT P.IDPROCESO, P.RADICADOPROCESO, U.NOMBRE||' '||U.APELLIDO FROM PROCESO P, USUARIOS U
            WHERE
                (U.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = :FASE_ARG
                AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
                AND P.USUARIOASIGNADO = U.IDUSUARIO;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()

    # DATOS ESTADO
    
    def get_cantidad_procesos_estado_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT COUNT(*), ESTADO FROM 
            (
                SELECT
                    EP.IDPROCESO,
                    MAX(EP.IDESTADO),
                    (SELECT NOMBREESTADO FROM ESTADO WHERE IDESTADO = MAX(EP.IDESTADO)) AS ESTADO
                FROM ETAPA_PROCESO EP, PROCESO P 
                WHERE 
                    P.IDPROCESO = EP.IDPROCESO
                    AND (P.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                    AND P.FASE = :FASE_ARG
                    AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
                GROUP BY EP.IDPROCESO
            ) MAX_ESTADO
            GROUP BY ESTADO;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()
    
    def get_procesos_estado_bd(self, fase, idservicio, iddependencia):
        sql = '''
            SELECT
                EP.IDPROCESO,
                P.RADICADOPROCESO,
                MAX(EP.IDESTADO),
                (SELECT NOMBREESTADO FROM ESTADO WHERE IDESTADO = MAX(EP.IDESTADO)) AS ESTADO
            FROM ETAPA_PROCESO EP, PROCESO P 
            WHERE 
                P.IDPROCESO = EP.IDPROCESO
                AND (P.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND P.FASE = :FASE_ARG
                AND (P.IDSERVICIO = :IDSERVICIO_ARG OR 0 = :IDSERVICIO_ARG)
            GROUP BY EP.IDPROCESO, P.RADICADOPROCESO;
        '''
        return self.db.engine.execute(text(sql), FASE_ARG=fase, IDSERVICIO_ARG=idservicio, DEPENDENCIA_ARG=iddependencia).fetchall()