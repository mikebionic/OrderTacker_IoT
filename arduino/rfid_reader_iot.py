
import serial, requests, json

config = {
	"serial_port": "/dev/ACM0",
	"baudrate": 9600,
	"server_host": "http://localhost",
	"server_port": "5000",
	"server_route": "/rfid_tag/",
	"location": "International Aeroport of Turkmenistan",
	"location_key": "crypted_code_of_international_aeroport"
}

try:
	with open('iot_config.json', 'r') as f:
		config = json.load(f)
except:
	pass


ser = serial.Serial(port=config['serial_port'], baudrate=config['baudrate'], timeout=1)
url = f"{config['server_host']}:{config['server_port']}{config['server_route']}"

while True:
    stream = ser.readline()
    print(stream)
    try:
        stream.indexOf("card_")
        card_code = stream.split("_")[1]
        print(f"{url}{card_code}")
        r = requests.get(f"{url}{card_code}")
    except Exception as ex:
        print(ex)