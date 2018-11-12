import sqlite3
from Youtube import *

class SQlite(AbstractRepo):

    #conectar con bd
    def __init__(self):
        self.conexion = sqlite3.connect('Youtube.db')
        self.cursor = self.conexion.cursor()

    def GuardarVideo(self, video):
        # Insertar video
        v = (video.Id,video.Nombre, video.Duracion, video.Canal, video.Fecha, video.Likes, video.Vistas, video.Descripcion,video.Compartidas)
        self.cursor.execute("INSERT INTO VIDEO (ID,NOMBRE,DURACION,CANAL,FECHA,LIKES,VISTAS,DESCRIPCION,Compartidas) VALUES (?,?,?,?,?,?,?,?,?)", v)
        self.conexion.commit()#guarda cambios
        video.Id = self.cursor.lastrowid

        # Insertar categorias
        categorias = []
        if video.Categorias is not None:
            for cat in video.Categorias:
                categorias.append((video.Id, cat))
        if len(categorias) < 1:
            categorias.append((video.Id, "sin categoria"))
        self.cursor.executemany("INSERT INTO CATEGORIA (VIDEO_ID, NOMBRE) VALUES (?, ?)", categorias)
        self.conexion.commit()
        return video

    def MostrarLista(self):
        videos = []
        self.cursor.execute("SELECT * from VIDEO")
        for db_video in self.cursor.fetchall():
            video = Video(db_video[1], db_video[2], db_video[3], db_video[4], db_video[5], db_video[6], db_video[7], id=db_video[0], categorias=[])
            print(db_video)
            self.cursor.execute("SELECT * from CATEGORIA where VIDEO_ID=?", (str(video.Id),))
            for row in self.cursor.fetchall():
                print(row)
                video.Categorias.append(row[2])

            videos.append(video)

        return videos

    def MostrarVideo(self, id):
        self.id=1
        self.cursor.execute("SELECT * from VIDEO where ID=1", str(id))
        db_video = self.cursor.fetchone()
        video = Video(db_video[1], db_video[2], db_video[3], db_video[4], db_video[5], db_video[6], db_video[7], id=db_video[0], categorias=[8])

        self.cursor.execute("SELECT * from CATEGORIA where VIDEO_ID=?", (str(id),))
        for row in self.cursor.fetchall():
            video.Categorias.append(row[2])

        return video


    def ModificarVideo(self, video):
        t = (video.Nombre, video.Duracion, video.Canal, video.Fecha, video.Likes, video.Vistas, video.Descripcion, video.Id)
        self.cursor.execute("UPDATE VIDEO SET NOMBRE=?, DURACION=?, CANAL=?, FECHA=?, LIKES=?, VISTAS=?, DESCRIPCION=? where ID=?", t)
        self.conexion.commit()

        self.cursor.execute("DELETE from CATEGORIA where VIDEO_ID=?", (str(video.Id),))
        self.conexion.commit()
        # Insertar categorias
        categorias = []
        if video.Categorias is not None:
            for cat in video.Categorias:
                categorias.append((video.Id, cat))
        if len(categorias) < 1:
            categorias.append((video.Id, "sin categoria"))
        self.cursor.executemany("INSERT INTO CATEGORIA (VIDEO_ID, NOMBRE) VALUES (?, ?)", categorias)
        self.conexion.commit()
        return video


    def BorrarVideo(self, id_video):
        self.cursor.execute("DELETE from CATEGORIA where VIDEO_ID=?", (str(id_video),))
        self.cursor.execute("DELETE from VIDEO WHERE ID=?", (str(id_video),))
        self.conexion.commit()
        return True

    def Close(self):
        self.conexion.close()

if __name__ == '__main__':
    v = Video("1","nombre diferente", "13", "canal de prueba", "09/09/2018", 53, 100, "video", "152")

    base_de_datos = SQlite()

    #Guardar video
    db_video = base_de_datos.GuardarVideo(v)
    print(db_video)

     #Get one video
    video_de_query = base_de_datos.MostrarVideo()
    print(video_de_query.Id)
    print(video_de_query.Nombre)
    print(video_de_query.Categorias)

    base_de_datos.BorrarVideo(4)

    base_de_datos.ModificarVideo(v)

    # Get All videos
    videos = base_de_datos.MostrarLista()
    for vid in videos:
        print(vid.Id, vid.Nombre, vid.Categorias)

    base_de_datos.Close()
