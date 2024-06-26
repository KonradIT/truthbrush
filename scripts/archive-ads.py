import sys
import requests
import traceback
import sqlite3
import os
import logging
import utils as u
from tables import ads_table, ads_migrations
from notifier import Notifier
import urlexpander

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # nopep8
from truthbrush.api import Api  # nopep8

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	api = Api()

	logging.info(":: getting ads from Truth Social")

	ads = api.ads()
	ads += api.ads(device="mobile") # guess
	connection = sqlite3.connect("output/ads.db")
	notifier = Notifier()
	for ad in ads:
		cursor = connection.cursor()
		cursor.execute(ads_table)
		for mig in ads_migrations:
			try:
				cursor.execute(mig)
			except:
				pass
		try:

			adtype = "ad"
			payload = ad.get("ad")
			username = ""
			faves = 0
			retruths = 0
			replies = 0
			if ad.get("status") != None:
				try:
					adtype = "status"
					payload = ad.get("status")
					username = payload.get("account").get("username")
					replies = payload.get("replies_count")
					faves = payload.get("favourites_count")
					retruths = payload.get("reblogs_count")
				except: pass
			unexurl = payload.get("card").get("url")
			if "smeagol.revcontent.com/v3/" in unexurl:
				unexurl = unexurl.replace("smeagol.revcontent.com/v3/", "smeagol.revcontent.com/cv/v3/")
			r = requests.get(unexurl)
			unexurl = r.url
			url = urlexpander.expand(unexurl)
			if "CLIENT_ERROR" in url:
				url = r.url
			print("%s - %s" % (url, payload.get("card").get("image")))
			cursor.execute("INSERT INTO ads VALUES(?,?,?,?,?,?,?,?)", (
				url,
				payload.get("card").get("image"),
				adtype == "status",
				payload.get("card").get("title"),
				username,
				faves,
				retruths,
				replies,
			))
		except sqlite3.IntegrityError:
			logging.error(traceback.format_exc())
			logging.info("Skipping due to it already exising.")
			continue
		except Exception as e:
			logging.error(traceback.format_exc())
			logging.info("\n\n")
			logging.info(ad)
			notifier.push("Error in TS Ads Archiver", traceback.format_exc())
			sys.exit(-1)

	connection.commit()
	connection.close()
