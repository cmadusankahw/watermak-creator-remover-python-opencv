#!/bin/bash
echo "-------------------------------------------------"
echo "------------LankaEAdds Updater v1.0--------------"
echo "-------------------------------------------------"
echo "Installing required Dependencies..."
pip install -r requirements.txt
pip3 install -r requirements.txt
echo "Starting Updating..."
python lanka_e_adds_updater.py riyasewana_scraper_data.csv
echo "All Updating Completed!"
echo "-------------------------------------------------"
