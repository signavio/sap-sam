import os
import glob
import logging
import re
import json
import time
import ast
import shutil

import pandas as pd

from typing import List
from zipfile import ZipFile
from pathlib import Path
from tqdm import tqdm

from sapsam.constants import *

_logger = logging.getLogger(__name__)

def extract_zip_file(path):
    with ZipFile(path, 'r') as zObject:

        # Extracting all the members of the zip 
        # into a specific location.
        zObject.extractall(path=path[:path.rfind("/")]+"/ExtractedSGXExport")

def get_directory_paths(directory_path) -> List[Path]:
    paths = glob.glob(directory_path + "/*")
    assert len(paths) > 0, f"Could not find any file in {Path(directory_path).absolute()} !"
    _logger.info("Found %d files", len(paths))
    return paths

def return_json_value_paths(file_path):
    jsonPath = re.search("_.json$", file_path)
    if jsonPath != None:
        return file_path
    else:
        return False

def return_json_metadata_paths(file_path):
    jsonPath = re.search("model_meta.json$", file_path)
    if jsonPath != None:
        return file_path
    else:
        return False

def return_directory_paths(file_path):
    if os.path.isdir(file_path):
        return file_path
    else:
        return False

def recursivly_fetch_json_paths(path):
    paths=get_directory_paths(path)
    
    # fetch all path which lead to a JSON value file
    json_value_paths = list(map(return_json_value_paths, paths))
    while False in json_value_paths:
        json_value_paths.remove(False)
        
    # fetch all paths which lead to JSON metadata file
    json_metadata_paths = list(map(return_json_metadata_paths, paths))
    while False in json_metadata_paths:
        json_metadata_paths.remove(False)
        
    # fetch all paths which lead to a directory
    directory_paths = list(map(return_directory_paths, paths))
    while False in directory_paths:
        directory_paths.remove(False)
        
    if(len(directory_paths)>0):
        for directory_path in directory_paths:
            json_value_paths.extend(recursivly_fetch_json_paths(directory_path)[0])
            json_metadata_paths.extend(recursivly_fetch_json_paths(directory_path)[1])
    return json_value_paths, json_metadata_paths

def convert_sgx_export(path):
    print("Extracting zip file from path "+str(path)+" ...")
    extract_zip_file(path)
    print("Zip extracted to path "+str(path[:path.rfind("/")]+"/ExtractedSGXExport"))
    
    print("Starting to get file paths...")
    all_json_value_paths, all_json_metadata_paths = recursivly_fetch_json_paths(str(path[:path.rfind("/")]+"/ExtractedSGXExport"))
    print("Found "+str(len(all_json_value_paths))+" json model files and "+str(len(all_json_metadata_paths))+" json metadata files. Loading data...")
    
    model_json_df=pd.DataFrame(columns = ['Revision ID', 'Model ID', 'Organisation ID', 'Datetime', 'Model JSON', 'Description', 'Name', 'Type', 'Namespace'])													
    for iloc in tqdm(range(0, len(all_json_value_paths))):
        json_value_file = open(all_json_value_paths[iloc])
        json_metadata_file = open(all_json_metadata_paths[iloc])

        # returns JSON object as a dictionary
        data = json.load(json_value_file)
        metadata = json.load(json_metadata_file)

        if 'type' in metadata:
            modelType=metadata['type']
        else:
            modelType=""

        model_json_df = pd.concat([model_json_df, pd.DataFrame({'Model ID': [all_json_metadata_paths[iloc][all_json_metadata_paths[iloc].find("model_")+6:all_json_metadata_paths[iloc].find("model_meta.json")-1]],
                                                                'Datetime': metadata['creationDate'],
                                                                'Model JSON': json.dumps(data),
                                                                'Name': metadata['name'],
                                                                'Type': modelType,
                                                                'Namespace': metadata['namespace']})], axis=0)
    return model_json_df.reset_index(drop=True)

def convert_sgx_to_csv():
    #directory_path = './../data/raw/sap_sam_2022/models/OPAL'
    sgx_files = [filename for filename in os.listdir(DATA_DATASET) if filename.endswith('.sgx')]
    csv_files = [filename for filename in os.listdir(DATA_DATASET) if filename.endswith('.csv')]
    zip_exports_path = DATA_DATASET / "zip_exports"
    
    print(f'Found {len(sgx_files)} SGX files.')
    if len(sgx_files) == 0 and len(csv_files) == 0:
        print('Found 0 SGX files and 0 CSV files. Did you import the data?')
        return
    elif len(sgx_files) == 0 and len(csv_files) > 0:
        print(f'Found {len(csv_files)} CSV files. Proceeding with analysis...')
        return
    else:
        print('Starting conversion...\n')
    
    for i, sgx_file in enumerate(sgx_files):
        zip_file = sgx_file.replace('.sgx', '.zip')
        #shutil.move(os.path.join('./../data/raw/sap_sam_2022/models/OPAL/', sgx_file), os.path.join('./../data/raw/sap_sam_2022/models/OPAL/', zip_file))
        shutil.move(DATA_DATASET / sgx_file, DATA_DATASET / zip_file)
        exported_file_name = DATA_DATASET / "{:04d}.csv".format(i)

        model_json_df = convert_sgx_export(str(DATA_DATASET / zip_file))
        model_json_df.to_csv(exported_file_name, sep=",", index=False)

        if os.path.exists(DATA_DATASET / "ExtractedSGXExport"):
            shutil.rmtree(DATA_DATASET / "ExtractedSGXExport")
        if not os.path.exists(zip_exports_path):
            os.makedirs(zip_exports_path, exist_ok=True)
        shutil.move(DATA_DATASET / zip_file, zip_exports_path / zip_file)
        print('\033[92m\u2713\033[0m Conversion successful\n')
    
    print('All SGX archives succesfully converted.')
