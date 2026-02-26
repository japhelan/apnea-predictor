# EDA 1.0 LOG

observations, changes, notes, questions, etc.

# Demographics Subset

## Feature Classification

### Categories

#### Nominal Categories

- (participants_sex, dem_0500)

#### Ordinal Categories

- (time_school_or_work_starts, sched_9910)
- (time_school_or_work_ends, sched_9920)

#### Binary Categories

- (irregular_schedule, sched_9910)

### Measures

#### Discrete Measures

- (participants_age, modified_dem_0110) - Ratio
- (height_in_inches, dem_0610) - Ratio
- (number_of_people_living_in_your_household, bthbts_0500) - Ratio
- (number_of_children_aged_5_years_or_younger_living_in_your_household, bthbts_0510) - Ratio
- (number_of_children_aged_6_17_living_in_your_household, bthbts_0520) - Ratio
- (number_of_adults_aged_18_59_living_in_your_household, bthbts_0530) - Ratio
- (number_of_adults_aged_60_years_of_older_living_in_your_household, bthbts_0540) - Ratio
- (days_per_week_in_school_or_work, sched_9900) - Ratio

#### Continuous Measures

- (body_mass_index_(bmi), dem_0800) - Ratio
- (weight_in_pounds, dem_0700) - Ratio

## Demographics Notes

# Health Subset

## Feature Classification

### Categories

#### Nominal Categories

- excercise time of day (soclhx_0600)
- ('street_or_recreational_drugs_consumption_ever', 'soclhx_1500')
- ('self-perception_of_weight', 'diet_0700')

#### Ordinal Categories

- All nose columns
  - ('nasal_congestion_or_stuffiness', 'nose_0100')
  - ('nasal_blockage_or_obstruction', 'nose_0200')
  - ('trouble_breathing_through_nose', 'nose_0300')
  - ('trouble_sleeping', 'nose_0400')
  - ('unable_to_get_enough_air_through_nose_during_exercise_or_exertion', 'nose_0500')
  - ('nose_total_score', 'nose_0600')
- All OSA columns
  - ('heartburn_or_belching_after_going_to_bed_days_per_week', 'osa_0100') - neveronlyfreq5dk
  - ('perspire_heavily_during_the_night_days_per_week', 'osa_0200') - neveronlyfreq5dk
  - ('dry_and/or_irritated_eyes', 'osa_0300') - neveronlyfreq5dk
- All PHQ Columns
  - ('patient_health_questionnaire_9_little_interest_or_pleasure_in_doing_things', 'phq_0100')
  - ('patient_health_questionnaire_9_feeling_down_depressed_or_hopeless', 'phq_0200')
  - ('patient_health_questionnaire_9_trouble_falling_or_staying_asleep_or_sleeping_too_much', 'phq_0300')
  - ('patient_health_questionnaire_9_feeling_tired_or_having_little_energy', 'phq_0400')
  - ('patient_health_questionnaire_9_poor_appetite_or_overeating', 'phq_0500')
  - ('patient_health_questionnaire_9_feeling_bad_about_yourself', 'phq_0600')
  - ('patient_health_questionnaire_9_trouble_concentrating', 'phq_0700')
  - ('patient_health_questionnaire_9_moving_or_speaking_slowly', 'phq_0800')
  - ('patient_health_questionnaire_9_thought_you_would_be_better_off_dead', 'phq_0900')
  - ('patient_health_questionnaire_9_total_score', 'phq_1000')
- All GAD Columns
  - ('generalized_anxiety_disorder-7_questionnaire_feeling_nervous_anxious_or_on_edge','gad_0100')
  - ('generalized_anxiety_disorder-7_questionnaire_not_being_able_to_stop_or_control_worrying','gad_0200')
  - ('generalized_anxiety_disorder-7_questionnaire_worrying_too_much_about_different_things','gad_0300')
  - ('generalized_anxiety_disorder-7_questionnaire_trouble_relaxing','gad_0400')
  - ('generalized_anxiety_disorder-7_questionnaire_being_so_restless_that_it_is_hard_to_sit_still','gad_0500')
  - ('generalized_anxiety_disorder-7_questionnaire_becoming_easily_annoyed_or_irritable','gad_0600')
  - ('generalized_anxiety_disorder-7_questionnaire_feeling_afraid_as_if_something_awful_might_happen','gad_0700')
  - ('generalized_anxiety_disorder-7_questionnaire_total_score','gad_0800')
- All FSS Columns
  - ('fatigue_severity_scale_motivation_is_lower_when_fatigued','fss_0100')
  - ('fatigue_severity_scale_exercise_brings_on_fatigue','fss_0200')
  - ('fatigue_severity_scale_i_am_easily_fatigued','fss_0300')
  - ('fatigue_severity_scale_fatigue_interferes_with_physical_functioning','fss_0400')
  - ('fatigue_severity_scale_fatigue_causes_frequent_problems_for_me','fss_0500')
  - ('fatigue_severity_scale_my_fatigue_prevents_sustained_physical_functioning','fss_0600')
  - ('fatigue_severity_scale_fatigue_interferes_with_carrying_out_certain_duties_and_responsibilities','fss_0700')
  - ('fatigue_severity_scale_fatigue_is_among_my_three_most_disabling_symptoms','fss_0800')
  - ('fatigue_severity_scale_fatigue_interferes_with_my_work_family_or_social_life','fss_0900')
  - ('fatigue_severity_scale_total_score','fss_1000')
- ('eating_impact_on_alertness/wakefulness', 'diet_0400')
-

#### Binary Categories

- excercise rarely or never
- alcohol consumption, rarely or never
- ('caffeine_consumption_rarely_or_never', 'soclhx_0901')
- ('cigarette_smoking_time_frame', 'soclhx_1310') (per day/week)
- alcohol consumption time frame (week/month)
- excercise time frame (early morning) (soclhx_0520)
- ('routinely_travel_to_other_time_zones', 'cir_0100')
- Have some nulls in as -44 but otherwise binary:
  - ('feel_more_alert_if_skip_lunch', 'diet_0500')
  - ('sleep_less_soundly_if_skip_dinner', 'diet_0600')
- ('usually_no_breakfast', 'diet_0801')
- ('usually_no_lunch', 'diet_0811')
- ('usually_no_dinner', 'diet_0821')
- ('cigarette_smoking_never_smoker', 'never_cigarette_smoker')
- ('cigarette_smoking_former_smoker', 'former_cigarette_smoker')
- ('smokeless_user_former_smoker', 'former_smokeless_user')
- ('cigarette_smoking_current_smoker', 'current_cigarette_smoker')
- ('smokeless_user_current_smoker', 'current_smokeless_user')

#### Time Data

- ('caffeine_consumption_time_of_last_drink', 'soclhx_1000')
- ('usual_breakfast_time', 'diet_0800')
- ('usual_lunch_time', 'diet_0810')
- ('usual_dinner_time', 'diet_0820')

### Measures

#### Discrete Measures

- bed partner or roomate
- alcohol consumption # of times
- ('alcohol_consumption_number_of_servings_per_day', 'soclhx_0730')
- ('caffeine_consumption_number_of_servings_per_day', 'soclhx_0900')
- ('cigarette_smoking_age_started', 'soclhx_1200')
- ('cigarette_smoking_number_of_cigarettes', 'soclhx_1300')
- ('cigarette_smoking_age_stopped', 'soclhx_1400')
- ('street_or_recreational_drugs_consumption_age_started', 'soclhx_1700')
- ('street_or_recreational_drugs_consumption_age_stopped', 'soclhx_1800')
- ('percentage_of_breakfast_among_all_food_intake_over_24_hours', 'diet_0300')
- ('percentage_of_lunch_among_all_food_intake_over_24_hours', 'diet_0310')
- ('percentage_of_dinner_among_all_food_intake_over_24_hours', 'diet_0320')
- ('percentage_of_snack_1_among_all_food_intake_over_24_hours', 'diet_0330')
  - ('percentage_of_snack_2_among_all_food_intake_over_24_hours', 'diet_0350')
  - ('percentage_of_snack_3_among_all_food_intake_over_24_hours', 'diet_0360')
  - ('percentage_of_snack_4_among_all_food_intake_over_24_hours', 'diet_0370')
  - ('percentage_of_snack_5_among_all_food_intake_over_24_hours', 'diet_0380')

#### Continuous Measures

#### Unsure

- ('food_intake_no_regular_meals', 'diet_0340'): only 1 value

## Health Notes

2/25

- the time frame features are associated with the count features, as in they mean if the count is over a week/month i think.
- Categories for time of snack2-5 and usually yes/no snack2-5 will most likely be removed as they are sparsley answered and not very related to what I am looking to solve (i think)
