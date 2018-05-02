# Input item name, outputs list of guid + type of item
import xml.etree.ElementTree as ET
import argparse
from copy import deepcopy

def get_objects(x, inputxml, attrib_type='name'):
	guid_list = []
	#Attempt iterparse method
	for event, elem in ET.iterparse(inputxml):
		try:
			if x in elem.attrib[attrib_type]:
				guid_list.append(deepcopy(elem))
		except:
			continue
		elem.clear()
	return guid_list

	#Working plain parse method
	#tree = ET.parse(inputxml)
	#for dialerobject in tree.iterfind('DIALEROBJECT[@name="{}"]'.format(x)):
	#	print('Name:' + dialerobject.attrib['name'] + '; Type:' + objectTypes[int(dialerobject.attrib['type'])] + '; GUID:' + dialerobject.attrib['id'])
	#	dialerobject.clear()

def print_objects(guid_list):
	objectTypes = {1:'Campaign', 2:'Workflows', 3:'Rule Sets', 4:'Stage Sets', 5:'Schedules', 6:'Servers', 7:'Zone Sets', 8:'Policy Sets', 9:'Filters', 10:'Connections', 11:'Manager', 12:'Skill Sets', 13:'Phone Number Types', 14:'Contact Column', 15:'Time Zone Map Data', 16:'DNC Sources', 17:'Scripts', 18:'Script Pages', 19:'Contact Lists'}	
	for elem in guid_list:
		name = elem.attrib['name'] if 'name' in elem.attrib else 'N/A'
		type = elem.attrib['type'] if 'type' in elem.attrib else 'N/A'
		guid = elem.attrib['id'] if 'id' in elem.attrib else 'N/A'
		print('Name:' + name + '; Type:' + objectTypes[int(elem.attrib['type'])] + '; GUID:' + elem.attrib['id'])

def main():
	parser = argparse.ArgumentParser(description='retrieves a list of guid/type of dialerobjects where name matches input string')
	parser.add_argument('name', help='dialerobject name to search')
	parser.add_argument('-i', '--input', default='dialer_config.xml', help='specify input xml config file location (default:.\\dialer_config.xml)')
	args = parser.parse_args()
	
	guid_list = get_objects(args.name,args.input)
	print_objects(guid_list)

if __name__ == '__main__':
	main()