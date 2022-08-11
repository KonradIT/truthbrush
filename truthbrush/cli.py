"""Defines the CLI for Truthbrush."""

import json
import os
import click
from datetime import date
import pkg_resources
from dotenv import load_dotenv

from .api import Api

load_dotenv()  # take environment variables from .env.
api = Api(os.getenv("TRUTHSOCIAL_USERNAME"), os.getenv("TRUTHSOCIAL_PASSWORD"))


@click.group()
def cli():
    """This is an API client for Truth Social."""


@cli.command()
def trends():
    """Pull trendy Truths."""

    print(json.dumps(api.trending()))


@cli.command()
def tags():
    """Pull trendy tags."""

    print(json.dumps(api.tags()))


@cli.command()
@click.argument("handle")
def user(handle: str):
    """Pull a user's metadata."""

    print(json.dumps(api.lookup(handle)))


@cli.command()
@click.argument("query")
@click.option(
    "--searchtype",
    help="Type of search query (accounts, statuses, or hashtags)",
    type=click.Choice(["accounts", "statuses", "hashtags"]),
)
@click.option("--limit", help="Limit the number of items returned", type=int)
@click.option("--resolve", help="Resolve", type=bool)
def search(searchtype: str, query: str, limit: int, resolve: bool):
    """Search for users, statuses or hashtags."""

    print(json.dumps(api.search(searchtype, query, limit, resolve)))


@cli.command()
def suggestions():
    """Pull the list of suggested users."""

    print(json.dumps(api.suggested()))


@cli.command()
@click.argument("handle")
@click.option("--maximum", help="the maximum number of followers to pull", type=int)
@click.option(
    "--resume",
    help="the `max_id` cursor to resume from, if necessary (pull this from logs to resume a failed/stalled export)",
    type=str,
)
def followers(handle: str, maximum: int = None, resume: str = None):
    """Pull a user's followers."""

    for follower in api.user_followers(handle, maximum=maximum, resume=resume):
        print(json.dumps(follower))


@cli.command()
@click.argument("handle")
@click.option(
    "--maximum", help="the maximum number of followed users to pull", type=int
)
@click.option(
    "--resume",
    help="the `max_id` cursor to resume from, if necessary (pull this from logs to resume a failed/stalled export)",
    type=str,
)
def following(handle: str, maximum: int = None, resume: str = None):
    """Pull users a given user follows."""

    for followed in api.user_following(handle, maximum=maximum, resume=resume):
        print(json.dumps(followed))


@cli.command()
@click.argument("username")
@click.option(
    "--replies/--no-replies",
    default=False,
    help="Include replies when pulling posts (defaults to no replies)",
)
@click.option(
    "--created-after",
    default=None,
    help="Only pull posts created on or after the specified date, e.g. 2021-10-02 (defaults to none).",
    type=date.fromisoformat,
)
def statuses(username: str, replies: bool = False, created_after: date = None):
    """Pull a user's statuses"""
    print(json.dumps(api.pull_statuses(username, created_after, replies)))
