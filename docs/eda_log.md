# EDA 1.0 LOG

observations, changes, notes, questions, etc.

Subset checklist

- [X] demographics
- [X] health
- [X] medhx
- [X] sleep patterns
- [X] parasomnias
- [X] restless leg syndrome (rls)
- [X] narcolepsy (narc)
- [X] insomnia
- [ ] sleep questionss
- [ ] sleep treatment

# Demographics Notes

- height in feet, height in inches, weight, and bmi are all different features and a subset should be selected. this will require more analysis later but is worth noting now.
- Need to combine work and school columns
- not going to mess with the columns related to people in the household as of right now, maybe in the future.

New columns made:

- day_start_time: datetime, what time school/work starts
- varying_day_start_time: yes/no; does the time your day start change
- day_end_time: datetime, when does school/final shift start
  - if needed go back and look at how this is calculated in relation to all 3 shifts potentially
- days_per_week_at_work_or_school: intuitive really

cut participants*ethnicity*(hispanic*or_latino)', 'participants_ethnicity*(sub_hispanic_or_latino_origin)',

'participants*race*(main)', 'participants*race*(sub)', 'english_as_native_language' , 'participants_proficiency_in_english' as they are either not important and/or could lead to unethical biases

# Health Notes

2/25

- the time frame features are associated with the count features, as in they mean if the count is over a week/month i think.
- Categories for time of snack2-5 and usually yes/no snack2-5 will most likely be removed as they are sparsley answered and not very related to what I am looking to solve (i think)
- as mentioned above the feature diet_0340 is only 1 value and should probably be removed
- alcohol consumption features should probably be condensed as they are sparse and dont give a lot of info directly
- same with cigarettes  and less so recreational drugs sets
- look into correlation with survey answers ; if problematic then figure that out later
- the usual meal time data might be kind of useless / overlap with the wake up go to bed time data from demographics; look into

changes made as of now: dropped diet_0340.

NEXT STEP: bivariate/multivariate stuff, correlation heatmaps and stuff

2/26

Correlation Notes

- Fatigue questionnares total score has high correlation with a lot of the columns. Perhaps best to remove that and then perhaps condense the subquestions
- Same with GAD questionnaire
- usual meal time features are highly correlated; maybe has to do with nulls?
- also some crossover between some questionnaires total score and other subquestions

Changes will be made in first set of feature engineering, but for now will keep everything. first action will be to remove the total_score columns of all the quests and rerun the correlation scores.

# Mdhx Notes

2/26

the only notes here is of a column that has 98% missing and 1 unique response. features of family history of depression/anxiety/ psychiatric care are correlated moderatley but those also make sense. maybe will be condensed later

right now changes made: ('dialysis_self-reported', 'mdhx_6420') removed

# Sleep Patterns Notes

2/28

- latency colums have hours and minutes; at the very least combine but they may just end up dropped
- this subset has multiple shift columns as well; will be dropped for the same reasons + for continuity with the demographics subset
- ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_3rd_shift', 'sched_1700') and ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_3rd_shift', 'sched_1800') are the same feature. i don't know how this happened
  - ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_3rd_shift_varies', 'sched_1701') and ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_3rd_shift_varies', 'sched_1801') have the same issue

Changes made initially

- coalesced bed time data split across current, next, third shift into one big column as later levels were very sparse
  - dropped the columns used to make this new column + duplicates
- simplified naming convention of all bed time features in the subset
  - info on all of these will be found in post 1.0 eda data dictionary
- also unified quality, latency, duration, nap + weekend variation features
- now 34 columns : )

TODO FOR NEXT TIME: slp pattern type changes + correlation checks DONE

3/2

correlation notes

- slp quality non work and work nights highly correlated
- alot of the time in bed / out bed permeations are correlated, especially when the only difference is work/non work day
- isq questions of feeling sleep is not sound and unrefreshing are very similar

not changing anything now, but will most likely be rearranged into new features later.

# Parasomnia notes

changing some columns to booleans but other than that pretty standard.

- ('acting_out_dreams_age_of_the_first_episode_dont_know', 'par_0531') is 100% missing when -55 (placeholder NaN) is replaced with a real nan. will be dropped for hopefully self explanitory reasons.
  - also ("violent_behavior_during_sleep_age_of_the_first_episode_dont_know","par_0631",)
- alot of correlation between the age of first episode columns across each of the parasomnias. considering how sparse this data is anyway i suppose it makes sense. will be handled later becasue I am sure the features will be condensed anyway.

# RLS Notes

- one column ('unpleasant_feelings_in_legs_age_of_the_first_episode_(present_and_past)_dont_know', 'rls_0801') was entirely missing so it was removed
- ('restless_legs_syndrome_(rls)_current_probability', 'rls_probability') should be encoded into numbers at some pointer later
  - the algorithm for determing probability is in the data dictionary : )
  - i am going to one hot encode it for now so correlation can be done upon it but this will most likely be changed somehow in future iterations
- from correlation:
  - two columns are fully correlated (rls_0500 and rls_0310)
  - the probability columns have a lot of semi correlation, most likely because it is algorithmically determined pretty directly. will figure out what to do with this later

# Narc Notes

dropped ('muscle_weakness_month_of_the_first_episode', 'narc_1710') for being completley useless

correlation notes:

- tons of highly correlated features here, between symtomps of narcolepsy/muscle weekness and their past and present variations. like way too many.
  - will cull a lot of these to alleviate the issue and check after

# Insomnia Notes

a row has 99 in the column ('self-reported_number_of_awakenings_on_week_nights_school_nights_work_nights_or_days_current_shift', 'sched_2400'). just a note.

the tab_xxxx features are how often you think about (something) in bed

time frame features refer to weekly/monthly amounts of whatever the assoicated (number) feature is

condensed the shift sleep data again

correlation similarities

- as expected, similarities between the school/nonschool nights + columns that just sound similar + rumination group columns

# Sleep Questionnaire Notes

todo: this
