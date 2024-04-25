### What is kafka streaming

* center components of kafka is topic

* Topics:

  + they are a continuous stream of events

  + an event is defined as a collection of data or variables that are recorded in a single unit of time and streamed to a destination

  + event is essentially a single data point with the associated timestamp

* Logs:

  + they are a way in which events of a topic are stored

  + it is centric to how data/events are stored inside a topic

* Events:

  + it consists of a message that stores info about the event and what is needed to be transmitted to the consumer

  + structure: key, value, timestamp (looks a lot like a json)

  + key is typically used to reference the target value, also typically used for partitioning

  + value is the target component of the data exchange

  + timestamp indicates when the value was transmitted in the event

### Advantageous of Kafka

* it provides robustness/reliability to streams/topic

  - this is due to kafka replicating data across different nodes

* very flexible in terms of size of streams and target consumer/audience

  - also flexible with storage/end point

* permits scalability --> can handle rapid ramp up of event volume traffic

* there is defined expiration of topics, which permits storage of events of lengthy periods of time

### The need for stream processing

* Traditionally, data management is managed by monolithic data structure - where data is created/stored/transformed in a single data location

* Microservices are small applications that work together and consists of interactions with each other and other larger/smaller data sources via usually APIs

  - this isn't an issue for monolith when transactions consists of small data volumes

  - this becomes an issue when the data volume grows at a fast rate

* Solution:

  - various microservices (applications) read and write different events within a kafka topic

  - kafka also provides CDC (change data capture): its sort of a "temp location" of events data between the central DWH and microservices. The central DWH can write data to a kafka topic and microservices can read from the topics

  - kafka can act as bridge between monolith and microservice type architectures


### Helpful Links

* YT [video](https://www.youtube.com/watch?v=zPLZUDPi4AY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=69)

* lecture [slides](https://docs.google.com/presentation/d/1bCtdCba8v1HxJ_uMm9pwjRUC-NAMeB-6nOG2ng3KujA/edit#slide=id.p1)

* medium article on [data management architecture](https://towardsdatascience.com/data-management-architectures-monolithic-data-architectures-and-distributed-data-mesh-63743794966c)
