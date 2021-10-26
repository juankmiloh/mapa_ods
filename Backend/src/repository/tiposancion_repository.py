from sqlalchemy.sql import text


class TiposancionRepository:
    def __init__(self, db):
        self.db = db

    def get_tiposancion_bd(self):
        sql = '''
            SELECT * FROM TIPOSANCION;
        '''
        return self.db.engine.execute(text(sql)).fetchall()