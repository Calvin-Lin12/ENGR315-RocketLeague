from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Names of Skillshots
SHOT_NAMES = {
    1: "Ceiling Shot",
    2: "Power Shot",
    3: "Wave Dash",
    5: "Air Dribble",
    6: "Front Flick",
    7: "Musty Flick",
}

# File locations
ROOT = Path(__file__).resolve().parent

DATA_FILE = ROOT / "data" / "RL_data.csv"

OUTPUT_DIR = ROOT / "question1_results"

# find the first time a button is pressed during a skillshot
def first_press_time(sequence, button):

    sequence = sequence.sort_values("Time")

    pressed = sequence.loc[sequence[button] > 0, "Time"]

    if pressed.empty:
        return np.nan

    return float(pressed.iloc[0] - sequence["Time"].iloc[0])

# Organize data into individual skillshot attempts
def build_attempt_table(data):

    attempts = []

    for number, sequence in data.groupby("SequenceNumber"):

        label = int(sequence["SequenceLabel"].iloc[0])

        if label not in SHOT_NAMES:
            continue

        jump_time = first_press_time(sequence, "jump")
        boost_time = first_press_time(sequence, "boost")

        attempts.append({
            "SequenceNumber": number,
            "Skillshot": SHOT_NAMES[label],
            "JumpTime": jump_time,
            "BoostTime": boost_time
        })

    return pd.DataFrame(attempts)

# Calculate statistics for jump and boost timings
def calculate_statistics(attempts):

    statistics = attempts.groupby("Skillshot")[
        ["JumpTime", "BoostTime"]
    ].agg(["count", "mean", "median", "min", "max"])

    return statistics


# Create box plots comparing jump and boost timings
def plot_timings(attempts):

    for column in ["JumpTime", "BoostTime"]:

        data = []
        labels = []

        for skillshot, group in attempts.groupby("Skillshot"):

            times = group[column].dropna()

            if times.empty:
                continue

            data.append(times)
            labels.append(skillshot)

        if not data:
            continue

        plt.figure(figsize=(10,6))
        plt.boxplot(data, tick_labels=labels)

        plt.title(f"{column} by Skillshot")
        plt.xlabel("Skillshot Type")
        plt.ylabel("Time (seconds)")

        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.savefig(OUTPUT_DIR / f"{column}_boxplot.png")
        plt.show()
        plt.close()


# Test how accurately jump and boost timings predict skillshots
def test_prediction_accuracy(attempts):

    rng = np.random.default_rng(42)

    train_indices = []
    test_indices = []

    # Separate attempts into training and testing groups
    for skillshot, group in attempts.groupby("Skillshot"):

        indices = group.index.to_numpy().copy()
        rng.shuffle(indices)

        if len(indices) < 2:
            train_indices.extend(indices)
            continue

        n_test = min(max(1, round(0.20 * len(indices))),
                     len(indices) - 1)

        test_indices.extend(indices[:n_test])
        train_indices.extend(indices[n_test:])


    if not test_indices:
        print("Not enough data to test accuracy.")
        return

    train = attempts.loc[train_indices]
    test = attempts.loc[test_indices]


    # Select the jump and boost timing columns
    columns = ["JumpTime", "BoostTime"]

    x_train = train[columns].fillna(-1).to_numpy()
    x_test = test[columns].fillna(-1).to_numpy()
    y_train = train["Skillshot"].to_numpy()
    y_test = test["Skillshot"].to_numpy()

    # Calculate Distances between timing measurements
    scale = x_train.std(axis=0)
    scale[scale == 0] = 1

    predictions = []

    for trial in x_test:

        distances = np.sum(((x_train - trial) / scale) ** 2,
                           axis=1)

        closest = np.argmin(distances)

        predictions.append(y_train[closest])

    # Calculate prediction accuracy
    accuracy = 100 * np.mean(
        np.array(predictions) == y_test
    )

    # Compare against predicting the most common skillshot
    most_common = train["Skillshot"].mode().iloc[0]
    baseline = 100 * np.mean(y_test == most_common)

    print(f"Prediction accuracy: {accuracy:.1f}%")
    print(f"Baseline accuracy: {baseline:.1f}%")
    print(f"Number of test attempts: {len(test)}")

# Load the Rocket League dataset
def load_data():

    data = pd.read_csv(DATA_FILE)
    return data

# Create a bar graph comparing average input timings
def plot_average_timings(attempts):

    # Calculate average juump and boost times for each skillshot
    averages = attempts.groupby("Skillshot")[
        ["JumpTime", "BoostTime"]
    ].mean()

    # Create a bar graph
    averages.plot(kind="bar", figsize=(10, 6))

    # Add labels and a title
    plt.title("Average Jump and Boost Timing by Skillshot")
    plt.xlabel("Skillshot Type")
    plt.ylabel("Average Time (Seconds)")

    # Adjust Graph Appearance
    plt.xticks(rotation=45)
    plt.legend(["Jump Time", "Boost Time"])
    plt.tight_layout()

    # Save and display Graph
    plt.savefig(OUTPUT_DIR / "Average_Timings.png")
    plt.show()
    plt.close()


# Run the complete analysis
def main():

    # Create a folder to save results
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load the original dataset
    data = load_data()

    # Organize the data into skillshot attempts
    attempts = build_attempt_table(data)

    if attempts.empty:
        print("No valid skillshot attempts were found.")
        return

    # Calculate and display timing statistics
    statistics = calculate_statistics(attempts)

    print("Jump and Boost Timing Statistics:")
    print(statistics)

    # Save the statistics and attempt data
    statistics.to_csv(OUTPUT_DIR / "timing_statistics.csv")
    attempts.to_csv(OUTPUT_DIR / "attempt_timings.csv", index=False)

    # Generate graphs
    plot_timings(attempts)
    plot_average_timings(attempts)

    # Test prediction accuracy
    test_prediction_accuracy(attempts)

if __name__ == "__main__":
    main()