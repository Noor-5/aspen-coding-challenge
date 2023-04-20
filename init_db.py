import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


def init():
        conn = psycopg2.connect(
                host=config.get('app', 'db_host'),
                database=config.get('app', 'db_name'),
                user=config.get('app', 'db_user'),
                password= config.get('app', 'db_password')
                )

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


if __name__ == '__main__':
        init()
