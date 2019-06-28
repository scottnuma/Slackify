import unittest
import sqlite3
import os


import slackify

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FILE = "/".join([TEST_DIR, "..", "scripts", "schema.sql"])


class TestTokenMethods(unittest.TestCase):
    test_database_file = ":memory:"
    conn = None

    def setUp(self):
        self.conn = sqlite3.connect(self.test_database_file)
        with open(SCHEMA_FILE) as schema_file:
            self.conn.executescript(schema_file.read())

    def tearDown(self):
        self.conn.close()
        self.conn = None

    def test_store_and_retrieve(self):
        test_token = "test_access_token"
        test_id = "test_id"
        self.assertEqual(
            1, slackify.spotify.store_access_token(self.conn, test_id, test_token)
        )
        self.assertEqual(
            test_token,
            slackify.spotify.spotify_database.get_access_token(self.conn, test_id),
        )
        self.assertEqual(
            None,
            slackify.spotify.spotify_database.get_access_token(self.conn, "random_id"),
        )

    def test_one_time_tokens(self):
        self.assertFalse(
            slackify.spotify.spotify_database.verify_token(
                self.conn, "lksjdfjlksj", "lkdfwee"
            )
        )
        channel_id = "thechannelid"
        token = slackify.spotify.spotify_database.generate_token(self.conn, channel_id)
        another_token = slackify.spotify.spotify_database.generate_token(
            self.conn, channel_id
        )
        self.assertNotEqual(token, another_token)
        self.assertTrue(
            slackify.spotify.spotify_database.verify_token(self.conn, channel_id, token)
        )
        self.assertTrue(
            slackify.spotify.spotify_database.verify_token(
                self.conn, channel_id, another_token
            )
        )


if __name__ == "__main__":
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    print(THIS_DIR)
    unittest.main()
