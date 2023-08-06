# Kafka-Temporal Mapper Client

Kafka-Temporal mapper client facilitates the interaction between the workflows and the Kafka-Temporal mapper server.
This library is used by the workflows and provides methods for publishing of the workflow and mapping events. 

The client provides two methods:
- **subscribe**: used to subscribe a workflow to the execution of another workflow.   
- **notify**: used by a workflow to notify the termination of its execution.  

### Installation
```bash
pip install kafka_temporal_mapper_client
```

### Usage
To use this library for notifying or subscribing:
```python
from kafka_temporal_mapper.client import KafkaTemporalClient

ktc = KafkaTemporalClient()

# subscribe workflow B to workflow A using a part of A's results as argument (@b.c)
ktc.subscribe('WorkflowB', [{'name':'WorkflowA', 'args': {"a":"hello", "b":"@b.c"}}]) 

# notify workflow A execution and its results
ktc.notify('WorkflowA', {"a":"hello", "b": {"c": "world"}})
```
