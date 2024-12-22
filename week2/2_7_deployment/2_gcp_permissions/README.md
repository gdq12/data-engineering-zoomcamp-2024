### Steps to set up permissions

1. verify that in the right project dashboard, in this case using `de-zoomcamp-dec24`

2. in the left column panel of dashboard go to `IAM &Admin`

3. create a service account 

    +  select `service accounts` in left column panel 

    + select `+ create service account` top bar of main part of screen

    + name it `magic-zoomcamp`

4. for assigning roles to the service account, apply the ones that are listed in the last link of the helpful links below 

    + Artifact Registry Read

    + Artifact Registry Writer
    
    + Cloud Run Developer
    
    + Cloud SQL
    
    + Service Account Token Creator

5. confirm everything and click `done`

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=O_H7DCmq2rA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=30)

* repo of mage terraform [templates](https://github.com/mage-ai/mage-ai-terraform-templates)

* mage with terraform [documentation](https://docs.mage.ai/production/deploying-to-cloud/using-terraform)

* deploying mage with terraforma and GCP [documentation](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)