# Join inspection data
data/inspections.csv: data/model_matrix.csv data/inspections_records.csv
	python3 04_join_inspection_details.py "data/inspections.csv" "data/model_matrix.csv" "data/inspections_records.csv"

# Retrieve inspection data
data/inspections_records.csv:
	python3 03_get_inspection_records.py "data/inspections_records.csv"

# Split dataset into training and test data
train_test_split: data/model_matrix.csv
	python3 02_train_test_split.py "data/train_data.csv" "data/test_data.csv" "data/model_matrix.csv"

# Prepare features according to Chicago paper
data/model_matrix.csv: data/clean_data.csv
	python3 01_prepare_model_matrix.py "data/model_matrix.csv" "data/clean_data.csv"

# Clean and filter processed data output from R scripts
data/clean_data.csv:
	python3 00_prepare_data.py "data/clean_data.csv" "../DATA/dat_model.Rds"

clean:
	rm data/*.csv
