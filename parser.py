# Willie Payne
# Will Eventually parse a music.xml file
# Bach MIDI Files grabbed from: http://www.bachcentral.com/midiindexcomplete.html

import xml.etree.ElementTree as ET

def parseXML(root):

	# Determine the number of divisions in the musicXML File
	# 	Essentially the size of a quarter note
	# 	Should not change within a single score, but may differ across scores
	for attributes in root.iter('attributes'):
		divisions = attributes.find('divisions').text

	# Iterate through each part
	for part in root.findall('part'):
		partID = part.get('id')
		
		# Iterate through each measure and get a measure number
		for measure in part.findall('measure'):
			measureNumber = measure.get('number')
			
			# Iterate through all the measure's attributes
			for attributes in measure.iter('attributes'):
				

				# Get time signature
				for time in attributes.findall('time'):
					beats = time.find('beats').text
					beatType = time.find('beat-type').text
					timeSig = "%s/%s" % (beats, beatType)

			# May use to get note's exact position
			measureLength = int(divisions) * int(beats)
			
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
					octave = 0
					
				#print position, duration, stepWithAlter, octave
				
				noteNumber = noteNumber + 1


			#print partID, measureNumber, timeSig, measureLength

def main():
	#tree = ET.parse('testMusic.xml')
	tree = ET.parse("musicXMLFiles/Bach Invention 1.xml")
	root = tree.getroot()
	parseXML(root)

if __name__ == '__main__':
	main()

