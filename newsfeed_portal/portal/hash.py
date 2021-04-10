import hashlib
import datetime

timestamp_now = int(datetime.datetime.timestamp(datetime.datetime.now()))
print("timestamp: " + str(timestamp_now))

client_message = str(timestamp_now) + "newsfeed"

generated_signature_by_client = hashlib.sha256(client_message.encode()).hexdigest()
print("signature:" + generated_signature_by_client)