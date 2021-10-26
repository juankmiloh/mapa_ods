from itertools import count
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import Null


class EtapaRepository:
    def __init__(self, db):
        self.db = db

    def get_etapa_bd(self):
        sql = '''
            SELECT * FROM ESTADO WHERE NOMBREESTADO NOT IN ('Finalizado') ORDER BY IDESTADO ASC;
        '''
        return self.db.engine.execute(text(sql)).fetchall()
    
    def get_etapa_proceso_bd(self, idProceso, idEtapa):
        sql = '''
            SELECT
                ETAPA.IDESTADO,
                ETAPA.NUMEROACTO,
                ETAPA.RADICADO,
                ETAPA.FECHAINICIO,
                ETAPA.FECHAFIN,
                ETAPA.OBSERVACION,
                ETAPA.FECHARECEPCION,
                ESTADO.NOMBREESTADO,
                ESTADO.OBLIGATORIEDAD,
                ESTADO.FECHA_FINAL,
                ESTADO.VARIOS_ACTOS,
                ESTADO.OBSERVACION,
                ESTADO.FECHA_RECEPCION,
                ESTADO.SIGUIENTEESTADO
            FROM ETAPA_PROCESO ETAPA, ESTADO
            WHERE IDPROCESO = :IDPROCESO_ARG
            AND (ETAPA.IDESTADO = :IDESTADO_ARG OR 0 = :IDESTADO_ARG)
            AND ETAPA.IDESTADO = ESTADO.IDESTADO
            ORDER BY FECHAINICIO ASC, ETAPA.NUMEROACTO;
        '''
        return self.db.engine.execute(text(sql), IDPROCESO_ARG=idProceso, IDESTADO_ARG=idEtapa).fetchall()

    def etapa_insert_bd(self, etapa):
        print('-------------------------------------')
        print('OBJ ETAPA -> ', etapa)
        print('-------------------------------------')
        if "fechaInicio" not in etapa:
            etapa["fechaInicio"] = None
        if "fechaFin" not in etapa:
            etapa["fechaFin"] = None
        if "observacion" not in etapa:
            etapa["observacion"] = None
        if "fechaRecepcion" not in etapa:
            etapa["fechaRecepcion"] = None

        sql = '''
            INSERT INTO ETAPA_PROCESO(IDPROCESO, IDESTADO, NUMEROACTO, RADICADO, FECHAINICIO, FECHAFIN, OBSERVACION, FECHAREGISTRO, FECHARECEPCION)
            VALUES (:IDPROCESO_ARG, :IDESTADO_ARG, :NUMEROACTO_ARG, :RADICADO_ARG, :FECHAINICIO_ARG, :FECHAFIN_ARG, :OBSERVACION_ARG, CURRENT_TIMESTAMP, :FECHARECEPCION_ARG);
        '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=etapa["idproceso"], IDESTADO_ARG=etapa["etapa"], NUMEROACTO_ARG=etapa["numeroacto"], RADICADO_ARG=etapa["radicado"], FECHAINICIO_ARG=etapa["fechaInicio"], FECHAFIN_ARG=etapa["fechaFin"], OBSERVACION_ARG=etapa["observacion"], FECHARECEPCION_ARG=etapa["fechaRecepcion"])

        self.update_fase_proceso(etapa["idproceso"])

        return self.getNumerosActos(etapa)  

    def etapa_update_bd(self, etapa):
        print('-------------------------------------')
        print('* ETAPA A ACTUALIZAR -> ', etapa)
        print('-------------------------------------')

        if etapa["fechaFin"] == 'No registra':
            etapa["fechaFin"] = None
        if etapa["fechaRecepcion"] == 'No registra':
            etapa["fechaRecepcion"] = None

        sql = '''
            UPDATE 
                ETAPA_PROCESO
	        SET 
                RADICADO = :RADICADO_ARG,
                FECHAINICIO = :FECHAINICIO_ARG,
                FECHAFIN = :FECHAFIN_ARG,
                OBSERVACION = :OBSERVACION_ARG,
                FECHARECEPCION = :FECHARECEPCION_ARG
	        WHERE 
                IDPROCESO = :IDPROCESO_ARG
                AND IDESTADO = :IDESTADO_ARG
                AND NUMEROACTO = :ACTO_ARG;
        '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=etapa["idproceso"], IDESTADO_ARG=etapa["etapa"], ACTO_ARG=etapa["numeroacto"], FECHAINICIO_ARG=etapa["fechaInicio"], FECHAFIN_ARG=etapa["fechaFin"], RADICADO_ARG=etapa["radicado"], OBSERVACION_ARG=etapa["observacion"], FECHARECEPCION_ARG=etapa["fechaRecepcion"])

        self.update_fase_proceso(etapa["idproceso"])

        return self.getNumerosActos(etapa)            
                        
    def etapa_delete_bd(self, etapa):
        print('-------------------------------------')
        print('* ETAPA A ELIMINAR -> ', etapa)
        print('-------------------------------------')
        sql = '''
            DELETE FROM
                ETAPA_PROCESO
            WHERE
                IDPROCESO = :IDPROCESO_ARG
                AND IDESTADO = :IDESTADO_ARG
                AND NUMEROACTO = :ACTO_ARG;
        '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=etapa["idproceso"], IDESTADO_ARG=etapa["etapa"], ACTO_ARG=etapa["numeroacto"])

        self.update_fase_proceso(etapa["idproceso"])

        return self.getNumerosActos(etapa) # devuelve el listado de actos de un proceso ordenados por fecha de inicio

    # Funcion que devuelve el listado de actos de un proceso ordenados por fecha de inicio
    def getNumerosActos(self, etapa):
        sql = '''
            SELECT * FROM ETAPA_PROCESO WHERE IDPROCESO = :IDPROCESO_ARG AND IDESTADO = :IDESTADO_ARG ORDER BY FECHAINICIO, NUMEROACTO;
        '''
        return self.db.engine.execute(text(sql), IDPROCESO_ARG=etapa["idproceso"], IDESTADO_ARG=etapa["etapa"]).fetchall()

    def updateNumeroActoEtapa(self, idproceso, etapa, numeroactoactual, fecharegistro, nuevonumeroacto):
        sql = '''
            UPDATE 
                ETAPA_PROCESO
	        SET 
                NUMEROACTO = :ACTONUEVO_ARG
	        WHERE 
                IDPROCESO = :IDPROCESO_ARG
                AND IDESTADO = :IDESTADO_ARG
                AND NUMEROACTO = :ACTOACTUAL_ARG
                AND FECHAREGISTRO = :FECHAREGISTRO_ARG;
        '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=idproceso, IDESTADO_ARG=etapa, ACTOACTUAL_ARG=numeroactoactual, FECHAREGISTRO_ARG=fecharegistro, ACTONUEVO_ARG=nuevonumeroacto)
    
    def acto_delete_bd(self, acto):
        print('-------------------------------------')
        print('* ACTO A ELIMINAR -> ', acto)
        print('-------------------------------------')
        sql = '''
            DELETE FROM
                ETAPA_PROCESO
            WHERE
                IDPROCESO = :IDPROCESO_ARG
                AND IDESTADO = :IDESTADO_ARG
                AND NUMEROACTO = :ACTO_ARG;
        '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=acto["idproceso"], IDESTADO_ARG=acto["etapa"], ACTO_ARG=acto["numeroacto"])

    def update_fase_proceso(self, idproceso):
        sql = '''
            SELECT COUNT(*) FROM (SELECT EP.IDESTADO FROM ETAPA_PROCESO EP, ESTADO E WHERE IDPROCESO=:IDPROCESO_ARG AND E.IDESTADO = EP.IDESTADO AND E.OBLIGATORIEDAD = 'SI' GROUP BY EP.IDESTADO) ETAPASPROCESO;
        '''
        countEtapasProceso = self.db.engine.execute(text(sql), IDPROCESO_ARG=idproceso).fetchall()
        
        sql = '''
            SELECT COUNT(*) FROM ESTADO WHERE OBLIGATORIEDAD = 'SI';
        '''
        countEtapas = self.db.engine.execute(text(sql), IDPROCESO_ARG=idproceso).fetchall()

        fase = 0

        print('------------ CANTIDAD ETAPAS PROCESO ----', countEtapasProceso, '----------------')
        print('------------ CANTIDAD ETAPAS BD ----', countEtapas, '----------------')

        if countEtapasProceso == countEtapas:
            print('------------ PROCESO TERMINADO ----------------')
            fase = 2 # Proceso terminado
        else:
            fase = 1 # Proceso En curso

        sql = '''
                UPDATE PROCESO SET FASE=:FASE_ARG WHERE IDPROCESO=:IDPROCESO_ARG;
            '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=idproceso, FASE_ARG=fase)
    
    # def update_fase_proceso(self, idproceso):
    #     sql = '''
    #         SELECT E.NOMBRE FROM ETAPA_PROCESO EP, ETAPA E WHERE PROCESO=:IDPROCESO_ARG AND EP.ETAPA=E.IDETAPA;
    #     '''
    #     resultsql = self.db.engine.execute(text(sql), IDPROCESO_ARG=idproceso).fetchall()

    #     countEtapas = 0
    #     terminado = False
    #     fase = 0
        
    #     for result in resultsql:
    #         etapa = result[0]
    #         if etapa != 'Memorando de devolución':
    #             if etapa != 'Memorando de alcance':
    #                 print('------------ ETAPA ----', etapa, '----------------')
    #                 countEtapas = countEtapas + 1
    #                 if etapa == 'Archivo':
    #                     terminado = True

    #     print('------------ CANTIDAD ETAPAS ----', countEtapas, '----------------')
    #     print('------------ TERMINADO ----', terminado, '----------------')

    #     if countEtapas >= 13 and terminado:
    #         print('------------ PROCESO TERMINADO ----------------')
    #         fase = 2 # Proceso terminado
    #     else:
    #         fase = 1 # Proceso En curso

    #     sql = '''
    #             UPDATE PROCESO SET FASE=:FASE_ARG WHERE IDPROCESO=:IDPROCESO_ARG;
    #         '''
    #     self.db.engine.execute(text(sql), IDPROCESO_ARG=idproceso, FASE_ARG=fase)