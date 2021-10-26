from itertools import count
from sqlalchemy.sql import text
from sqlalchemy.sql.elements import Null


class TercerosRepository:
    def __init__(self, db):
        self.db = db

    def get_terceros_bd(self):
        sql = '''
            SELECT T.IDTERCEROS, TP.NOMBRE AS PERSONA, T.DOCUMENTO, T.NOMBRE, T.DIRECCION, T.EMAIL FROM TERCEROS T, TIPOPERSONA TP
            WHERE T.IDTIPOPERSONA = TP.IDTIPOPERSONA;
        '''
        return self.db.engine.execute(text(sql)).fetchall()
    
    def get_terceros_proceso_bd(self, idProceso):
        sql = '''
            SELECT T.IDTERCEROS, TP.NOMBRE AS PERSONA, T.DOCUMENTO, T.NOMBRE, T.DIRECCION, T.EMAIL FROM TERCEROS T, TIPOPERSONA TP
            WHERE T.IDTIPOPERSONA = TP.IDTIPOPERSONA AND T.IDPROCESO = :IDPROCESO_ARG ORDER BY T.IDTERCEROS DESC;
        '''
        return self.db.engine.execute(text(sql), IDPROCESO_ARG=idProceso).fetchall()

    def terceros_insert_bd(self, terceros):
        print('-------------------------------------')
        print('OBJ TERCERO -> ', terceros)
        print('-------------------------------------')
        sql = '''
            INSERT INTO TERCEROS(IDPROCESO, IDTIPOPERSONA, DOCUMENTO, NOMBRE, DIRECCION, EMAIL)
            VALUES (:IDPROCESO_ARG, :IDTIPOPERSONA_ARG, :DOCUMENTO_ARG, :NOMBRE_ARG, :DIRECCION_ARG, :EMAIL_ARG);
        '''
        self.db.engine.execute(text(sql), IDPROCESO_ARG=terceros["idproceso"], IDTIPOPERSONA_ARG=terceros["persona"], DOCUMENTO_ARG=terceros["documento"], NOMBRE_ARG=terceros["nombre"], DIRECCION_ARG=terceros["direccion"], EMAIL_ARG=terceros["email"])

    def terceros_update_bd(self, terceros):
        print('-------------------------------------')
        print('* TERCERO A ACTUALIZAR -> ', terceros)
        print('-------------------------------------')

        sql = '''
            UPDATE 
                TERCEROS
	        SET 
                IDTIPOPERSONA = :IDTIPOPERSONA_ARG,
                DOCUMENTO = :DOCUMENTO_ARG,
                NOMBRE = :NOMBRE_ARG,
                DIRECCION = :DIRECCION_ARG,
                EMAIL = :EMAIL_ARG
	        WHERE IDTERCEROS = :IDTERCERO_ARG;
        '''
        self.db.engine.execute(text(sql), IDTERCERO_ARG=terceros["idtercero"], IDTIPOPERSONA_ARG=terceros["persona"], DOCUMENTO_ARG=terceros["documento"], NOMBRE_ARG=terceros["nombre"], DIRECCION_ARG=terceros["direccion"], EMAIL_ARG=terceros["email"])
            
                        
    def terceros_delete_bd(self, idtercero):
        print('-------------------------------------')
        print('* TERCERO A ELIMINAR -> ', idtercero)
        print('-------------------------------------')
        sql = '''
            DELETE FROM TERCEROS
            WHERE IDTERCEROS = :IDTERCERO_ARG;
        '''
        self.db.engine.execute(text(sql), IDTERCERO_ARG=idtercero)