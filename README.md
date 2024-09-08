# Useful Scripts
A collection of practical scripts designed to streamline various tasks and automate repetitive processes. Each script is crafted to serve a specific purpose and is equipped with features like logging and progress tracking for improved usability and reliability.
<details>
<summary><strong>File Mover</strong></summary>

- **Description**: A robust [script](file_mover.py) for efficiently moving files and directories from one location to another. It includes a progress bar to track the transfer status and comprehensive logging to monitor the process and handle errors effectively.
  
- **Why**: Developed to solve the issue of moving large volumes of data—such as photos and videos—that frequently caused Finder on macOS to crash. This script provides a reliable and resilient method to transfer large data sets, minimizing the risk of interruptions or failures.

- **Usage**: To run the file mover script, use the following command:
  
  For example : 
    ```sh
    python3 file_mover.py path/to/source path/to/destination 
    ```
  - --dry-run: Optional flag to simulate the move without actually moving files.

</details>

<details>
<summary><strong>Data Processing Automation</strong></summary>

- **Description**: The [beancount-automation](beancount-automation) project automates the processing of financial transaction data using Python. It consists of several components that work together to reformat CSV data, categorize transactions, and integrate them into a *Beancount* ledger.
  
- **Why**: Managing financial data manually can be tedious and error-prone.

#### How does it work ?
  - **Efficient Data Processing**: Converts raw CSV files into a structured Beancount format, saving you the time and effort of manual data entry.
  - **Semi Automated Categorization**: Classifies transactions into predefined categories based on their descriptions, ensuring consistency and accuracy in your financial records.
  - **Data Integration**: Merges new transactions with existing records while avoiding duplicates, keeping your ledger up-to-date without extra manual work.

#### Usage
  - TODO
  
</details>

## Tools
A set of utility tools designed to enhance the functionality of the scripts. These tools offer additional features like logging and customization to improve script performance and user experience.

<details>
<summary><strong>Logger</strong></summary>
  
  - **Description**: A versatile and customizable [logger](tools/logger.py) that enhances terminal output readability through color-coded messages. It supports various log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) and simplifies logging configuration across different scripts.
    
  - **Features**:
    - Color-coded log levels for better visibility.
    - Customizable format and date/time output.
    - Easy integration into multiple scripts for consistent logging practices.

</details>

## Initial Setup
TODO
