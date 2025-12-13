# Prep Log for demographic information

## Column Overview

contains 35 columns:

| Original name     | Meaning                                                             |
| :---------------- | :------------------------------------------------------------------ |
| dem_0600          | Height in feet                                                      |
| dem_0610          | Height in inches                                                    |
| dem_0700          | Weight in pounds                                                    |
| dem_0800          | Body mass index (BMI)                                               |
| dem_1100          | English as native language                                          |
| dem_1120          | Participant's proficiency in English                                |
| sched_0100        | Level of school                                                     |
| sched_0200        | Days per week in school                                             |
| sched_0300        | Time School Starts                                                  |
| sched_0301        | Time School Starts - Varies                                         |
| sched_0400        | Time School Ends                                                    |
| sched_0401        | Time School Ends - Varies                                           |
| sched_0500        | Regular or Irregular Work Schedule                                  |
| sched_0510        | Do you work a split shift?                                          |
| sched_0600        | Days per week at work                                               |
| sched_0700        | Self-reported work start time, current shift                        |
| sched_0800        | Self-reported work end time, current shift                          |
| sched_1100        | Self-reported work start time, next shift                           |
| sched_1200        | Self-reported work end time, next shift                             |
| sched_1500        | Self-reported work start time, 3rd shift                            |
| sched_1501        | Self-reported work start time, no 3rd shift                         |
| sched_1600        | Self-reported work end time, 3rd shift                              |
| sched_2100        | How often change work shifts                                        |
| bthbts_0500       | Number of people living in your household                           |
| bthbts_0510       | Number of children aged 5 years or younger living in your household |
| bthbts_0520       | Number of children aged 6 - 17 living in your household             |
| bthbts_0530       | Number of adults aged 18 - 59 living in your household              |
| bthbts_0540       | Number of adults aged 60 years of older living in your household    |
| dem_0100          | Participant's year of birth                                         |
| dem_0500          | Participant's sex                                                   |
| dem_0900          | Participant's ethnicity (hispanic or latino)                        |
| dem_0910          | Participant's ethnicity (sub hispanic or latino origin)             |
| dem_1000          | Participant's race (main)                                           |
| dem_1010          | Participant's race (sub)                                            |
| modified_dem_0110 | Participant's age                                                   |

## Notes on Columns

only need 1 from year of birth and participants age

height in feet and height in inches can be condensed

bmi probably not needed since redudnat and less informative then weight + height on their own

race and native language both not important and potentially harmful in creating bias

level of school is encdoed ordinally

should perhaps combine school/ work columns into a common "schedule"
