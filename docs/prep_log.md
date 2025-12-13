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
