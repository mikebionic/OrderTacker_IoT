from main import create_app
from main.config import Config

app = create_app()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port = 5000)
