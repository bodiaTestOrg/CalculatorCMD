import pyodbc

class DbManager():
    def __init__(self):
        pass

    def saveActions(self,dsn,data):
        conn = pyodbc.connect(dsn)
        cursor = conn.cursor()

        insertQuery = "INSERT INTO [Actions] ([time],[action]) VALUES(?,?)"
        cursor.executemany(insertQuery,data)

        conn.commit()
        cursor.close()
        conn.close()

        return True
    
    def getLogs(self,dsn):
        conn = pyodbc.connect(dsn)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM [Actions]")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows