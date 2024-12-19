INPUT_DATA_PATH = 'rides.csv'

RIDE_KEY_SCHEMA_PATH = 'schemas/taxi_ride_key.avsc'
RIDE_VALUE_SCHEMA_PATH = 'schemas/taxi_ride_value.avsc'

SCHEMA_REGISTRY_URL = 'http://172.18.0.4:8081' # updated accordingly after using docker inspect command
BOOTSTRAP_SERVERS = '172.18.0.3:29092' # updated accordingly after using docker inspect command
KAFKA_TOPIC = 'rides_avro'
