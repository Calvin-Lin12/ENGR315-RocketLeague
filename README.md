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
   * *Expected Answer / Analysis:* Compare action-sequence bins across skillshots with a chi-square test of independence. Player-level conclusions require player identifiers in the dataset.
3. **How effectively can multivariate linear regression use player movement and ball metrics to predict the success of a Rocket League shot, and which variables have the greatest influence on the predicted outcome?**
   * *Expected Answer / Analysis:* We plan to use multivariate linear regression to determine how player movement and ball metrics relate to shot success or failure. Then, analyze the regression coefficients to identify which variables have the strongest positive or negative relationships with a successful shot. We will also evaluate the model using \(R^2\) to determine how much variation in shot outcomes can be explained by the selected gameplay features.
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
 
* For Q2. Action-sequence bar charts
  * X-axis: Action sequence (Jump → Boost, Jump → Slide, etc.).
  * Y-axis: Percentage of attempts for each skillshot.
  * Chi-square test of independence compares skillshot with jump/boost order (jump first, boost first, or other).

* Q3. Regression Coefficient Plot
  * X-axis: Standardized regression coefficients.
  * Y-axis: Gameplay variables (ball speed, player speed, acceleration, distance to ball, etc.).
  * Bars: Show the strength and direction of each variable's relationship with shot success.
## Results (Answers to the Questions): (sub-task-6)
### Question 1: Jump and Boost Timing
For question 1, the  Python code aims to determine whether the timing of jump and boost inputs can help us differentiate between different types of Rocket League skillshots. To do this, we categorized our data into the six skillshot types listed in the research: Air Dribble, Ceiling Shot, Front Flick, Musty Flick, Power Shot, and Wave Dash. Based on this data, we were able to calculate the mean, median, maximum, and minimum, then use those values to predict whether a certain data point fit into one of our shot categories. With those predictions, we were able to get the accuracy by comparing the predicted category to the actual skillshot type. 

<img width="500" height="300" alt="Jump Time By Skillshot Figure 1" src="https://github.com/user-attachments/assets/9ca8dac4-84d3-4c86-9587-0d97aaa89ace" />

Figure 1. Box plot of jump timing for each type of skill shot.

<img width="500" height="300" alt="Boost Time By Skillshot Figure 2" src="https://github.com/user-attachments/assets/a5b774d3-9448-4064-a88b-5024c7076f21" />

Figure 2. Box plot of boost timing for each type of skill shot.

<img width="500" height="300" alt="Average Jump and Boost Timing by Skillshot Figure 3" src="https://github.com/user-attachments/assets/4b659d14-8354-42ce-9f78-8e8ed640c7e2" />

Figure 3. Bar chart of average jump and boost timing for each type of skill shot.

Graph overview:

From this data, we found that generally the jump timing and boost timing for each of our skill shots were relatively the same, with similar lower and upper quartile ranges and means. Additionally, we noticed that the jump timing for shots such as the Musty Flick and Power Shot had many outliers, unlike the other shots. This may be due to how these shots allow for greater variation in inputs compared to the rest of the shots. However, for boost timings, there were no significant outliers in our data to note. Overall, other than a couple of outliers, we found that there was no discernible difference in jump timing between shots. 

However, looking at the averages, we noticed that there were notable differences for shot types between jump and boost timings. This may be caused by the outliers in our data; shots such as the Musty Flick and Power Shots had a lot more outliers than the rest when it came to jump timing. Notable data points were the boost timing of the Ceiling shot, which had an average of 0.784 seconds, and Wave Dash, which had a jump time of 0.812 seconds. 

---

### Question 2: Action-Order Sequences
For question 2, the dataset has 255 attempts across six skillshots, but it does not say which player made each attempt. We therefore cannot confirm whether each sequence came from a different player. If we assume each sequence represents a different player, we can compare their action orders by skillshot. We grouped sequences by whether jump came before boost, boost came before jump, or the attempt did not include both actions. A chi-square test showed that the action-order patterns differed across skillshots: X²(10) = 67.91, p = 1.12 × 10⁻¹⁰, with Cramér's V = 0.365. Three of the 18 expected counts were below 5 (16.7%), and none were below 1.

Figures 4-9 show the action-sequence percentages for each skillshot.

<table>
  <tr>
    <td><img width="450" alt="Action sequences for Air Dribble" src="https://github.com/user-attachments/assets/ebe20e7e-de4c-434e-891c-a2158276d26a" /><br>Figure 4. Action sequences for Air Dribble.</td>
    <td><img width="450" alt="Action sequences for Ceiling Shot" src="https://github.com/user-attachments/assets/9f7fe59e-7f31-4878-9d18-4e82d3615528" /><br>Figure 5. Action sequences for Ceiling Shot.</td>
  </tr>
  <tr>
    <td><img width="450" alt="Action sequences for Front Flick" src="https://github.com/user-attachments/assets/5a56cbfa-953c-490c-8e30-5860247579df" /><br>Figure 6. Action sequences for Front Flick.</td>
    <td><img width="450" alt="Action sequences for Musty Flick" src="https://github.com/user-attachments/assets/7b3bbf6a-67c1-4b5b-a94f-1ef2f8f80b03" /><br>Figure 7. Action sequences for Musty Flick.</td>
  </tr>
  <tr>
    <td><img width="450" alt="Action sequences for Power Shot" src="https://github.com/user-attachments/assets/859f6b06-d963-4529-a505-23ec097fae5f" /><br>Figure 8. Action sequences for Power Shot.</td>
    <td><img width="450" alt="Action sequences for Wave Dash" src="https://github.com/user-attachments/assets/2aefd802-e8b5-4ec4-aec2-777d6633664d" /><br>Figure 9. Action sequences for Wave Dash.</td>
  </tr>
</table>

As shown in Figures 4-9, the action order differed by trick. Assuming each sequence came from a different player, boost came before jump in 75.6% of Air Dribble attempts. Jump came first in 63.3% of Ceiling Shots, 58.7% of Front Flicks, 52.8% of Musty Flicks, and 65.0% of Power Shots. Wave Dash attempts were more spread across the groups, with 39.5% in the other group. This suggests that players often use a similar broad action order for some tricks, while the most common order depends on the trick. This conclusion assumes each sequence comes from a different player; the dataset does not confirm this. The chi-square result shows differences across tricks, but does not by itself measure how much players' individual styles vary.

---

### Question 3: Multivariate Linear Regression 
Question 3 looks at all 298 attempts for the seven categories in the data. The original data was organized and grouped by SequenceLabel; these values were converted to boolean values, a value of 0 meant the data was "noise" (the shot failed), and labels 1-7 were relabeled as successful shots and given a value of 1. The predictions were made by utilizing the regression coefficient of least squares. The values >= 0.5 were considered successful shots and values that were below that were predicted to be failed. 

Regression Results:
R-squared: 0.2952
Prediction Accuracy: 88.93 %

- **Positive coefficient:** Associated with a higher predicted outcome (success).
- **Negative coefficient:** Associated with a lower predicted outcome (success).

TABLE 1: Table of regression coefficients for each gameplay variable.
| Gameplay Variable | Regression Coefficient |
|---|---:|
| Up | +0.1932 |
| Slow | +0.1757 |
| Jump | +0.0829 |
| Time | +0.0587 |
| Ball Acceleration | +0.0564 |
| Ball Speed | +0.0561 |
| Right | +0.0276 |
| Accelerate | +0.0210 |
| Left | +0.0151 |
| Goal | +0.0145 |
| Distance to Ball | +0.0122 |
| Distance to Ceiling | +0.0118 |
| Camera | -0.0057 |
| Player Speed | -0.0114 |
| Boost | -0.0331 |
| Slide | -0.0379 |
| Down | -0.0426 |
| Distance to Wall | -0.0725 |

**Table 2.** Comparison of actual outcomes and regression predictions.

| Actual Outcome | Predicted Failed (0) | Predicted Successful (1) | Total |
|---|---:|---:|---:|
| Failed (0) | 11 | 32 | 43 |
| Successful (1) | 1 | 254 | 255 |
| **Total** | **12** | **286** | **298** |

<table>
<img width="1000" height="700" alt="8174bd61-d169-4508-a2a1-725fa40e28cf" src="https://github.com/user-attachments/assets/d86bd5e2-52e3-400a-9d1a-f71b17ab03d5" />
Figure 10. Graph of regression coefficients for each gameplay variable.
<table>

From the data, we found that factors `Up` and `Slow` have the strongest positive coefficients, suggesting that these variables are associated with higher predicted success. `Distance to Wall` has the strongest negative coefficient, suggesting that increasing distance from the wall is associated with lower predicted success. However, these relationships indicate correlation, not necessarily cause-and-effect relationships. Additionally, even though the prediction accuracy was 88.93%, our R-squared was 0.2952. Since the R-squared value was low, it suggests that the high accuracy may be due to there being more successful shots in the original dataset than unsuccessful ones, leading to better prediction of successful attempts than failed ones. 
  
...

## Conclusions: (sub-task-7)
Just have the title as a placeholder to be populated later
## Actions that need to be completed:
* [ ] Clean and preprocess the raw Rocket League CSV dataset.
* [ ] Write initial Python scripts to parse variables (`BallSpeed`, `PlayerSpeed`, `SequenceLabel`).
* [ ] Generate statistical distribution plots for Question 1.
* [ ] Perform chi-square contingency analysis for Question 2 speed categories.
* [ ] Implement time-series plotting scripts for Question 3.
* **Current Hurdles:** Handling missing or noisy sequence label formatting in the raw dataset.
## References / Source files:
* Rocket League Action Sequence Dataset (Course-provided dataset source).
* Python documentation for Pandas, NumPy, and Matplotlib.
