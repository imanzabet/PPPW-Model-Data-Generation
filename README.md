# PPPW-Model-Data-Generation
## Overview
his project aims to generate synthetic data for input of PPPW statistical model. The code accepts both VAT-SFR (main_vat.py) and KTV (main_ktv) dataset as input and using data transform methods to combine them with UNOS and Patient DOB dataset, in order to transform them into a useful dataset for PPPW model. 

The PPPW statistical model requires millions of records of data in order to run properly and give accurate results. The GEE model typically works with  a large number of input data records in order to estimate correctly.

## Procedure
Due to the similarity of VAT-SFR and KtV data with PPPW data, we used them as the base of conversions in order to generate synthetic PPPW data. The below diagram shows an overview of how the combination of VAT-SFR/KtV and UNOS datasets has been produced in order to generate the synthetic/mock PPPW dataset. Two main important columns, which are "Age" and "Waitlist Flag," needed to be calculated based on PPPW measure logic.



![Alt text](images/image2020-10-16_12-34-9.png?raw=true "Title")



## Algorithm and Logic
In order to calculate "Age", the calculation was done based on the difference of patient birthdate and last day of month. For calculating "Waitlist Flag", a dummy variable of "W_End" was defined that was a result of calculating of some of the exceptions of UNOS dataset. The pseudo code below, shows the "W_End" calculation procedure. After that the "W_End" variable was used for generating "Waitlist Flag" column and set the flag to either "True" or "False".


![Alt text](images/1.png?raw=true "Title")
![Alt text](images/2.png?raw=true "Title")


### Handling UNOS dataset duplications
UNOS datasets consists of few records of duplications for a given patient_id, which made confusions for calculating waitlist flag. In the proposed algorithm, it needs to be identified whether for each record. last day of month is falling between "listing_date" and "W_End". If this happens for even one of the duplicated records, then the "Waitlist Flag" needs to be set to "True".



### Handling UNOS dataset exceptions
There are exceptions have been seen in UNOS referring to the patients who have "rmvd_dt" date later than their "death_dt". In those cases we need to correct this based on whichever comes sooner and these adjustments included in the dummy "W_End" variable.
