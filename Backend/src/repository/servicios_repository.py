from sqlalchemy.sql import text


class ServiciosRepository:
    def __init__(self, db):
        self.db = db

    def get_servicios_bd(self, iddependencia):
        sql = '''
            SELECT * FROM SERVICIO
            WHERE (DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG) AND DEPENDENCIA <> 1;
        '''
        return self.db.engine.execute(text(sql), DEPENDENCIA_ARG=iddependencia).fetchall()