### Q&As

1. Once the dataset is loaded, what's the shape of the data?

    * `(266855, 20)`

    * this was calculated by the line `print(f'fetched all data with a shape of {df.shape}')` in [load_df.py](magic-zoomcamp/data_loaders/load_df.py) 

2. Upon filtering the dataset where the passenger count is greater than 0 and the trip distance is greater than zero, how many rows are left?

    * `139370`

    * this was calculated by line `print(f'exporting a df with {df.shape[0]} records')` in [greentaxi_dta_cleaner.py](magic-zoomcamp/transformers/greentaxi_data_cleaner.py)

3. Which of the following creates a new column lpep_pickup_date by converting lpep_pickup_datetime to a date?

    * `data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date`

4. What are the existing values of VendorID in the dataset?

    * `1 or 2`

5. How many columns need to be renamed to snake case?

    * `4`

    * did it with the folllowing pandas syntax: `', '.join(df.columns[df.columns.str.contains('(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z]{1}[a-z])', regex = True)])`

6. Once exported, how many partitions (folders) are present in Google Cloud?

    * `96`

    * in the GCP interphase it counts 95 but 96 was the closest answer, was confirmed with the following pandas line: `data['lpep_pickup_date'].nunique()`

### Helpful Links

* Questions for the hw [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/02-workflow-orchestration/homework.md)