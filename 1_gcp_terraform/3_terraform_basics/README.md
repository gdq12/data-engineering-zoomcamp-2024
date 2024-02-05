### I. Terraform setup (GCP)

1. create a service account in GCP (its a user account for terraform, to only be used by the tool/code, not by a human)
    - go to: left hand panel on project console --> IAM & Admin --> service accounts in left hand panel --> `+ Create service account` top center

    - fill out form 
        * provide a name 
        * grant roles: 
            + Cloud Storage --> Storage Admin
            + Bigquery --> BigQuery Admin
            + ideally would want to provide limited permissions (to create and destroy objects) but keeping it broad here for learning purposes.

    - update permissions post creating service account: IAM in left panel --> edit principle of target service account --> modify required roles etc 

2. get config for local use 

    - go to: service accounts in left panel --> triple dots in account row --> manage keys --> add key --> create new key (json fomrmat)

    - the keys will auto download 

    - store keys in Documents directory `~/Documents`

### II. Local Installations 

1. Terraform 

    * install `HashiCorp Terraform` extension

    * install terraform in system 

        * instructions can be found here: https://developer.hashicorp.com/terraform/install

        ``` {bash}
        brew tap hashicorp/tap

        brew install hashicorp/tap/terraform
        ```

2. Google SDK installation 

    * google instruction for installing SDK can be found here: https://cloud.google.com/sdk/docs/install-sdk

    * downloaded the 64-bit: https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-388.0.0-darwin-x86_64.tar.gz

    * getting local configs

        ```{bash}
        # local python version 
        python3 -V

        # PC bit size
        uname m 
        ```

    * installation of zip file 

        ``` {bash}
        # get file to home directory 
        cd ~
        cp Downloads/google-cloud-cli-VERSION-darwin-x86_64.tar .

        # unarchive file 
        tar -xvf google-cloud-cli-VERSION-darwin-x86_64.tar

        # install google cloud sdk and add to path 
        sudo ./google-cloud-sdk/install.sh --screen-reader=true

        # path when prompted 
        /Users/gdq/.bashrc

        # agree to install python 3.7 for best performance

        # initialize sdk for the first time 
        sudo ./google-cloud-sdk/bin/gcloud init

        # auto log-in to google account via browser

        # prompt to select which project to use 
        ```

    + connect ENV vars to google cloud keys 

        ```{bash}
        # add this to ~/.bash_profile (using atom)
        export PATH=/Users/gdq/google-cloud-sdk/bin:$PATH
        # define this variable in terminal, add to ~/.bash-profile too
        export GOOGLE_APPLICATION_CREDENTIALS=/Users/gdq/Documents/file.json

        # verify authentiacation worked
        sudo gcloud auth application-default login 

        # will be redirector with web browser authentication (oath technique)

        # to initialize sdk everytime 
        sudo gcloud init
        ```


### III. Local env set up 

1. creating main.tf file 

    * syntax can be copied from and then customized from here: https://registry.terraform.io/providers/hashicorp/google/latest/docs

    * guidelines to add syntax on buckets can be found here: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket

    * run terraform format command and then init so can generate the provider code to connect to GCP

2. initiating terraform 

    * `terraform init` can be executed after the `main.tf` file is created.

    * this will create `.terraform` centric files and directories needed to run terraform.

    * `terraform plan` can be used to preview configurations that will be deployed prior to deployment

    * `terraform apply` actually deploys all configurations --> the deployed configurations are detailed in `terraform.tfstate`

3. remove all resources created by terraform via `terraform destroy`

4. keep terraform config files local only. good source can be found here: https://github.com/github/gitignore/blob/main/Terraform.gitignore


### IV. Good to know

- terraform commands 

    ```{bash}
    # format files in local directory (files must be saved (ctrl+S) prior to initiating command)
    terraform fmt

    # gets provider (code that permits terraform to communicate w/GCP)
    terraform init 

    # prints out configurations in terminal --> can use it to print out default configurations
    terraform plan 

    # to deploy configurations from main.tf
    terraform apply

    # to remove all resources created via main.tf
    terraform destroy
    ```

- terraform files 

    * `main.tf`

        + specifics on what resources to set up in GCP once terraform is deployed 

    * `.terraform`*

        + provider centric lines used to connect to GCP

    * `terraform.tfstate`

        + resource configurations currently present post terraform deployment

        + also changes when `terraform destroy` is executed 
    
    *  `terraform.tfstate.backup`

        + 'copy' of the tfstate file prior to `terraform destroy`

        + helps version control setting resources changes

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=Y2ux7gq3Z0o&t=4s)

* Lecturer's [notes](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform)