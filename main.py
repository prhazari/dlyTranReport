#!/usr/bin/env python
###
# Problem Statement:
# System A has produced the file Input.txt, which is a Fixed Width text file that contains
# the Future Transactions done by client 1234 and 4321.
#
# Requirements:
# The Business user would like to see the Total Transaction Amount of each unique product they have done for the day
# The Business user would like a program that can read in the Input file and generate a daily summary report
# The Daily summary report should be in CSV format (called Output.csv) with the following specifications
#
# The CSV has the following Headers
# - Client_Information
# - Product_Information
# - Total_Transaction_Amount
#
# Client_Information should be a combination of the CLIENT TYPE, CLIENT NUMBER, ACCOUNT NUMBER, SUBACCOUNT NUMBER
# fields from Input file Product_Information should be a combination of the EXCHANGE CODE, PRODUCT GROUP CODE, SYMBOL,
# EXPIRATION DATE Total_Transaction_Amount should be a Net Total of the (QUANTITY LONG - QUANTITY SHORT) values
# for each client per product
#
# Code Author: Prasenjit Hazarika
###

import sys
if sys.version_info < (3,6):
    sys.exit('Sorry, Python < 3.6 is not supported')

import logging
import os
import traceback
import argparse
import csv
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(
            description="""
                Creates daily Summary Report.
                """,
            epilog="""
                Author: Prasenjit Hazarika
                """
            )
    # General arguments
    parser.add_argument('-d', '--debug', action='store_true',
            help='Enable debug logging')
    parser.add_argument('-i', '--input', default='Input.txt',
            help='Fixed width text file containing future transactions.')
    parser.add_argument('-o', '--output', default='Output.csv',
            help='Output csv report filename. Default name is Output.csv')
    # parse arguments and return results
    return parser.parse_args()

####################################################
### Routine to write the report in csv file      ###
####################################################
def write_csv(headers, total_transaction_data, outfile):
    with open(outfile, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers,
                extrasaction='ignore')  # extrasaction='ignore' allows our row dictionaries to have additional keys which aren't specified in fieldnames= and hence not output into the CSV. Without this, DictWriter will complain about *extra* keys (why would they make that behaviour default??)
        csv_writer.writeheader()
        csv_writer.writerows(total_transaction_data)

### Main ###
try:
    # Logging Configuration
    logging.basicConfig(filename='log/run.log',
                        format=' [%(asctime)s][%(levelname)s] %(message)s',
                        level=logging.INFO)

    logging.info("Start of Script execution....")

    logging.debug("--> Parsing input arguments.")
    # Configure using passed options
    args = parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)  # show logging for >= DEBUG level
        print('Enabling debug logging')

    logging.debug('--> Checking if input file exists: %s' % args.input)
    if not os.path.exists(args.input):
        raise Exception('Input file %s does not exists' % args.input)
    logging.debug('--> Input file exists!!')

    logging.debug('--> Checking size of input file')
    if not os.path.getsize(args.input):
        raise Exception('Input file %s is empty' % args.input)
    logging.debug('--> Input file is non-empty!!')

    logging.debug('--> Checking if outfile extension: : %s' % args.output)
    name, extension = os.path.splitext(args.output)
    if extension != '.csv':
        raise Exception('Wrong output file extension: [%s]!! Expected .csv' % extension)
    logging.debug('--> Ok!!')

    outpath = os.path.dirname(args.output)
    if outpath.strip() != '' and outpath.strip() != './':
        logging.debug('--> Checking if outfile dir path exists: : %s' % outpath)
        if not os.path.exists(outpath):
            raise Exception('Output file directory[%s] does not exists!!' % outpath)
        logging.debug('--> OK')

    i_fields = {
                    'CLIENT TYPE'      :  (3, 7),
                    'CLIENT NUMBER'     : (7, 11),
                    'ACCOUNT NUMBER'    : (11, 15),
                    'SUBACCOUNT NUMBER' : (15, 19),
                    'PRODUCT GROUP CODE': (25, 27),
                    'EXCHANGE CODE'     : (27, 31),
                    'SYMBOL'            : (31, 37),
                    'EXPIRATION DATE'   : (37, 45),
                    'QUANTITY LONG'     : (52, 62),
                    'QUANTITY SHORT'    : (63, 73),
                    'TRANSACTION DATE'  : (121, 129),
    }

    logging.debug('--> Analyzing input file')
    df = pd.read_fwf(args.input, colspecs=list(i_fields.values()),
                      names=list(i_fields.keys()),
                      converters={
                                    'CLIENT NUMBER': lambda x: str(x),
                                    'ACCOUNT NUMBER': lambda x: str(x),
                                    'STATION NAME': lambda x: str(x),
                                    'SUBACCOUNT NUMBER': lambda x: str(x)
                                  }
                     )

    df['NET_QUANTITY'] = df['QUANTITY LONG'] - df['QUANTITY SHORT']

    #Apply Group by rule to sum-up unique transaction by per client per product.
    aggrObj = df.groupby(['CLIENT TYPE', 'CLIENT NUMBER', 'ACCOUNT NUMBER', 'SUBACCOUNT NUMBER','PRODUCT GROUP CODE', 'EXCHANGE CODE', 'SYMBOL', 'EXPIRATION DATE', 'TRANSACTION DATE'])['NET_QUANTITY'].sum()

    #reset index to get grouped columns back
    aggrObj = aggrObj.reset_index()


    #Covert dataframe to list of dictionary records
    records = aggrObj.to_dict('records')

    logging.debug('--> Building Transaction Data')
    total_transaction_data = []
    for entry in records:
        client_info = "{0}:{1}:{2}:{3}".format(entry['CLIENT TYPE'], entry['CLIENT NUMBER'],
                                               entry['ACCOUNT NUMBER'], entry['SUBACCOUNT NUMBER'])
        product_info = "{0}:{1}:{2}:{3}".format(entry['PRODUCT GROUP CODE'], entry['EXCHANGE CODE'],
                                                entry['SYMBOL'], entry['EXPIRATION DATE'])
        total_transaction_data.append({
            "Client_Information": client_info,
            "Product_Information": product_info,
            "Total_Transaction_Amount": entry['NET_QUANTITY']})

    csv_headers = ['Client_Information', 'Product_Information', 'Total_Transaction_Amount']

    logging.debug('--> Writing Transaction Data to csv report: %s', args.output)
    write_csv(csv_headers,total_transaction_data, args.output)
    logging.debug('--> Successfully wrote csv report!!')
    #import code;code.interact(local=locals())
except Exception as e:
    PROBLEM_STR = str(e)
    logging.exception('***: {0}'.format(PROBLEM_STR))
    print('*** ERROR: {0}'.format(PROBLEM_STR))
    traceback.print_exc()
finally:
    logging.info("End of Script execution....")