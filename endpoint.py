from flask import Flask
from flask_cors import CORS, cross_origin
import psycopg2
import sys
import war as war
from flask import jsonify


app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="noormostafa")
    return conn

@app.route('/simulate', methods =["PATCH"])
def simulate_war():
    # Run war simulation
    result = war.play_war()
    # Update db by incrementing score of winning player
    try:
        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()
        tmpl = '''
            UPDATE Scores
            SET score = score + 1
            WHERE playerid = %s
        '''
        cmd = cur.mogrify(tmpl, [result])
        
        cur.execute(cmd)
        cur.close()
        conn.close()
        
        # response = jsonify(f"Player {result} won")
        return jsonify(f"Player {result} won!")
    except Exception as e:
        print(e)
        return 
    

@app.route('/<int:playerid>', methods = ["GET"])
def get_score(playerid):
    try:
        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()
        tmpl = '''
            SELECT score
            FROM Scores
            WHERE playerid = %s
        '''
        
        cmd = cur.mogrify(tmpl, [playerid])
        
        cur.execute(cmd)
        result = jsonify(cur.fetchone())
        cur.close() 
        conn.close()  

        return (result)
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    app.run(port = 5000)
