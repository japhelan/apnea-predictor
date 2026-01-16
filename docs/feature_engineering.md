# Feature Engineering Log

1/15/26

Starting with the Demographics subset

- all columns with >80% missing are not being considered right now

## Initial Notes

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
