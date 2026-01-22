# Feature Engineering Log

1/15/26

Starting with the Demographics subset

- all columns with >80% missing are not being considered right now

## Demographic Notes (v1.0)

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

## Lifestyle Notes (v1.0)

- lots of these are surveys and are therefore highly correlated
- lots of diet columns that should be fixed
- going to split each survey into its own subset as I believe it will be useful later
- Dropped the following columns:

  - 'usual_additional_meal/snack_time1', 'usually_no_additional_meal/snack1', 'usual_additional_meal/snack_time2', 'usually_no_additional_meal/snack2', 'usual_additional_meal/snack_time3', 'usually_no_additional_meal/snack3', 'usual_additional_meal/snack_time4', 'usually_no_additional_meal/snack4', 'usual_additional_meal/snack_time5', 'usually_no_additional_meal/snack5', 'percentage_of_snack_2_among_all_food_intake_over_24_hours', 'percentage_of_snack_3_among_all_food_intake_over_24_hours', 'percentage_of_snack_4_among_all_food_intake_over_24_hours', 'percentage_of_snack_5_among_all_food_intake_over_24_hours', 'percentage_of_breakfast_among_all_food_intake_over_24_hours', 'percentage_of_lunch_among_all_food_intake_over_24_hours', 'percentage_of_dinner_among_all_food_intake_over_24_hours', 'percentage_of_snack_1_among_all_food_intake_over_24_hours', 'food_intake_no_regular_meals'
    - I didn't think any of these would be useful and most had high null pcts
- Changes made:

  - renamed dry_and/or_irritated_eyes to dry_and_or_irritated_eyes_days_per_week for clarity and unity
  - subsetted the fss, gad7, phq9, and nose surveys
  - dropped the above columns

## Medical History Notes (v1.0)

- Changes made:
  - Removed 'genetic_testing_source_self-reported', 'dialysis_self-reported', 'dentures_removed_while_sleeping_self-reported' as they had extremely low numbers of present values
