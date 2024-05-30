import os
import logging
import time

image_directory = '//TRUENAS/public/Documents/Kelsea Science Data/ARC'

subject_prefix = '60'
subject_regions = ['NAcc','NAcs']
subject_sections = [1,2,3,4,5]
subject_channels = ['cy5','dapi','gfp','txred']
subject_file_formats = ['tiff']

# file name breakdown
# 60.01_lARC_0000_cy5.jpg
# {subject}_{region}_{section}_{channel}.csv
def extract_metadata(subject_file):
    logging.info(subject_file)
    output_dict = {}
    split_subject = subject_file.split('_')
    if(not(len(split_subject) == 4)):
        logging.error(f'subject_file: {subject_file} not correctly formatted.')
        logging.error('{subject}_{region}_{section}_{channel}.csv')
    output_dict['subject'] = split_subject[0]
    output_dict['region'] = split_subject[1]
    output_dict['section'] = split_subject[2]
    output_dict['channel'] = split_subject[3].split('.')[0]
    output_dict['file_type'] = split_subject[3].split('.')[1]
    return output_dict

def get_unique(key, files):
    unique_keys = []
    for file in files:
        if file[key] not in unique_keys:
            unique_keys.append(file[key])
    return unique_keys

# def validate_file_type(subject, region, section, channel, file_type, files):
#     file_name = f'{subject}_{region}_{section}_{channel}.{file_type}'
#     return file_name in files

# def validate_channels(subject, region, section, channel, files):
#     return False

# def validate_sections(subject, region, section, files):
#     return False

# def validate_regions(subject, region, files):
#     return False

# def validate_subject(subject, files):
#     return False


# setup logging
# logging.basicConfig(filename=f'missing-adult-images_{time.time()}.txt', encoding='utf-8', level=logging.INFO)
logging.basicConfig(encoding='utf-8', level=logging.INFO)
logging.info('Validating data files...')

# is base path valid?
if(not(os.path.exists(image_directory))):
    logging.error(f'Data path: {image_directory} is not valid')
    exit()

file_list = os.listdir(image_directory)
extracted_files = {}

# extract metadata for all files in the directory
for data_file in file_list:
    extracted_files[data_file] = extract_metadata(data_file)

# validate we have all the files we need
for check_file in extracted_files:
    valid_files = []
    logging.info(get_unique('subject', extracted_files))
