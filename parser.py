# Willie Payne
# Will Eventually parse a music.xml file

import xml.etree.ElementTree as ET

def parseXML(root):
	# Iterate through each part
	for part in root.findall('part'):
		partID = part.get('id')
		
		# Iterate through each measure and get a measure number
		for measure in part.findall('measure'):
			measureNumber = measure.get('number')
			
			# Iterate through all of the measure's attributes
			for attributes in measure.iter('attributes'):
				

				# get time signature
				for time in attributes.findall('time'):
					beats = time.find('beats').text
					beatType = time.find('beat-type').text
					timeSig = "%s/%s" % (beats, beatType)
					
				#divisions = attributes.find('divisions').text
			
			# Get the notes in the measure
			for note in measure.findall('note'):
				duration = note.find('type').text


			print partID, measureNumber, timeSig

def main():
	tree = ET.parse('testMusic.xml')
	root = tree.getroot()
	parseXML(root)

if __name__ == '__main__':
	main()

