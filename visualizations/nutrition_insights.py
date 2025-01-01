import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("nutrition_insights.log"),
        logging.StreamHandler()
    ]
)

def generate_nutrition_insights(file_path):
    """
    Generate nutrition-based insights from the cleaned dataset.

    Args:
        file_path (str): Path to the cleaned CSV file.
    """
    try:
        logging.info("Starting Nutrition-Based Insights...")

        # Load cleaned data
        logging.info("Loading cleaned data from %s", file_path)
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully. Number of rows: %d, Columns: %d", df.shape[0], df.shape[1])

        # 1. Identify menu items with the highest and lowest calorie counts
        if 'calories' in df.columns:
            logging.info("Identifying menu items with the highest and lowest calorie counts...")
            max_calories = df[df['calories'] == df['calories'].max()]
            min_calories = df[df['calories'] == df['calories'].min()]
            logging.info("Menu item(s) with the highest calorie count:\n%s", max_calories)
            logging.info("Menu item(s) with the lowest calorie count:\n%s", min_calories)

        # 2. Determine the average nutritional content of popular menu categories
        if 'category' in df.columns:
            logging.info("Calculating average nutritional content for popular categories...")
            nutritional_columns = ['calories', 'total_fat', 'protein', 'carbohydrates']
            avg_nutrition = df.groupby('category')[nutritional_columns].mean()
            logging.info("Average nutritional content by category:\n%s", avg_nutrition)

        # Optionally save the insights to a file
        insights_path = "nutrition_insights.csv"
        avg_nutrition.to_csv(insights_path)
        logging.info("Nutrition insights saved to %s", insights_path)

        logging.info("Nutrition-Based Insights completed successfully.")

    except Exception as e:
        logging.error("An error occurred during the Nutrition-Based Insights process: %s", e)
        raise

if __name__ == "__main__":
    # Example: Replace 'cleaned_data.csv' with the path to your cleaned dataset
    generate_nutrition_insights("Nutrical_Datasetacoutput.csv")
