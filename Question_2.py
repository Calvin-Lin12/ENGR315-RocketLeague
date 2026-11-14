from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import chi2_contingency
from Rocket_League_Project import dataName, load_Data

## Names of Skillshots
SHOT_NAMES = {
    -1: "Noise",
    1: "Ceiling Shot",
    2: "Power Shot",
    3: "Wave Dash",
    5: "Air Dribble",
    6: "Front Flick",
    7: "Musty Flick",
}

## File locations
ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "question2_results"


## Organizing each attempt by skillshot and action sequence
def build_attempt_table(data):

    actions = ["jump", "boost", "slide"]
    attempts = []

    for number, sequence in data.groupby("SequenceNumber"):

        label = int(sequence["SequenceLabel"].iloc[0])

        if label not in SHOT_NAMES:
            continue

        first_action_times = {}

        for action in actions:
            pressed = sequence.loc[sequence[action] > 0, "Time"]

            if not pressed.empty:
                first_action_times[action] = pressed.min()

        action_sequence = " > ".join(
            sorted(first_action_times, key=first_action_times.get)
        ) or "None"

        attempts.append({
            "SequenceNumber": number,
            "Skillshot": SHOT_NAMES[label],
            "ActionSequence": action_sequence,
        })

    return pd.DataFrame(attempts)


## Counting attempts for each action sequence and skillshot
def build_sequence_table(attempts):

    table = pd.crosstab(
        attempts["Skillshot"],
        attempts["ActionSequence"],
    )

    return table


## Testing whether action sequence counts differ by skillshot
def test_action_sequences(table):

    _, p_value, _, _ = chi2_contingency(table)

    return p_value


## Creating a bar graph showing action sequence percentages for each skillshot
def plot_action_sequences(table):

    percentages = table.div(table.sum(axis=1), axis=0) * 100

    for skillshot, row in percentages.iterrows():

        sequences = row[row > 0].sort_values()

        plt.figure(figsize=(10, 6))
        sequences.plot(kind="barh")

        plt.title(f"Action Sequences for {skillshot}")
        plt.xlabel("Attempts (%)")
        plt.ylabel("Action Sequence")
        plt.xlim(0, 100)
        plt.tight_layout()

        filename = skillshot.lower().replace(" ", "_")
        plt.savefig(OUTPUT_DIR / f"{filename}_action_sequences.png")
        plt.show()
        plt.close()


## Loading the dataset, running analysis, and creating plots
def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    data = load_Data(dataName("RL_data"))
    attempts = build_attempt_table(data)

    if attempts.empty:
        print("No valid skillshot attempts were found.")
        return

    table = build_sequence_table(attempts)
    p_value = test_action_sequences(table)

    print("Action Sequence Counts by Skillshot:")
    print(table)
    print(f"Chi-square p-value: {p_value:.2e}")

    table.to_csv(OUTPUT_DIR / "action_sequence_counts.csv")
    plot_action_sequences(table)


if __name__ == "__main__":
    main()
