from pathlib import Path

import pandas as pd

## Function for finding the filepath of the csv
def dataName(file):
    ## Find the CSV file in the project's data folder
    return Path(__file__).resolve().parent / "data" / f"{file}.csv"


## Loads data from a given datapath into a pandas matrix
def load_Data(path):
    """
    :param path: Path to the CSV file
    :return: DataFrame with one row per sample
    """

    ## Read the CSV file into a pandas DataFrame
    return pd.read_csv(path)

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
if __name__ == "__main__":
    data = dataName("RL_data")
    load = load_Data(data)
    print(load)
