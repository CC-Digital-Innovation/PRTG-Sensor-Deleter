import csv
import io
import logging
import re
import sys
import urllib.parse
from datetime import datetime

import configparser
import requests
import pandas as pd


# Module information.
__author__ = 'Anthony Farina'
__copyright__ = 'Copyright 2021, PRTG Sensor Deleter'
__credits__ = ['Anthony Farina']
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = 'Anthony Farina'
__email__ = 'farinaanthony96@gmail.com'
__status__ = 'Released'


# Global variables from the config file for easy referencing.
CONFIG = configparser.ConfigParser()
CONFIG.read('../config.ini')
SERVER_URL = CONFIG['PRTG Info']['server-url']
USERNAME = urllib.parse.quote_plus(CONFIG['PRTG Info']['username'])
PASSWORD = urllib.parse.quote_plus(CONFIG['PRTG Info']['password'])
PASSHASH = urllib.parse.quote_plus(CONFIG['PRTG Info']['passhash'])


# This function will go into the provided PRTG instance and delete sensors
# by name. PRTG may need to be restarted once the script stops. It will log
# which sensors were deleted and when in a log file.
def prtg_sensor_deleter() -> None:
    # Make a logger that logs what's happening in a log file and the console.
    now_log = datetime.now()
    logging.basicConfig(filename='deletion_log-' + now_log.strftime(
        '%Y-%m-%d_%I-%M-%S-%p-%Z') + '.log', level=logging.INFO,
                        format='[%(asctime)s] [%(levelname)s] %(message)s',
                        datefmt='%m-%d-%Y %I:%M:%S %p %Z')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    # Prepare the PRTG API call URL that will get all the sensors.
    sensor_url = SERVER_URL + \
        '/api/table.xml?content=sensors' \
        '&output=csvtable&columns=probe,group,device,name,objid,' \
        'type&count=50000&username=' + USERNAME
    sensor_url = add_auth(sensor_url)

    # Get the sensor information from PRTG.
    logging.info('Retrieving all sensors from PRTG...')
    sensor_resp = requests.get(url=sensor_url)
    logging.info('All sensors retrieved from PRTG!')

    # Make a clean dataframe object from the sensor information received.
    logging.info('Formatting response from PRTG...')
    sensor_resp_csv_strio = io.StringIO(sensor_resp.text)
    sensor_resp_csv_df = pd.read_csv(sensor_resp_csv_strio)
    sensor_resp_csv_df = remove_raw(sensor_resp_csv_df)

    # Turn the CSV response dataframe into a CSV file.
    sensor_csv_file = sensor_resp_csv_df.to_csv(sep=',', index=False,
                                                encoding='utf-8')

    # Parse the CSV file as a dictionary.
    sensor_dict = csv.DictReader(sensor_csv_file)
    logging.info('Response from PRTG has been formatted!')

    # Count the number of successful and unsuccessful deletions.
    deletions = 0
    errors = 0

    # Iterate through all PRTG sensors and delete unwanted ones from PRTG.
    for sensor in sensor_dict:
        # Check if this sensor is unwanted.
        if sensor['Object'] == 'EXAMPLE_SENSOR_NAME':
            # Log and attempt to delete the sensor from PRTG.
            logging.info('Deleting sensor [' + sensor['ID'] + ']...')
            delete_url = SERVER_URL + \
                '/api/deleteobject.htm?id=' + sensor['ID'] + '&approve=1' \
                '&username=' + USERNAME
            delete_url = add_auth(delete_url)
            delete_resp = requests.get(delete_url)

            # Check if the deletion was successful.
            if delete_resp.status_code != 200:
                logging.error('Error deleting sensor -- [Probe: ' + sensor[
                    'Probe'] + '] [Group: ' + sensor['Group']
                              + '] [Device: ' + sensor['Device']
                              + '] [Sensor Name: ' + sensor['Object']
                              + '] [Sensor ID: ' + sensor['ID'] + '] -- ')
                logging.error('Caused by: ' + str(delete_resp.status_code))
                logging.error(delete_resp.reason)
                errors += 1
            # The deletion was successful.
            else:
                logging.info('Sensor -- [Probe: ' + sensor[
                    'Probe'] + '] [Group: ' + sensor['Group']
                             + '] [Device: ' + sensor['Device']
                             + '] [Sensor Name: ' + sensor['Object']
                             + '] [Sensor ID: ' + sensor['ID']
                             + '] -- was successfully deleted from PRTG!')
                deletions += 1

    logging.info('')
    logging.info('===========================================================')
    logging.info('')
    logging.info('Deletion job completed.')
    logging.info('Total sensor deletions: ' + str(deletions))
    logging.info('Total sensor deletion errors: ' + str(errors))


# Every time table information is called from the PRTG API, the response has
# 'readable' columns and 'raw' columns. Their are subtle differences,
# but the raw columns are not needed. This function removes all the 'raw'
# columns from a dataframe object of the PRTG API response and returns a
# dataframe object with only the non-raw columns.
def remove_raw(raw_df: pd.DataFrame) -> pd.DataFrame:
    # Prepare a list of desired column names.
    col_labels = list()

    # Iterate through the column labels to remove column labels ending with
    # '(RAW)'.
    for col in raw_df.columns:
        # Add only desired column labels to the list.
        if not bool(re.search('\\(RAW\\)$', col)):
            col_labels.append(col)

    # Return the dataframe object that only has desired columns.
    return_df = raw_df[col_labels]
    return return_df


# This function will append the PRTG authentication to the end of the given
# PRTG API call URL. It will append either the password or passhash,
# whichever was provided in the config file. Passhash has priority if both
# fields are filled in.
def add_auth(url: str) -> str:
    # Check if the password or passhash will be used to authenticate the
    # access to the PRTG instance.
    if PASSHASH == '':
        url = url + '&password=' + PASSWORD
    else:
        url = url + '&passhash=' + PASSHASH

    return url


# The main method that runs the script. There are no input arguments.
if __name__ == '__main__':
    # Run the script.
    prtg_sensor_deleter()
