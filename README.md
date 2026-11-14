# ENGR315-RocketLeague: Rocket League Player Speed and Skillshot Analysis
## Team Name and Names of the Contributors (sub-task-1)
### Team Name: Team 10
### Group Members:
* Daniel Teach
* Calvin Lin
* Logan McElwain
## Objective and Motivation: (sub-task-2)
### Dataset Details:
* **Background:** This is a dataset about a video game called Rocket League, tracking player inputs and in-game data while players performed different advanced moves or skillshots.
* **Variables (19 total):** Ball Acceleration, Time, (Car) Distance Wall, DistanceCeil, DistanceBall, PlayerSpeed, BallSpeed, up, accelerate, slow, goal, left, boost, camera, down, right, slide, jump, and sequencelabel.
* **Purpose:** Created to study action sequence analysis and model how players execute specific video game skills, helping us understand how physical player controls correlate with successful in-game tricks.
### Selected Questions & Expected Answers:
1. **Can player input timings (jump/boost) accurately predict which specific skillshot is being performed?**
   * *Expected Answer / Analysis:* We expect to analyze the jump and boost timings associated with each skillshot category to identify distinct input patterns. We can compare the mean, median, maximum, and minimum input timings for each category to determine whether these patterns can help predict which skillshot is being performed.
2. **Do certain player action sequences repeat consistently across different players performing the same trick, or is there high variance in individual playstyles?**
   * *Expected Answer / Analysis:* We expect to compare the sequences of player actions (jump, boost, dodge, etc.) across different players performing the same skillshot. We will place these sequences in bins and perform a chi-square shot to see if the results are statistically significant.
3. **How effectively can we cluster unlabelled failed attempts away from successful trick categories based solely on movement and ball metric features?**
   * *Expected Answer / Analysis:* We plan to use a clustering sort of K-means, which will be based on player movement and ball metrics, including ball velocity, player velocity, acceleration, etc. We will examine whether failed attempts form distinct clusters from successful skillshot categories. Then use silhouette scores and compare the resulting clusters against the known success/failure categories to see if there's a significant difference between the shots.
## Introduction/Context of project: 
Rocket League is a video game where the user controls a car across a variety of game modes. Most Rocket League game modes are similar to soccer, where competing teams try to score on the opponent's net. Since the game was released in 2015, players have developed a variety of popular in-game mechanics. We will be looking at the inputs players make when attempting these mechanics to answer our questions.
## Implementation Details: (sub-task-3 and sub-task-4)
### Methods, Metrics, Tools, and Plots:
* **Metrics to Calculate:** Maximum ball velocity, initial/average player speed, speed distributions, duration of shot, jump, boost, acceleration, speed over time intervals, etc. (All variables in the dataset are going to be used)
* **Tools / Python Packages:** Python pandas, NumPy, and Matplotlib/Seaborn for data manipulation, statistical binning, chi-square analysis, K-means, silhouette scores, and time-series plotting.
* **Planned Visualizations:**
* For Q1. Box plot
  * X-axis: Skillshot category (Musty, Flip Reset, Aerial, etc.).
  * Y-axis: Input timing (seconds).
  * Separate graphs: One for jump timing and one for boost timing, etc.
 
* For Q2. Histogram
  * X-axis: Action sequence (Jump → Boost, Jump → Dodge, Jump → Boost → Dodge, etc.).
  * Y-axis: Frequency of occurrence.
  * Bar colors/label: Different players or skillshot categories.
  * Chi-square test: observed graph vs. expected counts graph

* For Q3. Scatter plot
  * X-axis: First principal component (variable with the most difference in dataset).
  * Y-axis: Second principal component (second most difference in dataset).
  * Colors: Different K-means clusters.
  * Markers: Distinguish successful and failed attempts after clustering.
## Results (Answers to the Questions): (sub-task-6)

For question 1, the  Python code aims to determine whether the timing of jump and boost inputs can help us differentiate between different types of Rocket League skillshots. To do this, we categorized our data into the six skillshot types listed in the research: Air Dribble, Ceiling Shot, Front Flick, Musty Flick, Power Shot, and Wave Dash. Based on this data, we were able to calculate the mean, median, maximum, and minimum, then use those values to predict whether a certain data point fit into one of our shot categories. With those predictions, we were able to get the accuracy by comparing the predicted category to the actual skillshot type. 

<img width="1000" height="600" alt="Jump Time By Skillshot Figure 1" src="https://github.com/user-attachments/assets/9ca8dac4-84d3-4c86-9587-0d97aaa89ace" />
Figure 1. Box plot of jump timing for each type of skill shot.

<img width="1000" height="600" alt="Boost Time By Skillshot Figure 2" src="https://github.com/user-attachments/assets/a5b774d3-9448-4064-a88b-5024c7076f21" />
Figure 2. Box plot of boost timing for each type of skill shot.

<img width="1000" height="600" alt="Average Jump and Boost Timing by Skillshot Figure 3" src="https://github.com/user-attachments/assets/4b659d14-8354-42ce-9f78-8e8ed640c7e2" />
Figure 3. Bar chart of average jump and boost timing for each type of skill shot.

Graph overview:

From this data, we found that generally the jump timing and boost timing for each of our skill shots were relatively the same, with similar lower and upper quartile ranges and means. Additionally, we noticed that the jump timing for shots such as the Musty Flick and Power Shot had many outliers, unlike the other shots. This may be due to how these shots allow for greater variation in inputs compared to the rest of the shots. However, for boost timings, there were no significant outliers in our data to note. Overall, other than a couple of outliers, we found that there was no discernible difference in jump timing between shots. 

However, looking at the averages, we noticed that there were notable differences for shot types between jump and boost timings. This may be caused by the outliers in our data; shots such as the Musty Flick and Power Shots had a lot more outliers than the rest when it came to jump timing. Notable data points were the boost timing of the Ceiling shot, which had an average of 0.784 seconds, and Wave Dash, which had a jump time of 0.812 seconds. 

For question 2:
WIP

## Conclusions: (sub-task-7)
Just have the title as a placeholder to be populated later
## Actions that need to be completed:
* [ ] Clean and preprocess the raw Rocket League CSV dataset.
* [ ] Write initial Python scripts to parse variables (`BallSpeed`, `PlayerSpeed`, `sequencelabel`).
* [ ] Generate statistical distribution plots for Question 1.
* [ ] Perform chi-square contingency analysis for Question 2 speed categories.
* [ ] Implement time-series plotting scripts for Question 3.
* **Current Hurdles:** Handling missing or noisy sequence label formatting in the raw dataset.
## References / Source files:
* Rocket League Action Sequence Dataset (Course-provided dataset source).
* Python documentation for Pandas, NumPy, and Matplotlib.
