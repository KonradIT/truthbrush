
# Main table
posts_table = """CREATE TABLE IF NOT EXISTS posts (id text PRIMARY KEY,
	created_at text,
	sensitive integer,
	spoiler_text text,
	visibility text,
	uri text,
	url text,
	replies_count integer,
	reblogs_count integer,
	favourites_count integer,
	favourited integer,
	reblogged integer,
	muted integer,
	bookmarked integer,
	content text,
	mentions text,
	tags text,
	emojis text,
	_pulled text,
	language text,
	in_reply_to_id text,
	in_reply_to_account_id text);"""
posts_table_values = ("?," * (posts_table.count("\n") + 1))[:-1]

reblogs_table = """CREATE TABLE IF NOT EXISTS reblogs (id text PRIMARY KEY,
	parent_post_id text
	created_at text,
	sensitive integer,
	spoiler_text text,
	visibility text,
	uri text,
	url text,
	replies_count integer,
	reblogs_count integer,
	favourites_count integer,
	favourited integer,
	reblogged integer,
	muted integer,
	bookmarked integer,
	content text,
	mentions text,
	tags text,
	emojis text,
	language text,
	in_reply_to_id text,
	in_reply_to_account_id text,
	FOREIGN KEY (parent_post_id) REFERENCES posts (id));"""
reblogs_table_values = ("?," * 21)[:-1]

media_attachment_table = """CREATE TABLE IF NOT EXISTS media_attachments (id text PRIMARY KEY,
	parent_post_id text,
	parent_reblog_id text,
 	type text,
	url text,
	preview_url text,
	text_url text,
	blurhash text,
	external_video_id text,
	description text,
	preview_remote_url text,
	remote_url text,
	FOREIGN KEY (parent_post_id) REFERENCES posts (id)
 	FOREIGN KEY (parent_reblog_id) REFERENCES reblogs (id));
"""

media_attachment_table_values = (
    "?," * (media_attachment_table.count("\n") - 2))[:-1]

ads_table = """CREATE TABLE IF NOT EXISTS ads (id text PRIMARY KEY, image text)"""
ads_migrations = ["ALTER TABLE ads ADD COLUMN is_status BOOL DEFAULT false",
"ALTER TABLE ads ADD COLUMN title TEXT",
"ALTER TABLE ads ADD COLUMN status_username TEXT"]
