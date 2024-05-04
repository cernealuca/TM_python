# implementare de traducere date cu cel mai ieftin API
# cel de la microsoft

import csv
import requests
import os
import json

# Configure your Microsoft Translator key and endpoint
subscription_key = 'your-subscription-key'
endpoint = 'your-translator-endpoint'
location = 'your-resource-location'  # e.g., global, westus, etc.

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json'
}

path = '/translate?api-version=3.0'
params = '&from=fr&to=en'
constructed_url = endpoint + path + params

def translate_text(text):
    body = [{'text': text}]
    response = requests.post(constructed_url, headers=headers, json=body)
    result = response.json()
    return result[0]['translations'][0]['text'] if result else text

def translate_csv(input_file_path, output_file_path):
    with open(input_file_path, mode='r', encoding='utf-8') as infile, \
         open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)  # Assuming the first row is headers
        writer.writerow(headers)  # Write headers to the output file

        for row in reader:
            translated_row = [translate_text(cell) if cell else cell for cell in row]
            writer.writerow(translated_row)

# Example Usage
# translate_csv('path_to_your_input.csv', 'path_to_your_output.csv')
