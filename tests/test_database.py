import unittest
import sqlite3

import slackify

class TestTokenMethods(unittest.TestCase):
    test_database_file = "tests/test_tokens.db"
    conn = None

    def setUp(self):
        sql_query = """CREATE TABLE IF NOT EXISTS tokens (
                        id BLOB PRIMARY KEY,
                        token TEXT NOT NULL
                        );"""

        conn = sqlite3.connect(self.test_database_file)
        cur = conn.cursor()
        cur.execute(sql_query)
        conn.commit()

    def tearDown(self):
        sql_query = """DROP TABLE tokens"""
        conn = sqlite3.connect(self.test_database_file)
        cur = conn.cursor()
        cur.execute(sql_query)
        conn.commit()
                

    def test_store_and_retrieve(self):
        conn = sqlite3.connect(self.test_database_file)
        test_token = "test_access_token"
        test_id = b"test_id"
        self.assertEqual(1, slackify.spotify.store_access_token(conn, test_id, test_token))
        self.assertEqual(test_token, slackify.spotify.retrieve_access_token(conn, test_id))

if __name__ == "__main__":
    unittest.main()