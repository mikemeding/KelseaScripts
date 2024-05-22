import os
import logging
import time

image_directory = 'F:\\Adult Images 2'
# starting_subject_number = 1
# ending_subject_number = 52 
# skip_subject_list = [2,8,16,19,20,24,26,27,29,30,34,38,40,45,47,49,51]
# check_only_subjects = [8,19,24,26,27,29,30,34,38,45,73,98]
check_only_subjects = [1,3,4,7,10,11,12,14,15,17,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,37,38,39,41,43,44,45,46,47,48,50,73]
subject_prefix = '60'
subject_regions = ['NAcc','NAcs']
subject_sections = [1,2,3,4,5]
subject_channels = ['cy5','dapi','gfp','txred']
subject_file_formats = ['tiff']

# setup logging
# logging.basicConfig(filename=f'missing-adult-images_{time.time()}.txt', encoding='utf-8', level=logging.INFO)
logging.basicConfig(encoding='utf-8', level=logging.INFO)
logging.info('Validating data files...')

# is base path valid?
if(not(os.path.exists(image_directory))):
    logging.error(f'Data path: {image_directory} is not valid')
    exit()

# check valid paths for all files
# for subject_number in range(starting_subject_number, ending_subject_number+1):
for subject_number in check_only_subjects:
    # if(subject_number in skip_subject_list):
    #     continue # skip this subject number
    for subject_region in subject_regions:
        for subject_section in subject_sections:
            for subject_channel in subject_channels:
                for subject_file_format in subject_file_formats:
                    subject_file_name = subject_prefix + '.' \
                        + str(subject_number).zfill(2) + '_' \
                        + subject_region + '_' \
                        + str(subject_section).zfill(4) + '_' \
                        + subject_channel \
                        + '.' + subject_file_format
                    subject_file_path = os.path.join(image_directory, subject_file_name)
                    if(not(os.path.isfile(subject_file_path))):
                        logging.error(f'failed subject_file_path: {subject_file_path}')
    