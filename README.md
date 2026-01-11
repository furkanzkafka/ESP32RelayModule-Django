# ESP32 Relay Control System

A Django web application that controls an ESP32-based relay system through AWS IoT Core MQTT messaging. This system provides a secure and reliable way to remotely control relay operations through a web interface. Project mainly build for [lans](https://lans.app/about).

## 🔧 System Architecture

```
Web Interface (Django) <-> AWS IoT Core <-> ESP32 Relay
      [MQTT Publish]       [MQTT Subscribe]
```

## 🚀 Features

- Secure relay control through AWS IoT Core
- Real-time MQTT messaging
- Web-based control interface
- SSL/TLS security with certificate-based authentication
- Error handling and status feedback
- Secure certificate management

## 📋 Prerequisites

- Python 3.8+
- Django 4.2+
- AWS IoT Core account
- ESP32 device with relay module
- AWS IoT certificates
- paho-mqtt library

## 🛠️ Installation

1. Clone the repository
```bash
git clone [your-repository-url]
cd esp32-relay-control
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` with your AWS IoT Core settings:
```plaintext
AWS_IOT_ENDPOINT=your-endpoint.iot.region.amazonaws.com
AWS_IOT_PORT=Your Port
AWS_IOT_TOPIC= Your Topic
AWS_IOT_CLIENT_ID= Your Client ID
DJANGO_SECRET_KEY=your-secret-key
```

## 🔒 AWS IoT Core Setup

1. Create an AWS IoT Core Thing
   - Go to AWS IoT Core Console
   - Create a Thing for your ESP32
   - Create and download certificates

2. Certificate Setup
   - Create a `certificates` directory in project root
   - Add your AWS IoT certificates:
     - Root CA certificate (`AWS_ROOT_CA_FILENAME`)
     - Device certificate (`AWS_DEVICE_CERT_FILENAME`)
     - Private key (`AWS_PRIVATE_KEY_FILENAME`)
   - Update certificate filenames in `.env`

3. Configure IoT Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iot:Connect",
                "iot:Publish",
                "iot:Subscribe",
                "iot:Receive"
            ],
            "Resource": [
                "arn:aws:iot:your-region:your-account:client/${iot:Connection.Thing.ThingName}",
                "arn:aws:iot:your-region:your-account:topic/relaycontrol"
            ]
        }
    ]
}
```

## 🏃‍♂️ Running the Application

1. Apply migrations
```bash
python manage.py migrate
```

2. Start the development server
```bash
python manage.py runserver
```

3. Access the control panel at `http://localhost:8000`

## 🔐 Security Considerations

- Keep certificates secure and never commit them to version control
- Use proper file permissions for certificate files
- Regularly rotate certificates
- Monitor AWS IoT Core logs for unauthorized access attempts
- Use HTTPS in production
- Implement user authentication for the web interface

## 🌐 MQTT Communication

The system uses the following MQTT topic and message format

## 💻 Development

### Project Structure
```
esp32-relay-control/
├── certificates/          # AWS IoT certificates (not in version control)
├── relay_control/        # Django app
│   ├── views.py         # Main control logic
│   └── urls.py          # URL routing
├── templates/           # HTML templates
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

### Key Components

1. **RelayController Class**
   - Handles MQTT communication
   - Manages SSL/TLS certificates
   - Processes relay commands

2. **Web Interface**
   - Simple control panel
   - Status feedback
   - Error handling

## 📝 License

MIT

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## 🙏 Acknowledgments

- AWS IoT Core documentation
- Django documentation
- Paho MQTT library
