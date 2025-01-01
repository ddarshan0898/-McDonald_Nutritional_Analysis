import pandas as pd
import numpy as np
import argparse
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("clean_csv.log"),
        logging.StreamHandler()
    ]
)

def clean_csv_data(file_path, output_path):
    """
    Cleans the data in a CSV file and saves the cleaned data to a new file.

    Args:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to save the cleaned CSV file.
    """
    try:
        logging.info("Starting the cleaning process.")

        # Load data
        logging.info("Loading data from %s", file_path)
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully. Number of rows: %d, Columns: %d", df.shape[0], df.shape[1])

        # Display initial info
        logging.info("Initial data info:")
        logging.info(df.info())

        # Standardize column names
        logging.info("Standardizing column names...")
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        logging.info("Column names standardized: %s", df.columns.tolist())

        # Handle missing values
        logging.info("Handling missing values...")
        for column in df.columns:
            if df[column].isnull().sum() > 0:
                if df[column].dtype == 'object':
                    mode = df[column].mode()[0]
                    df[column].fillna(mode, inplace=True)
                    logging.info("Filled missing values in column '%s' with mode: %s", column, mode)
                else:
                    median = df[column].median()
                    df[column].fillna(median, inplace=True)
                    logging.info("Filled missing values in column '%s' with median: %f", column, median)

        # Remove duplicates
        logging.info("Removing duplicates...")
        initial_rows = df.shape[0]
        df.drop_duplicates(inplace=True)
        logging.info("Removed %d duplicate rows.", initial_rows - df.shape[0])

        # Convert data types if necessary
        logging.info("Converting data types where applicable...")
        for column in df.select_dtypes(include=['object']).columns:
            try:
                df[column] = pd.to_datetime(df[column])
                logging.info("Converted column '%s' to datetime.", column)
            except ValueError:
                logging.info("Column '%s' could not be converted to datetime.", column)

        # Outlier detection and handling
        logging.info("Handling outliers...")
        for column in df.select_dtypes(include=[np.number]).columns:
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)].shape[0]
            df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
            df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])
            logging.info("Column '%s': Handled %d outliers.", column, outliers)

        # Save cleaned data
        logging.info("Saving cleaned data to %s", output_path)
        df.to_csv(output_path, index=False)
        logging.info("Cleaned data saved successfully.")

        # Display final info
        logging.info("Final data info:")
        logging.info(df.info())

    except Exception as e:
        logging.error("An error occurred during the cleaning process: %s", e)
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean CSV data.")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to save the cleaned CSV file")
    args = parser.parse_args()

    clean_csv_data(args.input_file, args.output_file)