import dotenv
import logging
import os
from pushbullet import Pushbullet
from typing import Optional

class Notifier:

	def __init__(self):
		api_key = os.getenv("PUSHBULLET_API_KEY")
		assert api_key != ""
		self.pb = Pushbullet(api_key)

	def push(self, title, body: str) -> Optional[None]:
		self.pb.push_note(title, body)