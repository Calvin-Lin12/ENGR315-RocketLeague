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



if __name__ == "__main__":
    main()