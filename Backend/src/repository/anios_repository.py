from sqlalchemy.sql import text


class AniosRepository:
    def __init__(self, db):
        self.db = db

    def get_anios_bd(self, anio):
        sql = '''
            SELECT CAR_CARG_ANO, CAR_CARG_PERIODO 
            FROM SUI_SIMPLIFICA_2015.CAR_T1554_RECLAMACIONES_GLP 
            WHERE ( CAR_CARG_ANO = :ANIO_ARG OR 0 = :ANIO_ARG ) 
            GROUP BY CAR_CARG_ANO, CAR_CARG_PERIODO 
            ORDER BY CAR_CARG_ANO, CAR_CARG_PERIODO ASC
        '''
        return self.db.engine.execute(text(sql), ANIO_ARG=anio).fetchall()