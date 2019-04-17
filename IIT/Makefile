all: model_train_test_split inspections_train_test_split data_portal_inspections

data/historical_weather.csv:
	python3 06_get_weather.py "data/historical_weather.csv"

data_portal_inspections: data/canvass_records.csv.gz data/complaint_records.csv.gz

data/complaint_records.csv.gz:
	python3 05_get_data_portal_records.py "05_get_complaint_records.sql" "data/complaint_records.csv.gz"

data/canvass_records.csv.gz:
	python3 05_get_data_portal_records.py "05_get_canvass_records.sql" "data/canvass_records.csv.gz"

# Split inspection data into training and test data
inspections_train_test_split: data/inspections.csv
	python3 02_train_test_split.py "data/inspections_train.csv" "data/inspections_test.csv" "data/inspections.csv"

# Join inspection data
data/inspections.csv: data/model_matrix.csv data/inspection_records.csv
	python3 04_join_inspection_details.py "data/inspections.csv" "data/model_matrix.csv" "data/inspection_records.csv"

# Retrieve inspection data
data/inspection_records.csv:
	python3 03_get_inspection_records.py "data/inspection_records.csv"

# Split dataset into training and test data
model_train_test_split: data/model_matrix.csv
	python3 02_train_test_split.py "data/train_data.csv" "data/test_data.csv" "data/model_matrix.csv"

# Prepare features according to Chicago paper
data/model_matrix.csv: data/clean_data.csv
	python3 01_prepare_model_matrix.py "data/model_matrix.csv" "data/clean_data.csv"

# Clean and filter processed data output from R scripts
data/clean_data.csv:
	python3 00_prepare_data.py "data/clean_data.csv" "../DATA/dat_model.Rds"

clean:
	rm data/clean_data.csv
	rm data/inspections_test.csv
	rm data/test_data.csv
	rm data/inspection_records.csv
	rm data/inspections_train.csv
	rm data/inspections.csv
	rm data/model_matrix.csv
	rm data/train_data.csv
	rm data/complaint_records.csv.gz
	rm data/canvass_records.csv.gz