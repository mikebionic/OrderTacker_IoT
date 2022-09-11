from main_pack import create_app
from main_pack.config import Config

app = create_app()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port = 5000)
