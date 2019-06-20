install:
	. venv/bin/activate; pip3 install -r requirements.txt

test:
	. venv/bin/activate; pytest tests.py

run:
	. venv/bin/activate; python3 scraper.py