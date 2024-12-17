### ksqlDB

* its a version of SQL but for streams 

* this is mostly used for dev and testing, as a quick way to do spot checks on pipelines etc

* this can be used in production but be weary of its limitations and how it is used

* best to use Java API to know which commands sent and how the results relate to which command etc 

* coommands used in lecture: [commands.md](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/ksqldb/commands.md)

* what is required first is to create a stream table of dimensions interested in from the topic --> then can execute typical sql commands on it (select *, count(*), group by, where conditioning, window funcs etc)

* query functions that are based on `create streams` are more like flows that are only applicable to newly passing messages 

* `create table` creates a persistant query in the background and act almost like a `table` within kafka

### Pros and Cons 

* pros: 

    - it is good to use as POC of concepts prior to building a whole application 

    - it is also good to use to provide live data to a dashboard quickly without having to build extensive backend infra 

* cons: 

    - would say that this is applicable only to live produced data, not really possible with large volume of historical data 

    - have to create own cluster just for the db - doesnt run on stream clusters 

    - can be expensive cause requires own cluster and consume a lot of credits 

### Kafka connect

* there are numerous connectors already available 

* this is available in confluence cloud or also other open source platforms 

* usually can be connected via a curl request 

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=DziQ4a4tn9Y&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=77)

* lecture [slides](https://docs.google.com/presentation/d/1fVi9sFa7fL2ZW3ynS5MAZm0bRSZ4jO10fymPmrfTUjE/edit#slide=id.g2505704cc3_1_35)

* kafka [documentation](https://kafka.apache.org/documentation/) for further reading

* confluence [documentation](https://docs.confluent.io/platform/current/streams/concepts.html) on kafka streams

* confluence [documentation](https://www.confluent.io/blog/windowing-in-kafka-streams/) on windowing

* confluence [hands-on](https://developer.confluent.io/courses/kafka-streams/windowing/) coding for windowing