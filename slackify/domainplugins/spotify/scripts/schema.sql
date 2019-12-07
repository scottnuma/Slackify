CREATE TABLE IF NOT EXISTS playlist_info (
    channel_id TEXT PRIMARY KEY,
    playlist_id TEXT,
    spotify_user_id TEXT
);

CREATE TABLE IF NOT EXISTS user_auth (
    spotify_user_id TEXT PRIMARY KEY,
    token TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS one_time_links (
        channel_id TEXT NOT NULL,
        token TEXT NOT NULL,
        timestamp TEXT NOT NULL
);
