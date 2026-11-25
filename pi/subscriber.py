import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "localhost"
PORT = 1883
TOPICS = ["espresso/temperature", "espresso/weight", "espresso/pressure"]

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker")
        for topic in TOPICS:
            client.subscribe(topic)
    else:
        print("Connection failed, code:", reason_code)

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print("[{}] {}: {}".format(timestamp, msg.topic, msg.payload.decode()))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()
