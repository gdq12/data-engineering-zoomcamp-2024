### Prerequisites list

* install terraform installed locally 

    + permits for spinning up resources in a more orderly and time efficient fashion 

    + version controls infrastructure code for collaboration 

* gcloud CLI

* GCP permissions 

    + so to permit resource creation required for project 

* mage terraform template 

    + a predefined template from a mage repo that allows for `terraform apply` command to spin up a mage friendly resource with ease 

### Terraform Installtion 

1. installing Hashicorp tap and terraform via homebrew

    ```
    brew tap hashicorp/tap

    brew install hashicorp/tap/terraform

    # just execute to verify working with the latest version 
    brew update
    brew upgrade hashicorp/tap/terraform
    ```

2. verify that terraform is installed by executing `terraform --help` in cmd line, which should print out list of flags that can be executed 

### gCloud CLI Installation 

1. verify that have pre requisites

    ```
    # have btw python 3.8 - 3.13
    python3 -V

    # determine which PC hardware have 
    uname -m
    ```

2. download zip for `macOS 64-bit (x86_64)`

3. excute the following in terminal

    ```
    # get file to home directory 
    cd ~
    cp Downloads/google-cloud-cli-VERSION-darwin-x86_64.tar .

    # unarchive file 
    tar -xvf google-cloud-cli-VERSION-darwin-x86_64.tar

    # install google cloud sdk and add to path 
    sudo ./google-cloud-sdk/install.sh --screen-reader=true

    # path of installetion should of been /Users/gdq/.bashrc
    # but instead used /Users/gdq/.bash_profile
    # .bash_profile version prior to installtion was saved as .bash_profile.backup

    # agree to install python 3.11 for best performance

    # initialize sdk for the first time (best to do this in chrome browser with account profile signed in already)
    sudo ./google-cloud-sdk/bin/gcloud init

    # auto log-in to google account via browser

    # prompt to select which project to use 
    ```

### Helpful Links 

* Youtube [video](https://www.youtube.com/watch?v=zAwAX5sxqsg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=29)

* installing terraform [documentation](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

* installing gcloud CLI [documnetation](https://cloud.google.com/sdk/docs/install)

* repo of mage terraform [templates](https://github.com/mage-ai/mage-ai-terraform-templates)

* mage with terraform [documentation](https://docs.mage.ai/production/deploying-to-cloud/using-terraform)

* deploying mage with terraforma and GCP [documentation](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)