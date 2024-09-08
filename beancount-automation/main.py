import modules.bank_importer as bi
import modules.data_processor as dp
import os


def main():
    try:
        # Set up paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        
        data_to_import_path = os.path.join(parent_dir, 'beancount-automation', 'import')
        data_path = os.path.join(parent_dir, 'beancount-automation', 'data')
        csv_file_path = os.path.join(data_path, 'merged_data.csv')
        beancount_file_path = os.path.join(data_path, 'ledger.beancount')

        # Process new data
        dp.process_all_new_data(data_to_import_path)

        # Convert CSV to Beancount format
        bank_importer = bi.MyBankImporter()
        bank_importer.convert_csv_to_beancount(csv_file_path, beancount_file_path)

    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
