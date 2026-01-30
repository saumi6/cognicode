import os
import google.generativeai as genai
from typing import Optional
from config import Config

class GeminiClient:
    """Client for interacting with Google's Gemini LLM"""
    
    def __init__(self):
        """Initialize the Gemini client with API key from config"""
        self.api_key = Config.GEMINI_API_KEY
        self.model_name = Config.GEMINI_MODEL
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate_content(self, prompt: str) -> Optional[str]:
        """
        Generate content using Gemini LLM
        
        Args:
            prompt: The input prompt for content generation
            
        Returns:
            Generated content as string, or None if failed
        """
        try:
            # Generate content
            response = self.model.generate_content(prompt)
            
            # Extract text from response
            if response and response.text:
                return response.text.strip()
            else:
                return None
                
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def generate_test_cases(self, function_signature: str, function_docstring: str = None) -> Optional[str]:
        """
        Generate test cases for a specific function
        
        Args:
            function_signature: The function signature to test
            function_docstring: Optional docstring for context
            
        Returns:
            Generated test cases as string, or None if failed
        """
        prompt = f"""Generate comprehensive pytest test cases for the following Python function:

Function Signature: {function_signature}
{f'Docstring: {function_docstring}' if function_docstring else ''}

Generate test cases that include:
1. Normal/happy path scenarios
2. Edge cases (boundary conditions, empty inputs, etc.)
3. Error cases (invalid inputs that should raise exceptions)
4. Use pytest.mark.parametrize where appropriate

Return only the test functions, no additional explanation.
"""
        
        return self.generate_content(prompt)
    
    def is_configured(self) -> bool:
        """Check if the client is properly configured"""
        return bool(self.api_key and self.model_name)
    
    def test_connection(self) -> bool:
        """Test the connection to Gemini API"""
        try:
            test_prompt = "Say 'Hello' in Python code."
            response = self.generate_content(test_prompt)
            return response is not None
        except Exception:
            return False