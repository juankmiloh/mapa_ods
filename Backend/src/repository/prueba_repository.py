from sqlalchemy.sql import text


class PruebaRepository:
    def __init__(self, db):
        self.db = db

    def prueba_inicial_bd(self):
        sql = '''
            SELECT * FROM JHERRERAA.CAUSAS_INTERR
        '''
        return self.db.engine.execute(text(sql))

    def prueba_insert_bd(self, nombre_estado):
        # sql = '''
        #     INSERT INTO public.estado(nombreestado)
        #     VALUES (:nombre_estado_sql)
        # '''
        sql = '''
            INSERT INTO public.servicio(nombre)
            VALUES (:nombre_estado_sql);
        '''
        print('SERVICIO INSERT SQL -> ', sql)
        return self.db.engine.execute(text(sql), nombre_estado_sql=nombre_estado)
