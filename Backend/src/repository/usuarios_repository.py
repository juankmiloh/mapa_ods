from sqlalchemy.sql import text
import base64
import os
import random
import glob
import errno
import shutil

class UsuariosRepository:
    def __init__(self, db):
        self.db = db

    def autenticar_usuario(self, usuario):
        print('LOGIN USUARIO - >', usuario)
        sql = '''
            SELECT TOKEN FROM USUARIOS
            WHERE 
                NICKNAME = :USER_ARG
            AND CONTRASENA = :PASS_ARG;
        '''
        return self.db.engine.execute(text(sql), USER_ARG=usuario["username"].lower(), PASS_ARG=usuario["password"]).fetchall()

    def getData_usuario(self, token):
        print('TOKEN USUARIO -> ', token)
        sql = '''
            SELECT 
                R.DESCRIPCION,
                U.DESCRIPCION,
                U.NICKNAME,
                U.NOMBRE||' '||U.APELLIDO AS USUARIO,
                U.IDUSUARIO,
                CASE WHEN (U.GENERO = 1 AND U.ROL = 1) THEN 'Administrador'
                ELSE CASE WHEN (U.GENERO = 2 AND U.ROL = 1) THEN 'Administradora'
                ELSE CASE WHEN (U.GENERO = 1 AND U.ROL = 2) THEN 'Proyectista'
                ELSE CASE WHEN (U.GENERO = 2 AND U.ROL = 2) THEN 'Proyectista'
                ELSE CASE WHEN (U.GENERO = 1 AND U.ROL = 3) THEN 'Revisor'
                ELSE CASE WHEN (U.GENERO = 2 AND U.ROL = 3) THEN 'Revisora'
                ELSE 'Consulta' END END END END END END AS PRIVILEGIO,
                U.AVATAR,
				U.DEPENDENCIA
            FROM USUARIOS U, ROL R
            WHERE 
                U.ROL = R.IDROL
                AND TOKEN = :TOKEN_ARG;
        '''
        return self.db.engine.execute(text(sql), TOKEN_ARG=token).fetchall()

    def get_usuarios_bd(self, dependencia):
        print('--- Dependencia - >', dependencia)
        sql = '''
            SELECT * FROM USUARIOS 
            WHERE
                (DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND ROL <> 3
                AND ROL <> 4
                ORDER BY NOMBRE ASC;
        '''
        return self.db.engine.execute(text(sql), DEPENDENCIA_ARG=dependencia).fetchall()
    
    def get_revisores_bd(self, dependencia):
        print('--- Dependencia - >', dependencia)
        sql = '''
            SELECT * FROM USUARIOS 
            WHERE
                (DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND ROL <> 2
                AND ROL <> 4
                ORDER BY NOMBRE ASC;
        '''
        return self.db.engine.execute(text(sql), DEPENDENCIA_ARG=dependencia).fetchall()

    def get_lista_usuarios_bd(self, dependencia):
        print('--- Dependencia - >', dependencia)
        sql = '''
            SELECT
                CASE WHEN (U.GENERO = 1 AND U.ROL = 1) THEN 'Administrador'
                ELSE CASE WHEN (U.GENERO = 2 AND U.ROL = 1) THEN 'Administradora'
                ELSE CASE WHEN (U.GENERO = 1 AND U.ROL = 2) THEN 'Proyectista'
                ELSE CASE WHEN (U.GENERO = 2 AND U.ROL = 2) THEN 'Proyectista'
                ELSE CASE WHEN (U.GENERO = 1 AND U.ROL = 3) THEN 'Revisor'
                ELSE CASE WHEN (U.GENERO = 2 AND U.ROL = 3) THEN 'Revisora'
                ELSE 'Consulta' END END END END END END AS PRIVILEGIO,
                U.*,
                G.NOMBRE
            FROM USUARIOS U, ROL R, GENERO G
            WHERE 
                (U.DEPENDENCIA = :DEPENDENCIA_ARG OR 1 = :DEPENDENCIA_ARG)
                AND U.ROL = R.IDROL
                AND U.GENERO = G.IDGENERO
            ORDER BY U.NOMBRE ASC;
        '''
        return self.db.engine.execute(text(sql), DEPENDENCIA_ARG=dependencia).fetchall()
    
    def get_rol_bd(self):
        sql = '''
            SELECT * FROM ROL;
        '''
        return self.db.engine.execute(text(sql)).fetchall()
    
    def get_nicknames_bd(self):
        sql = '''
            SELECT NOMBRE, APELLIDO, NICKNAME FROM USUARIOS;
        '''
        return self.db.engine.execute(text(sql)).fetchall()

    def usuarios_insert_bd(self, nombre_estado):
        # sql = '''
        #     INSERT INTO public.estado(nombreestado)
        #     VALUES (:nombre_estado_sql)
        # '''
        sql = '''
            INSERT INTO public.servicio(nombre)
            VALUES (:nombre_estado_sql);
        '''
        return self.db.engine.execute(text(sql), nombre_estado_sql=nombre_estado)
    
    def usuarios_create_bd(self, usuario):
        path = 'src/assets/'+usuario['nickname']

        sql = '''
            INSERT INTO USUARIOS
            (NOMBRE, APELLIDO, GENERO, NICKNAME, DESCRIPCION, ROL, AVATAR, CONTRASENA, TOKEN, EMAIL, DEPENDENCIA) 
            VALUES (:NOMBRE_ARG, :APELLIDO_ARG, :GENERO_ARG, :NICKNAME_ARG, :DESCRIPCION_ARG, :ROL_ARG, :AVATAR_ARG, :CONTRASENA_ARG, :TOKEN_ARG, :EMAIL_ARG, :DEPENDENCIA_ARG);
        '''

        if usuario['avatar'][0:5] != "/user": # Si la imagen no es una URL sino un Base64
            self.createDirAssets()
            self.createDir(path)
            imgPerfil = self.createImage(path, usuario, usuario['api'])
        else: # Si la imagen es una URL
            imgPerfil = usuario['avatar']

        return self.db.engine.execute(text(sql), NOMBRE_ARG=usuario['nombre'], APELLIDO_ARG=usuario['apellido'], GENERO_ARG=usuario['genero'], NICKNAME_ARG=usuario['nickname'], DESCRIPCION_ARG=usuario['descripcion'], ROL_ARG=usuario['rol'], AVATAR_ARG=imgPerfil, CONTRASENA_ARG=usuario['contrasena'], TOKEN_ARG=usuario['token'], EMAIL_ARG=usuario['email'], DEPENDENCIA_ARG=usuario['dependencia'])
    
    def usuario_update_bd(self, usuario):
        print('-------------------------------------')
        print('* USUARIO A ACTUALIZAR -> ', usuario['nicknameold'])
        print('-------------------------------------')

        path = 'src/assets/'+usuario['nickname']

        if usuario['contrasena'] != '':
            sql = '''
                UPDATE USUARIOS SET
                    NOMBRE = :NOMBRE_ARG,
                    APELLIDO = :APELLIDO_ARG,
                    GENERO = :GENERO_ARG,
                    NICKNAME = :NICKNAME_ARG,
                    DESCRIPCION = :DESCRIPCION_ARG,
                    ROL = :ROL_ARG,
                    AVATAR = :AVATAR_ARG,
                    CONTRASENA = :CONTRASENA_ARG,
                    TOKEN = :TOKEN_ARG,
                    EMAIL = :EMAIL_ARG,
                    DEPENDENCIA = :DEPENDENCIA_ARG
                WHERE IDUSUARIO = :IDUSUARIO_ARG;
            '''
        else:
            sql = '''
                UPDATE USUARIOS SET
                    NOMBRE = :NOMBRE_ARG,
                    APELLIDO = :APELLIDO_ARG,
                    GENERO = :GENERO_ARG,
                    NICKNAME = :NICKNAME_ARG,
                    DESCRIPCION = :DESCRIPCION_ARG,
                    ROL = :ROL_ARG,
                    AVATAR = :AVATAR_ARG,
                    TOKEN = :TOKEN_ARG,
                    EMAIL = :EMAIL_ARG,
                    DEPENDENCIA = :DEPENDENCIA_ARG
                WHERE IDUSUARIO = :IDUSUARIO_ARG;
            '''

        if usuario['avatar'][0:5] != "/user": # Si la imagen no es una URL sino un Base64
            self.createDirAssets()
            self.delDirImage(usuario['nicknameold']) # por si cambia el nombre de usuario
            self.createDir(path)
            imgPerfil = self.createImage(path, usuario, usuario['api'])
        else: # Si la imagen es una URL
            imgPerfil = usuario['avatar']

        return self.db.engine.execute(text(sql), IDUSUARIO_ARG=usuario['idusuario'], NOMBRE_ARG=usuario['nombre'], APELLIDO_ARG=usuario['apellido'], GENERO_ARG=usuario['genero'], NICKNAME_ARG=usuario['nickname'], DESCRIPCION_ARG=usuario['descripcion'], ROL_ARG=usuario['rol'], AVATAR_ARG=imgPerfil, CONTRASENA_ARG=usuario['contrasena'], TOKEN_ARG=usuario['token'], EMAIL_ARG=usuario['email'], DEPENDENCIA_ARG=usuario['dependencia'])

    def usuario_delete_bd(self, idusuario, nickname):
        print('-------------------------------------')
        print('* USUARIO A ELIMINAR -> ', idusuario)
        print('-------------------------------------')
        sql = '''
            DELETE FROM USUARIOS
	        WHERE IDUSUARIO = :IDUSUARIO_ARG;
        '''
        resultsql = self.db.engine.execute(text(sql), IDUSUARIO_ARG=idusuario)

        self.delDirImage(nickname)

        return resultsql

    def createDirAssets(self):
        path = 'src/assets'
        try:
            os.mkdir(path) # Se crea carpeta donde se guardan las imagenes de los user
        except OSError as e: # Se captura error si ya existe la carpeta
            if e.errno != errno.EEXIST:
                raise
    
    def createDir(self, path):
        try:
            os.mkdir(path) # Se crea carpeta donde se guarda la imagen
        except OSError as e: # Se captura error si ya existe la carpeta
            py_files = glob.glob(path+'/*.*') # Se obtienen archivos con cualquier extension (.jpeg .gif)

            for py_file in py_files:
                try:
                    os.remove(py_file) # Si hay archivos se eliminan
                except OSError as e:
                    print(f"Error:{ e.strerror}")

    def createImage(self, path, usuario, api):
        aleatorio = str(random.randrange(1, 101)) # Numero que se concatena al nombre de la imagen
        img_avatar = usuario['avatar'] # Obtenemos la imagen
        print('imagen --> ', img_avatar)
        img_split = img_avatar.split(",", 1) # Separamos el base64
        img_headers = img_split[0].split("/") # Separamos los encabezados de la imagen
        img_type = img_headers[1].split(";")[0] # Obtenemos el type de la imagen

        base64_img = img_split[1] # Obtenemos solo el base64 sin encabezados
        base64_img_bytes = base64_img.encode('utf-8') # Se codifica el base64
        script_dir = os.path.dirname(path+"/") # Ruta donde se guarda la imagen
        name_img = usuario['nickname']+aleatorio+"."+img_type # Nombre de la imagen
        abs_file_path = os.path.join(script_dir, name_img) # Ruta de la imagen

        with open(abs_file_path, "wb") as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes) # Se crea la imagen
            file_to_save.write(decoded_image_data) # Se guarda imagen en disco

        folder = usuario['nickname']

        imgPerfil = '/user/image?folder='+folder+'&image='+name_img

        return imgPerfil

    def delDirImage(self, nickname):

        path = 'src/assets/'+nickname

        try:
            shutil.rmtree(path)
        except OSError as e:
            print(f"Error:{ e.strerror}")
