### Steps 

1. check out GCP UI to see what is going on at the moment

    + go to dashboard 

    + in the left column panel select `cloud run`

    + check to see which resources have been created or are running 

2. select on a resource, in the next page will be provided a URL

3. are required to "waitlist" host IP so have permission to see URL 

    + go to tab networks and change option from internal access to all access 

    + then when refresh URL can see the mage UI interpahse that is running in GCP 

### Additional Notes 

* ideally when developing pipeline and pushing them to production, they should be developed locally and then push to github, then can use git sync so the mage cloud docker can pull the latest configurations and run the updated code in prod 

* when not want pipeline to run anymore, can use terraform to destroy all the resources via `terraform destroy`

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=0YExsb2HgLI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=32)

* repo of mage terraform [templates](https://github.com/mage-ai/mage-ai-terraform-templates)

* mage with terraform [documentation](https://docs.mage.ai/production/deploying-to-cloud/using-terraform)

* deploying mage with terraforma and GCP [documentation](https://docs.mage.ai/production/deploying-to-cloud/gcp/setup)

* git sync remote mage docker [documentation](https://docs.mage.ai/guides/data-sync/git-sync)

* next step [google slides](https://docs.google.com/presentation/d/1yN-e22VNwezmPfKrZkgXQVrX5owDb285I2HxHWgmAEQ/edit#slide=id.g262fb0d2905_0_12)