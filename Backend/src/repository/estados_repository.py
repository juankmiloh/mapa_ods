from sqlalchemy.sql import text


class EstadosRepository:
    def __init__(self, db):
        self.db = db

    def get_estados_bd(self):
        sql = '''
            SELECT * FROM ESTADO WHERE NOMBREESTADO NOT IN ('Finalizado') ORDER BY IDESTADO ASC;
        '''
        return self.db.engine.execute(text(sql)).fetchall()