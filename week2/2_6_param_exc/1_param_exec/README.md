### I.Customize data push by run date 

- for setting up pipelines for repeated runs, should parameterize data push by date of execution 

- can fetch the run time date from `kwargs`: it stores a couple of keyword arguments from the pipeline. to see the keyword arguments available can execute `print(kwargs)`

- execution date can be fetched from kwargs and f formated into the object key via `kwargs['execution_date'].date()`

### II. Creating run time variables 

- this can be done for the pipeline and for triggers

- for the pipeline, go to the `variables` icon on the left panel of the GUI, when creating or editing a trigger it is also found on the left pannel of the GUI under `Runtime variables`

- they are also created in the pipelines `metadata.yaml`. documentation on how to define them can be found [here](https://docs.mage.ai/getting-started/runtime-variable#using-runtime-variables)

### Helpful Links

* Yoututbe [video](https://www.youtube.com/watch?v=H0hWjWxB-rg)