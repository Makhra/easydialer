#find orphaned contact column
#fix orphaned contact column?
import xml.etree.ElementTree as ET

def find_orphaned_CC(inputxml='crash_dialer_config.xml'):
	tree = ET.parse(inputxml)
	root = tree.getroot()
	assigned_columns = []
	defined_ContactColumns = []
	missing_ContactColumn = []
	CC_list = root.findall('./DIALEROBJECT[@type="14"]')
	for CC in CC_list:
		for column in CC_list:
			if column and column not in defined_ContactColumns:
				defined_ContactColumns.append(column)
		
	
			
	#returns list of unique missing contact column
	#for campaign in tree.iterfind('DIALEROBJECT[@type="1"]'):
	#	for column in campaign.find('./PROPERTIES/contactcolumns').text.split('|'):
	#		if column and column not in defined_ContactColumns and column not in missing_ContactColumn:
	#			missing_ContactColumn.append(column)
	
	#returns list of campaign alongside assigned contact column which does not exist as type="14" object
	for campaign in tree.iterfind('DIALEROBJECT[@type="1"]'):
		problem_ContactColumn = []
		for column in campaign.find('./PROPERTIES/contactcolumns').text.split('|'):
			if column and column not in defined_ContactColumns:
				problem_ContactColumn.append(column)
		if len(problem_ContactColumn) > 0:
			missing_ContactColumn.append([campaign.attrib['id'], problem_ContactColumn])
	print(len(defined_ContactColumns))
	for item in missing_ContactColumn:
		print(item[0] + ': ' + str(item[1]))
	#print(missing_ContactColumn)

def main():
	find_orphaned_CC()

if __name__ == '__main__':
	main()