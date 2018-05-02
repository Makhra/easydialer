import xml.etree.ElementTree as ET
import argparse
from . import getguid as GET
from . import extractobject as EXT
from . import copyobject as COP
from . import checkduplicates as DUP

def indent(elem, level=0):
	i = "\n" + level*"\t"
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "\t"
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i

def list_guids(args):
	guid_list = GET.get_objects(args.name,args.input)
	GET.print_objects(guid_list)

def extract_diaobj(args):
	tree = ET.parse(args.input)
	root = tree.getroot()
	extracted_elem = EXT.extract_object(root, args.guid, int(args.verbosity))
	
	for item in extracted_elem:
		print(item.get('name'))
	indent(extracted_elem)
	COP.write_elem(extracted_elem)

def copy_diaobj(args):
	copy_target = COP.fetch_elem(args.guid, args.input)
	copied_elem = COP.generate_copies(copy_target, args.num)
	COP.write_elem(copied_elem)
	
def chk_dup(args):
	duplicates = DUP.chk_duplicate_guids(args.input)
	
	for dup in duplicates:
		guid_list = GET.get_objects(dup, 'dialer_config.xml', 'id')
		GET.print_objects(guid_list)
	
def main():
	parser = argparse.ArgumentParser(description='performs various actions (extract/duplicate dialerobjects, health-check...) on the Pureconnect Interaction Dialer configuration file',  prog='EasyDialer')
	subparsers = parser.add_subparsers(help='Features:')
	
	#arguments related to the GetGuid command
	parser_getguid = subparsers.add_parser('getguid', aliases=['gg'], description='GetGuid: Lists all dialer objects containing the passed argument in its name', help='lists all dialer objects containing the name argument in its name')
	parser_getguid.add_argument('name', help='dialerobject name to search')
	parser_getguid.add_argument('-i', '--input', default='dialer_config.xml', help='specify input xml config file location (default:.\\dialer_config.xml)')
	parser_getguid.set_defaults(func=list_guids)
	
	#arguments related to the ExtractObject command
	parser_extractobject = subparsers.add_parser('extract', aliases=['ex'], description='ExtractObject: Extracts the dialer object related to the guid passed as argument to a new xml file', help='extracts dialer object and relevant children based on guid argument')
	parser_extractobject.add_argument('guid', help='guid to extract')
	parser_extractobject.add_argument('-v', '--verbosity', default='1', type=int, help='determine amount of information to extract')
	parser_extractobject.add_argument('-i', '--input', default='dialer_config.xml', help='specify input xml config file location (default:.\\dialer_config.xml)')
	parser_extractobject.add_argument('-b', '--beautify', action='store_true', help='setting this flag will indent the output xml file - does not work with japanese yet')
	parser_extractobject.set_defaults(func=extract_diaobj)
	
	#arguments related to the CopyObject command
	parser_copyobject = subparsers.add_parser('copy', aliases=['cp'], description='CopyObject: Creates copies of the dialer object related to the guid passed as argument',  help='copies dialer object based on guid argument')
	parser_copyobject.add_argument('guid', help='guid to extract')
	parser_copyobject.add_argument('-n', '--num', default='2', type=int, help='amount of copies to generate')
	parser_copyobject.add_argument('-i', '--input', default='dialer_config.xml', help='specify input xml config file location (default:.\\dialer_config.xml)')
	parser_copyobject.set_defaults(func=copy_diaobj)
	
	parser_chkduplicates = subparsers.add_parser('chkduplicates', aliases=['cd'], description='CheckDuplicates: check input file for dialer objects with duplicate guid', help='check input file for dialer objects with duplicate guid')
	parser_chkduplicates.add_argument('-i', '--input', default='dialer_config.xml', help='specify input xml config file location (default:.\\dialer_config.xml)')
	parser_chkduplicates.set_defaults(func=chk_dup)
	
	args = parser.parse_args()
	args.func(args)

if __name__ == '__main__':
	main()