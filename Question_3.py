
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from Rocket_League_Project import dataName, load_Data


# File locations
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "question3_results"

## Collect and clean the data
def process_data():

    df = load_Data(dataName("RL_data"))

    # Remove duplicates and missing values
    df = df.drop_duplicates()
    df = df.dropna()

    # Group all rows belonging to the same attempt
    grouped = df.groupby("SequenceNumber")

    # Calculate average gameplay measurements
    features = df.drop(columns=["SequenceNumber", "SequenceLabel"])
    X = features.groupby(df["SequenceNumber"]).mean()

    # Get actual attempt outcomes
    labels = grouped["SequenceLabel"].first()

    # Convert outcomes into numbers
    # 0 = Failed, 1 = Successful
    y = (labels != -1).astype(int)

    return X, y


## Standardize the gameplay variables
def standardize_data(X):

    # Calculate mean and standard deviation
    means = X.mean()
    standard_deviations = X.std()

    # Calculate z-scores
    X_scaled = (X - means) / standard_deviations

    return X_scaled, means, standard_deviations


## Calculate regression coefficients
def regression(X, y):

    # Add a column of ones for the intercept
    X_with_intercept = np.column_stack((
        np.ones(len(X)),
        X
    ))

    # Calculate coefficients using least squares
    coefficients = np.linalg.lstsq(
        X_with_intercept, y, rcond=None
    )[0]

    return coefficients


## Calculate predicted outcomes
def predict_outcomes(coefficients, X):

    # Add intercept column
    X_with_intercept = np.column_stack((
        np.ones(len(X)),
        X
    ))

    # Calculate predicted outcomes
    predictions = X_with_intercept @ coefficients

    # Convert predictions into 0 or 1
    predicted_outcomes = (predictions >= 0.5).astype(int)

    return predictions, predicted_outcomes


## Interpret the regression coefficients
def plot_coefficients(coefficients, X):

    # Skip the first coefficient because it is the intercept
    results = pd.DataFrame({
        "Variable": X.columns,
        "Coefficient": coefficients[1:]
    })

    # Sort by absolute coefficient size
    results["Absolute Value"] = results["Coefficient"].abs()
    results = results.sort_values("Absolute Value", ascending=True)

    # Create bar chart
    plt.figure(figsize=(10, 7))

    plt.barh(
        results["Variable"],
        results["Coefficient"]
    )

    plt.axvline(0, color="black", linewidth=1)

    plt.xlabel("Standardized Regression Coefficient")
    plt.ylabel("Gameplay Variables")
    plt.title("Relationship Between Gameplay Variables and Shot Success")

    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()

    # Save and show graph
    plt.savefig(OUTPUT_DIR / "Regression_Coefficients.png")
    plt.show()

    print("\nRegression Coefficients:")
    print(
        results[["Variable", "Coefficient"]]
        .sort_values("Coefficient", ascending=False)
        .round(4)
    )


## Run program
def main():

    X, y = process_data()

    print("Total Attempts:", len(X))
    print("Failed Attempts:", sum(y == 0))
    print("Successful Attempts:", sum(y == 1))

    # Standardize the data
    X_scaled, means, standard_deviations = standardize_data(X)

    # Calculate regression coefficients
    coefficients = regression(X_scaled, y)

    # Calculate predicted outcomes
    predictions, predicted_outcomes = predict_outcomes(
        coefficients, X_scaled
    )

    # Calculate R-squared manually
    r2 = 1 - (
        np.sum((y - predictions) ** 2) /
        np.sum((y - y.mean()) ** 2)
    )

    # Calculate prediction accuracy
    accuracy = np.mean(predicted_outcomes == y)

    print("\nRegression Results:")
    print("R-squared:", round(r2, 4))
    print("Prediction Accuracy:", round(accuracy * 100, 2), "%")

    # Compare actual and predicted outcomes
    print("\nActual vs Predicted Outcomes:")
    print(pd.crosstab(
        y,
        predicted_outcomes,
        rownames=["Actual"],
        colnames=["Predicted"]
    ))

    # Plot regression coefficients
    plot_coefficients(coefficients, X)


main()



