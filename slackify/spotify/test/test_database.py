import unittest
import os
import secrets

from google.cloud import firestore

from slackify.spotify import database
from slackify.settings import Config


def deleteCollection(coll_ref):
    docs = coll_ref.stream()

    for doc in docs:
        print(u"Deleting doc {} => {}".format(doc.id, doc.to_dict()))
        doc.reference.delete()


class TestTokenMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = database.get_db("testing")

    @classmethod
    def tearDownClass(cls):
        for coll in [
            database.TOKEN_COLLECTION,
            database.PLAYLIST_COLLECTION,
            database.USER_COLLECTION,
        ]:
            deleteCollection(cls.conn.collection(coll))

    def test_store_and_retrieve(self):
        test_token = "test_access_token"
        test_id = "test_id"
        self.assertIsNotNone(
            database.store_access_token(self.conn, test_id, test_token)
        )
        self.assertEqual(test_token, database.get_access_token(self.conn, test_id))
        self.assertEqual(None, database.get_access_token(self.conn, "random_id"))

    def test_one_time_tokens(self):
        self.assertFalse(database.verify_token(self.conn, "lksjdfjlksj", "lkdfwee"))
        channel_id = "thechannelid"
        token = database.generate_token(self.conn, channel_id)
        another_token = database.generate_token(self.conn, channel_id)
        self.assertNotEqual(token, another_token)
        self.assertTrue(database.verify_token(self.conn, channel_id, token))
        self.assertTrue(database.verify_token(self.conn, channel_id, another_token))

    def test_contains_channel(self):
        channel_id = secrets.token_hex(16)
        self.assertFalse(database.contains_channel(self.conn, channel_id))
        self.assertIsNone(database.get_playlist_user(self.conn, channel_id))
        playlist_id = "playlist_id"
        database.store_playlist_id(self.conn, channel_id, playlist_id)
        spotify_user_id = "spotify_user_id"
        database.store_user_id(self.conn, channel_id, spotify_user_id)
        self.assertTrue(database.contains_channel(self.conn, channel_id))
        retrieved_playlist_id, retrieved_spotify_user_id = database.get_playlist_user(
            self.conn, channel_id
        )
        self.assertEqual(playlist_id, retrieved_playlist_id)
        self.assertEqual(spotify_user_id, retrieved_spotify_user_id)

    def test_delete_channel(self):
        channel_id = secrets.token_hex(16)
        playlist_id = "playlist_id"
        database.store_playlist_id(self.conn, channel_id, playlist_id)
        token = database.generate_token(self.conn, channel_id)
        self.assertTrue(database.contains_channel(self.conn, channel_id))

        database.delete_channel(self.conn, channel_id)
        self.assertFalse(database.contains_channel(self.conn, channel_id))
        self.assertFalse(database.verify_token(self.conn, channel_id, token))

    def test_verify_token(self):
        channel_id = secrets.token_hex(16)
        token = database.generate_token(self.conn, channel_id)
        self.assertTrue(database.verify_token(self.conn, channel_id, token))
        self.assertFalse(database.verify_token(self.conn, channel_id, token))


if __name__ == "__main__":
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    print(THIS_DIR)
    unittest.main()
