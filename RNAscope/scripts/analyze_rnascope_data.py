import csv
import os
import logging

cell_profiler_data_path = 'F:\\output_7-25-23_Adult'
output_file_name = 'output_Adult2.csv'
output_path =  'F:\\results\\'

# setup logging
logging.basicConfig(encoding='utf-8', level=logging.INFO)
logging.info('Starting RNAScope Data Analysis')

if(not(os.path.exists(cell_profiler_data_path))):
    logging.error(f'Data path: {cell_profiler_data_path} is not valid')
    exit()

# file name breakdown
# MinipumpRNAscope_2.15_NAcs_0001_RedCells.csv2.01_NAcc_0000_cy5.tiff
# {prefix}_{subject}_{region}_{section}_{channel}.csv
def extract_metadata(subject_file):
    output_dict = {}
    split_subject = subject_file.split('_')
    if(not(len(split_subject) == 5)):
        logging.error(f'subject_file: {subject_file} not correctly formatted.')
        logging.error(f'example file format: MinipumpRNAscope_2.15_NAcs_0001_RedCells.csv')
        logging.error('{prefix}_{subject}_{region}_{section}_{channel}.csv')
    output_dict['prefix'] = split_subject[0]
    output_dict['subject'] = split_subject[1]
    output_dict['region'] = split_subject[2]
    output_dict['section'] = split_subject[3]
    output_dict['channel'] = split_subject[4].split('.')[0]
    output_dict['subject_name'] = split_subject[1] + '_' + split_subject[2] + '_' + split_subject[3]
    return output_dict
    

def get_results_data(subject_file_path, subject_metadata):
    logging.info(f'Processing file: {subject_file_path}')
    with open(subject_file_path, newline='') as csvfile:
        subject_data = {}
        subject_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(subject_reader) # skip the csv header row
        subject_data['subject_name'] = subject_metadata['subject_name']
        if(subject_metadata['channel'] == 'Cells'): # if we have a 'Cells' file
            subject_total = 0
            for row in subject_reader:
                subject_total += 1
            subject_data['total_cells'] = subject_total # just find the total number of rows
        else: # else calculate the puncta
            if(subject_metadata['channel'] == 'MagentaCells'): # if we have a 'Magenta' file
                subject_total = 0
                green_puncta = 0 # ignore zeros
                green_total = 0
                magenta_puncta = 0 # do not ignore zeros
                red_puncta = 0 # ignore zeros
                red_total = 0
                for row in subject_reader:
                    subject_total += 1
                    magenta_puncta += float(row[3])
                    if(float(row[2]) > 0):
                        green_total += 1
                        green_puncta += float(row[2])
                    if(float(row[4]) > 0):
                        red_total += 1
                        red_puncta += float(row[4])
                if(subject_total > 0):
                    magenta_puncta = magenta_puncta/subject_total
                    if(green_total > 0):
                        green_puncta = green_puncta/green_total
                    if(red_total > 0):
                        red_puncta = red_puncta/red_total

                subject_data[subject_metadata['channel']] = subject_total
                subject_data[subject_metadata['channel']+'_green_puncta'] = green_puncta
                subject_data[subject_metadata['channel']+'_green_sum'] = green_total
                subject_data[subject_metadata['channel']+'_red_puncta'] = red_puncta
                subject_data[subject_metadata['channel']+'_red_sum'] = red_total
                subject_data[subject_metadata['channel']+'_puncta'] = magenta_puncta
            else:
                subject_total = 0
                subject_puncta = 0
                for row in subject_reader:
                    if(not(len(row)==12)):
                        logging.error(f'Data row: {row} is incorrectly formatted')
                    subject_total += 1
                    subject_puncta += float(row[2])
                if(subject_total > 0):
                    subject_puncta = subject_puncta/subject_total # take the average of column 3
                else:
                    subject_puncta = 0
                subject_data[subject_metadata['channel']] = subject_total
                subject_data[subject_metadata['channel']+'_puncta'] = subject_puncta
        return subject_data

def get_unique_subject_names(list_of_subjects):
    unique_list = []
    for subject in list_of_subjects:
        if(not(subject['subject_name'] in unique_list)):
            unique_list.append(subject['subject_name'])
    return unique_list


def get_matching_subject_names(list_of_subjects, matching_name):
    matching_list = []
    for subject in list_of_subjects:
        if(subject['subject_name'] == matching_name):
            matching_list.append(subject)
    return matching_list

def combine_subject_data(list_of_subjects):
    combined_dict = {}
    for subject in list_of_subjects:
        for key in subject.keys():
            if not(key in combined_dict) and key in subject:
                combined_dict[key] = subject[key]
    return combined_dict

#================================================================================ 

file_list = os.listdir(cell_profiler_data_path) # get all files in the given cell profiler directory
full_result_list = []
for subject_file in file_list:
    subject_file_path = os.path.join(cell_profiler_data_path, subject_file)
    if(not(os.path.isfile(subject_file_path))):
        logging.error(f'subject_file_path: {subject_file_path} not valid')

    subject_metadata = extract_metadata(subject_file)
    logging.debug(f'Subject metadata: {subject_metadata}')
    result_data = get_results_data(subject_file_path, subject_metadata)
    logging.debug(f'Results: {result_data}')
    full_result_list.append(result_data)

# final data processing
final_result_list = []
logging.info('Starting final data processing')
unique_subject_list = get_unique_subject_names(full_result_list)
logging.debug(f'Unique subject_name list: {unique_subject_list}')   
for unique_subject in unique_subject_list:
    uncombined_subject_list = get_matching_subject_names(full_result_list, unique_subject) # all matching records for a single subject
    combined_subject = combine_subject_data(uncombined_subject_list)
    logging.debug(f'combined_subject_list: {combined_subject}')
    final_result_list.append(combined_subject)

# open output.csv file for writing outputs
if not os.path.exists(output_path):
    logging.error(f'Results path does not exist: {output_path}')
    logging.error(f'Attempting to create path: {output_path}')
    os.makedirs(output_path)
with open(output_path+'\\'+output_file_name, 'w+', newline='') as write_file:
    logging.info(f'Writing results to file: {output_path}\\{output_file_name}')
    field_names = ["subject_name","GreenCells","GreenCells_puncta", "MagentaCells","MagentaCells_puncta","MagentaCells_green_puncta","MagentaCells_green_sum","MagentaCells_red_puncta","MagentaCells_red_sum","RedCells","RedCells_puncta", "total_cells"]
    writer = csv.DictWriter(write_file, fieldnames=field_names)
    writer.writeheader()
    for subject in final_result_list:
        writer.writerow(subject)
