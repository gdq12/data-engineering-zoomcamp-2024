### What is a kafka cluster?

* nodes/machine talking to each other 

* kafka communication with each other: 

    - used to be facilitated by zookeeper --> facilitate all on topics and partitions 

    - now uses kafka internals: now stores all topics and its metadata 

### Topics for NY taxi data sets 

* in this case 1 topic is rides --> consists records of all rides reported by the TLC taxi website

* each stream of the topic consisted of a vendorId (key) and all the metadata about that ride (values)

* producer is the one providing the records via messages in kafka 

### How kafka provides reliability 

* This is mostly due to kafkas **replication** mechanism

* within a kafka cluster, there are multiple nodes/machines. For a given topic there are a minimum of 2 nodes that are assigned to the topic: leader and a follower 

* the producer and consumer of the topic interact with the leader node to update/consume/provide records of the topic. For everytime a record is added to the the leader node by the producer, a copy of that messag.record is sent to the follower node

* in case the leader node is disabled/incapacitated, the follower node hold the copy of the topic from the leader node and can continue to work in the leaders case. There may be a slight delay but eventually the producer and consumer would then connect to the follower cluster 

* the follower cluster then becomes a leader cluster, then another cluster eventually transitions to become a follower cluster and receives copies of the messages of that topic

### Retention

* how long data will be retained by kafka 

* this is usually set in the beginning of the setup, it essentially dictates how old records of a given topic will be before it is deleted from kafka 

### Partitions 

* partitions can be applied within a single topic 

* for a single topic, its partitions can reside in different nodes (they are both consider leader nodes in this case) and their copies can reside in other nodes. 

* A node can be a leader for one partition and a follower for another paritition 

* consumers can interact with partitions in different nodes, they would jusst interact with the leader node for that respective partition 

* a consumer can read from multiple partitions at a time, but a partition can only feed messages to 1 consumer

* there are instances when a consumer is connected to multiple partitions and has an overload of messages which leads to processing delays. A second consumer can be introduced and connect to one of the partitions, so as to transition a bit closer to 1:1 relationship between partitions and consumer 

* for a given consumer, there can be multiple receivers, kafka will recognize them as going to the same consumer because they share the same consumer group ID 

* for a given topic, if there are 2 partitions, they can only be connected to 2 consumers max (even if there are more consumers available). But if 1 of the consumers failed, then kafka will know to redirect the messages to the next available consumer within the same group ID 

### Offsets 

**up to 20:29 in video**



### Helpful Links

* YT [video](https://www.youtube.com/watch?v=SXQtWyRpMKs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=73)

* lecture [slides](https://docs.google.com/presentation/d/1bCtdCba8v1HxJ_uMm9pwjRUC-NAMeB-6nOG2ng3KujA/edit#slide=id.p1)