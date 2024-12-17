### Testing theory 

* in previous example built a kafka class "Stream builder"
    
    - it took messages from 2 topics -->

    - join the messages on a key and performed some sort of calculation -->

    - and then outputted it to a new topic 

* the steps mentioned above is known as a topology

    - this is what can be tested in kafka via a topology driver 

### Java scripts 

* the topology of interest to be tested in the stream builder script was [JsonKStream.java](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/main/java/org/example/JsonKStream.java)

* testing the above script was done with [JsonKStreamTest.java](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/test/java/org/example/JsonKStreamTest.java) and [JsonKStreamJoinsTest.java](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/test/java/org/example/JsonKStreamJoinsTest.java)

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=TNx5rmLY8Pk&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=75)

* lecture [slides](https://docs.google.com/presentation/d/1fVi9sFa7fL2ZW3ynS5MAZm0bRSZ4jO10fymPmrfTUjE/edit#slide=id.g2505704cc3_1_35)

* kafka [documentation](https://kafka.apache.org/documentation/) for further reading

* confluence [documentation](https://docs.confluent.io/platform/current/streams/concepts.html) on kafka streams