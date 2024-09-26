
import mysql.connector
import time
from game_of_life_globals import DATABASE_CONFIG


class game_database:
    def __init__(self):
        self.connection = self.connect_to_mysql()

    def __del__(self):
        self.connection.close()
    
    def connect_to_mysql(config, attempts=3, delay=2):
        attempt = 1
        # Implement a reconnection routine
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**DATABASE_CONFIG)
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    # Attempts to reconnect failed; returning None
                    print("Failed to connect, exiting without a connection: %s", err)
                    return None
                print(
                    "Connection failed: %s. Retrying (%d/%d)...",
                    err,
                    attempt,
                    attempts-1,
                )
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return None
    
    def show_all_sessions(self):
        with self.connection.cursor() as cursor:
            query = ("""
                    select session.session_id, session.date, session.metadata, counted.count, counted.latest  from `session`
                    inner join 
                    (select session_id, count(*) as count, max(`date`) as latest  from session_data group by session_id) 
                    as counted
                    on session.session_id = counted.session_id;
                    """)
            cursor.execute(query)

            for (line) in cursor:
                yield {
                    'session_id' : line[0],
                    'date' :   line[1],
                    'metadata' : line[2],
                    'steps' : line[3],
                    'last' : line[4],
                }
    
    def show_all_sessions(self):
        with self.connection.cursor() as cursor:
            query = ("""
                    select session.session_id, session.date, session.metadata, counted.count, counted.latest  from `session`
                    inner join 
                    (select session_id, count(*) as count, max(`date`) as latest  from session_data group by session_id) 
                    as counted
                    on session.session_id = counted.session_id;
                    """)
            cursor.execute(query)

            for (line) in cursor:
                yield {
                    'session_id' : line[0],
                    'date' :   line[1],
                    'metadata' : line[2],
                    'steps' : line[3],
                    'last' : line[4],
                }


    def session_id_already_exists(self, session_id):
        with self.connection.cursor() as cursor:
            query = f"SELECT EXISTS(SELECT 1 FROM session WHERE session_id = %s)"
            cursor.execute(query, (session_id,))
            exists = cursor.fetchone()[0]
            return exists
        
    def new_life(self, session_id, metadata, new_life_string):
        self.store_session(session_id, metadata)
        self.store_state(session_id, life_string=new_life_string, step=0)

    def store_session(self, session_id, metadata):
        with self.connection.cursor() as cursor:
            try:
                query = "INSERT INTO Session (session_id, metadata) VALUES (%s, %s)"
                cursor.execute(query, (session_id, metadata))
                self.connection.commit()
        
                print(f"Session {session_id} with metadata {metadata} inserted successfully!")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.connection.rollback()

    def store_state(self, session_id, life_string, step):
        with self.connection.cursor() as cursor:
            try:
                query = "INSERT INTO `session_data` (`session_id`, `data`, `step`) VALUES (%s, %s, %s)"
                cursor.execute(query, (session_id, life_string, int(step)))
                self.connection.commit()
        
                print(f"Session {session_id} with metadata {life_string} inserted successfully!")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                self.connection.rollback()

    def get_session_by_id(self, session_id):
        with self.connection.cursor() as cursor:
            query = ("""
                    SELECT session.session_id, session.date, session.metadata, counted.count, counted.latest
                    FROM `session`
                    INNER JOIN 
                    (SELECT session_id, COUNT(*) AS count, MAX(`date`) AS latest
                    FROM session_data
                    WHERE session_id = %s
                    GROUP BY session_id) AS counted
                    ON session.session_id = counted.session_id;
                    """)
            cursor.execute(query, (session_id,)) 
            
        
            line = cursor.fetchone()

            if line:
                return {
                    'session_id': line[0],
                    'date': line[1],
                    'metadata': line[2],
                    'steps': line[3],
                    'last': line[4],
                }
            else:
                return None
            
    def get_states(self, session_id):
        with self.connection.cursor() as cursor:
            # TODO : optimize query so that we only get the relevant row
            query = ("""
                    select data, step from session_data where session_id=%s order by step;
                    """)
            cursor.execute(query, (session_id,))         
            lines = cursor.fetchall()
            
            if lines:
                return lines
            else:
                return None
            
    

