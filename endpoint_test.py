import unittest
from flask import Flask
from flask_testing import TestCase
import psycopg2
import endpoint as ep
import init_db as db
import war as war
from flask import jsonify


class MyFlaskAppTests(TestCase):
    def create_app(self):

        return ep.app

    def setUp(self):
        db.init()
        return

    def test_simulate_war_endpoint(self):
        # Test /simulate endpoint with a PATCH request
        with self.app.test_client() as client:
            # Get scores prior to running simulation:
            conn = ep.get_db_connection()
            cur = conn.cursor()
            tmpl = '''
                SELECT score
                FROM Scores
                WHERE playerid = %s
            '''
            cmd = cur.mogrify(tmpl, [1])
            cur.execute(cmd)
            old_score_1 = cur.fetchone()[0]
            cmd = cur.mogrify(tmpl, [2])
            cur.execute(cmd)
            old_score_2 = cur.fetchone()[0]


            # Send a PATCH request to /simulate endpoint
            response = client.patch('/simulate')
            data = response.get_json()

            # Assert response status code is 200
            self.assertEqual(response.status_code, 200)
            
            # Assert response contains expected data
            self.assertIn('won', data)
            self.assertIn('Player', data)

            # Assert database score were updated to reflect winner
            if "1" in data:
                cmd = cur.mogrify(tmpl, [1])
                cur.execute(cmd)
                new_score_1 = cur.fetchone()[0]
                assert(new_score_1 - 1 == old_score_1)
            elif "2" in data:
                cmd = cur.mogrify(tmpl, [2])
                cur.execute(cmd)
                new_score_2 = cur.fetchone()[0]
                assert(new_score_2 -1 == old_score_2)


    def test_get_score_endpoint(self):
        # Test /<int:playerid> endpoint with a GET request
        with self.app.test_client() as client:
            # Send a GET request to /<int:playerid> endpoint with playerid = 1
            response = client.get('/1')
            data = response.get_json()

            # Assert response status code is 200
            self.assertEqual(response.status_code, 200)
            
            # Assert response contains expected data
            # self.assertIn('score', data)
            self.assertIsInstance(data[0], int)
            assert(data[0] >= 0)
            
            # Send a GET request to /<int:playerid> endpoint with playerid = 2
            response = client.get('/2')
            data = response.get_json()

            # Assert response status code is 200
            self.assertEqual(response.status_code, 200)
            
            # Assert response contains expected data
            # self.assertIn('score', data)
            self.assertIsInstance(data[0], int)
            assert(data[0] >= 0)


    def tearDown(self):
        # Clean up test data, such as deleting test data from the database
        # ...
        return


if __name__ == '__main__':
    unittest.main()
