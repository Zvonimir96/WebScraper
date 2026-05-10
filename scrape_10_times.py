#!/home/zvone/proj/webScraper/venv/bin/python
import sys
import subprocess

for i in range(10):
    print(f"Pokretanje {i+1}/10")
    subprocess.run([sys.executable, "scrape_page.py"], check=True)
