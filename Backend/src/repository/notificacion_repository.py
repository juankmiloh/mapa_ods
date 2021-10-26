from itertools import count
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import Null


class NotificacionRepository:
    def __init__(self, db):
        self.db = db

    def get_notificacion_bd(self):
        sql = '''
            SELECT * FROM NOTIFICACION_PROCESO;
        '''
        return self.db.engine.execute(text(sql)).fetchall()
    
    def get_notificacion_proceso_bd(self, idProceso):
        sql = '''
            SELECT * FROM NOTIFICACION_PROCESO WHERE IDPROCESO = :IDPROCESO_ARG ORDER BY IDNOTIFICACION ASC;
        '''
        return self.db.engine.execute(text(sql), IDPROCESO_ARG=idProceso).fetchall()

    def notificacion_insert_bd(self, notificacion):
        print('-------------------------------------')
        print('OBJ NOTIFICACION -> ', notificacion)
        print('-------------------------------------')
        sql = '''
            INSERT INTO NOTIFICACION_PROCESO(IDPROCESO, RADICADO, FECHAAUTORIZACION, EMAIL, FECHAREGISTRO)
            VALUES (:IDPROCESO_ARG, :RADICADO_ARG, :FECHAAUTORIZACION_ARG, :EMAIL_ARG, CURRENT_TIMESTAMP);
        '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=notificacion["idproceso"], RADICADO_ARG=notificacion["radicado"], FECHAAUTORIZACION_ARG=notificacion["fechaAutorizacion"], EMAIL_ARG=notificacion["email"])

    def notificacion_update_bd(self, notificacion):
        print('-------------------------------------')
        print('* NOTIFICACION A ACTUALIZAR -> ', notificacion)
        print('-------------------------------------')

        sql = '''
            UPDATE 
                NOTIFICACION_PROCESO
	        SET 
                RADICADO = :RADICADO_ARG,
                FECHAAUTORIZACION = :FECHAAUTORIZACION_ARG,
                EMAIL = :EMAIL_ARG
	        WHERE IDNOTIFICACION = :IDNOTIFICACION_ARG;
        '''
        self.db.engine.execute(text(sql), IDNOTIFICACION_ARG=notificacion["idnotificacion"], RADICADO_ARG=notificacion["radicado"], FECHAAUTORIZACION_ARG=notificacion["fechaAutorizacion"], EMAIL_ARG=notificacion["email"])
            
                        
    def notificacion_delete_bd(self, idnotificacion):
        print('-------------------------------------')
        print('* NOTIFICACION A ELIMINAR -> ', idnotificacion)
        print('-------------------------------------')
        sql = '''
            DELETE FROM NOTIFICACION_PROCESO
            WHERE IDNOTIFICACION = :IDNOTIFICACION_ARG;
        '''
        self.db.engine.execute(text(sql), IDNOTIFICACION_ARG=idnotificacion)