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

	invention3 = ET.parse("musicXMLFiles/Bach Invention 3.xml").getroot()
	invention3 = parseXML(invention3, 3, 1, "D Major")
	populateDatabase(invention3)
	checkDatabase()

	invention4 = ET.parse("musicXMLFiles/Bach Invention 4.xml").getroot()
	invention4 = parseXML(invention4, 4, 1, "D Minor")
	populateDatabase(invention4)
	checkDatabase()

	invention5 = ET.parse("musicXMLFiles/Bach Invention 5.xml").getroot()
	invention5 = parseXML(invention5, 5, 1, "Eb Major")
	populateDatabase(invention5)
	checkDatabase()

	invention6 = ET.parse("musicXMLFiles/Bach Invention 6.xml").getroot()
	invention6 = parseXML(invention6, 6, 1, "E Major")
	populateDatabase(invention6)
	checkDatabase()

	invention7 = ET.parse("musicXMLFiles/Bach Invention 7.xml").getroot()
	invention7 = parseXML(invention7, 7, 1, "E Minor")
	populateDatabase(invention7)
	checkDatabase()

	invention8 = ET.parse("musicXMLFiles/Bach Invention 8.xml").getroot()
	invention8 = parseXML(invention8, 8, 1, "F Major")
	populateDatabase(invention8)
	checkDatabase()

	invention9 = ET.parse("musicXMLFiles/Bach Invention 9.xml").getroot()
	invention9 = parseXML(invention9, 9, 1, "F Minor")
	populateDatabase(invention9)
	checkDatabase()

	invention10 = ET.parse("musicXMLFiles/Bach Invention 10.xml").getroot()
	invention10 = parseXML(invention10, 10, 1, "G Major")
	populateDatabase(invention10)
	checkDatabase()

	invention11 = ET.parse("musicXMLFiles/Bach Invention 11.xml").getroot()
	invention11 = parseXML(invention11, 11, 1, "G Minor")
	populateDatabase(invention11)
	checkDatabase()

	invention12 = ET.parse("musicXMLFiles/Bach Invention 12.xml").getroot()
	invention12 = parseXML(invention12, 12, 1, "A Major")
	populateDatabase(invention12)
	checkDatabase()

	invention13 = ET.parse("musicXMLFiles/Bach Invention 13.xml").getroot()
	invention13 = parseXML(invention13, 13, 1, "A Minor")
	populateDatabase(invention13)
	checkDatabase()

	invention14 = ET.parse("musicXMLFiles/Bach Invention 14.xml").getroot()
	invention14 = parseXML(invention14, 14, 1, "Bb Major")
	populateDatabase(invention14)
	checkDatabase()

	invention15 = ET.parse("musicXMLFiles/Bach Invention 15.xml").getroot()
	invention15 = parseXML(invention15, 15, 1, "B Minor")
	populateDatabase(invention15)
	checkDatabase()

if __name__ == '__main__':
	main()