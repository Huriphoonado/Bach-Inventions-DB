# Willie Payne
# Will Eventually parse a music.xml file
# Bach MIDI Files grabbed from: http://www.bachcentral.com/midiindexcomplete.html

import xml.etree.ElementTree as ET
import sqlite3 as lite
import sys
import time

DATABASE = '/tmp/invention.db'
con = lite.connect(DATABASE)

class BachInvention:
	def __init__(self, number, book, key):
		self.number = number
		self.book = book
		self.key = key
		self.parts = []

class Part:
	def __init__(self, partID):
		self.partID = partID
		self.measures = []

class Measure:
	def __init__(self, number, timeSig):
		self.number = number
		self.timeSig = timeSig
		self.notes = []

class Note:
	def __init__(self, position, duration, pitch, octave):
		self.position = position
		self.duration = duration
		self.pitch = pitch
		self.octave = octave

def parseXML(root, number, book, key):
	newInvention = BachInvention(number, book, key)
	# Determine the number of divisions in the musicXML File
	# 	Essentially the size of a quarter note
	# 	Should not change within a single score, but may differ across scores
	# for attributes in root.iter('attributes'):
		# divisions = attributes.find('divisions').text

	# Iterate through each part
	for part in root.findall('part'):
		partID = part.get('id')
		newPart = Part(part.get('id'))
		
		# Iterate through each measure and get a measure number
		for measure in part.findall('measure'):
			measureNumber = measure.get('number')

			# Iterate through all the measure's attributes
			for attributes in measure.iter('attributes'):
				

				# Get time signature - may not actually change
				for time in attributes.findall('time'):
					beats = time.find('beats').text
					beatType = time.find('beat-type').text
					timeSig = "%s/%s" % (beats, beatType)

			# May use to get note's exact position
			#measureLength = int(divisions) * int(beats)

			newMeasure = Measure(measureNumber, timeSig)
			
			# Get the notes in the measure
			noteNumber = 1
			for note in measure.findall('note'):
				duration = note.find('type').text # eg "whole"
				position = noteNumber

				# Check if note or rest
				if note.find('pitch') != None:
					# Get the note's pitch
					pitch = note.find('pitch')
					# Check if we are at a rest or a note
					step = pitch.find('step').text
					octave = int(pitch.find('octave').text)
					# Alter tag may or may not exist
					if pitch.find('alter') != None:
						alter = pitch.find('alter').text
					else:
						alter = "0"	
					stepWithAlter = step + alter
				else:
					stepWithAlter = 'Rest'
					octave = None
				
				newNote = Note(position, duration, stepWithAlter, octave)	
				newMeasure.notes.append(newNote) 
				
				noteNumber = noteNumber + 1

			newPart.measures.append(newMeasure)

		newInvention.parts.append(newPart)
	
	return newInvention

# Simply clears and remakes all of the tables in the Invention Database
def createDatabase():
	with con:
		cur = con.cursor()
		cur.executescript(open("schema.sql", "r").read())

def populateDatabase(invention):
	with con:
		cur = con.cursor()
		iNum = invention.number
		iBook = invention.book
		
		# Insert Invention
		cur.execute("INSERT INTO invention Values(?, ?, ?)", (iNum, iBook, invention.key))

		# Insert Parts
		for p in invention.parts:
			cur.execute("INSERT INTO part Values(?, ?, ?)", (iNum, iBook, p.partID))

			# Insert Measures
			for m in p.measures:
				cur.execute("INSERT INTO measure Values(?, ?, ?, ?, ?)", (iNum, iBook, p.partID, m.number, m.timeSig))

				# Insert Notes
				for n in m.notes:
					cur.execute("INSERT INTO note Values(?, ?, ?, ?, ?, ?, ?, ?)", (iNum, iBook, p.partID, m.number, n.position, n.duration, n.pitch, n.octave))

def checkDatabase():
	with con:
		cur = con.cursor()
		cur.execute("SELECT COUNT(*) FROM invention")
		inventionCount = cur.fetchall()
		cur.execute("SELECT COUNT(*) FROM note")
		noteCount = cur.fetchall()

		print "Database Connection Succesful: There are %i notes in %i Bach Invention(s)." % (noteCount[0][0], inventionCount[0][0])

def main():
	test = ET.parse('testMusic.xml').getroot()

	createDatabase()
	
	invention1 = ET.parse("musicXMLFiles/Bach Invention 1.xml").getroot()
	invention1 = parseXML(invention1, 1, 1, "C Major")
	populateDatabase(invention1)
	checkDatabase()

	invention2 = ET.parse("musicXMLFiles/Bach Invention 2.xml").getroot()
	invention2 = parseXML(invention2, 2, 1, "C Minor")
	populateDatabase(invention2)
	checkDatabase()

if __name__ == '__main__':
	main()