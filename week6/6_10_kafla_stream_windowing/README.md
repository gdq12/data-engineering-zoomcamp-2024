### Global Kafka Tables 

- global kafka tables (kTables) 

- follows concept of broadcasting

- each node contains a kTable -> contains a topic --> topic paritioned accordingly

- data in each node/kTable is partially there 

- in order to jin data, must then reshuffle so all keys are present within each side of the join 

- in order to avoid this expensive actvity (reshuffling) --> kTables come into play 

    + instead of each node using simple kTables (kafka tables), global kTables are used instead 

    + each node will consists of all partitions/data and therefore reshuffling is unecessary 

- limitations:

    + since all data is stored in node itself --> this can lead to memory/size issue 

    + so global kTables need to be of smaller size 

    + an example of global kTable would be a dimension table, where no history transactio data takes place like fact tables --> these tables can then be present in each of the nodes to reduce need of reshuffling etc 

- how to create global kTables:

    + streamBuilder.globalTble(topicName) 

    + they can then be used for joins and other functions in kafka

### kafka joins

- very simi to regular sql joins: inner, left, outer 

- for inner nad left joins, can do mix match of tables types in joins:

    + KStream - KStream 

    + KTable - KTable 

    + KStream - KTable 

    + KStream - GlobalKTable 

- while outer join can't mix match joins: 

    + KStream - KStream 

    + KTable - KTable 

### Kafka Window functions 

* example method of windowing 

    - they are defined as start and end time periods for kafka messages the fall within that defined window and can be used for transtional functions such as joins 

    - the window size dictates the number of successful join transactions. If two messages fall in good time points within the window (aka not one of them within the last second) then a join can occur. If this is not the case then a join will not occur.

    - a grace period at the end of the time window can be added to increase the number of possible joins, aka to capture those messages that occured at the end of the time window 

* types of windowing (methods of defining start and end points of a window) 

    - tumbling: fixed size, non-overlapping

        + window can be define my start/end second intervals 

        + windows are defined by record key, aka each record key have their own windows per interval 

    - hopping: fixed size, overlapping 

        + these are time windows that have staggering sequential start times 

        + for instance 5-min windows with 1 min "hop", meaning that each consecutive window doesnt wait 5 min to start (aka the previous winodw to conclude), but they start 1 min after the previous one started

        + again, each window is created per record key 

    - sliding: fized size, overlapping windows that work on differences between record timestamps

    - session: dynamically-sized, non-overlapping, data-driven windows 

        + an example would be a 5min window with an inactivity gap 

        + this would mean that the first window would be defined by 5min --> theren there would be a pause in starting a new window only when new activity/stream activity is detected within more than 5min

        + this is advantageos because session boundaries can be defined by end user activiity 

        + so session frequency is completely activity dependent 

### Windowing demo via code 

* example of tumbling window implementation: [JsonKStreamWindow.java](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/main/java/org/example/JsonKStreamWindow.java)

* the [JsonProducer.java](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/06-streaming/java/kafka_examples/src/main/java/org/example/JsonProducer.java) was run before the above mentioned script to create messages 

### Helpful Links

* YT [video](https://www.youtube.com/watch?v=r1OuLdwxbRc&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=77)

* lecture [slides](https://docs.google.com/presentation/d/1fVi9sFa7fL2ZW3ynS5MAZm0bRSZ4jO10fymPmrfTUjE/edit#slide=id.g2505704cc3_1_35)

* kafka [documentation](https://kafka.apache.org/documentation/) for further reading

* confluence [documentation](https://docs.confluent.io/platform/current/streams/concepts.html) on kafka streams

* confluence [documentation](https://www.confluent.io/blog/windowing-in-kafka-streams/) on windowing

* confluence [hands-on](https://developer.confluent.io/courses/kafka-streams/windowing/) coding for windowing