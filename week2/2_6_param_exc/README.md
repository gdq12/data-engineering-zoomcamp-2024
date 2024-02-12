### I.Customize data push by run date 

- for setting up pipelines for repeated runs, should parameterize data push by date of execution 

- can fetch the run time date from `kwargs`: it stores a couple of keyword arguments from the pipeline. to see the keyword arguments available can execute `print(kwargs)`

- execution date can be fetched from kwargs and f formated into the object key via `kwargs['execution_date'].date()`

### II. Creating run time variables 

- this can be done for the pipeline and for triggers

- for the pipeline, go to the `variables` icon on the left panel of the GUI, when creating or editing a trigger it is also found on the left pannel of the GUI under `Runtime variables`

- they are also created in the pipelines `metadata.yaml`. documentation on how to define them can be found [here](https://docs.mage.ai/getting-started/runtime-variable#using-runtime-variables)

### III. Backfilling data 

- its like going back in time and collecting possible missing data 

- if data collection is based on an execution date, then its like creating a for loop to fetch info from that execution date 

- caution this is dependent on the pipeline using `kwargs['execution_date']` in the pipeline scripts 

- this can be set up in the UI, as explained [here](https://docs.mage.ai/orchestration/backfills/guides)

- it seems that no code files are created for this, but apart from using the UI, one can make API calls to execute this. documentation on this is found [here](https://docs.mage.ai/api-reference/backfills/overview)

### Helpful Links

* Yoututbe [video parameters](https://www.youtube.com/watch?v=H0hWjWxB-rg)

* Youtube [video backfills](https://www.youtube.com/watch?v=ZoeC6Ag5gQc&t=2s)