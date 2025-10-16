import sys
from google import genai

client = genai.Client(api_key="AIzaSyC_kG-SR8gaM8HN0YaRgbytlm0NLdz-oPw")

ocr_text = sys.stdin.read()

prompt = (
    "Extract the medicine details from the following prescription text. "
    "Return the result as a JSON array of objects (make sure the output is a single line string). "
    "Each object should contain: 'medicine' → the name of the medicine, 'frequency' → when to take the medicine in the form 'morning-afternoon-night' (e.g., '1-0-1'), 'days' → estimated number of days the medicine will last based on quantity and frequency, or 'PRN' if it's to be taken as needed. "
    f"Here is the prescription text:\n{ocr_text}"
)

response = client.models.generate_content(
    model="gemini-2.5-flash", contents=prompt
)

print(response.text)
