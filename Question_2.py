from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import chi2_contingency
from Rocket_League_Project import dataName, load_Data

## Names of Skillshots
SHOT_NAMES = {
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


## Group attempts by the relative order of jump and boost
def build_action_order_table(attempts):

    def action_order(sequence):
        actions = sequence.split(" > ")

        if "jump" in actions and "boost" in actions:
            if actions.index("jump") < actions.index("boost"):
                return "Jump before boost"

            return "Boost before jump"

        return "Other"

    grouped = attempts.copy()
    grouped["ActionOrder"] = grouped["ActionSequence"].map(action_order)

    return pd.crosstab(
        grouped["Skillshot"],
        grouped["ActionOrder"],
    ).reindex(
        columns=["Jump before boost", "Boost before jump", "Other"],
        fill_value=0,
    )


## Testing whether action order and skillshot are associated
def test_action_sequences(table):

    return chi2_contingency(table)


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

    sequence_table = build_sequence_table(attempts)
    order_table = build_action_order_table(attempts)
    chi2_statistic, p_value, degrees_of_freedom, expected = (
        test_action_sequences(order_table)
    )
    sample_size = int(order_table.to_numpy().sum())
    cramers_v = (
        chi2_statistic
        / (sample_size * min(order_table.shape[0] - 1, order_table.shape[1] - 1))
    ) ** 0.5

    print("Action-order Counts by Skillshot:")
    print(order_table)
    print(
        f"Chi-square test: X^2({degrees_of_freedom}) = "
        f"{chi2_statistic:.2f}, p = {p_value:.2e}"
    )
    print(f"Cramer's V: {cramers_v:.3f}")
    print(
        f"Expected counts below 5: {(expected < 5).sum()} of "
        f"{expected.size}; below 1: {(expected < 1).sum()}"
    )

    sequence_table.to_csv(OUTPUT_DIR / "action_sequence_counts.csv")
    order_table.to_csv(OUTPUT_DIR / "action_order_chi_square_counts.csv")
    plot_action_sequences(sequence_table)


if __name__ == "__main__":
    main()
