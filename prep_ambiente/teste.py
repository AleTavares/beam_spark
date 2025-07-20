import kagglehub

# Download latest version
path = kagglehub.dataset_download("datahackers/state-of-data-brazil-2023", path='./data.csv')

print("Path to dataset files:", path)