import pytesseract
from PIL import Image
from google import genai
import json
import os

# --- Tesseract Config ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows path

# --- Initialize Gemini ---
api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyC_kAvA09PcJmp2a5kEM7E4I9WRpYPt7SA')  # Use env variable or fallback
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- OCR Step ---
image_path = r"C:\Users\nithe\Downloads\samplelab.png"
try:
    image = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(image)
except Exception as e:
    print(f"Error reading image: {e}")
    exit()

print("\n🧾 OCR Extracted Text:\n", ocr_text)

# --- User Input ---
region = input("\nEnter region: ")
condition = input("Enter medical condition: ")
weight = input("Enter weight (in kgs): ")
age = input("Enter age: ")

# --- Build Enhanced Prompt for API-friendly JSON ---
prompt = f"""
You are a medical AI assistant. Analyze the following lab report and provide a structured response.

Lab Report OCR Text:
{ocr_text}

Patient Information:
- Region: {region}
- Medical Condition: {condition}
- Weight: {weight} kg
- Age: {age}

IMPORTANT: Respond ONLY with valid JSON in this exact format (no markdown, no extra text):

{{
  "patient_info": {{
    "region": "{region}",
    "condition": "{condition}",
    "weight_kg": "{weight}",
    "age": "{age}"
  }},
  "lab_analysis": {{
    "extracted_values": [
      {{"parameter": "glucose", "value": 0, "unit": "mg/dL", "status": "normal/high/low"}},
      {{"parameter": "cholesterol", "value": 0, "unit": "mg/dL", "status": "normal/high/low"}}
    ],
    "summary": "Brief health summary based on lab values",
    "concerns": ["List any concerning values"]
  }},
  "diet_plan": {{
    "monday": {{
      "breakfast": "Specific meal description",
      "lunch": "Specific meal description", 
      "dinner": "Specific meal description",
      "snacks": "Healthy snack options"
    }},
    "tuesday": {{
      "breakfast": "Specific meal description",
      "lunch": "Specific meal description", 
      "dinner": "Specific meal description",
      "snacks": "Healthy snack options"
    }},
    "wednesday": {{
      "breakfast": "Specific meal description",
      "lunch": "Specific meal description", 
      "dinner": "Specific meal description",
      "snacks": "Healthy snack options"
    }},
    "thursday": {{
      "breakfast": "Specific meal description",
      "lunch": "Specific meal description", 
      "dinner": "Specific meal description",
      "snacks": "Healthy snack options"
    }},
    "friday": {{
      "breakfast": "Specific meal description",
      "lunch": "Specific meal description", 
      "dinner": "Specific meal description",
      "snacks": "Healthy snack options"
    }},
    "saturday": {{
      "breakfast": "Specific meal description",
      "lunch": "Specific meal description", 
      "dinner": "Specific meal description",
      "snacks": "Healthy snack options"
    }},
    "sunday": {{
      "breakfast": "Specific meal description",
      "lunch": "Specific meal description", 
      "dinner": "Specific meal description",
      "snacks": "Healthy snack options"
    }}
  }},
  "recommendations": {{
    "foods_to_include": ["List beneficial foods based on lab results"],
    "foods_to_avoid": ["List foods to limit/avoid"],
    "key_nutrients": ["Important nutrients to focus on"],
    "hydration": "Daily water intake recommendation",
    "exercise": "Basic exercise recommendations"
  }}
}}

Instructions:
- Extract ALL lab values from the OCR text
- Consider {region} food preferences
- Tailor meals to address any abnormal lab values
- Provide specific, practical meal suggestions
- Return ONLY the JSON structure above, no markdown formatting
"""

# --- Send to Gemini ---
try:
    response = model.generate_content(prompt)
    result_text = response.text.strip()
    
    # Clean up response - remove markdown formatting if present
    if "```json" in result_text:
        result_text = result_text.split("```json")[1].split("```")[0].strip()
    elif "```" in result_text:
        result_text = result_text.split("```")[1].split("```")[0].strip()
    
    # Validate and parse JSON
    try:
        parsed_result = json.loads(result_text)
        
        # Pretty print the validated JSON
        formatted_json = json.dumps(parsed_result, indent=2, ensure_ascii=False)
        
        print("\n🧠 AI Analysis Results (API-Ready JSON):")
        print("=" * 60)
        print(formatted_json)
        
        # Save to file for API use
        with open("diet_plan_api_response.json", "w", encoding="utf-8") as f:
            json.dump(parsed_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 API-ready JSON saved to: diet_plan_api_response.json")
        print("✅ JSON validation: PASSED - Ready for API integration!")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON validation failed: {e}")
        print("Raw response (for debugging):")
        print(result_text)
        
        # Save raw response for debugging
        with open("debug_raw_response.txt", "w", encoding="utf-8") as f:
            f.write(result_text)
        print("🔧 Raw response saved to debug_raw_response.txt")

except Exception as e:
    print(f"❌ Error during Gemini API call: {e}")