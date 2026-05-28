python3 -m venv venv
source venv/bin/activate

python scripts/generate_logs.py
python analyzer.py data/sample.log
