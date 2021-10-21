Description:
------------
This python script allows a business user to provide the a fixed width text transaction file and generate a daily summary report
User could change the location and name of the output.
By default is Output.csv generated in the same location as the script.

The Daily summary report has the following specifications:
The CSV has the following Headers
- Client_Information
- Product_Information
- Total_Transaction_Amount

Client_Information will contain concatenated string of CLIENT TYPE, CLIENT NUMBER, ACCOUNT NUMBER, SUBACCOUNT NUMBER fields from Input file
Product_Information will contain concatenated string of EXCHANGE CODE, PRODUCT GROUP CODE, SYMBOL, EXPIRATION DATE
Total_Transaction_Amount will be a Net Total of the (QUANTITY LONG - QUANTITY SHORT) values for each client per product

Preqrequiste:
-------------
This program runs on python 3.6 and above. It uses pandas package to do run analytics.
Ensure panda is 1.1.5 or above. 

Syntax and Usage:
-----------------
$python3 main.py -i Input.txt -o Output.csv 
For verbose logs provide -d or --debug option

More Details:
$ python3 main.py --help
usage: main.py [-h] [-d] [-i INPUT] [-o OUTPUT]

Creates daily Summary Report.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Enable debug logging
  -i INPUT, --input INPUT
                        Fixed width text file containing future transactions.
  -o OUTPUT, --output OUTPUT
                        Output csv report filename. Default name is Output.csv

Logging:
--------
Log file could be found in log/run.log
Sample log for successfull run

$ python3 main.py -i Input.txt -o Output.csv -d
Enabling debug logging
$ cat log/run.log 
 [2021-10-21 14:41:15,744][INFO] Start of Script execution....
 [2021-10-21 14:41:15,747][DEBUG] --> Checking if input file exists: Input.txt
 [2021-10-21 14:41:15,748][DEBUG] --> Input file exists!!
 [2021-10-21 14:41:15,748][DEBUG] --> Checking size of input file
 [2021-10-21 14:41:15,748][DEBUG] --> Input file is non-empty!!
 [2021-10-21 14:41:15,748][DEBUG] --> Checking if outfile extension: : Output.csv
 [2021-10-21 14:41:15,748][DEBUG] --> Ok!!
 [2021-10-21 14:41:15,748][DEBUG] --> Analyzing input file
 [2021-10-21 14:41:15,841][DEBUG] --> Building Transaction Data
 [2021-10-21 14:41:15,841][DEBUG] --> Writing Transaction Data to csv report: Output.csv
 [2021-10-21 14:41:15,842][DEBUG] --> Successfully wrote csv report!!
 [2021-10-21 14:41:15,842][INFO] End of Script execution....
 
 Unit-Testing:
 --------------
 To run unit test:
 python3 -m unittest unit-test/test_report.py
 note: Ensure unittest and other dependent package are installed  
 Sample run -->
 $ python3 -m unittest unit-test/test_report.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.046s

OK
