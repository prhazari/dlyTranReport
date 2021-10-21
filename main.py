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
import traceback
from util.report import genDlyTransRep, parse_args

### Main ###
if __name__ == '__main__':
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
            print('Debug logging Enabled')

        genDlyTransRep(args.input, logging, args.output)
    except Exception as e:
        PROBLEM_STR = str(e)
        logging.exception('***: {0}'.format(PROBLEM_STR))
        print('*** ERROR: {0}'.format(PROBLEM_STR))
        traceback.print_exc()
    finally:
        logging.info("End of Script execution....")