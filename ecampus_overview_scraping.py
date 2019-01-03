# coding: utf-8


import requests
from bs4 import BeautifulSoup
import re
import logging
import sys
import os
import configparser

# logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fhandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)

# load config
config_login = configparser.ConfigParser()
config_login.read('config/login_data.ini')

config_urls = configparser.ConfigParser()
config_urls.read('config/links.ini')

# Ecampus login
base_url = config_urls['ecampus']['base_url']
action = config_urls['ecampus']['action']
login_url = base_url + action

login_data = {'username': config_login['ecampus']['username'],
              'password': config_login['ecampus']['password']}

with requests.Session() as session:
    post = session.post(login_url, data=login_data)

if 'Cookie authchallenge' not in str(session.cookies): # check if login was successful
    logger.error(("""Login failed for url: "{link}" """).format(link=login_url))
    logger.error("Check your login-specification")
    sys.exit()


def save_file_from_url(url, file_path):
    """ Download url's content, and save it into the specified directory """
    if 'https' not in url:  # check url is valid
        logger.warning('Not a valid link: {link}'.format(link=url))
    else:
        # create directory if not already there
        if file_path:
            if not os.path.exists(file_path):
                os.makedirs(file_path)

        response_pdf = session.get(url)
        content_disposition = response_pdf.headers.get('content-disposition')
        if content_disposition:
            file_names = re.findall('filename="(.+)"', content_disposition)  # get file names from response content
            for file in file_names:
                if not os.path.exists(file_path + '/' + file):
                    # save file in the respective folder
                    with open(file_path + '/' + file, 'wb') as pdf_file:
                        logger.info('Save file "{file}" to {directory}'.format(file=file,
                                                                               directory=file_path))
                        pdf_file.write(response_pdf.content)
                        pdf_file.close()


def recursive_ecampus_scraping(url, directory=[]):
    """ Walk recursively through each folder-element from the overview, and extract its embedded links to the files"""
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')  # parse html
    a_s = soup.select('h4 > a')  # selects all elements "a" which are directly within an element "h4"
    for a in a_s:
        a_attributes = a.attrs
        if 'target' in a_attributes:  # indicates that html-element is a button for either folder or file
            if 'top' in a_attributes['target']:  # indicates that it is a folder
                temp_direc = '/'.join(directory).strip()  # current directory as string
                logger.info('Go into folder {folder}: {link}'.format(folder='/'.join(directory + [a.getText()]).strip(),
                                                                     link=url))
                save_file_from_url(a.get('href'), temp_direc)  # creates directory
                # start recursion with the folder-element's link and the updated directory
                recursive_ecampus_scraping(a.get('href'), directory + [a.getText()])

            elif 'blank' in a_attributes['target']:  # indicates that it is a file
                temp_direc = '/'.join(directory).strip()
                file_name = a.getText().strip()
                logger.info('Download "{file}" from {folder}: {link}'.format(file=file_name,
                                                                             folder=temp_direc,
                                                                             link=a.get('href')))
                save_file_from_url(a.get('href'), temp_direc)


recursive_ecampus_scraping(config_urls['ecampus']['overview_url'])
