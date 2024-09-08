import os
import csv
from beancount.core import data
from beancount.core.amount import Amount
from beancount.core.number import D
from beancount.ingest.importer import ImporterProtocol
from beancount.core import flags
from datetime import datetime
from modules.config import BEANCOUNT_HEADER, MASTERCARD_BIN, LANDLORD_NAME, BANK_ACCOUNT_1, BANK_ACCOUNT_2

# Define categories as dictionaries for efficient lookups
CATEGORY_MAP = {
    'Home:Rent': [LANDLORD_NAME],
    'Home:Electricity': ['HYDRO-SHERBROOKE'],
    'Food:Restaurant': ['BEKKAH', 'RIMA', 'SIBOIRE', 'KAAPEH', 'COMME CHEZ SOI', 'RICHESSES', 'KOBO', 'GLACEE EN FOLIE', 'BOBA-LINDA', 'MARCHE FERME BEULIEU', 'DOMINO', 'CHOCOLATS FAVORIS', 'Geogene', 'TIM HORTONS', 'HANABI'],
    'Food:Groceries': ['MAXI', 'PROVIGO', 'COSTCO WHOLESALE', 'IGA', 'METRO', '5IEME SAISON', 'SUPER C', 'AVRIL', 'ANDES', 'FROMAGERIE DE LA GARE', 'MARCHE BELVEDERE'],
    'Car:Gasoline': ['COSTCO ESSENCE', 'PETRO CANADA'],
    'Home:PhoneAndInternet': ['FIZZ'],
    'Treats:PersonalCare': ['HM', 'ZARA', 'SIMONS', 'OLD NAVY', 'EUPHORIK', 'SEPHORA', 'REITMANS'],
    'Car:Maintenance': ['CANADIAN TIRE', 'GARAGE SYLVAIN POULIOT'],
    'Finance:Interest': ['INTERET'],
    'Insurance': ['INSURANCE']
}

def categorize_transactions(description):
    """
    Categorize transactions based on the description.
    """
    for category, keywords in CATEGORY_MAP.items():
        if any(keyword in description for keyword in keywords):
            return category
    return 'Others'

def csv_to_beancount(line):
    """
    Convert a CSV line to a Beancount transaction.
    """
    date_str, description, outflow, inflow, account_number = line
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    
    amount = D(outflow) if outflow else D(inflow)
    amountAsset = Amount(-amount, "CAD") if outflow else Amount(amount, "CAD")
    amountExpense = Amount(amount, "CAD")
    
    category = categorize_transactions(description)

    account = BANK_ACCOUNT_1 if account_number.startswith(MASTERCARD_BIN) else (BANK_ACCOUNT_2 if account_number.startswith("PCA") else "Assets:Unknown")

    meta = data.new_metadata("file.csv", 0)
    postings = [
        data.Posting(account, amountAsset, None, None, None, None),
        data.Posting("Expenses:" + category, amountExpense, None, None, None, None)
    ]

    return data.Transaction(meta, date, flags.FLAG_OKAY, description, description, data.EMPTY_SET, data.EMPTY_SET, postings)

def read_existing_transactions(file_path):
    """
    Read existing transactions from the Beancount file.
    """
    if not os.path.exists(file_path):
        return set()

    with open(file_path, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def generate_file_with_header(output_file):
    """
    Generate the Beancount file with the header if it does not exist.
    """
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write(BEANCOUNT_HEADER)

def save_to_beancount_file(entries, output_file):
    """
    Save Beancount entries to a file.
    """
    generate_file_with_header(output_file)
    existing_transactions = read_existing_transactions(output_file)

    new_transactions = []

    for entry in entries:
        date = entry.date.isoformat()
        description = entry.narration
        transaction_str = f'{date} * "{description}"'

        if transaction_str not in existing_transactions:
            new_transactions.append(entry)

    if new_transactions:
        with open(output_file, 'a') as f:
            f.write(f'; Transactions added on {datetime.now().strftime("%d %B %Y at %H:%M")}\n')
            for entry in new_transactions:
                date = entry.date.isoformat()
                description = entry.narration
                f.write(f'{date} * "{description}"\n')
                for posting in entry.postings:
                    account = posting.account
                    amount = posting.units.number
                    currency = posting.units.currency
                    f.write(f'  {account:<40} {amount:>10} {currency}\n')
                f.write('\n')

class MyBankImporter(ImporterProtocol):
    def identify(self, file):
        return file.name.endswith('.csv')

    def file_account(self, file):
        return "Assets:Bank:Checking"

    def extract(self, file_path):
        """
        Read and parse the file and convert the original data into Beancount data structures.
        """
        entries = []
        with open(file_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for line in csv_reader:
                if line:  # Skip empty lines
                    entries.append(csv_to_beancount(line))
        return entries

    def convert_csv_to_beancount(self, csv_file, beancount_file):
        entries = self.extract(csv_file)
        save_to_beancount_file(entries, beancount_file)
