### Clonfluent Cloud setup

- chose this direction based on instructor advice stating the java libraries are better for this

- accessing confluent cloud [page](https://www.confluent.io/get-started/) was only possible in safari browser

1) create account using link above

2) log-in and create a cluster

  - select an environemnt (defualt)

  - select basic cluster

  - `GCP`

  - Region: `Frankfurt (europe-west3)`

  - skip payment info for now since have trial credit

  - cluster name: `wk6_kafka_tutorial`

  - `Launch Cluster`

  - description: `vid4_wk6_kafka_tutorial`

  - save the downloaded file to documents folder in PC

**Best way to find cluster of interest is to click around until reach the following path: Home> Environments > envName > clusterName**

3) Create API Key

  - click on the newly created cluster name to go to its dashboard

  - `API Keys` in the left panel of cluster dashboard

  - `Global Access`

4) create a topic

  - `Topics` in the left panel of cluster dashboard

  - `Create topic`

  - topic name: `tutorial_topic`

  - partitions: `2`

  - show advanced settings:

    + retention time: `1 day` (to keep costs from adding up)

  - `save & create`

5) create a dummy message to test it out

  - go to the `Messages` tab

  - `Produce new message`

  - quickly check proposed json --> `Produce`

  - click on message from list produced in topic

  - toggle window of message details will appear on the left where can inspect different parts of the message: `Key`/`Value`/`Headers`

6) Create a connector

  - click on `Connectors` tab in left panel of the dashboard

  - search for and click on `Datagen Source`

  - `Additional Configuration`

  - select `tutorial_topic`

  - `Continue`

  - `Global access`

  - `Generate API key & download`

  - save key to documents folder in local PC

  - API key description: `datagen_tutorial_topic_vid4_wk6`

  - select output record value format: `JSON`

  - select a schema: `Orders`

  - verify connector size ok/suitable

  - `Continue`

  - connector name: `ordersConnector_tutorial_vid4_wk6`

  - `Continue` --> wait for provisions etc, come back in a couple of min

7) Explore connector status

  - select connector to go to its dashboard

  - `Explore metrics`

  - `Metric` --> select which metric want to graph so can see how the "volume" of the metric changes over time

8) Explore topic status

  - go to topic dashboard and select topic of interest

  - will see stats in terms of bytes produced/transmitted vs consumed

  - can also click on the different tabs and get different update of info

  - for instance, can go to the message tab and check out the events that have been streamed thus far

9) shut down connector so as not to burn through the trial credits

  - go to the connector dashboard

  - select connector of interest

  - `Pause`

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=ZnEZFEYKppw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=70)

* lecture [slides](https://docs.google.com/presentation/d/1bCtdCba8v1HxJ_uMm9pwjRUC-NAMeB-6nOG2ng3KujA/edit#slide=id.p1)

* confluent get started documentation [page](https://www.confluent.io/confluent-cloud/thank-you/)
