### I. Mage background 

- was built with the following in mind: flow state, feedback loops and cognitive load

- mage high level infrastructure: 

    1. blocks: 
    
        + used to export/transform/load data
        
        + They are the atomic unit that make up a transformation
        
        + They are a single unit of a pipeline

        + can be written in sql/pythin/R

        + types of blocks: sonsor, conditional, dynamic and webhooks

    2. pipeline: dags/data workflows. they consits of block units 

    3. projects: the home base/instance. Can also consists of multiple projects 

    * pipelines 

### II. Pluses of tools 

- additional features: data integration, unified pipelines, multi-user environments, templating 

- hybrid environment: supports its own GUI for user friendly editing experience and collaboration. Can also use other interphase like VS code. Blocks to be reused for engineering best practices

- imrpoved dev experience: permits parallel code/testing and dependency on multiple tools 

- integrate engineering best practices (testing, and DRY methods)


### Core Concepts 

- project: the largest unit of Mage. There can be miltiple projects in a single Mage instance environment 

    * can think of this as a single Github Repo

- pipelines: they reside within a single project. they are aka DAGs

    * workflow that performs a given data operation 

    * they are structured in a yaml file

- blocks: they are a single unit of a pipeline 

    * they can be written in any code (sql, R or python)

    * can be executed independently or in a work flow

    * wont start running in a pipeline until the upstream dependencies are met

    * reduce of copy/pasting blocks into different project/pipelines by allow reusability (and customization when needed)

### Block anatomy 

1. Imports of needed libraries/modules 

2. decorator to declare what type of block it is 

3. functions (to return a data frame)

4. assertion/test to validate the function output 

- good to knows:

    + when a block is run, only the function is executed 

### Helpful Links

* Youtube [video](https://www.youtube.com/watch?v=AicKRcK3pa4)

* Lecture [slides](https://docs.google.com/presentation/d/1y_5p3sxr6Xh1RqE6N8o2280gUzAdiic2hPhYUUD6l88/edit#slide=id.g262e1cce745_0_184)