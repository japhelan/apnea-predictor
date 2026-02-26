# Data Prep LOG

## Data Preparation

### Loading Data

subject_code is the unique identifier across the harmonized and larger dataset

stages_dataset-0.3.0 (which will be referred to simply as "stages" from now on) has 433 columns and 1881 rows

stages-harmonized-dataset-0.3.0 (which will be "stages-harmonized") has 10 columns and 1881 rows

data dicitonaries for both can be found in ../data/stages/datasets/

## stages dataprep

split columns into the following categories (based off data dictionary)

    - demographics (merged with stages-harmonized columns to here)

    - general health and lifestyle

    - medical history

    - sleep questionnares

    - sleep treament

### Demographics

contains 35 columns:

'dem_0100', 'modified_dem_0110',

'dem_0500', 'dem_0600', 'dem_0610', 'dem_0700', 'dem_0800', 'dem_0900', 'dem_0910',

'dem_1000', 'dem_1010', 'dem_1100', 'dem_1120',

'sched_0100', 'sched_0200', 'sched_0300', 'sched_0301', 'sched_0400', 'sched_0401', 'sched_0500', 'sched_0510', 'sched_0600', 'sched_0700',

'sched_0800', 'sched_1100', 'sched_1200', 'sched_1500', 'sched_1501', 'sched_1600', 'sched_2100', '

bthbts_0500', 'bthbts_0510', 'bthbts_0520', 'bthbts_0530', 'bthbts_0540'

### Lifestyle

contains 90 columns:

'fss_0100', 'fss_0200', 'fss_0300', 'fss_0400', 'fss_0500', 'fss_0600', 'fss_0700', 'fss_0800', 'fss_0900', 'fss_1000'

'gad_0100', 'gad_0200', 'gad_0300', 'gad_0400', 'gad_0500', 'gad_0600', 'gad_0700', 'gad_0800'

'phq_0100', 'phq_0200', 'phq_0300', 'phq_0400', 'phq_0500', 'phq_0600', 'phq_0700', 'phq_0800', 'phq_0900', 'phq_1000'

'nose_0100', 'nose_0200', 'nose_0300', 'nose_0400', 'nose_0500', 'nose_0600'

'osa_0100', 'osa_0200', 'osa_0300', 'cir_0100', 'bthbts_0100'

'diet_0300', 'diet_0310', 'diet_0320', 'diet_0330', 'diet_0340', 'diet_0350', 'diet_0360', 'diet_0370', 'diet_0380',

'diet_0400', 'diet_0500', 'diet_0600', 'diet_0700', 'diet_0800', 'diet_0801', 'diet_0810', 'diet_0811', 'diet_0820', 'diet_0821', 'diet_0830', 'diet_0831', 'diet_0840', 'diet_0841', 'diet_0850', 'diet_0851', 'diet_0860', 'diet_0861', 'diet_0870', 'diet_0871',

'soclhx_0501', 'soclhx_0520', 'soclhx_0600', 'soclhx_0700', 'soclhx_0701', 'soclhx_0710', 'soclhx_0730', 'soclhx_0900', 'soclhx_0901', 'soclhx_1000', 'soclhx_1200', 'soclhx_1300', 'soclhx_1310', 'soclhx_1400', 'soclhx_1500', 'soclhx_1700', 'soclhx_1800'

'current_cigarette_smoker', 'current_smokeless_user', 'former_cigarette_smoker', 'former_smokeless_user', 'never_cigarette_smoker']

### Medical History

contains 40 columns:

'famhx_0100', 'famhx_0200', 'famhx_0300', 'famhx_0400', 'famhx_0500', 'famhx_0600', 'famhx_0700', 'famhx_0800', 'famhx_0900', 'famhx_1000', 'famhx_1100', 'famhx_1200', 'famhx_1300'

'mdhx_1200', 'mdhx_1300', 'mdhx_1400'

'mdhx_5700', 'mdhx_5710', 'mdhx_5720', 'mdhx_5800', 'mdhx_5810', 'mdhx_5820', 'mdhx_5900', 'mdhx_5910', 'mdhx_5920', 'mdhx_5950'

'mdhx_6000', 'mdhx_6030', 'mdhx_6100', 'mdhx_6200', 'mdhx_6300', 'mdhx_6310', 'mdhx_6320', 'mdhx_6400', 'mdhx_6420', 'mdhx_6500', 'mdhx_6600', 'mdhx_6700', 'mdhx_6900', 'mdhx_6910'

### Sleep Questionnares

245 columns:

this should probably be split further

### Sleep Treatment

19 columns:

'pap_0100', 'pap_0200', 'pap_0300', 'pap_0400', 'pap_0500', 'pap_0600', 'pap_0700', 'pap_0800', 'pap_1200', 'pap_1300', 'pap_1400', 'pap_1600',

'pap_1700', 'pap_1800', 'pap_1900', 'pap_2100',

'mdhx_0700', 'mdhx_0800', 'mdhx_0400'

### Subsets Overview 1

Combined there are 429 columns

Missing columns: {'subject_code', 'modified_created_at', 'visitcode', 'modified_completed'} (dont want)

### Sleep Questionnaire subset 1

'ess_0100', 'ess_0200', 'ess_0300', 'ess_0400', 'ess_0500', 'ess_0600', 'ess_0700', 'ess_0800', 'ess_0900'

'map_0100', 'map_0200', 'map_0300', 'map_0400', 'map_0500', 'map_0600', 'map_0700', 'map_0800', 'map_0900', 'map_1000', 'map_1010', 'map_1020', 'map_1030', 'map_1040', 'map_1041', 'map_1100', 'map_1110', 'map_1120', 'map_1130', 'map_1131', 'map_lr'

'narc_0050', 'narc_0100', 'narc_0110', 'narc_0200', 'narc_0210', 'narc_0300', 'narc_0310', 'narc_0400', 'narc_0410', 'narc_0500', 'narc_0510', 'narc_0600', 'narc_0700', 'narc_0800', 'narc_0900', 'narc_1000', 'narc_1100', 'narc_1200', 'narc_1300', 'narc_1400', 'narc_1500', 'narc_1600', 'narc_1610', 'narc_1650', 'narc_1700', 'narc_1701', 'narc_1900', 'narc_2000', 'narc_2100', 'narc_2110', 'narc_2200', 'narc_1710'

'par_0100', 'par_0101', 'par_0110', 'par_0200', 'par_0201', 'par_0210', 'par_0230', 'par_0300', 'par_0301', 'par_0310', 'par_0400', 'par_0500', 'par_0501', 'par_0510', 'par_0530', 'par_0531', 'par_0600', 'par_0601', 'par_0610', 'par_0630', 'par_0631', 'par_0700', 'par_0701', 'par_0710', 'par_0800', 'par_0900', 'par_0901', 'par_0910'

'slpy_0101', 'slpy_0100', 'slpy_0110', 'slpy_0201', 'slpy_0200', 'slpy_0210', 'slpy_0301', 'slpy_0300', 'slpy_0310', 'slpy_0400', 'slpy_0410'

'index_1', 'index_3', 'index_4', 'score', 'rls_0100', 'rls_0200', 'rls_0310', 'rls_0400', 'rls_0410', 'rls_0500', 'rls_0510', 'rls_0600', 'rls_0610', 'rls_0700', 'rls_0710', 'rls_0300', 'rls_0800', 'rls_0801', 'rls_0900', 'rls_0910', 'rls_probability', 'rls_severity'

### Sleep Questionnaire subset 2

'fosq_0100', 'fosq_0200', 'fosq_0300', 'fosq_0400', 'fosq_0500', 'fosq_0600', 'fosq_0700', 'fosq_0800', 'fosq_0900', 'fosq_1000', 'fosq_1100'

'isi_0100', 'isi_0200', 'isi_0300', 'isi_0400', 'isi_0500', 'isi_0600', 'isi_0700', 'isi_score', 'isq_0100', 'isq_0110', 'isq_0120', 'isq_0200', 'isq_0210', 'isq_0220', 'isq_0300', 'isq_0310', 'isq_0320', 'isq_0400', 'isq_0410', 'isq_0420', 'isq_0500', 'isq_0510', 'isq_0520', 'isq_0600', 'isq_0700', 'isq_0800', 'isq_0900', 'isq_1000', 'isq_1100', 'isq_1200', 'isq_1300', 'isq_score'

'tab_0100', 'tab_0200', 'tab_0300', 'tab_0400', 'tab_0500', 'tab_0600', 'tab_0700', 'tab_0800', 'tab_0900', 'tab_1000'

'cir_0200', 'cir_0300', 'cir_0400', 'cir_0500', 'cir_0600', 'cir_0700'

'mdhx_0200', 'mdhx_5500', 'mdhx_5600', 'bthbts_0300', 'soclhx_0100', 'soclhx_0101', 'soclhx_0110', 'soclhx_0200', 'soclhx_0210', 'soclhx_0300', 'soclhx_0400', 'soclhx_0800'

'sched_2400', 'sched_2500', 'sched_2510', 'sched_2600', 'sched_2900', 'sched_3000', 'sched_3010', 'sched_3100', 'sched_3400', 'sched_3500', 'sched_3510', 'sched_3600', 'sched_3900', 'sched_4000', 'sched_4010', 'sched_4100', 'sched_4200', 'sched_4201', 'sched_4210', 'sched_0900',

'sched_0901', 'sched_1000', 'sched_1001', 'sched_1300', 'sched_1301', 'sched_1400', 'sched_1401', 'sched_1700', 'sched_1701', 'sched_1800', 'sched_1801', 'sched_1900', 'sched_1901', 'sched_2000', 'sched_2001', 'sched_2200', 'sched_2210', 'sched_2300', 'sched_2310', 'sched_2700', 'sched_2710', 'sched_2800', 'sched_2810', 'sched_3200', 'sched_3210', 'sched_3300', 'sched_3310', 'sched_3700', 'sched_3710', 'sched_3800', 'sched_3810'

At this point I am going to split into multiple files for each subset to prevent making one huge cluttered log
