from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define script paths
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(script_dir))

def load_config(file_path):
    """Load a configuration file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        raise IOError(f"Error reading config file: {e}")

# Load and validate environment variables
BEANCOUNT_HEADER_PATH = os.getenv('BEANCOUNT_HEADER_PATH')
if BEANCOUNT_HEADER_PATH:
    BEANCOUNT_HEADER_PATH = os.path.join(parent_dir, BEANCOUNT_HEADER_PATH)
else:
    raise ValueError("BEANCOUNT_HEADER_PATH environment variable not set.")

BANK_ACCOUNT_1 = os.getenv('BANK_ACCOUNT_1')
BANK_ACCOUNT_2 = os.getenv('BANK_ACCOUNT_2')
MASTERCARD_BIN = os.getenv('MASTERCARD_BIN')
LANDLORD_NAME = os.getenv('LANDLORD_NAME')

# Check if critical environment variables are set
required_vars = {
    "BANK_ACCOUNT_1": BANK_ACCOUNT_1,
    "BANK_ACCOUNT_2": BANK_ACCOUNT_2,
    "MASTERCARD_BIN": MASTERCARD_BIN,
    "LANDLORD_NAME": LANDLORD_NAME,
}

for var_name, var_value in required_vars.items():
    if not var_value:
        raise ValueError(f"Environment variable '{var_name}' is not set.")

# Lazy load the Beancount header only if needed
BEANCOUNT_HEADER = None
def get_beancount_header():
    global BEANCOUNT_HEADER
    if BEANCOUNT_HEADER is None:
        BEANCOUNT_HEADER = load_config(BEANCOUNT_HEADER_PATH)
    return BEANCOUNT_HEADER
