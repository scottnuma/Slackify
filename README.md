# Slackify

Slackify is a Slack bot that listens for Spotify song links and adds them to a playlist.

For example, all Spotify songs sent to a channel such as `#music` could be added to a public playlist that has songs from everyone in your company.

## Architecture

Slackify has two main components. The web server handles all communication with Slack and creates tasks. The task executor asynchronously processes these tasks, often by communicating with Spotify and other 3rd parties.
