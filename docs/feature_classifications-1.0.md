# Feature Classification (Pre EDA-1.0)

# Demographics Subset

## Categories

### Nominal Categories

- (participants_sex, dem_0500)

### Ordinal Categories

- (time_school_or_work_starts, sched_9910)
- (time_school_or_work_ends, sched_9920)

### Binary Categories

- (irregular_schedule, sched_9910)

## Measures

### Discrete Measures

- (participants_age, modified_dem_0110) - Ratio
- (height_in_inches, dem_0610) - Ratio
- (number_of_people_living_in_your_household, bthbts_0500) - Ratio
- (number_of_children_aged_5_years_or_younger_living_in_your_household, bthbts_0510) - Ratio
- (number_of_children_aged_6_17_living_in_your_household, bthbts_0520) - Ratio
- (number_of_adults_aged_18_59_living_in_your_household, bthbts_0530) - Ratio
- (number_of_adults_aged_60_years_of_older_living_in_your_household, bthbts_0540) - Ratio
- (days_per_week_in_school_or_work, sched_9900) - Ratio

### Continuous Measures

- (body_mass_index_(bmi), dem_0800) - Ratio
- (weight_in_pounds, dem_0700) - Ratio

# Health Subset

## Categories

### Nominal Categories

- excercise time of day (soclhx_0600)
- ('street_or_recreational_drugs_consumption_ever', 'soclhx_1500')
- ('self-perception_of_weight', 'diet_0700')

### Ordinal Categories

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

### Binary Categories

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

### Time Data

- ('caffeine_consumption_time_of_last_drink', 'soclhx_1000')
- ('usual_breakfast_time', 'diet_0800')
- ('usual_lunch_time', 'diet_0810')
- ('usual_dinner_time', 'diet_0820')

## Measures

### Discrete Measures

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

### Continuous Measures

### Unsure

- ('food_intake_no_regular_meals', 'diet_0340'): only 1 value

# Medhx Subset

## Categories

### Nominal Categories

- None

### Ordinal Categories

- ('menopausal_status', 'mdhx_1300')
- ('number_of_full_siblings_from_the_same_birth_parents', 'famhx_1300')

### Binary Categories

- All other categories are binary:
- ('pregnancy_current','mdhx_1200')
- ('oophorectomy_bilateral_self-reported','mdhx_1400')
- ('hypertension_self-reported','mdhx_5700')
- ('congestive_heart_failure_self-reported','mdhx_5710')
- ('cardiovascular_problem_other_self-reported','mdhx_5720')
- ('asthma_self-reported','mdhx_5800')
- ('chronic_obstructive_pulmonary_disease_self-reported','mdhx_5810')
- ('pulmonary_problem_other_self-reported','mdhx_5820')
- ('allergies_or_sinus_problems_self-reported','mdhx_5900')
- ('tonsillectomy_or_adenoidectomy_self-reported','mdhx_5910')
- ('nasal_jaw_or_apnea_surgery_self-reported','mdhx_5920')
- ('ear_nose_and_throat_problem_or_surgery_other_self-reported','mdhx_5950')
- ('dental_problems_self-reported','mdhx_6000')
- ('dentures_removed_while_sleeping_self-reported','mdhx_6030')
- ('gastrointestinal_problem_or_surgery_self-reported','mdhx_6100')
- ('neurologic_problem_self-reported','mdhx_6200'),('hypercholesterolemia_self-reported','mdhx_6300')
- ('type_2_diabetes_self-reported','mdhx_6310'),('endocrine_or_metabolic_problem_self-reported','mdhx_6320')
- ('urologic_or_kidney_problem_self-reported','mdhx_6400')
- ('psychiatric_or_mental_health_problem_self-reported','mdhx_6600')
- ('medical_problem_or_surgery_other_self-reported','mdhx_6700')
- ('genetic_testing_self-reported','mdhx_6900')
- ('genetic_testing_source_self-reported','mdhx_6910')
- ('family_history_of_insomnia','famhx_0100')
- ('family_history_of_sleep_apnea','famhx_0200')
- ('family_history_of_narcolepsy','famhx_0300')
- ('family_history_of_restless_leg_syndrome','famhx_0400')
- ('family_history_of_other_sleep_disorder','famhx_0500')
- ('family_history_of_sleepwalking','famhx_0600')
- ('family_history_of_fibromyalgia_or_chronic_fatigue','famhx_0700')
- ('family_history_of_depression','famhx_0800')
- ('family_history_of_anxiety','famhx_0900')
- ('family_history_of_other_psychiatric_illness','famhx_1000')
- ('family_history_of_psychiatric_treatment','famhx_1100')
- ('family_history_of_death_during_sleep','famhx_1200')

## Measures

### Discrete Measures

- None

### Continuous Measures

- None

### Unsure

('dialysis_self-reported', 'mdhx_6420') (only 0 and only 28 total responses) (REMOVED after eda 1.0)

# Sleep Patterns Subset

## Categories

### Nominal Categories

### Ordinal Categories

- ('last_use_tv_or_computer_before_bed','bthbts_0300') (unit = hours)
- _('self-reported_sleep_quality_for_irregular_work_current_shift','sched_2600')_
- _('self-reported_sleep_quality_on_week_nights_school_nights_work_nights_or_days_next_shift','sched_3100')_
- _('self-reported_sleep_quality_on_week_nights_school_nights_work_nights_or_days_3rd_shift','sched_3600')_
- ('self-reported_sleep_quality_for_weekend_nights_non-school_nights_non-work_nights_or_days','sched_4100')
- ('self-reported_frequency_of_napping','soclhx_0100')
- ('self-reported_frequency_of_napping','soclhx_0110')
- ('feeling_refreshed_after_nap','soclhx_0300')
- ('easily_awakened_after_nap','soclhx_0400')
- ('feeling_that_sleep_is_not_sound','isq_0400')
- ('feeling_that_sleep_is_not_sound_number','isq_0410')
- ('feeling_that_sleep_is_not_sound_time_frame','isq_0420')
- ('feeling_that_sleep_is_unrefreshing','isq_0500')
- ('feeling_that_sleep_is_unrefreshing__number','isq_0510')
- ('feeling_that_sleep_is_unrefreshing_time_frame','isq_0520')
- ('how_much_does_your_sleep_bother_you','isq_0600')
- ('frequency_of_eat/drink_in_sleep_time_frame','par_0310')

### Binary Categories

- ('alcohol_consumption_as_sleep_aid','soclhx_0800')
- ('frequency_of_eat/drink_in_sleep_never_or_dont_know','par_0301')

### Time Data

- ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_current_shift','sched_0900')
- ('self-reported_out-bed_time_on_week_nights_school_nights_work_nights_or_days_current_shift','sched_1000')
- ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_next_shift','sched_1300')
- ('self-reported_out-bed_time_on_week_nights_school_nights_work_nights_or_days_next_shift','sched_1400')
- ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_3rd_shift','sched_1700')
- ('self-reported_in-bed_time_on_week_nights_school_nights_work_nights_or_days_3rd_shift','sched_1800')
- ('self-reported_in-bed_time_on_weekend_nights_non-school_nights_non-work_nights_or_days','sched_1900')
- ('self-reported_out-bed_time_on_weekend_nights_non-school_nights_non-work_nights_or_days','sched_2000')

## Measures

### Discrete Measures

- ('self-reported_usual_duration_of_naps','soclhx_0200')
- ('self-reported_usual_duration_of_naps','soclhx_0210')
- ('amount_of_sleep_needed_to_feel_fully_rested_hours','sched_4200')
- ('amount_of_sleep_needed_to_feel_fully_rested_minutes','sched_4210')
- _('self-reported_sleep_latency_on_weekend_nights_non-school_nights_non-work_nights_or_days','sched_3700')_
- _('self-reported_sleep_latency_on_weekend_nights_non-school_nights_non-work_nights_or_days','sched_3710')_
- _('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_weekend_nights_non-school_nights_non-work_nights_or_days','sched_3800')_
- _('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_weekend_nights_non-school_nights_non-work_nights_or_days','sched_3810')
- _('self-reported_sleep_latency_on_week_nights_school_nights_work_nights_or_days_3rd_shift','sched_3200')_
- _('self-reported_sleep_latency_on_week_nights_school_nights_work_nights_or_days_3rd_shift','sched_3210')_
- _('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_week_nights_school_nights_work_nights_or_days_3rd_shift','sched_3300')_
- _('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_week_nights_school_nights_work_nights_or_days_3rd_shift','sched_3310')_
- _('self-reported_sleep_latency_on_week_nights_school_nights_work_nights_or_days_next_shift','sched_2700')_
- _('self-reported_sleep_latency_on_week_nights_school_nights_work_nights_or_days_next_shift','sched_2710')_
- _('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_week_nights_school_nights_work_nights_or_days_next_shift','sched_2800')_
- _('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_week_nights_school_nights_work_nights_or_days_next_shift','sched_2810')_
- ('self-reported_sleep_latency_on_week_nights_school_nights_work_nights_or_days_current_shift','sched_2200')
- ('self-reported_sleep_latency_on_week_nights_school_nights_work_nights_or_days_current_shift','sched_2210')
- ('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_week_nights_school_nights_work_nights_or_days_current_shift','sched_2300')_
- _('self-reported_total_sleep_duration_(i.e._total_sleep_time)_on_week_nights_school_nights_work_nights_or_days_current_shift','sched_2310')_

### Continuous Measures

### Unsure

- check latency columns in data dictionary
- Get columns that have only 1 value .

# Parasomnias Subset

## Categories

### Nominal Categories

- ('hypnogogic_hallucinations_time_frame', 'map_1120')
- ('frequency_of_leg_twitch/kick_time_frame', 'par_0110')
- ('frequency_of_acting_out_dreams_time_frame', 'par_0510')
- ('frequency_of_violent_behavior_during_sleep_time_frame', 'par_0610')
- ('frequency_of_nightmares_time_frame', 'par_0710')

### Ordinal Categories

- ('hypnogogic_hallucinations_age_of_the_first_episode', 'map_1130')
- ('sleepwalk_age_of_the_first_episode', 'par_0230')
- ('frequency_of_teeth_grinding', 'par_0400')
- ('frequency_of_acting_out_dreams_times', 'par_0500')
- ('acting_out_dreams_age_of_the_first_episode', 'par_0530')
- ('frequency_of_violent_behavior_during_sleep_times', 'par_0600')
- ('violent_behavior_during_sleep_age_of_the_first_episode', 'par_0630')
- ('frequency_of_nightmares_times', 'par_0700')

### Binary Categories

- ('frequency_of_leg_twitch/kick_never_or_dont_know', 'par_0101')
- ('frequency_of_sleepwalk_never_or_dont_know', 'par_0201')
- ('frequency_of_acting_out_dreams_never_or_dont_know', 'par_0501')
- ('acting_out_dreams_age_of_the_first_episode_dont_know', 'par_0531')
- ('frequency_of_violent_behavior_during_sleep_never_or_dont_know', 'par_0601')
- ('violent_behavior_during_sleep_age_of_the_first_episode_dont_know', 'par_0631')
- ('frequency_of_nightmares_never_or_dont_know', 'par_0701')
- ('seizures_during_sleep', 'par_0800')

## Measures

### Discrete Measures

- ('hypnogogic_hallucinations_days_per_week', 'map_1100')
- ('hypnogogic_hallucinations_number_of_times', 'map_1110')
- ('frequency_of_leg_twitch/kick_number_of_times', 'par_0100')
- ('frequency_of_sleepwalk_number_of_times', 'par_0200')
-

### Continuous Measures
