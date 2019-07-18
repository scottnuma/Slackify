import unittest
from unittest import mock

import slackify
from slackify import handlers


class TestHandleAppMention(unittest.TestCase):
    def setUp(self):
        self.mock_slack_client = mock.MagicMock()
        self.mock_msg = mock.MagicMock()
        self.test_username = "test_username"
        self.test_channel_id = "test_channel"
        self.timestamp = 24601
        self.mock_msg.__getitem__.side_effect = {
            "user": self.test_username,
            "channel": self.test_channel_id,
            "event_ts": self.timestamp,
        }.__getitem__

    def test_wrong_subtype(self):
        self.mock_msg.get.return_value = "something"
        self.assertIsNone(
            handlers.handle_app_mention(
                self.mock_slack_client, self.mock_msg, self.test_channel_id
            )
        )

    def test_help_msg(self):
        self.mock_msg.get.side_effect = lambda key: "help me" if key == "text" else None

        handlers.handle_app_mention(
            self.mock_slack_client, self.mock_msg, self.test_channel_id
        )

        self.mock_slack_client.api_call.assert_called_once()
        args = self.mock_slack_client.api_call.call_args
        self.assertEqual(args[0][0], "chat.postMessage")
        self.assertEqual(args[1]["channel"], self.test_channel_id)
        self.assertIsInstance(args[1]["text"], str)
        self.assertEqual(args[1]["thread_ts"], self.timestamp)

    def test_link(self):
        self.mock_msg.get.side_effect = lambda key: "link" if key == "text" else None

        handlers.handle_app_mention(
            self.mock_slack_client, self.mock_msg, self.test_channel_id
        )

        self.mock_slack_client.api_call.assert_called()
        args_list = self.mock_slack_client.api_call.call_args_list
        self.assertEqual(args_list[0][0][0], "chat.postEphemeral")
        msg = args_list[0][1]["text"]
        self.assertTrue(self.test_channel_id in msg)
        self.assertEqual(args_list[0][1]["user"], self.test_username)
        self.assertEqual(args_list[1][0][0], "reactions.add")

    def test_unlink(self):
        self.mock_msg.get.side_effect = lambda key: "unlink" if key == "text" else None

        handlers.handle_app_mention(
            self.mock_slack_client, self.mock_msg, self.test_channel_id
        )

        self.mock_slack_client.api_call.assert_called()
        args_list = self.mock_slack_client.api_call.call_args_list
        self.assertEqual(args_list[0][0][0], "chat.postEphemeral")
        msg = args_list[0][1]["text"]
        self.assertTrue(self.test_channel_id in msg)
        self.assertEqual(args_list[0][1]["user"], self.test_username)

        self.assertEqual(args_list[1][0][0], "reactions.add")
