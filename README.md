# AquaBill

![AquaBill Logo](/aquabill/static/imgs/logo.png)

AquaBill is an Internet of Things (IoT) application designed to help apartment residents monitor their water usage and expenses. Utilizing a combination of Arduino and ESP32 devices, the system provides real-time water consumption data through a robust web dashboard built with Django, HTML, CSS, and JavaScript.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Contributors](#contributors)

## Installation

To set up AquaBill on your local environment, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Aqua-Bill.git
   pip install requirements.txt


## Usage

After installing and setting up AquaBill, access the web dashboard by navigating to `http://localhost:8000` in your web browser. Here you can:

- **View Real-time Water Usage:** See up-to-the-minute data on water consumption for your apartment.
- **Access Historical Data:** Review daily and monthly usage statistics to monitor trends and potential leaks.
- **Manage Costs:** Automatically calculate and track your water expenses based on usage.

## Features

- **Real-Time Monitoring:** Instant updates on water consumption directly from IoT devices.
- **Historical Analysis:** Access detailed reports of past consumption with daily and monthly breakdowns.
- **Cost Tracking:** Automatic calculations to keep track of your water spending.
- **User-Friendly Dashboard:** A fully interactive dashboard built with Django, HTML, CSS, and JavaScript.

## Dependencies

- Django
- Arduino IDE
- ESP32
- Libraries for HTTP communication between microcontrollers and the server

## Configuration

Before using the system, ensure each Arduino and ESP32 device is configured to:
1. Send HTTP requests to the Django backend.
2. Connect to the internet via WiFi or any other suitable network configuration.
3. Attched to a water flow sensor.
4. Connected to the same network as the Django server.


- **Connectivity Issues:** Ensure all devices are properly connected to the internet.
- **Data Errors:** Check the format and integrity of the data being sent from the IoT devices.

## Contributors

- **[Mothanna](https://github.com/Mothannahuss)**
