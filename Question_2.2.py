from pathlib import Path
import pandas as pd
from scipy.stats import chi2_contingency

# File locations
ROOT = Path(__file__).resolve().parent

DATA_FILE = ROOT / "data" / "RL_data.csv"

OUTPUT_DIR = ROOT / "question1_results"

## Question 2: Do certain player action sequences repeat consistently across
## different players performing the same trick, or is there high variance
## in individual playstyles?

def dataName(file):
    ## Find & open all_participant_data_rsi.csv file
    # database name
    database_name = file
    # path to drop-jump folder
    path_to_folder = "data/"

    # select a signal file to run
    signal_filepath = path_to_folder + database_name + ".csv"

    return signal_filepath


## Loads data from a given datapath into a pandas matrix
def load_Data(path):
    """
    :param path: Path to the CSV file
    :return: DataFrame with one row per sample
    """

    # Data from the csv file is turned into a pandas matrix
    data = open(path)
    dataframe = pd.read_csv(data)
    data.close()

    return dataframe

## Types of shots made in the game
def shotType(dataframe):
    """
    :param dataframe: Data of Rocket League Data
    :return: Dataframes for the following skillshot: noise, ceiling shot, power shot,
    air dribble, front flick, & musty flick
    """
    # Dataframes for each shot category
    frame_Noise = dataframe[dataframe['SequenceLabel'] == -1]
    frame_Ceiling = dataframe[dataframe['SequenceLabel'] == 1]
    frame_Power = dataframe[dataframe['SequenceLabel'] == 2]
    frame_Wave = dataframe[dataframe['SequenceLabel'] == 3]
    frame_Dribble = dataframe[dataframe['SequenceLabel'] == 5]
    frame_Fflick = dataframe[dataframe['SequenceLabel'] == 6]
    frame_Mflick = dataframe[dataframe['SequenceLabel'] == 7]

    return frame_Noise, frame_Ceiling, frame_Power, frame_Wave, frame_Dribble, frame_Fflick, frame_Mflick
##
data = dataName("RL_data")
load = load_Data(data)


actions = ["jump", "boost", "slide"]
rows = []

for _, group in load.groupby("SequenceNumber"):
    first = {
        action: group.loc[group[action] > 0, "Time"].min()
        for action in actions if (group[action] > 0).any()
    }
    sequence = " > ".join(sorted(first, key=first.get)) or "None"
    rows.append((group["SequenceLabel"].iloc[0], sequence))

table = pd.crosstab([row[0] for row in rows], [row[1] for row in rows])
chi2, p, _, _ = chi2_contingency(table)
print(table)
print(f"Chi-square p-value: {p:.4f}")