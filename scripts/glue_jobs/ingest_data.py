# %%
import requests
from bs4 import BeautifulSoup
import boto3
import zipfile
import io
import logging
import gc
import pandas as pd

S3_BUCKET_NAME = 'factored-datathon-2024-voyager-temp'   
print(S3_BUCKET_NAME)
AWS_REGION = 'us-east-1'   
EVENTS_URL = "https://data.gdeltproject.org/events/index.html"
GKG_URL = "https://data.gdeltproject.org/gkg/index.html"
MINIMUM_DATE = 20240601# locally20240801#

logger = logging.getLogger('ingest_data')
logging.basicConfig( level=logging.INFO)


def get_file_list_from_url(url, filetype):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a_elements = soup.find_all('a')
        links = [a.get('href') for a in a_elements if a.get('href')]
        curated_links = [file for file in links if file.startswith('202')]
        filtered_by_date = [file for file in curated_links if int(file[0:8])>MINIMUM_DATE]
        if filetype == 'events':
            keyword = '.export.'
        elif filetype == 'gkg':
            keyword = '.gkg.csv'
        elif filetype == 'gkg_counts':
            keyword = '.gkgcounts.csv'
        else:
            raise Exception('wrong filetype')
        filter_by_filetype = [file for file in filtered_by_date if keyword in file]
        link_list = list(map(lambda x: url.replace('index.html','')+x, filter_by_filetype  ))
        gc.collect()
        return link_list

    else:
        logger.info(f"Error al obtener la página: {response.status_code}")

def get_ingested_files(filetype, current_list):
    if filetype=='events':
        folder_name = 'raw/events'
    elif filetype=='gkg_counts':
        folder_name = 'raw/gkg_counts'
        
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=folder_name)
    processed_files = pd.DataFrame(response['Contents'])
    processed_files['processed_date'] = processed_files['Key'].map(lambda x: x.split('/')[2].replace('year=','') + x.split('/')[3].replace('month=','')+ x.split('/')[4].replace('day=',''))
    
    files_to_download = pd.DataFrame(current_list,columns=['event_file_list'])
    files_to_download['files_to_download'] = files_to_download['event_file_list'].map(lambda x: x.split('/')[-1][0:8])
    missing_files = pd.merge(files_to_download, processed_files, left_on='files_to_download', right_on='processed_date', how='outer', indicator='missing')
    missing_files = list(missing_files.loc[missing_files['missing']=='left_only','event_file_list'])
    return missing_files


def download_unzip_save_file(file_url,filetype):
    file_response = requests.get(file_url, verify=False, stream=True)
    filename = file_url.split('/')[-1]
    logger.info(file_url)
    year = str(filename[0:4])
    month = str(filename[4:6])
    day = str(filename[6:8])
    file_response.raise_for_status() 
    file_content = file_response.content
    # filename = file_url.split('/')[-1]
    with zipfile.ZipFile(io.BytesIO(file_content)) as z:
        file_name_in_zip = z.namelist()[0]  
        logger.info(z.namelist()[0])
        logger.info(file_name_in_zip)
        with z.open(file_name_in_zip) as unzipped_file:
            # If we want to test Locally
            logger.info(file_name_in_zip)
            defined_key = f'raw/{filetype}/year={year}/month={month}/day={day}/{file_name_in_zip}'
            # session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
            s3 = boto3.client('s3', region_name=AWS_REGION)
            s3.upload_fileobj(Fileobj = unzipped_file, Bucket =S3_BUCKET_NAME, Key =defined_key)
    gc.collect()

def ingest_events(filetype='events'):
    try:
        all_files = get_file_list_from_url(EVENTS_URL, filetype)
        link_list = get_ingested_files(filetype,all_files)
        for file in link_list:
            download_unzip_save_file(file,filetype)
            gc.collect()
    except Exception:
        logger.info('Something Happened when ingest_events() executed')

def ingest_gkgs(filetype):
    try:
        all_files = get_file_list_from_url(GKG_URL,filetype)
        link_list = get_ingested_files(filetype,all_files)
        for file in link_list:
            download_unzip_save_file(file,filetype)
            gc.collect()
    except Exception:
        logger.info('Something Happened when ingest_events() executed')
    


ingest_events()
ingest_gkgs('gkg_counts')