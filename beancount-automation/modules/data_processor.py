import os
import shutil
import pandas as pd
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from tools.logger import setup_logger
logger = setup_logger()

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)


def reformat_data(file_path):
    file_name = os.path.basename(file_path)
    logger.info(f"Processing {file_name}")

    # Check if the file should be skipped (e.g., already formatted or irrelevant file)
    if "cibc" in file_name.lower() or "reformatted" in file_name:
        logger.warning(f"This data is already well formatted. Skipping reformatting for {file_name}.")
        return file_path  # Return original file path

    # Ensure the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")

    logger.info(f"Reformatting {file_name} data...")
    data = pd.read_csv(file_path, header=None)

    # Select and rename columns
    data = data[[3, 5, 7, 8, 2]]
    data.columns = ['date', 'description', 'outflow', 'inflow', 'card_number']

    # Clean the data
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
    data['outflow'] = data['outflow'].fillna('')
    data['inflow'] = data['inflow'].fillna('')

    # Save reformatted data
    reformatted_file_path = os.path.join(parent_dir, 'import', f'reformatted_{file_name}')
    data.to_csv(reformatted_file_path, index=False, header=False)
    
    return reformatted_file_path


def merge_data(reformatted_file_path):
    logger.info(f"Merging data from {reformatted_file_path}")
    merge_path = os.path.join(parent_dir, 'data', 'merged_data.csv')

    # Ensure the merge file exists
    if not os.path.isfile(merge_path):
        with open(merge_path, 'w') as f:
            f.write("")

    # Load existing and incoming data
    before_merge_data = pd.read_csv(merge_path, header=None, names=['date', 'description', 'outflow', 'inflow', 'card_number'])
    incoming_data = pd.read_csv(reformatted_file_path, header=None, names=['date', 'description', 'outflow', 'inflow', 'card_number'])

    # Filter out already existing data
    incoming_data_unique = incoming_data[~incoming_data.set_index(['date', 'description', 'outflow', 'inflow', 'card_number']).index.isin(
        before_merge_data.set_index(['date', 'description', 'outflow', 'inflow', 'card_number']).index)]

    if incoming_data_unique.empty:
        logger.warning(f"{reformatted_file_path} contains no new data to merge. It has probably already been merged.")
        return

    # Drop any columns with only NA values from both dataframes
    before_merge_data = before_merge_data.dropna(axis=1, how='all')
    incoming_data_unique = incoming_data_unique.dropna(axis=1, how='all')

    # Combine and sort data by date
    merged_data = pd.concat([before_merge_data, incoming_data_unique])
    merged_data['date'] = pd.to_datetime(merged_data['date'])
    merged_data = merged_data.sort_values('date')

    # Save the merged data
    merged_data.to_csv(merge_path, index=False, header=False)
    logger.info("Data merged successfully.")


def clean_folder(folder_path):
    logger.info(f"Cleaning folder: {folder_path}")
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename == '.gitkeep':
            continue
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error(f"Failed to delete {file_path}. Reason: {e}")


def process_all_new_data(folder_path):
    if not os.path.exists(folder_path) or not any(filename != '.gitkeep' for filename in os.listdir(folder_path)):
        logger.warning("No new data to process.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Process only unformatted CSV files
        if file_path.endswith('.csv') and 'reformatted' not in file_path:
            reformatted_file_path = reformat_data(file_path)
            merge_data(reformatted_file_path)

    # Clean up after processing
    clean_folder(folder_path)
