import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("documentation_report.log"),
        logging.StreamHandler()
    ]
)

def document_and_report(insights_path):
    """
    Summarize findings and generate a report based on the nutritional analysis.

    Args:
        insights_path (str): Path to the nutritional insights file.
    """
    try:
        # Load nutritional insights data
        logging.info("Loading nutritional insights data from %s", insights_path)
        df = pd.read_csv(insights_path)
        logging.info("Data loaded successfully. Number of rows: %d, Columns: %d", df.shape[0], df.shape[1])

        # Key Findings
        logging.info("Generating key findings...")
        highest_calorie_category = df.loc[df['calories'].idxmax()]
        lowest_calorie_category = df.loc[df['calories'].idxmin()]
        avg_calories = df['calories'].mean()
        avg_fat = df['total_fat'].mean()
        avg_protein = df['protein'].mean()
        avg_carbs = df['carbohydrates'].mean()

        logging.info("Key findings generated successfully.")

        # Generate Report
        report_path = "nutrition_analysis_report.txt"
        with open(report_path, "w") as file:
            file.write("### Nutritional Analysis Report\n\n")
            file.write("#### Key Findings:\n")
            file.write(f"- Category with the highest calories: {highest_calorie_category['category']} "
                       f"({highest_calorie_category['calories']} kcal)\n")
            file.write(f"- Category with the lowest calories: {lowest_calorie_category['category']} "
                       f"({lowest_calorie_category['calories']} kcal)\n")
            file.write(f"- Average Calories: {avg_calories:.2f} kcal\n")
            file.write(f"- Average Total Fat: {avg_fat:.2f} g\n")
            file.write(f"- Average Protein: {avg_protein:.2f} g\n")
            file.write(f"- Average Carbohydrates: {avg_carbs:.2f} g\n\n")

            file.write("#### Benefits of Nutritional Analysis:\n")
            file.write(
                "1. **For Customers**: Provides transparency, enabling informed dietary choices based on caloric and nutritional needs.\n"
                "   - Helps health-conscious individuals choose low-calorie or high-protein items.\n"
                "   - Assists customers with specific dietary preferences (e.g., low-fat or high-carb options).\n"
                "2. **For McDonald's**: Enhances customer trust and promotes healthy eating initiatives.\n"
                "   - Identifies popular low-calorie and high-nutrition items to promote them further.\n"
                "   - Facilitates menu optimization by balancing health and taste preferences.\n"
            )
            file.write("\n### Conclusion:\n")
            file.write(
                "This nutritional analysis provides actionable insights to improve menu offerings and better serve the dietary needs of McDonald's diverse customer base."
            )

        logging.info("Documentation and Reporting completed successfully. Report saved to %s", report_path)

    except Exception as e:
        logging.error("An error occurred during Documentation and Reporting: %s", e)
        raise


# Call the function with the path to the nutritional insights file
if __name__ == "__main__":
    document_and_report("nutrition_insights.csv")
