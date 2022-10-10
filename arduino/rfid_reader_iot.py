
import serial, requests, json

config = {
    "serial_port": "/dev/ttyACM0",
    "baudrate": 9600,
    "server_host": "http://localhost",
    "server_port": "5000",
    "server_route": "/api/order_locator/",
    "entrance_type": "entrance",
    "location": "International Aeroport of Turkmenistan",
    "location_key": "crypted_code_of_international_aeroport",
    "description": "Sargyt Aşgabat aeroportda hasabata alyndy we ammara geçirildi"
}

try:
	with open('iot_config.json', 'r') as f:
		config = json.load(f)
except:
	pass

ser = serial.Serial(port=config['serial_port'], baudrate=config['baudrate'], timeout=1)
url = f"{config['server_host']}:{config['server_port']}{config['server_route']}?location={config['location']}&location_key={config['location_key']}&entrance_type={config['entrance_type']}&description={config['description']}"

while True:
    stream = str(ser.readline())
    try:
        if (len(stream) > 5):
            # example "card_8A:4B:81:7F\r\n"
            stream.index("card_")
            card_code = stream.split("_")[1][:11]
            print(f"{url}{card_code}")
            r = requests.get(f"{url}&code={card_code}")
    except Exception as ex:
        print(ex)