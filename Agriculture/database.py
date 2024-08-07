# import sqlite3
# import pandas as pd
# import os


# class SQLiteDB:
#     def __init__(self):
#         pass

#     def table_creation(self):
#         """
#             Method Name: table_creation
#             Description: This method is used to create a new table in database .
#             Output:  Returns html table created from input data.
#             On Failure: None
#             Written By: Digiotai
#             Version: 1.0
#             Revisions: None
#         """

#         try:
#             with sqlite3.connect("db.sqlite3") as c:
#                 # Getting the uploaded file
#                 cursor = c.cursor()
#                 query = """
#                 CREATE TABLE user_details (
#                   user_name VARCHAR(40) NOT NULL, 
#                   password VARCHAR(40) NOT NULL,
#                   first_name VARCHAR(40) NOT NULL,
#                   last_name VARCHAR(40) NOT NULL,
#                   address VARCHAR(150) NOT NULL,
#                   email varchar(50),
#                   mobile varchar(14)
#                   );"""
#                 cursor.execute(query)
#                 c.commit()
#         except Exception as e:
#             print(e)

#     def table_deletion(self):
#         """
#             Method Name: tabledeletion
#             Description: This method is used to delete an existing table from database .
#             Output:  None
#             On Failure: None

#             Written By: Digiotai
#             Version: 1.0
#             Revisions: None
#         """
#         try:
#             with sqlite3.connect("db.sqlite3") as c:
#                 # Getting the uploaded file
#                 cursor = c.cursor()
#                 query = """
#                 DROP TABLE {name}
#                   );"""
#                 cursor.execute(query)
#                 c.commit()
#         except Exception as e:
#             print(e)

#     def add_user(self, user_name, password, first_name, last_name, address, email, mobile):
#         try:
#             with sqlite3.connect("db.sqlite3") as c:
#                 # Getting the uploaded file
#                 cursor = c.cursor()
#                 query = f"""
#                 INSERT INTO user_details (user_name, password, first_name, last_name, address, email, mobile) 
#                 VALUES('{user_name}','{password}','{first_name}','{last_name}','{address}','{email}','{mobile}');"""
#                 cursor.execute(query)
#                 c.commit()
#         except Exception as e:
#             print(e)

#     def get_user_data(self, user_name):
#         try:
#             with sqlite3.connect("db.sqlite3") as c:
#                 # Getting the uploaded file
#                 cursor = c.cursor()
#                 query = f"""SELECT * from user_details where user_name='{user_name}'"""
#                 cursor.execute(query)
#                 res = cursor.fetchone()
#                 print(res)
#                 c.commit()
#                 return res
#         except Exception as e:
#             print(e)

#     def update_user(self, user_name, plan, count):
#         with sqlite3.connect("db.sqlite3") as c:
#             # Getting the uploaded file
#             cursor = c.cursor()
#             query = f"""UPDATE user_details SET count = count - 1,Quota='{plan}',count='{count}' where user_name='{user_name}'"""
#             cursor.execute(query)
#             res = cursor.fetchone()
#             c.commit()
#             return res

#     def get_users(self):
#         try:
#             with sqlite3.connect("db.sqlite3") as c:
#                 # Getting the uploaded file
#                 cursor = c.cursor()
#                 query = f"""SELECT user_name from user_details """
#                 cursor.execute(query)
#                 res = cursor.fetchall()
#                 res = [i[0] for i in res]
#                 c.commit()
#                 return res
#         except Exception as e:

#             print(e)



# if __name__ == "__main__":
#     db = SQLiteDB()
#     # db.table_creation()
#     db.add_user('kpi')
#     print(db.get_user_data('test'))
#     # print(db.update_count('Rami'))
#     # print(db.get_user_data('Rami'))






import psycopg2
import pandas as pd
import os

class PostgreSQLDB:
    def __init__(self, dbname, user, password, host='cornelius.db.elephantsql.com', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except Exception as e:
            print(e)
            return None

    def table_creation(self):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                CREATE TABLE IF NOT EXISTS user_details (
                  user_name VARCHAR(40) NOT NULL, 
                  password VARCHAR(40) NOT NULL,
                  first_name VARCHAR(40) NOT NULL,
                  last_name VARCHAR(40) NOT NULL,
                  address VARCHAR(150) NOT NULL,
                  email VARCHAR(50),
                  mobile VARCHAR(14)
                );
                """
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def table_deletion(self, table_name):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = f"DROP TABLE IF EXISTS {table_name};"
                cursor.execute(query)
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def add_user(self, user_name, password, first_name, last_name, address, email, mobile):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                INSERT INTO user_details (user_name, password, first_name, last_name, address, email, mobile) 
                VALUES(%s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, (user_name, password, first_name, last_name, address, email, mobile))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def get_user_data(self, user_name):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "SELECT * FROM user_details WHERE user_name=%s;"
                cursor.execute(query, (user_name,))
                res = cursor.fetchone()
                cursor.close()
                conn.close()
                return res
        except Exception as e:
            print(e)

    def update_user(self, user_name, plan, count):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = """
                UPDATE user_details 
                SET count = %s, Quota = %s 
                WHERE user_name = %s;
                """
                cursor.execute(query, (count, plan, user_name))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def get_users(self):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "SELECT user_name FROM user_details;"
                cursor.execute(query)
                res = cursor.fetchall()
                res = [i[0] for i in res]
                cursor.close()
                conn.close()
                return res
        except Exception as e:
            print(e)


if __name__ == "__main__":
    db = PostgreSQLDB(dbname='uibmogli', user='uibmogli', password='8ogImHfL_1G249lXtM3k2EAIWTRDH2mX')
    db.table_creation()
    db.add_user('test_user', 'password', 'First', 'Last', '123 Street', 'email@example.com', '1234567890')
    print(db.get_user_data('test_user'))
