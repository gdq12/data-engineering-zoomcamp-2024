### I. Terraform Background info

1. open source tool by hashi corp 
2. Benefits 
    1. permit provision of resources (i.e. Cloud resources) with declarative configuration files (to make it easier to restructure etc). 
    2. goes by an IA c-style approach —> supporting devops best practices for chain management —> ideal for testing and deployment 
    3. version control of cloud configuration for ETL or ELT jobs.
    4. permits reproducibility amoungst colleagues 
    5. ensure resource cleanup, avoid surprise charges
3. Limitations 
    1. doesn't manage/update code on infrastructure: doesn't create/deploy software
    2. not change immutable resources: example not change machine type via code, also not auto change buckets 
    3. cannot manage resources outside those defined in the files 
4. IC
    1. it is infrastructure as code 
    2. framework which allows to build and change infrastructure in a repetitive and safe way (can version control the configurations and share as well) 
    3. its like a git version control but for infrastructure 
    4. this is 100% dependent on configuration files, there is no GUI
    5. its a state base approach to track changes throughout deployment

### II. INtro to Terraform Commands

- `init`: Once files have been defined, it'll fetch code and bring it locally
- `plan`: provides a summary of what will occur, aka for example what resources will be created 
- `apply`: run processes based on what is instructucted in files 
- `destroy`: will bring down all resources that were created via terraform 

### Helpful Links 

* Youtube [video](https://www.youtube.com/watch?v=s2bOYDCKl_M&t=1s)

* Lecturer's [notes](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/1_terraform_overview.md)