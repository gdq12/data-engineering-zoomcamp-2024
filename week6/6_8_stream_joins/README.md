### Theory on joining topic streams

- in kafka joins are only possible on the key of the particular message 

- can modify the group key for each topic from the producer 

- in this topology scenario: 

    + create 2 topics: ride w/drop-off location as key, and pickup location topic w/pickup location as key

    + join on location IDs

    + this is beneficial instances where an application or service needs to find the relationship of 2 topics to update the end user app instantaenously. 

    + no need to then import this data into a monolith system to then provide a quick result 

    + good to remember: both topics need to have the same number of partitions, keys join only on inner joins, all keys mut be paired off 

- reviewed the java script code which can be found [here](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/main/java/org/example/JsonKStreamJoins.java)

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=NcpKlujh34Y&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=74)

* lecture [slides](https://docs.google.com/presentation/d/1fVi9sFa7fL2ZW3ynS5MAZm0bRSZ4jO10fymPmrfTUjE/edit#slide=id.g2505704cc3_1_35)

* kafka [documentation](https://kafka.apache.org/documentation/) for further reading

* confluence [documentation](https://docs.confluent.io/platform/current/streams/concepts.html) on kafka streams