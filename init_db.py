import psycopg2


def init():
        conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="noormostafa")

        cur = conn.cursor()

        # Execute a command: this creates a new table
        cur.execute('DROP TABLE IF EXISTS scores;')
        cur.execute('CREATE TABLE scores ('
                                        'PlayerID int  NOT NULL,'
                                        'Score int  NOT NULL,'
                                        'CONSTRAINT Score_pk PRIMARY KEY (PlayerID));'
                                        )

        # Insert data
        cur.execute('INSERT INTO Scores (PlayerID, Score)'
                'VALUES (1, 0);')
        cur.execute('INSERT INTO Scores (PlayerID, Score)'
                'VALUES (2, 0);')

        conn.commit()

        cur.close()
        conn.close()



