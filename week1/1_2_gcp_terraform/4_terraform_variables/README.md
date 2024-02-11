### I. Terraform files general

- `main.tf` defines the resources that should be created upon `terraform apply`

- `variables.tf` are predefined variables that can be passed on to `main.tf` when `terrfaorm apply` is executed

### II. variable.tf syntax

- each variable has 2 major components: description and default 

    ```{bash}
    variable "var_name" {
    description = "simple description"
    default     = "var_value"
    }
    ```

- default value from the json is what should be passed on to `main.tf`. To do this, place `var.var_name` in the field needed in `main.tf`

- this makes it easier to define variables that used multiple times in the `main.tf` file. So when something needs to be changed, the change can be made in `variables.tf` in a single location rather than the multiple location in `main.tf`.

- defining project credentials: optimal when want to use `main.tf` and `variables.tf` across various projects and not need to customize this field every time.

    ```{bash}
    # in variables.tf
    variable "credentials" {
    description = "project credentials"
    default     = "/path/to/json/fileName.json"
    }

    # in main.tf
    provider "google" {
    project     = var.project
    region      = var.region
    credentials = file(var.credentials)
    }
    ```

### III. Good to knows from pervious cohorts 

- authenticate gcloud CLI (leads to web-browser verification)

    ```{bash}
    sudo gcloud auth application-default login 
    ```


### Helpful Links

* Course [notes](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp)

* Lesson [video](https://www.youtube.com/watch?v=PBi0hHjLftk&t=4s)