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
   * *Expected Answer / Analysis:* We expect to find the mean, median, max, and min ball velocities for each skill shot category to see distinct velocity signatures[cite: 4].
2. **Do certain player action sequences repeat consistently across different players performing the same trick, or is there high variance in individual playstyles?**
   * *Expected Answer / Analysis:* By categorizing speeds into low, medium, and high bins, we can use chi-square tests to determine if there is a statistically significant difference in player speed distributions across different skillshots[cite: 5].
3. **How effectively can we cluster unlabelled failed attempts away from successful trick categories based solely on movement and ball metric features?**
   * *Expected Answer / Analysis:* Tracking speed over time will show distinct motion phases (like accelerating vs. steady trajectories), highlighting that power shots exhibit higher peak acceleration compared to aerials and flicks[cite: 6].
## Introduction/Context of project: 
This section isn’t mandatory, but if you feel like some content needs to be introduced in order to understand the methods and questions, please add all the necessary details here.
## Implementation Details: (sub-task-3 and sub-task-4)
### Methods, Metrics, Tools, and Plots:
* **Metrics to Calculate:** Maximum ball velocity, initial/average player speed, speed distributions, and speed over time intervals.
* **Tools / Python Packages:** Python pandas, NumPy, and Matplotlib/Seaborn for data manipulation, statistical binning, chi-square analysis, and time-series plotting.
* **Planned Visualizations:** 
  * Frequency distribution curves of maximum ball velocity by skillshot[cite: 4].
  * Stacked bar charts showing low, medium, and high speed categories per skillshot label[cite: 4, 5].
  * Time-series line graphs tracking player speed trajectories over time[cite: 6].
## Results (Answers to the Questions): (sub-task-6)
Just have the title as a placeholder to be populated later
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
