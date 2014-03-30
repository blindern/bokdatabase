# -*- coding: utf-8 -*-
import cmd
#import json
#import urllib2
#import pprint
from collections import OrderedDict
from apiclient.discovery import build
from pymongo import MongoClient

# sett opp MongoDB-tilkobling
# foreløpig ingen pålogging i prototypen..
client = MongoClient()
database = client['biblioteket']
boker = database['boker']

# hent inn API-nøkkel til Google Books
# denne filen skal kun inneholde nøkkelen
with open('api_key') as apifile:
	key = apifile.read().strip()

# sett opp Google-tjeneste for søking
service = build('books', 'v1', developerKey=key)

def sokISBN(isbn):
	request = service.volumes().list(q=('isbn:%s' % isbn))
	response = request.execute()

	try:
		return response['items'][0]['volumeInfo']
	except (NameError, KeyError, IndexError):
		return None


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

	def do_fjern(self, args):
		s = raw_input("Scan ISBN: ")

		res = boker.find({"industryIdentifiers.identifier": s})

		if res.count() == 0:
			print "Fant ikke boka!"
			return

		for x in res:
			boker.remove(x['_id'])

		print "Boka ble fjernet"


	def do_EOF(self, args):
		print
		return -1

	def do_exit(self, args):
		return -1

	def do_registrer(self, args):
		registrer = Registrer()
		registrer.cmdloop()


class Registrer(cmd.Cmd):
	def __init__(self):
		cmd.Cmd.__init__(self)
		self.prompt = ": "
		self.intro = "Scan eller skriv inn ISBN-kode!"

	def do_exit(self, args):
		return -1

	def do_EOF(self, args):
		print
		return -1

	def default(self, line):
		print "Du søker etter: %s" % line

		obj = sokISBN(line)
		if not obj:
			print "Ingen treff ble funnet."
			return

		newobj = {}
		newobj['gdata'] = obj
		
		for x in ('title', 'subtitle', 'authors', 'publishedDate', 'description', 'industryIdentifiers', 'pageCount', 'categories'):
			if x in obj:
				newobj[x] = obj[x]

		print "Du er i ferd med å registrere følgende bok:"
		
		texts = OrderedDict([
			("title", "Tittel"),
			("subtitle", "Undertittel"),
			("authors", "Forfattere"),
			("publishedDate", "Publiseringsdato"),
			("description", "Beskrivelse"),
			("industryIdentifiers", "ISBN-kode(r)"),
			("pageCount", "Sideantall"),
			("categories", "Kategorier")])

		# list opp alle felter
		i = 1
		for key, value in texts.iteritems():
			if not key in newobj:
				v = "*Ingen verdi*"
			else:
				v = newobj[key]
				if key == "authors" or key == "categories":
					v = "\n  %s" % "\n  ".join([("* %s" % a) for a in v])
				if key == "industryIdentifiers":
					v = "\n  %s" % "\n  ".join([("* %s (%s)" % (a['identifier'], a['type'])) for a in v])
			print "[%d] %s: %s" % (i, value, v)
			i+=1

		# sjekk om boka allerede er registrert
		if "industryIdentifiers" in newobj:
			search = []
			for x in newobj['industryIdentifiers']:
				search.append({"industryIdentifiers.identifier": x['identifier']})
			q = {"$or": search}
			res = boker.find(q)
			if res.count() > 0:
				print "Vi har allerede en bok med samme ISBN!"
				s = raw_input('Ønsker du å fortsette? [J/n]: ')
				if not (s == "" or s == "j" or s == "J"):
					print "Avbryter.."
					return

		#id = 
		boker.insert(newobj)
		#elm = boker.find_one(id)

		print "Boka ble lagt til"
		return -1

if __name__ == "__main__":
	console = Console()
	console.cmdloop()