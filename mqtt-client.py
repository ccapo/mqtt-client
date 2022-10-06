import paho.mqtt.client as mqtt
import signal
import logging
import json

logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%y-%m-%d %H:%M:%S')

customer_uuid = '5829835c-4773-44e1-90c1-33fd583328ef'
client_uuid = '060ab0cc-2873-43c8-a191-21455d1d0145'
group_id = 123

# Default client topics
topics = dict()
topics['sub_all']         = f"cmd/sub/{customer_uuid}"
topics['sub']             = f"cmd/sub/{customer_uuid}/{client_uuid}"
topics['scan_all']        = f"cmd/scan/{customer_uuid}"
topics['scan']            = f"cmd/scan/{customer_uuid}/{client_uuid}"
topics['contain_all']     = f"cmd/contain/{customer_uuid}"
topics['contain']         = f"cmd/contain/{customer_uuid}/{client_uuid}"
topics['uncontain_all']   = f"cmd/uncontain/{customer_uuid}"
topics['uncontain']       = f"cmd/uncontain/{customer_uuid}/{client_uuid}"
topics['upgrade_all']     = f"cmd/upgrade/{customer_uuid}"
topics['upgrade']         = f"cmd/upgrade/{customer_uuid}/{client_uuid}"

# Dynamic client topics
topics['scan_group']      = f"cmd/scan/{customer_uuid}/group/{group_id}"

# Default server topics
srv_topics = dict()
srv_topics['sub']         = "cmd/sub/status"
srv_topics['scan']        = "cmd/scan/status"
srv_topics['containment'] = "cmd/containment/status"
srv_topics['upgrade']     = "cmd/upgrade/status"
srv_topics['healthcheck'] = f"data/healthcheck/{customer_uuid}"

class MQTTClass:
  def __init__(self, client_id = None, host = 'localhost', port = 1883, keepalive = 60):
    clean_session = False
    if client_id is None or client_id == '':
      clean_session = True
    self.client = mqtt.Client(client_id = client_id, clean_session = clean_session)

    self.topics = topics

    self.client.on_connect = self.on_connect
    self.client.on_disconnect = self.on_disconnect
    self.client.on_message = self.on_message

    self.client.message_callback_add(topics['command_all'], self.on_message_command)
    self.client.message_callback_add(topics['command'], self.on_message_command)

    self.client.message_callback_add(topics['scan_all'], self.on_message_scan)
    self.client.message_callback_add(topics['scan'], self.on_message_scan)
    # Dynamically add/remove
    self.client.message_callback_add(topics['scan_group'], self.on_message_scan)

    self.client.message_callback_add(topics['contain_all'], self.on_message_contain)
    self.client.message_callback_add(topics['contain'], self.on_message_contain)

    self.client.message_callback_add(topics['uncontain_all'], self.on_message_uncontain)
    self.client.message_callback_add(topics['uncontain'], self.on_message_uncontain)

    self.client.message_callback_add(topics['upgrade_all'], self.on_message_upgrade)
    self.client.message_callback_add(topics['upgrade'], self.on_message_upgrade)

    self.client.message_callback_add(topics['log_all'], self.on_message_log)
    self.client.message_callback_add(topics['log'], self.on_message_log)

    logger = logging.getLogger(__name__)
    self.client.enable_logger(logger)

    self.client.connect_async(host, port, keepalive)

  # The callback for when the client receives a CONNACK response from the server.
  def on_connect(self, client, userdata, flags, rc):
    logging.info(f"MQTT Broker Connection Request: {mqtt.connack_string(rc)}")
    if rc == 0:
      # Subscribing in on_connect() means that if we lose the connection and
      # reconnect then subscriptions will be renewed.
      for _, topic in topics.items():
        client.subscribe(topic)

  def on_disconnect(self, client, userdata, rc):
    if rc != 0:
      logging.error("Unexpected MQTT Broker Disconnection", exc_info=True)
    else:
      logging.info(f"MQTT Broker Disconnection Request: {mqtt.connack_string(rc)}")

  def on_message_command(self, client, userdata, msg):
    # Add logic to subscribe/unsubscribe from a topic, as well as add/remove message callback
    #data = json.loads(msg.payload)
    #logging.info(f"foo: {data['foo']}")
    logging.info(f"[command] {str(msg.payload,'utf-8')}")

  def on_message_scan(self, client, userdata, msg):
    logging.info(f"[scan] {str(msg.payload,'utf-8')}")

  def on_message_contain(self, client, userdata, msg):
    logging.info(f"[contain] {str(msg.payload,'utf-8')}")

  def on_message_uncontain(self, client, userdata, msg):
    logging.info(f"[uncontain] {str(msg.payload,'utf-8')}")

  def on_message_upgrade(self, client, userdata, msg):
    logging.info(f"[upgrade] {str(msg.payload,'utf-8')}")

  def on_message_log(self, client, userdata, msg):
    logging.info(f"[log] {str(msg.payload,'utf-8')}")

  # The callback for when a PUBLISH message is received from the server.
  def on_message(self, client, userdata, msg):
    logging.warning(f"Unrecognized topic: '{msg.topic}'")

  def start(self):
    self.client.loop_start()

  def stop(self):
    self.client.loop_stop()

# MQTTClient instance
mc = MQTTClass(host = '192.168.1.30')

# Our signal handler
def signal_handler(signum, frame):
  mc.stop()
  print("")
  logging.info(f"Signal {signum} received, exiting...")
  exit(0)

# Register our signal handler with desired signal
signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
  # Blocking call that processes network traffic, dispatches callbacks and
  # handles reconnecting.
  # Other loop*() functions are available that give a threaded interface and a
  # manual interface.
  mc.start()

  signal.pause()