import traceback
import sqlite3
import os
import logging
import sys
import utils as u
from tables import ads_table, ads_migrations
import requests

sys.path.insert(1, os.path.join(sys.path[0], ".."))  # nopep8
from truthbrush.api import Api  # nopep8


def delete(cursor, id):
	cursor.execute("DELETE FROM ads WHERE id=?", (id,))

def update(cursor, id, newId):
	cursor.execute("UPDATE ads SET id=? WHERE id=?", (newId,id,))


if __name__ == "__main__":

	logging.basicConfig(level=logging.INFO)

	logging.info("Fixing")

	s = requests.Session()
	connection = sqlite3.connect("output/ads.db")

	cursor = connection.cursor()
	cursor.execute("SELECT id FROM ads WHERE id LIKE '%smeagol.revcontent.com/v3%'")

	rows = cursor.fetchall()

	for row in rows:

		cursor = connection.cursor()
		logging.info(row[0])
		fixedURL = row[0].replace("smeagol.revcontent.com/v3/", "smeagol.revcontent.com/cv/v3/")
		r = s.get(fixedURL)
		r.raise_for_status()
		logging.info("New URL: "+ str(r.url))

		try:
			update(cursor, row[0], r.url)
		except sqlite3.IntegrityError:
			logging.error(traceback.format_exc())
			logging.info("Skipping due to it already exising.")
			continue
		except Exception as e:
			logging.error(traceback.format_exc())
			logging.info("\n\n")
			sys.exit(-1)

	connection.commit()
	connection.close()

