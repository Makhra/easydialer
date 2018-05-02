# Extracts xml dialerobject content based on guid
import xml.etree.ElementTree as ET
import argparse
import xml.dom.minidom as MD

def extract_object(root, guid, verbosity=0):
	elem = root.find('DIALEROBJECT[@id="{}"]'.format(guid))
	if not elem:
		return None

	if elem.attrib['type'] == "1":
		
		#Create new tree, add Campaign item to it
		resultTree = ET.Element('DIALERCONFIG2')
		resultTree.append(elem)
		
		if 1 & verbosity: #if first bit is True, append calllist info
			#DB stuff: Contact list / Contact columns / DB connection
			#add ContactList item to new tree
			resultTree.append(extract_object(root, elem.find('./PROPERTIES/calllist').text))
			
			#add ContactColumns items to new tree
			for column in elem.find('./PROPERTIES/contactcolumns').text.split('|'):
				if column:
					resultTree.append(extract_object(root, column))
		
		if 2 & verbosity: #if second bit is True, append Contact Dialing info
			#Contact dialing: policies / filters / contact filters / DNC / skill set / Timezone
			
			#add Policies to tree
			policyset = extract_object(root, elem.find('./PROPERTIES/policysetids').text)
			if policyset:
				for policy in policyset.split('|'):
					if policy:
						resultTree.append(extract_object(root, policy))
			
		if 4 & verbosity: #if third bit is True, append Campaign/Agents events info
			#Campaign/agent events: Schedule / Rule
			
			#add RuleSet to tree
			ruleset = extract_object(root, elem.find('./PROPERTIES/rulesetid').text)
			if ruleset:
				resultTree.append(ruleset)
				
		if 8 & verbosity: #if fourth bit is True, append Script info
			#Script stuff: Scripts / script pages / stages
			
			#add base script if it exist, alongside each related script pages
			basescript = extract_object(root, elem.find('./PROPERTIES/basescript').text)
			if basescript:
				#discard wrapper element, import items
				for item in basescript:
					resultTree.append(item)

		
		return resultTree
		
	elif elem.attrib['type'] == "17":
		#Add script to wrapper element
		resultTree = ET.Element('DIALERCONFIG2')
		resultTree.append(elem)
		
		#Add each script page to wrapper element
		for page in elem.find('./PROPERTIES/scriptpages').text.split('|'):
			if page:
				resultTree.append(extract_object(root, page))
		return resultTree
		
	else:
		return elem


def main():
	parser = argparse.ArgumentParser(description='extracts xml dialerobject content based on guid')
	parser.add_argument('guid', help='dialerobject guid to search')
	parser.add_argument('-v', '--verbosity', default='0', help='determine amount of information to extract')
	parser.add_argument('-i', '--input', default='dialer_config.xml', help='specify input xml config file location (default:.\\dialer_config.xml)')
	parser.add_argument('-b', '--beautify', action='store_true', help='setting this flag will indent the output xml file - does not work with japanese yet')
	
	args = parser.parse_args()
	
	tree = ET.parse(args.input)
	root = tree.getroot()
	result = extract_object(root, args.guid,int(args.verbosity))
	
	for item in result:
		print(item.get('name'))

	otree = ET.ElementTree(result)
	o = open('sample_config.xml', 'wb')
	otree.write(o, encoding='UTF-8')
	o.close()

if __name__ == '__main__':
	main()