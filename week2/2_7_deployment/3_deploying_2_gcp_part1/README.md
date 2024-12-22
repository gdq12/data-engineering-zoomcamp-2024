### setting up terraform templates 

1. verify that have gcloud installed and running 

    ```
    sudo gcloud auth list 

    sudo gcloud storage ls
    ```

2. git clone or copy mage terraform templates from [mage template repo](https://github.com/mage-ai/mage-ai-terraform-templates)

    ```
    cd ~/git_repos

    git clone https://github.com/mage-ai/mage-ai-terraform-templates

    cp -r ~/git_repos/mage-ai-terraform-templates/gcp/. ~/git_repos/data-engineering-zoomcamp-2024/week2/2_7_deployment/4_deploying_2_gcp_part2/.
    ```

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=9A872B5hb_0)

* repo of mage terraform [templates](https://github.com/mage-ai/mage-ai-terraform-templates)

* mage with terraform [documentation](https://docs.mage.ai/production/deploying-to-cloud/using-terraform)

* deploying mage with terraforma and GCP [documentation](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)