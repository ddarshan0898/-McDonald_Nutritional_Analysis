import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("eda_analysis.log"),
        logging.StreamHandler()
    ]
)

def perform_eda(file_path):
    """
    Perform Exploratory Data Analysis (EDA) on the cleaned dataset.

    Args:
        file_path (str): Path to the cleaned CSV file.
    """
    try:
        logging.info("Starting Exploratory Data Analysis (EDA)...")

        # Load cleaned data
        logging.info("Loading cleaned data from %s", file_path)
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully. Number of rows: %d, Columns: %d", df.shape[0], df.shape[1])

        # Display initial summary
        logging.info("Dataset overview:")
        logging.info(df.info())
        logging.info("Summary statistics:\n%s", df.describe(include='all'))

        # Distribution of calorie counts
        if 'calories' in df.columns:
            logging.info("Analyzing the distribution of calorie counts...")
            calorie_stats = df['calories'].describe()
            logging.info("Calorie Statistics:\n%s", calorie_stats)

        # Nutritional content analysis
        nutritional_columns = ['fat', 'protein', 'carbohydrates']
        for col in nutritional_columns:
            if col in df.columns:
                logging.info("Analyzing '%s' distribution...", col)
                stats = df[col].describe()
                logging.info("'%s' Statistics:\n%s", col, stats)

        # Trends and patterns
        logging.info("Exploring trends and patterns...")
        if 'calories' in df.columns and 'protein' in df.columns:
            correlation = df[['calories', 'protein']].corr().iloc[0, 1]
            logging.info("Correlation between 'calories' and 'protein': %.2f", correlation)
        
        # Additional Insights (Example: grouping and aggregation)
        if 'category' in df.columns and 'calories' in df.columns:
            logging.info("Analyzing average calories by category...")
            avg_calories = df.groupby('category')['calories'].mean()
            logging.info("Average Calories by Category:\n%s", avg_calories)

        logging.info("EDA completed successfully.")

    except Exception as e:
        logging.error("An error occurred during the EDA process: %s", e)
        raise

if __name__ == "__main__":
    # Example: Replace 'cleaned_data.csv' with the path to your cleaned dataset
    perform_eda("Nutrical_Datasetacoutput.csv")
