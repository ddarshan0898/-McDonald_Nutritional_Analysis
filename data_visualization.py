import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_visualization.log"),
        logging.StreamHandler()
    ]
)

def visualize_data(file_path, output_dir="visualizations"):
    """
    Perform data visualization on the cleaned dataset.

    Args:
        file_path (str): Path to the cleaned CSV file.
        output_dir (str): Directory to save the visualizations.
    """
    try:
        logging.info("Starting Data Visualization...")

        # Load cleaned data
        logging.info("Loading cleaned data from %s", file_path)
        df = pd.read_csv(file_path)
        logging.info("Data loaded successfully. Number of rows: %d, Columns: %d", df.shape[0], df.shape[1])

        # Ensure output directory exists
        import os
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. Bar Chart: Average Nutritional Content by Category
        if 'category' in df.columns:
            logging.info("Creating bar chart for average nutritional content by category...")
            nutritional_columns = ['calories', 'total_fat', 'protein', 'carbohydrates']
            avg_nutrition = df.groupby('category')[nutritional_columns].mean()
            avg_nutrition.plot(kind='bar', figsize=(10, 6))
            plt.title("Average Nutritional Content by Category")
            plt.ylabel("Average Value")
            plt.xlabel("Category")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{output_dir}/average_nutrition_by_category.png")
            logging.info("Bar chart saved as 'average_nutrition_by_category.png'.")

        # 2. Histogram: Calorie Distribution
        if 'calories' in df.columns:
            logging.info("Creating histogram for calorie distribution...")
            plt.figure(figsize=(8, 6))
            sns.histplot(df['calories'], kde=True, bins=30, color='blue')
            plt.title("Calorie Distribution")
            plt.xlabel("Calories")
            plt.ylabel("Frequency")
            plt.tight_layout()
            plt.savefig(f"{output_dir}/calorie_distribution.png")
            logging.info("Histogram saved as 'calorie_distribution.png'.")

        # 3. Box Plot: Nutritional Content
        logging.info("Creating box plots for nutritional content...")
        nutritional_columns = ['calories', 'total_fat', 'protein', 'carbohydrates']
        for col in nutritional_columns:
            if col in df.columns:
                plt.figure(figsize=(8, 6))
                sns.boxplot(x='category', y=col, data=df)
                plt.title(f"{col.capitalize()} by Category")
                plt.xlabel("Category")
                plt.ylabel(col.capitalize())
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(f"{output_dir}/boxplot_{col}_by_category.png")
                logging.info("Box plot for '%s' saved as 'boxplot_%s_by_category.png'.", col, col)

        # 4. Pair Plot: Explore Relationships
        logging.info("Creating pair plot for nutritional columns...")
        sns.pairplot(df, vars=['calories', 'fat', 'protein', 'carbohydrates'], hue='category', palette='Set2')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/pairplot_nutrition.png")
        logging.info("Pair plot saved as 'pairplot_nutrition.png'.")

        logging.info("Data Visualization completed successfully. Visualizations saved in %s.", output_dir)

    except Exception as e:
        logging.error("An error occurred during the Data Visualization process: %s", e)
        raise

if __name__ == "__main__":
    # Example: Replace 'cleaned_data.csv' with the path to your cleaned dataset
    visualize_data("Nutrical_Datasetacoutput.csv")
