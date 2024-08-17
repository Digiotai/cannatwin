# import psycopg2
# import pandas as pd
# import json

# class PostgreSQLDB:
#     def __init__(self, dbname, user, password, host='cornelius.db.elephantsql.com', port=5432):
#         self.dbname = dbname
#         self.user = user
#         self.password = password
#         self.host = host
#         self.port = port

#     def connect(self):
#         try:
#             conn = psycopg2.connect(
#                 dbname=self.dbname,
#                 user=self.user,
#                 password=self.password,
#                 host=self.host,
#                 port=self.port
#             )
#             return conn
#         except Exception as e:
#             print(e)
#             return None

#     def table_creation(self):
#         try:
#             conn = self.connect()
#             if conn is not None:
#                 cursor = conn.cursor()
                
#                 # Create user_details table with user_id as the primary key
#                 user_details_query = """
#                 CREATE TABLE IF NOT EXISTS user_details (
#                   user_id SERIAL PRIMARY KEY,
#                   user_name VARCHAR(40) NOT NULL, 
#                   password VARCHAR(40) NOT NULL,
#                   first_name VARCHAR(40) NOT NULL,
#                   last_name VARCHAR(40) NOT NULL,
#                   address VARCHAR(150) NOT NULL,
#                   email VARCHAR(50),
#                   mobile VARCHAR(14)
#                 );
#                 """
#                 cursor.execute(user_details_query)
                
#                 # Create user_uploaded_data table with a foreign key reference to user_id
#                 user_uploaded_data_query = """
#                 CREATE TABLE IF NOT EXISTS user_uploaded_data (
#                   id SERIAL PRIMARY KEY,
#                   user_id INTEGER NOT NULL REFERENCES user_details(user_id),
#                   data JSONB,
#                   uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 );
#                 """
#                 cursor.execute(user_uploaded_data_query)

#                 conn.commit()
#                 cursor.close()
#                 conn.close()
#         except Exception as e:
#   
#           print(e)

#     def table_deletion(self, table_name):
#         try:
#             conn = self.connect()
#             if conn is not None:
#                 cursor = conn.cursor()
#                 query = f"DROP TABLE IF EXISTS {table_name};"
#                 cursor.execute(query)
#                 conn.commit()
#                 cursor.close()
#                 conn.close()
#         except Exception as e:
#             print(e)

#     def add_user(self, user_name, password, first_name, last_name, address, email, mobile):
#         try:
#             conn = self.connect()
#             if conn is not None:
#                 cursor = conn.cursor()
#                 query = """
#                 INSERT INTO user_details (user_name, password, first_name, last_name, address, email, mobile) 
#                 VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING user_id;
#                 """
#                 cursor.execute(query, (user_name, password, first_name, last_name, address, email, mobile))
#                 user_id = cursor.fetchone()[0]  # Get the generated user_id
#                 conn.commit()
#                 cursor.close()
#                 conn.close()
#                 return user_id  # Return the user_id
#         except Exception as e:
#             print(e)

#     def get_user_data(self, user_name):
#         try:
#             conn = self.connect()
#             if conn is not None:
#                 cursor = conn.cursor()
#                 query = "SELECT * FROM user_details WHERE user_name=%s;"
#                 cursor.execute(query, (user_name,))
#                 res = cursor.fetchone()
#                 cursor.close()
#                 conn.close()
#                 return res
#         except Exception as e:
#             print(e)

#     def store_file_data(self, user_id, df):
#         try:
#             conn = self.connect()
#             if conn is not None:
#                 cursor = conn.cursor()
#                 # Convert DataFrame to JSON format
#                 data_json = df.to_json(orient='records')
#                 query = """
#                 INSERT INTO user_uploaded_data (user_id, data) 
#                 VALUES (%s, %s);
#                 """
#                 cursor.execute(query, (user_id, data_json))
#                 conn.commit()
#                 cursor.close()
#                 conn.close()
#         except Exception as e:
#             print(e)

#     def get_uploaded_data(self, user_id):
#         try:
#             conn = self.connect()
#             if conn is not None:
#                 cursor = conn.cursor()
#                 query = """
#                 SELECT data FROM user_uploaded_data 
#                 WHERE user_id = %s;
#                 """
#                 cursor.execute(query, (user_id,))
#                 result = cursor.fetchall()
#                 cursor.close()
#                 conn.close()
#                 # Convert the result from JSON format to a DataFrame
#                 data = [pd.DataFrame(json.loads(row[0])) for row in result]
#                 return data
#         except Exception as e:
#             print(e)

# if __name__ == "__main__":
#     db = PostgreSQLDB(dbname='uibmogli', user='uibmogli', password='8ogImHfL_1G249lXtM3k2EAIWTRDH2mX')
#     db.table_creation()
#     user_id = db.add_user('test_user', 'password', 'First', 'Last', '123 Street', 'email@example.com', '1234567890')
#     print(db.get_user_data('test_user'))



import psycopg2
import pandas as pd
import json

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
                
               
                
                # Create user_details table with user_id as the primary key and email as unique
                user_details_query = """
                CREATE TABLE IF NOT EXISTS user_details (
                  user_name VARCHAR(40) NOT NULL,
                  password VARCHAR(40) NOT NULL,
                  first_name VARCHAR(40) NOT NULL,
                  last_name VARCHAR(40) NOT NULL,
                  address VARCHAR(150) NOT NULL,
                  email VARCHAR(50) UNIQUE NOT NULL,
                  mobile VARCHAR(14)
                );
                """
                cursor.execute(user_details_query)
                
                # Create user_uploaded_data table with a foreign key reference to email
                user_uploaded_data_query = """
                CREATE TABLE IF NOT EXISTS user_uploaded_data (
                  id SERIAL PRIMARY KEY,
                  email VARCHAR(50) NOT NULL REFERENCES user_details(email),
                  data JSONB,
                  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
                cursor.execute(user_uploaded_data_query)

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
                VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING user_id;
                """
                cursor.execute(query, (user_name, password, first_name, last_name, address, email, mobile))
                user_id = cursor.fetchone()[0]  # Get the generated user_id
                conn.commit()
                cursor.close()
                conn.close()
                return user_id  # Return the user_id
        except Exception as e:
            print(e)

    def get_user_data(self, email):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                query = "SELECT * FROM user_details WHERE email=%s;"
                cursor.execute(query, (email,))
                res = cursor.fetchone()
                cursor.close()
                conn.close()
                return res
        except Exception as e:
            print(e)

    def store_file_data(self, email, df):
        try:
            conn = self.connect()
            if conn is not None:
                cursor = conn.cursor()
                # Convert DataFrame to JSON format
                data_json = df.to_json(orient='records')
                query = """
                INSERT INTO user_uploaded_data (email, data) 
                VALUES (%s, %s);
                """
                cursor.execute(query, (email, data_json))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            print(e)

    def get_uploaded_data(self, email):
        try:
            conn = self.connect()
            if conn is not None:
              cursor = conn.cursor()
              query = """
              SELECT data FROM user_uploaded_data 
              WHERE email = %s;
              """
              cursor.execute(query, (email,))
              result = cursor.fetchall()
              cursor.close()
              conn.close()

            # If data is stored as JSON string, parse it; otherwise, just return it
            data = []
            for row in result:
                if isinstance(row[0], str):
                    data.append(json.loads(row[0]))
                else:
                    data.append(row[0])

            return data

        except Exception as e:
           print(e)
        return None


if __name__ == "__main__":
    db = PostgreSQLDB(dbname='uibmogli', user='uibmogli', password='8ogImHfL_1G249lXtM3k2EAIWTRDH2mX')
    db.table_creation()
    #user_id = db.add_user('test_user5', 'password', 'First', 'Last', '123 Street', 'emaiwel@gmail.com', '1234567890')
    #print(db.get_user_data('test_user5'))

    
    print(db.get_user_data("test_user1"))

