import time
import csv
from unstract.llmwhisperer import LLMWhispererClientV2

client = LLMWhispererClientV2(base_url="https://llmwhisperer-api.us-central.unstract.com/api/v2", api_key='S5-YhFKbkKSqJDypokqKyd3MkPfptBwHvUos4ZnJqE0')

result = client.whisper(file_path="test6.pdf")

print(result)

while True:
    status = client.whisper_status(whisper_hash=result["whisper_hash"])
    if status["status"] == "processed":
        resultx = client.whisper_retrieve(
            whisper_hash=result["whisper_hash"]
        )
        break
    time.sleep(5)

extracted_text = resultx['extraction']['result_text']

print(extracted_text)

import time
from unstract.llmwhisperer import LLMWhispererClientV2

# Initialize client
client = LLMWhispererClientV2(
    base_url="https://llmwhisperer-api.us-central.unstract.com/api/v2", 
    api_key='S5-YhFKbkKSqJDypokqKyd3MkPfptBwHvUos4ZnJqE0'
)

# Call whisper API
result = client.whisper(file_path="test6.pdf")
#print(result)

# Check processing status
while True:
    status = client.whisper_status(whisper_hash=result["whisper_hash"])
    if status["status"] == "processed":
        resultx = client.whisper_retrieve(whisper_hash=result["whisper_hash"])
        break
    time.sleep(5)

# Extract text
extracted_text = resultx['extraction']['result_text']
#print(extracted_text)

# Save to a text file
output_file = "data.txt"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(extracted_text)

#print(f"Extracted text saved to {output_file}")



# Define input and output file names
txt_file = "extracted_text.txt"
csv_file = "extracted_text.csv"

# Read the text file
with open(txt_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Write to a CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Writing each line as a separate row
    for line in lines:
        writer.writerow([line.strip()])  # Each line is stored in a single column

print(f"Text file converted to CSV and saved as {csv_file}")
