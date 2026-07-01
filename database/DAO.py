from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct a.* 
                from album a , track t 
                where a.AlbumId =t.AlbumId
                """
        cursor.execute(query)
        for row in cursor:
            results.append(Album(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getListaBrani():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.AlbumId, t.TrackId, t.GenreId
                    from track t, album a
                    where t.AlbumId = a.AlbumId
                """
        cursor.execute(query)
        for row in cursor:
            results.append((row["AlbumId"], row["TrackId"], row["GenreId"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct t1.AlbumId as a1, t2.AlbumId as a2
                    from track t1, track t2
                    where t1.TrackId != t2.TrackId
                    and t1.GenreId = t2.GenreId
                    and t1.AlbumId < t2.AlbumId
                        """
        cursor.execute(query)
        for row in cursor:
            results.append((row["a1"], row["a2"]))

        cursor.close()
        conn.close()
        return results

    # PER SAPERE QUANTE RIGHE TI RESTITUISCE UNA QUERY:
    #select  count(*)
    #from   (
        #    select distinct t1.AlbumId as a1, t2.AlbumId as a2
        #    from track t1, track t2
        #    where t1.TrackId != t2.TrackId
        #    and t1.GenreId = t2.GenreId
        #    and t1.AlbumId < t2.AlbumId
    #) as sub;

    @staticmethod
    def getEdges1():
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.AlbumId as a, t.GenreId as g
                        from track t, album a
                        where t.AlbumId = a.AlbumId
                            """
        cursor.execute(query)
        for row in cursor:
            results.append((row["a"], row["g"]))

        cursor.close()
        conn.close()
        return results

