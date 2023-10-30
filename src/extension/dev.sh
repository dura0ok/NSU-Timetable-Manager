cd ../python/server || exit 1
rm -rf myvenv
python3 -m venv myvenv
source myvenv/bin/activate
pip install -r requirements.txt
python app.py

