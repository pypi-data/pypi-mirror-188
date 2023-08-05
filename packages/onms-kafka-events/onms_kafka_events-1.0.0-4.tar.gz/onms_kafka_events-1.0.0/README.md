![package version](https://img.shields.io/pypi/v/onms_kafka_events)
![python version](https://img.shields.io/pypi/pyversions/onms_kafka_events)

# onms_kafka_events

This library will allow you to generate event objects in Python to send to a Kafka topic for OpenNMS Horizon/Meridian to process.

Documentation for this project is available at https://opennms-forge.github.io/kafka-consumer-py/

Documentation for configuring the Kafka Consumer feature on your Horizon/Meridian server can be found at https://docs.opennms.com/horizon/latest/operation/deep-dive/events/sources/kafka.html.

## Installation

```
pip install onms-kafka-events
```

## Associating events to nodes

When received, the eventd daemon will attempt to associate the event to a node in the following order:

 * If the `nodeId` field is included, the event will be matched to the node with that database ID.
 * If the event does not have `nodeID`, the parameters `_foreignSource` and `_foreignId` can be included to associate the event based on the requisition name and ID.
 * Any event that cannot match a node on either of these criteria will not be associated with a node.

## Example

```py
from onms_kafka_events import KafkaConnection, Severity

my_producer = KafkaConnection(
    servers=["broker01:9092", "broker02:9092"], topic="opennms-kafka-events"
)

my_event = my_producer.create_event(
    uei="uei.opennms.org/custom/event",
    severity=Severity.WARNING,
    node_id=1234,
    custom="value"
)

result = my_producer.send_event(my_event)
```
