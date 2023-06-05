from langchain.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(file_path='./podium_data.csv')
data = loader.load()
print(len(data))
