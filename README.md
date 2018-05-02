# EasyDialer
Command line utility offering possibility to perform various operations on the Pureconnect Interaction Dialer configuration file


## Current available features:

#### GetGuid: Lists all dialer objects containing the passed name argument in its xml object name
```sh
EasyDialer {getguid,gg} [-h] [-i INPUT] name
  name				name of object to query  
  -h, --help			show help message and exit  
  -i INPUT, --input INPUT	specify input xml config file location (default:.\dialer_config.xml  
```

  
#### Extract: Extracts the dialer object related to the guid passed as argument to a new xml file
```sh
EasyDialer {extract,ex} [-h] [-v VERBOSITY] [-i INPUT] [-b] guid

  guid				guid of object to extract  
  -h, --help			show help message and exit  
  -v VERBOSITY, --verbosity VERBOSITY
  				determine amount of information to extract  
  -i INPUT, --input INPUT	specify input xml config file location (default:.\dialer_config.xml)  
```
  

#### Copy: Creates copies of the dialer object related to the guid passed as argument
```sh
EasyDialer {copy,cp} [-h] [-n NUM] [-i INPUT] guid
  guid				guid of object to duplicate  
  -h, --help			show help message and exit  
  -n NUM, --num NUM		amount of copies to generate  
  -i INPUT, --input INPUT	specify input xml config file location (default:.\dialer_config.xml)  
```
  

#### ChkDuplicates: Checks input file for dialer objects with duplicate guid
```sh
EasyDialer {chkduplicates,cd} [-h] [-i INPUT]
  -h, --help			show help message and exit  
  -i INPUT, --input INPUT	specify input xml config file location (default:.\dialer_config.xml)  
```
