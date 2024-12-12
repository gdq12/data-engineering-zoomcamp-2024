### Java code for building a kafka stream

* this to be reviewed at a later time 

* it looks like it might of been this [script](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/main/java/org/example/JsonKStream.java)

### Walk through of stream application

* message import into kafka 

    - each topic is a `PU location` time --> this IDs the group key 

    - all rides/records with the same timestamp were grouped together and assigned the same group ID

* in small scale (where thre is 1 app) both partitions of topic are sent to that 1 app/node

* in the case where topics are sent to more than 1 node/app

    - each of the 2 partitions will be sent to each app

    - then computations (group by and count) will take place in the app

    - if the messages aren't paritioned correctly between then the count calculation may be in correct --> this is all dependent on the group key 

    - kafka compensates for this: 

        + producer is writting to different paritions -->

        + kafka hashes the group key and divides it by the paritions count --> this means that the key determines in which partition the data will go into 

        + with the above mentioned method, it means that each group key will always go to the same paritionin the same app 

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=dUyA_63eRb0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=73)

* lecture [slides](https://docs.google.com/presentation/d/1fVi9sFa7fL2ZW3ynS5MAZm0bRSZ4jO10fymPmrfTUjE/edit#slide=id.g2505704cc3_1_35)

* kafka [documentation](https://kafka.apache.org/documentation/) for further reading

* confluence [documentation](https://docs.confluent.io/platform/current/streams/concepts.html) on kafka streams