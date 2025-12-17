# convert_data_to_utf8.py
import codecs

with codecs.open('data.json', 'r', encoding='utf-16') as f:
    data = f.read()

with open('data.json', 'w', encoding='utf-8') as f:
    f.write(data)
