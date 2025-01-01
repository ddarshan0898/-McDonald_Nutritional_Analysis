import pandas as pd
import numpy as np

def clean_csv_data(file_path, output_path):
    """
    Cleans the data in a CSV file and saves the cleaned data to a new file.

    Args:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to save the cleaned CSV file.
    """
    try:
        # Load data
        print("Loading data...")
        df = pd.read_csv(file_path)

        # Display initial info
        print("Initial data info:")
        print(df.info())

        # Standardize column names
        print("Standardizing column names...")
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Handle missing values
        print("Handling missing values...")
        for column in df.columns:
            if df[column].isnull().sum() > 0:
                if df[column].dtype == 'object':
                    # Fill missing values for categorical columns with mode
                    df[column].fillna(df[column].mode()[0], inplace=True)
                else:
                    # Fill missing values for numerical columns with median
                    df[column].fillna(df[column].median(), inplace=True)

        # Remove duplicates
        print("Removing duplicates...")
        df.drop_duplicates(inplace=True)

        # Convert data types if necessary
        print("Converting data types...")
        for column in df.select_dtypes(include=['object']).columns:
            try:
                df[column] = pd.to_datetime(df[column])
            except ValueError:
                pass  # Not a datetime column

        # Outlier detection and handling (if applicable)
        print("Handling outliers...")
        for column in df.select_dtypes(include=[np.number]).columns:
            q1 = df[column].quantile(0.25)
            q3 = df[column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            df[column] = np.where(df[column] < lower_bound, lower_bound, df[column])
            df[column] = np.where(df[column] > upper_bound, upper_bound, df[column])

        # Save cleaned data
        print("Saving cleaned data...")
        df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")

        # Display final info
        print("Final data info:")
        print(df.info())

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# Replace 'input.csv' and 'output_cleaned.csv' with your file paths
# clean_csv_data('input.csv', 'output_cleaned.csv')
