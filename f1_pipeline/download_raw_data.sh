mkdir ./f1_pipeline/csv_data
wget -P ./f1_pipeline/csv_data http://ergast.com/downloads/f1db_csv.zip

unzip ./f1_pipeline/csv_data/f1db_csv.zip -d ./f1_pipeline/csv_data && rm ./f1_pipeline/csv_data/f1db_csv.zip 