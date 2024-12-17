### Schmemas: Ensuring Kafka Stream Structure

* producer and consumers are required to communicate messages in the same format and language at all time to prevent stream flow from coming to a halt 

* to ensure that the above is met, shcemas are used 

* schemas are essentially a contract between producers and consumers 

* Producer creates the schema for they already know the data structure --> distribute schemas to consumers 

* then producers and consumers with the same schemas can communicate with each other 

* it is almost like producers and consumers having the same data dictionary without knowing much about each other 

* This also means when it comes to a topic that is very popular with many consumers, it is difficult to make updates/changes for the producer is required to remain compliant with all the different consumers 

### Schema Registry

* controls comms btw producers/consumers 

* also verifies compatability 

* schema/producer/consumer interaction sequence 

    - producer sends the proposed schema for data streaming to the schema registry 

    - if its schema version 0 it is accepted, if the schema has already been registered and it doesnt comply with the registry then it is rejected 

    - Once producer has schema approval from the registery, it can start streaming messages of the topic towards its consumers

    - while this streaming occurs, consumers fetch the schema dictionary from the schema registry. It can fetch a different version of that stream schema compared to the one that the producer is using. So long as there are no compatability issues, all is good 

### Avro 

* data serialization system 

* makes prod and consumer compatible with each other w/o actual communication 

* mostly used in production

* numerous types of data structures 

### Compatibility types 

* forward compatability 

    - where for instance producers can provide data based on schema version 2 and consumers can consume data based on version 1 of schema 

    - this would be beneficial in cases for example where producers add a field within their exported message but its an optional field to be consumed by consumer 

* backward compatability 

    - consumers can consume with version 2 schema but producers continue to provide message with version 1 schema 

    - this is beneficial for example also when an optional field is introduced, where consumer wont raise an error message because it will permit the additional optional field 

* mixed version (full compatible) 

    - producers and consumers are producing and consuming with completely different versions of schemas and all is still compatible 

### Code in demo

* [java/kafka_examples/src/main/avro](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/06-streaming/java/kafka_examples/src/main/avro) directory 

* [AvroProducer.java](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/main/java/org/example/AvroProducer.java) 


### Helpful Links

* YT [video](https://www.youtube.com/watch?v=tBY_hBuyzwI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=78)

* lecture [slides](https://docs.google.com/presentation/d/1fVi9sFa7fL2ZW3ynS5MAZm0bRSZ4jO10fymPmrfTUjE/edit#slide=id.g2505704cc3_1_35)

* kafka [documentation](https://kafka.apache.org/documentation/) for further reading

* confluence [documentation](https://docs.confluent.io/platform/current/streams/concepts.html) on kafka streams

* avro [homepage](https://avro.apache.org/)

* avro deserializer [documentation](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html) in confluence cloud 

