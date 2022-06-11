# wrote this script with the side effects of a corona vaccine AND sleep deprived.

import traceback
import json
import sqlite3
import os
import sys
import logging
import utils as u
from tables import posts_table, posts_table_values, reblogs_table, reblogs_table_values, media_attachment_table, media_attachment_table_values
from typing import Optional
from schemas import Post

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from truthbrush.api import Api


def write_to_db(account: str, post: Post) -> Optional[Exception]:
    # Writes the post to a SqliteDB, conserving everything to the best of my abilities
    # Maybe I'll append to a CSV as well

    connection = sqlite3.connect("output/%s_posts.db" % account)
    cursor = connection.cursor()

    tables = [
        posts_table,
        reblogs_table,
        media_attachment_table
    ]
    for table in tables:
        cursor.execute(table)

    cursor.execute("INSERT INTO posts VALUES(%s)" % posts_table_values, (
        post.id,
        post.created_at,
        int(post.sensitive),
        post.spoiler_text,
        post.visibility,
        post.uri,
        post.url,
        post.replies_count,
        post.reblogs_count,
        post.favourites_count,
        int(post.favourited),
        int(post.reblogged),
        int(post.muted),
        int(post.bookmarked),
        post.content,
        ",".join([i.get("username") for i in post.mentions]),
        ",".join([i.get("name") for i in post.tags]),
        ",".join(post.emojis),
        post.pulled,
        post.language,
        post.in_reply_to_id,
        post.in_reply_to_account_id
    ))

    if post.reblog:
        cursor.execute("INSERT INTO reblogs VALUES(%s)" % reblogs_table_values, (
            post.reblog.id,
            post.id,
            post.reblog.created_at,
            post.reblog.spoiler_text,
            post.reblog.visibility,
            post.reblog.uri,
            post.reblog.url,
            post.reblog.replies_count,
            post.reblog.reblogs_count,
            post.reblog.favourites_count,
            int(post.reblog.favourited),
            int(post.reblog.reblogged),
            int(post.reblog.muted),
            int(post.reblog.bookmarked),
            post.reblog.content,
            ",".join([i.get("username") for i in post.reblog.mentions]),
            ",".join([i.get("name") for i in post.reblog.tags]),
            ",".join(post.reblog.emojis),
            post.reblog.language,
            post.reblog.in_reply_to_id,
            post.reblog.in_reply_to_account_id
        ))

    media_attachments = []
    parent_id = ""
    is_media_attachment_reblog = False
    if len(post.media_attachments) != 0:
        media_attachments = post.media_attachments
        parent_id = post.id

    if post.reblog:
        if len(post.reblog.media_attachments) != 0:
            media_attachments = post.reblog.media_attachments
            is_media_attachment_reblog = True
            parent_id = post.reblog.id

    if len(media_attachments) != 0:
        for media_attachment in media_attachments:
            try:
                cursor.execute("INSERT INTO media_attachments VALUES(%s)" % media_attachment_table_values, (
                    media_attachment.id,
                    "" if is_media_attachment_reblog else parent_id,
                    "" if not is_media_attachment_reblog else parent_id,
                    media_attachment.type,
                    media_attachment.url,
                    media_attachment.preview_url,
                    media_attachment.text_url,
                    media_attachment.blurhash,
                    media_attachment.external_video_id,
                    media_attachment.description,
                    media_attachment.preview_remote_url,
                    media_attachment.remote_url
                ))
            except sqlite3.IntegrityError:
                pass

    connection.commit()
    connection.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api = Api(os.getenv("TRUTHSOCIAL_USERNAME"),
              os.getenv("TRUTHSOCIAL_PASSWORD"))

    logging.info("Getting posts from Truth Social")

    with open(os.path.join("scripts", "accounts.json"), "r") as accounts_file:
        accounts = json.loads(accounts_file.read())

    for account in accounts:
        logging.info("Looking at %s" % account)

        _, date_yesterday = u.get_day(days_back=1)
        posts = api.pull_statuses(username=account,
                                  created_after=date_yesterday,
                                  replies=True)
        for post in posts:
            try:
                cpost = Post.from_dict(post)
            except Exception as e:
                logging.error(traceback.format_exc())
                logging.info("\n\n")
                logging.info(post)
                sys.exit(-1)
            try:
                write_to_db(account, cpost)
            except sqlite3.IntegrityError:
                logging.info("Nothing to add")
                sys.exit(0)
            except Exception as e:
                logging.error(traceback.format_exc())
                logging.info("\n\n")
                logging.info(post)
                sys.exit(-1)
