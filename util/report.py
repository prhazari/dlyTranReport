###
# Author: Prasenjt
#
# Report functions.
###

import argparse
import csv
import os
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
def write_csv(headers, outdata, outfile):
    if headers is None \
        or outdata is None \
        or outfile is None:
        raise ValueError('One of the inputs argument is Null')
    try:
        with open(outfile, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=headers,
                    extrasaction='ignore')  # extrasaction='ignore' allows our row dictionaries to have additional keys which aren't specified in fieldnames= and hence not output into the CSV. Without this, DictWriter will complain about *extra* keys (why would they make that behaviour default??)
            csv_writer.writeheader()
            csv_writer.writerows(outdata)
    except Exception as e:
        raise e

def genDlyTransRep(inputfile, logging_cxt, outfile='Output.csv'):
    if inputfile is None \
        or outfile is None \
        or logging_cxt is None:
        raise ValueError('One of the inputs argument is Null')

    logging_cxt.debug('--> Checking if input file exists: %s' % inputfile)
    if not os.path.exists(inputfile):
        raise ValueError('Input file %s does not exists' % inputfile)
    logging_cxt.debug('--> Input file exists!!')

    logging_cxt.debug('--> Checking size of input file')
    if not os.path.getsize(inputfile):
        raise ValueError('Input file %s is empty' % inputfile)
    logging_cxt.debug('--> Input file is non-empty!!')

    logging_cxt.debug('--> Checking if outfile extension: : %s' % outfile)
    name, extension = os.path.splitext(outfile)
    if extension != '.csv':
        raise ValueError('Wrong output file extension: [%s]!! Expected .csv' % extension)
    logging_cxt.debug('--> Ok!!')

    outpath = os.path.dirname(outfile)
    if outpath.strip() != '' and outpath.strip() != './':
        logging_cxt.debug('--> Checking if outfile dir path exists: : %s' % outpath)
        if not os.path.exists(outpath):
            raise ValueError('Output file directory[%s] does not exists!!' % outpath)
        logging_cxt.debug('--> OK')

    try:
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

        logging_cxt.debug('--> Analyzing input file')
        df = pd.read_fwf(inputfile, colspecs=list(i_fields.values()),
                          names=list(i_fields.keys()),
                          converters={
                                        'CLIENT NUMBER': lambda x: str(x),
                                        'ACCOUNT NUMBER': lambda x: str(x),
                                        'STATION NAME': lambda x: str(x),
                                        'SUBACCOUNT NUMBER': lambda x: str(x),
                                        #remove trailing '.'
                                        'SYMBOL'           : lambda x: str(x).rstrip('.')
                                      }
                         )

        df['NET_QUANTITY'] = df['QUANTITY LONG'] - df['QUANTITY SHORT']

        #Apply Group by rule to sum-up unique transaction by per client per product.
        aggrObj = df.groupby(['CLIENT TYPE', 'CLIENT NUMBER', 'ACCOUNT NUMBER', 'SUBACCOUNT NUMBER','PRODUCT GROUP CODE', 'EXCHANGE CODE', 'SYMBOL', 'EXPIRATION DATE', 'TRANSACTION DATE'])['NET_QUANTITY'].sum()

        #reset index to get grouped columns back
        aggrObj = aggrObj.reset_index()


        #Covert dataframe to list of dictionary records
        records = aggrObj.to_dict('records')

        logging_cxt.debug('--> Building Transaction Data')
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

        logging_cxt.debug('--> Writing Transaction Data to csv report: %s', outfile)
        write_csv(csv_headers,total_transaction_data, outfile)
        logging_cxt.debug('--> Successfully wrote csv report!!')
        #import code;code.interact(local=locals())
        return True
    except Exception as e:
        raise e