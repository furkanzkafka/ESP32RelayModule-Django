# relay_control/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import paho.mqtt.client as mqtt
import ssl
import os
import logging
import environ
from threading import Event, Timer 

env = environ.Env()

logger = logging.getLogger(__name__)


class RelayController:
    def __init__(self):
        self.aws_endpoint = env('AWS_IOT_ENDPOINT')
        self.port = env.int('AWS_IOT_PORT')
        self.topic = env('AWS_IOT_TOPIC')
        self.client_id = env('AWS_IOT_CLIENT_ID')
        self.connected = Event()
        self.message_sent = Event()
        self.connection_error = None

    def on_connect(self, client, userdata, flags, rc):
        """Callback when client connects"""
        connection_codes = {
            0: "Connected successfully",
            1: "Incorrect protocol version",
            2: "Invalid client ID",
            3: "Server unavailable",
            4: "Bad username or password",
            5: "Not authorized"
        }
        if rc == 0:
            logger.info("Successfully connected to AWS IoT Core")
            self.connected.set()
        else:
            error_message = connection_codes.get(rc, f"Unknown error (code: {rc})")
            logger.error(f"Connection failed: {error_message}")
            self.connection_error = error_message

    def on_publish(self, client, userdata, mid):
        """Callback when message is published"""
        logger.info(f"Message {mid} published successfully")
        self.message_sent.set()

    def on_disconnect(self, client, userdata, rc):
        """Callback when client disconnects"""
        if rc != 0:
            logger.warning(f"Unexpected disconnection (code: {rc})")
        else:
            logger.info("Disconnected successfully")

    def get_cert_paths(self):
        base_path = os.path.join(settings.BASE_DIR, env('CERTIFICATES_PATH'))
        return {
            'ca_certs': os.path.join(base_path, env('AWS_ROOT_CA_FILENAME')),
            'certfile': os.path.join(base_path, env('AWS_DEVICE_CERT_FILENAME')),
            'keyfile': os.path.join(base_path, env('AWS_PRIVATE_KEY_FILENAME')),
        }

    def trigger_unlock(self):
        try:
            cert_paths = self.get_cert_paths()

            # Reset event flags
            self.connected.clear()
            self.message_sent.clear()
            self.connection_error = None

            # Create and configure MQTT client
            client = mqtt.Client(client_id=self.client_id)
            client.on_connect = self.on_connect
            client.on_publish = self.on_publish
            client.on_disconnect = self.on_disconnect

            # Configure TLS/SSL
            client.tls_set(
                ca_certs=cert_paths['ca_certs'],
                certfile=cert_paths['certfile'],
                keyfile=cert_paths['keyfile'],
                tls_version=ssl.PROTOCOL_TLSv1_2,
                cert_reqs=ssl.CERT_REQUIRED,
                ciphers=None
            )

            # Connect with timeout
            client.connect(self.aws_endpoint, self.port, keepalive=60)
            client.loop_start()

            # Wait for connection with timeout
            if not self.connected.wait(timeout=5.0):
                client.loop_stop()
                if self.connection_error:
                    return False, f"Connection failed: {self.connection_error}"
                return False, "Connection timeout"

            # Publish message
            client.publish(self.topic, payload="UNLOCK", qos=1)

            # Wait for publish confirmation
            if not self.message_sent.wait(timeout=5.0):
                client.loop_stop()
                return False, "Message publish timeout"

            # Clean disconnect
            client.loop_stop()
            client.disconnect()

            return True, "Successfully connected to AWS IoT Core and sent unlock command"

        except Exception as e:
            logger.error(f"Error in trigger_unlock: {str(e)}", exc_info=True)
            return False, f"Error: {str(e)}"

def index(request):
    return render(request, 'index.html')


def trigger_relay(request):
    if request.method == 'POST':
        controller = RelayController()
        success, message = controller.trigger_unlock()

        response_data = {
            'success': success,
            'message': message
        }

        # Log the response
        if success:
            logger.info(f"Relay trigger successful: {message}")
        else:
            logger.error(f"Relay trigger failed: {message}")

        return JsonResponse(response_data)
