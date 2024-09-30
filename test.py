import os 
file_path = 'stoic-quote.json'
if os.path.exists(file_path):
    print("File exists")
else:
    print("File does not exist")
