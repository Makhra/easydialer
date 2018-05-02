import xml.etree.ElementTree as ET
import argparse
from copy import deepcopy
from time import time

def fetch_elem(guid, input_file='dialer_config.xml'):
	tree = ET.parse(input_file)
	root = tree.getroot()
	elem = root.find('DIALEROBJECT[@id="{}"]'.format(guid))
	return elem

def generate_copies(elem, counter=2):
	copies = ET.Element('DIALEROBJECT')
	itemType = elem.attrib['type'].zfill(3)
	itemId = elem.attrib['id']
	i = 1
	while(i <= counter):
		element = randomize_attributes(elem, itemId, itemType, i)
		copies.append(element)
		i += 1
	print(copies)
	return copies

def randomize_attributes(elem, itemId, itemType, i):
		#ensures that guid and name will not be duplicates in the config file
		now = str(time()).replace('.', '').zfill(17)
		element = deepcopy(elem)
		
		#appending counter value to original name
		element.set('name', elem.attrib['name'] + '-' + format(i, '04d'))
		
		#formatting guid based on input object guid, current time, input object type and counter, in order to ensure it will remain unique
		element.set('id', itemId[0:9] + '-' + now[0:4] + '-' + now[4:8] + '-' + now[8:12] + '-' + now[12:16] + itemType + format(i, '04d') + '}')
		return element

def write_elem(elem):
	otree = ET.ElementTree(elem)
	o = open('sample_config.xml', 'wb')
	otree.write(o, encoding='UTF-8')
	o.close()

def main():
	parser = argparse.ArgumentParser(description='retrieves a list of guid/type of dialerobjects where name matches input string')
	parser.add_argument('guid', help='dialerobject guid to search')
	parser.add_argument('-i', '--input', default='dialer_config.xml', help='specify input xml config file location (default:.\\dialer_config.xml)')
	parser.add_argument('-n', '--num', default='2', help='amount of copies to generate')
	args = parser.parse_args()

	copy_target = fetch_elem(args.guid, args.input)
	copied_elem = generate_copies(copy_target, int(args.num))
	write_elem(copied_elem)

if __name__ == '__main__':
	main()