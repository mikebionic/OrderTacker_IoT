# Haryt Nirede - Smart RFID-Based Order Tracking System

![Project Screenshot](https://mikebionic.github.io/portfolio/static/projects/web_proj/sargyt.webp)

**Haryt Nirede** is an innovative IoT-enabled order tracking application that combines RFID technology with a modern web interface for real-time product localization and access control. Built as a rapid prototype in two weeks, it demonstrates efficient integration of Arduino-based hardware with a Flask web application.

🏆 **Achievement**: 2nd place at Digital Solutions 2022 (Sanly Çözgüt)

## 🎥 Demo Video
[Watch on YouTube](https://www.youtube.com/watch?v=-3AhmyTGvKg)

---

## 📋 Table of Contents
- [Application Overview](#application-overview)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Hardware Setup](#hardware-setup)
- [Configuration](#configuration)
- [Contributing](#contributing)

---

## 🔧 Application Overview

### Core Features
- **RFID-based Access Control**: Track entries/exits using RFID cards or fingerprint sensors
- **Real-time Logging**: Monitor access events with timestamps and location data
- **Multi-location Support**: Handle multiple access points and locations
- **User Management**: Admin interface for managing users and their access credentials
- **RESTful API**: Complete API for integration with external systems
- **IoT Integration**: Arduino-based RFID readers with serial communication

### Technology Stack
- **Backend**: Flask (Python 3.8+)
- **Database**: SQLite (configurable to other databases)
- **Frontend**: HTML/CSS/JavaScript templates
- **Hardware**: Arduino Uno + MFRC522 RFID Module
- **Communication**: Serial/USB communication between Arduino and Python

### Useful Links
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MFRC522 Arduino Library](https://github.com/miguelbalboa/rfid)
- [Python Serial Library](https://pyserial.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

---

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   RFID Reader   │────│  Python Script   │────│  Flask Web App  │
│   (Arduino)     │USB │ (rfid_reader.py) │HTTP│   (Backend)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        │
                                                ┌───────▼────────┐
                                                │  SQLite DB     │
                                                │  (app.db)      │
                                                └────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Arduino IDE (for hardware setup)
- USB cable for Arduino connection

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:mikebionic/OrderTacker_IoT.git
   cd OrderTacker_IoT/web
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database**
   ```bash
   python migrate.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Web Interface: `http://localhost:5000`
   - API Base URL: `http://localhost:5000/api`

---

## 📡 API Documentation

### Authentication Routes

#### RFID Logger (Card-based)
```http
GET /api/rfid_logger/?code={CARD_CODE}&location={LOCATION_NAME}
```
**Parameters:**
- `code` (required): RFID card code (e.g., "8A:4B:81:7F")
- `location` (optional): Location identifier (default: "entrance")

**Response:**
```json
{
  "user": {
    "id": 2,
    "username": "plan",
    "name": "Plan",
    "surname": "Planyyew",
    "position": "Iş ýörediji"
  },
  "location": {
    "id": 1,
    "name": "entrance",
    "full_name": "Plan yerin girelgesi"
  },
  "entrance_type": 1
}
```

#### Fingerprint Logger
```http
GET /api/finger_logger/?device_key={SECRET}&finger_id={ID}
```
**Parameters:**
- `device_key` (required): Device authentication key
- `finger_id` (required): Fingerprint sensor ID
- `access_type` (optional): Access method description

### Data Retrieval Routes

#### Get Access Logs
```http
GET /api/access_logs/?finger_id={ID}&entrance_type={TYPE}&location_id={LOC_ID}
```
**Query Parameters:**
- `finger_id`: Filter by specific finger/card ID
- `entrance_type`: Filter by entry (1) or exit (0)
- `location_id`: Filter by location
- `access_type`: Filter by access method

#### Get Fingerprint Data
```http
GET /api/fingerprints_data/
```
*Requires authentication*

#### Configure Fingerprint
```http
POST /api/configure_fingerprint/
Content-Type: application/json

{
  "finger_id": 1,
  "name": "User Display Name"
}
```

### Order Locator (IoT Integration)
```http
GET /api/order_locator/?location={LOCATION}&location_key={KEY}&entrance_type={TYPE}&description={DESC}&code={CARD_CODE}
```

---

## 🔌 Hardware Setup

### Arduino Components
- **Arduino Uno/Nano** (or compatible)
- **MFRC522 RFID Module**
- **Servo Motor** (for door control)
- **LED Indicator**
- **Buzzer**
- **Push Button**
- **Breadboard and jumper wires**

### Arduino Pinout Configuration

| Component | Arduino Pin | Description |
|-----------|-------------|-------------|
| MFRC522 SDA | Pin 10 | SPI Slave Select |
| MFRC522 SCK | Pin 13 | SPI Clock |
| MFRC522 MOSI | Pin 11 | SPI MOSI |
| MFRC522 MISO | Pin 12 | SPI MISO |
| MFRC522 RST | Pin 9 | Reset Pin |
| Servo Signal | Pin 2 | PWM Control |
| LED Indicator | Pin 2 | Status Light |
| Buzzer | Pin 4 | Audio Feedback |
| Push Button | Pin 7 | Manual Override |

### Hardware Assembly

1. **Connect MFRC522 RFID Module:**
   ```
   MFRC522    Arduino Uno
   -------------------------
   VCC     -> 3.3V
   RST     -> Pin 9
   GND     -> GND
   MISO    -> Pin 12
   MOSI    -> Pin 11
   SCK     -> Pin 13
   SDA     -> Pin 10
   ```

2. **Connect Additional Components:**
   - Servo: Signal to Pin 2, Power to 5V, Ground to GND
   - LED: Anode to Pin 2 (with 220Ω resistor), Cathode to GND
   - Buzzer: Positive to Pin 4, Negative to GND
   - Button: One terminal to Pin 7, other to GND (using internal pullup)

### Arduino Code Setup

1. **Install Required Libraries:**
   - Open Arduino IDE
   - Go to Sketch → Include Library → Manage Libraries
   - Install: "MFRC522" by GithubCommunity
   - Install: "Servo" (usually pre-installed)

2. **Upload the Code:**
   - Open `rfid_reader.ino` in Arduino IDE
   - Select your board and port
   - Upload the sketch

3. **Add RFID Cards:**
   ```cpp
   String registeredCards[] = {
     "8A:4B:81:7F",  // Add your card IDs here
     "DA:32:1B:3F",
     "C9:CE:B1:C2"
   };
   ```

### Testing Hardware
1. Connect Arduino to computer via USB
2. Open Serial Monitor (9600 baud)
3. Present RFID card to reader
4. Should see output: `card_XX:XX:XX:XX`

---

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Flask Configuration
SECRET_KEY=your-very-secret-key-change-this-for-production
FLASK_DEBUG=true

# Database Configuration
DATABASE_URL=sqlite:///app.db

# Admin User Configuration
ADMIN_USERNAME=admin
ADMIN_PIN=1234

# Device Configuration
DEVICE_SECRET=finger_secret_key
```

### IoT Configuration (iot_config.json)
```json
{
  "serial_port": "/dev/ttyACM0",
  "baudrate": 9600,
  "server_host": "http://localhost",
  "server_port": "5000",
  "server_route": "/api/rfid_logger/",
  "entrance_type": "entrance",
  "location": "Main Office",
  "location_key": "secure_location_key",
  "description": "Access logged at main entrance"
}
```

### Database Models

The system uses four main models:

1. **User**: Store user information and credentials
2. **Finger**: RFID/Fingerprint mappings to users
3. **Location**: Physical locations/access points
4. **Access_log**: Historical access records

### Running IoT Reader

1. **Connect Arduino** to your computer
2. **Update serial port** in `iot_config.json`
3. **Run the reader script:**
   ```bash
   python rfid_reader_iot.py
   ```

The script will:
- Read RFID cards from Arduino serial output
- Send HTTP requests to your Flask API
- Log all activities

---

## 🛠️ Development

### Project Structure
```
haryt-nirede/
├── main/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── models.py            # Database models
│   ├── api/
│   │   ├── __init__.py      # API blueprint
│   │   └── routes.py        # API endpoints
│   └── views/
│       ├── __init__.py      # Views blueprint
│       └── routes.py        # Web routes
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── iot_config.json         # IoT device configuration
├── rfid_reader_iot.py      # Python IoT reader
├── rfid_reader.ino         # Arduino sketch
├── app.py                  # Application entry point
├── init_db.py              # Database initialization
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables
```

### Adding New RFID Cards

1. **Hardware Method (Arduino):**
   ```cpp
   String registeredCards[] = {
     "8A:4B:81:7F",
     "NEW:CARD:ID",  // Add here
   };
   ```

2. **Database Method:**
   ```python
   # In init_db.py or via API
   new_finger = Finger(
       user_id=user_id,
       code="NEW:CARD:ID",
       name="Card Description"
   )
   db.session.add(new_finger)
   db.session.commit()
   ```

### API Testing
```bash
# Test RFID logger
curl "http://localhost:5000/api/rfid_logger/?code=8A:4B:81:7F&location=entrance"

# Test access logs
curl "http://localhost:5000/api/access_logs/?entrance_type=1"

# Test fingerprint logger
curl "http://localhost:5000/api/finger_logger/?device_key=finger_secret_key&finger_id=1"
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Digital Solutions 2022 (Sanly Çözgüt)** for the platform and recognition
- **MFRC522 Community** for the excellent Arduino RFID library
- **Flask Community** for the robust web framework

---

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check existing documentation
- Review the demo video for visual guidance

**Built with ❤️ for smart logistics and access control systems**