"""
Debug Groq connection and API
"""
import os
from groq import Groq

def test_groq_connection():
    print("🔍 Testing Groq Connection\n")
    
    # Check API key
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found (length: {len(api_key)})")
    
    try:
        # Initialize client
        client = Groq(api_key=api_key)
        print("✅ Groq client initialized")
        
        # Test simple request
        print("🧪 Testing simple request...")
        
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": "Say hello in Python code"
                }
            ],
            temperature=0.1,
            max_tokens=100,
        )
        
        if completion.choices and len(completion.choices) > 0:
            response = completion.choices[0].message.content
            print(f"✅ Response received: {response[:100]}...")
            return True
        else:
            print("❌ No response from Groq")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_groq_connection()