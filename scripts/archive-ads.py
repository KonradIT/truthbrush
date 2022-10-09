import sys
import requests
import traceback
import sqlite3
import os
import logging
import utils as u
from tables import ads_table
from notifier import Notifier

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # nopep8
from truthbrush.api import Api  # nopep8

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	api = Api()

	logging.info(":: getting ads from Truth Social")

	def resolve(uri) -> str:
		r = requests.get(uri, allow_redirects=False)
		assert r.status_code == 302
		return r.headers["Location"]
	ads = api.ads().get("ads")
	connection = sqlite3.connect("output/ads.db")
	notifier = Notifier()
	for ad in ads:
		print("%s - %s" % (resolve(ad.get("click")), ad.get("asset")))
		cursor = connection.cursor()
		cursor.execute(ads_table)
		try:
			cursor.execute("INSERT INTO ads VALUES(?,?)", (
				resolve(ad.get("click")),
				ad.get("asset"),
			))
		except sqlite3.IntegrityError:
			logging.error(traceback.format_exc())
			logging.info("Skipping due to it already exising.")
			continue
		except Exception as e:
			logging.error(traceback.format_exc())
			logging.info("\n\n")
			logging.info(resolve(ad.get("click")))
			notifier.push("Error in TS Ads Archiver", traceback.format_exc())
			sys.exit(-1)
	
	connection.commit()
	connection.close()
