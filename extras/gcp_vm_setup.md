### I. Creating an instance

1. go to Compute engine in the list of categories on the left and choose “VM instance”
2. approve create API
3. generate SHH key (for logging into instance)
    1. follow instructions from webpage: https://cloud.google.com/compute/docs/connect/create-ssh-keys
    2. make sure that have ~/.ssh directory already
    3. create SSH key pair in ~/.ssh directory 
    
    ```bash
    # creates private and public keys 
    ssh-keygen -t rsa -f ~/.ssh/gcp -C gdq -b 2048
    ```
    
4. add public ssh key in google cloud 
    1. copy public key to compute_engine/metadata/add_ssh_key —> all VM created will inherit this ssh key 
    
    ```bash
    cat gcp.pub
    ```
    
5. create instance 
    1. go to Compute Engine —> VM instances —> create instance 
    2. following configs set:
        1. name: de-zoomcamp
        2. region: europe-west1 (Belgium)
        3. machine type: e2-standard-4 (4 vCPU, 16 GB Memory)
        4. boot disk:
            1. operation system: ubuntu
            2. version: ubuntu 20.04 LTS
            3. size: 30 GB
6. access VM via terminal 
    1. copy external IP after creating instance 
    
    ```bash
    ssh -i ~/.ssh/gcp gdq@externalIP
    ```
    
7. spot checking machine
    
    ```bash
    # check machine configurations 
    htop
    
    # verify gcloud installed 
    gcloud --version
    ```
    

### II. Configure Instance (execute in instance terminal)

1. download anaconda for linux 
    
    ```bash
    # downloading anaconda 
    wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
    
    # agreeing to terms and services 
    bash Anaconda3-2022.05-Linux-x86_64.sh
    
    # will take a while to install 
    ```
    
2. in the meantime create a config file in ~/.ssh
    
    ```bash
    # to create config file 
    touch ~/.ssh/config
    
    # modify config in text editor like atom 
    Host de-zoomcamp
      HostName externalIP
      User gdq
      IdentityFile ~/.ssh/gcp
    ```
    
3. logging back in to VM using alias from config file 
    
    ```bash
    cd ~
    
    ssh de-zoomcamp
    ```
    
4. installing docker (in bash vm )
    
    ```bash
    sudo apt-get update
    
    sudo apt-get install docker.io
    ```
    
5. connect visual studio to the VM
    1. install extension: remote ssh
    2. open a remote window
    3. connect to host
    4. select alias de-zoomcamp
6. clone repo in vm 
    
    ```bash
    git clone https://github.com/DataTalksClub/data-engineering-zoomcamp.git
    ```
    
7. run docker without sudo 
    1. commands can be found here: https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md
    
    ```bash
    sudo groupadd docker
    
    sudo gpasswd -a $USER docker
    
    # log in and out of machine 
    ctrl + D
    ssh de-zoomcamp
    
    # testing for docker daemon up and running 
    docker images 
    ```
    
8. install docker compose 
    1. visit docker compose github and select the latest release: https://github.com/docker/compose https://github.com/docker/compose
    2. fetch the link for docker-compose-linux-x86_64: https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-linux-x86_64
    3. go back to terminal with gcp connex and create a bin directory where all executable files will be stored, download docker compose installation file in that directory 
    
    ```bash
    # prep VM for download
    cd ~
    mkdir bin
    cd bin/
    
    # download docker-compose 
    wget https://github.com/docker/compose/releases/download/v2.6.0/docker-compose-linux-x86_64 -O docker-compose
    
    # to make file executable 
    chmod +x docker-compose
    
    # checking on the downloaded file 
    ./docker-compose version
    
    # add docker compose to path so it can be executed from any directory 
    nano .bashrc
    export PATH="${HOME}/bin:${PATH}"
    
    # for changes to take effect and not have to log in/out
    source .bashrc
    
    # check the path application worked 
    which docker-compose
    
    # test docker compose in action 
    cd ~/data-engineering-zoomcamp/week_1_basics_n_setup/2_docker_sql/
    docker-compose up -d 
    ```
    
9. installing pg CLI
    
    ```bash
    # pgcli didnt work for me 
    pip install pgcli
    pgcli -h localhost -U root -d ny_taxi
    
    # instead used psql 
    sudo apt install postgresql-client-common
    sudo apt -y install postgresql-client-12
    psql -h localhost -U root -d ny_taxi
    
    # different way to install pgcli (successfull!)
    pip uninstall pgcli
    conda install -c conda-forge pgcli
    pip install -U mycli
    pgcli -h localhost -U root -d ny_taxi
    ```
    
10. forwarding postgres port 5432 to local machine 
    1. in VS, go to PORTS —> forward a port —> enter port number 5432
    2. then can access via the following command: pgcli -h localhost -U root -d ny_taxi
    3. can also forward port for pgAdmin (8080) so can access GUI via browser 
    4. forward port for jupyter notebook (8888)
11. install terraform for linux 
    
    ```bash
    # commands from here: https://www.terraform.io/downloads
    ## download package manager 
    curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
    sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
    sudo apt-get update && sudo apt-get install terraform
    
    ## download binary
    cd ~/bin
    wget https://releases.hashicorp.com/terraform/1.2.2/terraform_1.2.2_linux_amd64.zip
    sudo apt install unzip
    unzip terraform_1.2.2_linux_amd64.zip
    rm *.zip
    
    # testing that discoverable globally
    cd ~
    terraform -version 
    ```
    
12. running terraform scripts in VM gcloud 
    1. transfer json cred file to remote machine via sftp 
    
    ```bash
    # connect to the remote machine via sftp 
    cd /Users/gdq/Documents
    sftp de-zoomcamp
    
    # create a .gc directory 
    mkdir .gc 
    cd .gc 
    put de-zoomcamp-may-july22-352411-d7c01470cfae.json
    
    # verify that data transfer worked 
    ls ~/.gc
    ```
    
13. configure google cloud to CLI
    
     a. add google json cred to path in VM 
    
    ```bash
    # assign path to variable 
    export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/de-zoomcamp-may-july22-352411-d7c01470cfae.json
    
    # authenticate credentials 
    gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
    ```
    
14. run terraform scripts in VM 
    
    ```bash
    # execute terraform file from git repo 
    cd data-engineering-zoomcamp/week_1_basics_n_setup/1_terraform_gcp/terraform
    
    # execute terraform (have the project ID ready to provide when prompted)
    terraform init
    terraform plan
    terraform apply 
    ```
    

### III. Shutting down the machine

1. to pause or have the machine stop spinning with the VM:

```bash
sudo shutdown now 
```

1. IMPORTANT TO NOTE: when restart machine, it will have a new external IP so have to update the ~/.ssh/config file 
2. when pause instance, will not be charged for the computing but still for the storage
3. to not be charged for storage, delete instance

### Helpful Links 

* Youtube [video](https://www.youtube.com/watch?v=ae-CV2KfoN0&t=18s)