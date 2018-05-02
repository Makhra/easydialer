import xml.etree.ElementTree as ET

def chk_duplicate_guids(inputxml='dialer_config.xml'):
	tree = ET.parse(inputxml)
	root = tree.getroot()
	guids = []
	duplicates = []

	for elem in root.findall("./DIALEROBJECT"):
		if  elem.attrib['id'] in guids:
			print('Dup:' + elem.attrib['id'])
			duplicates.append(elem.attrib['id'])
		else:
			guids.append(elem.attrib['id'])
	return duplicates
	
def main():
	from . import getguid as GET
	
	duplicates = chk_duplicate_guids()
	for dup in duplicates:
			guid_list = GET.get_objects(dup, 'dialer_config.xml', 'id')
			GET.print_objects(guid_list)
	
if __name__ == '__main__':
	main()