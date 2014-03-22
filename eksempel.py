# -*- coding: utf-8 -*-
import cmd
import json
import urllib2
from pymongo import MongoClient

client = MongoClient()

database = client['biblioteket']
boker = database['boker']


class Console(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = "=>> "
		self.intro = "Velkommen til bibliotekets boksystem ved Blindern Studenterhjem!"

	def do_vis(self, args):
		"""vis\n\tVis registrerte bøker"""

		reg = boker.find()
		if not reg:
			print "Ingen bøker er registrert i systemet."
			return

		print "Bøker registrert:"
		for bok in boker.find():
			print " * %s (%s)" % (bok['title'], bok['publishedDate'])

	def do_EOF(self, args):
		print
		return -1

	def do_exit(self, args):
		return -1

	def do_registrer(self, args):
		registrer = Registrer()
		registrer.cmdloop()

	def do_exit(self, args):
		return -1


class Registrer(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = ": "
		self.intro = "Scan ISBN-kode!"

	def do_exit(self, args):
		return -1

	def do_EOF(self, args):
		print
		return -1

	def default(self, line):
		print "Du søker etter: %s" % line

		data = urllib2.urlopen("https://www.googleapis.com/books/v1/volumes?q=isbn:%s" % line).read()

		obj = json.loads(data)
		obj = obj['items'][0]['volumeInfo']

		id = boker.insert(obj)
		elm = boker.find_one(id)

		print "Du har registrert følgende bok:"
		print "Tittel: %s" % elm['title']
		print "Publisert: %s" % elm['publishedDate']

		#return -1

if __name__ == "__main__":
	console = Console()
	console.cmdloop()