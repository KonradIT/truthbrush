from email.generator import Generator
from time import sleep
from typing import Any, Iterator, List
from loguru import logger
from requests.sessions import HTTPAdapter
from dateutil import parser as date_parse
from datetime import datetime, timezone, date
from urllib3 import Retry
import requests
import json
import logging
import os

logging.basicConfig(level=logging.INFO)


BASE_URL = "https://truthsocial.com"
API_BASE_URL = "https://truthsocial.com/api"
USER_AGENT = "TruthSocial/71 CFNetwork/1331.0.7 Darwin/21.4.0"

# Oauth client credentials, from https://truthsocial.com/packs/js/application-e63292e218e83e726270.js
CLIENT_ID = "9X1Fdd-pxNsAgEDNi_SfhJWi8T-vLuV2WVzKIbkTCw4"
CLIENT_SECRET = "ozF8jzI4968oTKFkEnsBC-UbLPCdrSv0MkXGQu2o_-M"

proxies = {"http": os.getenv("http_proxy"), "https": os.getenv("https_proxy")}


class Api:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.ratelimit_max = 300
        self.ratelimit_remaining = None
        self.ratelimit_reset = None
        if username and password:
            self.auth_id = self.get_auth_id(username, password)

    def _make_session(self):
        s = requests.Session()
        s.proxies.update(proxies)
        retries = Retry(
            total=10,
            backoff_factor=0.5,
            status_forcelist=[413, 429, 503, 403, 500, 501, 502, 503, 504, 524],
        )
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s

    def _check_ratelimit(self, resp):
        if resp.headers.get("x-ratelimit-limit") is not None:
            self.ratelimit_max = int(resp.headers.get("x-ratelimit-limit"))
        if resp.headers.get("x-ratelimit-remaining") is not None:
            self.ratelimit_remaining = int(resp.headers.get("x-ratelimit-remaining"))
        if resp.headers.get("x-ratelimit-reset") is not None:
            self.ratelimit_reset = date_parse.parse(
                resp.headers.get("x-ratelimit-reset")
            )

        if (
            self.ratelimit_remaining is not None and self.ratelimit_remaining <= 50
        ):  # We do 50 to be safe; their tracking is a bit stochastic... it can jump down quickly
            now = datetime.utcnow().replace(tzinfo=timezone.utc)
            time_to_sleep = (
                self.ratelimit_reset.replace(tzinfo=timezone.utc) - now
            ).total_seconds()
            logger.warning(
                f"Approaching rate limit; sleeping for {time_to_sleep} seconds..."
            )
            sleep(time_to_sleep)

    def _get(self, url: str, params: dict = None) -> Any:
        resp = self._make_session().get(
            API_BASE_URL + url,
            params=params,
            headers={
                "authorization": "Bearer " + self.auth_id,
                "user-agent": USER_AGENT,
            },
        )

        # Will also sleep
        self._check_ratelimit(resp)

        return resp.json()

    def _get_paginated(self, url: str, params: dict = None, resume: str = None) -> Any:
        next_link = API_BASE_URL + url

        if resume is not None:
            next_link += f"?max_id={resume}"

        while next_link is not None:
            resp = self._make_session().get(
                next_link,
                params=params,
                headers={
                    "authorization": "Bearer " + self.auth_id,
                    "user-agent": USER_AGENT,
                },
            )

            next_link = resp.links.get("next", {}).get("url")
            logger.info(f"Next: {next_link}, resp: {resp}, headers: {resp.headers}")
            yield resp.json()

            # Will also sleep
            self._check_ratelimit(resp)

    def lookup(self, user_handle: str = None) -> dict:
        """Lookup a user's information."""

        assert user_handle is not None
        return self._get("/v1/accounts/lookup", params=dict(acct=user_handle))

    def trending(self):
        """Return trending truths."""

        return self._get("/v1/truth/trending/truths")

    def tags(self):
        """Return trending tags."""

        return self._get("/v1/trends")

    def suggested(self, maximum: int = 50) -> dict:
        """Return a list of suggested users to follow."""

        return self._get(f"/v2/suggestions?limit={maximum}")

    def user_followers(
        self,
        user_handle: str = None,
        user_id: str = None,
        maximum: int = 1000,
        resume: str = None,
    ) -> Iterator[dict]:
        assert user_handle is not None or user_id is not None
        user_id = user_id if user_id is not None else self.lookup(user_handle)["id"]

        n_output = 0
        for followers_batch in self._get_paginated(
            f"/v1/accounts/{user_id}/followers", resume=resume
        ):
            for f in followers_batch:
                yield f
                n_output += 1
                if maximum is not None and n_output >= maximum:
                    return

    def user_following(
        self,
        user_handle: str = None,
        user_id: str = None,
        maximum: int = 1000,
        resume: str = None,
    ) -> Iterator[dict]:
        assert user_handle is not None or user_id is not None
        user_id = user_id if user_id is not None else self.lookup(user_handle)["id"]

        n_output = 0
        for followers_batch in self._get_paginated(
            f"/v1/accounts/{user_id}/following", resume=resume
        ):
            for f in followers_batch:
                yield f
                n_output += 1
                if maximum is not None and n_output >= maximum:
                    return

    def pull_statuses(
        self, username: str, created_after: date, replies: bool
    ) -> List[dict]:
        """Pull the given user's statuses. Returns an empty list if not found."""

        params = {}
        all_posts = []
        id = self.lookup(username)["id"]
        while True:
            try:
                url = f"/v1/accounts/{id}/statuses"
                if not replies:
                    url += "?exclude_replies=true"
                result = self._get(url, params=params)
            except json.JSONDecodeError as e:
                logger.error(f"Unable to pull user #{id}'s statuses': {e}")
                break
            except Exception as e:
                logger.error(f"Misc. error while pulling statuses for {id}: {e}")
                break

            if "error" in result:
                logger.error(
                    f"API returned an error while pulling user #{id}'s statuses: {result}"
                )
                break

            if len(result) == 0:
                break

            if not isinstance(result, list):
                logger.error(f"Result is not a list (it's a {type(result)}): {result}")

            posts = sorted(result, key=lambda k: k["id"])
            params["max_id"] = posts[0]["id"]

            most_recent_date = (
                date_parse.parse(posts[-1]["created_at"])
                .replace(tzinfo=timezone.utc)
                .date()
            )
            if created_after and most_recent_date < created_after:
                # Current and all future batches are too old
                break

            for post in posts:
                post["_pulled"] = datetime.now().isoformat()
                date_created = (
                    date_parse.parse(post["created_at"])
                    .replace(tzinfo=timezone.utc)
                    .date()
                )
                if created_after and date_created < created_after:
                    continue

                all_posts.append(post)

        return all_posts

    def get_auth_id(self, username: str, password: str) -> str:
        """Logs in to Truth account and returns the session token"""
        url = BASE_URL + "/oauth/token"
        try:

            payload = {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "grant_type": "password",
                "username": username,
                "password": password,
            }

            sess_req = requests.request(
                "POST",
                url,
                params=payload,
                headers={
                    "user-agent": USER_AGENT,
                },
            )
            sess_req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed login request: {str(e.response.status_code)}")
            return None

        if not sess_req.json()["access_token"]:
            raise ValueError("Invalid truthsocial.com credentials provided!")

        return sess_req.json()["access_token"]
