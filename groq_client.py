"""
Groq LLM Client for test generation
Alternative to Gemini client with potentially better code generation
"""
import os
from typing import Optional
from groq import Groq
from config import Config

class GroqClient:
    """Client for interacting with Groq's LLM models"""
    
    def __init__(self):
        """Initialize the Groq client with API key from config"""
        self.api_key = os.getenv('GROQ_API_KEY') or Config.GROQ_API_KEY
        self.model_name = os.getenv('GROQ_MODEL', 'llama-3.1-70b-versatile')
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required. Please set it in your .env file.")
        
        # Initialize the Groq client
        self.client = Groq(api_key=self.api_key)
    
    def generate_content(self, prompt: str) -> Optional[str]:
        """
        Generate content using Groq LLM
        
        Args:
            prompt: The input prompt for content generation
            
        Returns:
            Generated content as string, or None if failed
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert Python developer who writes complete, functional, and well-tested code. Always generate complete implementations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for more consistent code generation
                max_completion_tokens=4096,
                top_p=0.1,
                stream=False,  # Get complete response at once
                stop=None
            )
            
            if completion.choices and len(completion.choices) > 0:
                return completion.choices[0].message.content.strip()
            else:
                return None
                
        except Exception as e:
            print(f"Error generating content with Groq: {e}")
            return None
    
    def generate_content_stream(self, prompt: str) -> Optional[str]:
        """
        Generate content using Groq LLM with streaming (for large responses)
        
        Args:
            prompt: The input prompt for content generation
            
        Returns:
            Generated content as string, or None if failed
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert Python developer. Generate complete, functional test code with proper assertions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_completion_tokens=4096,
                top_p=0.1,
                stream=True,
                stop=None
            )
            
            # Collect streamed response
            content = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    content += chunk.choices[0].delta.content
            
            return content.strip() if content else None
                
        except Exception as e:
            print(f"Error generating streamed content with Groq: {e}")
            return None
    
    def generate_test_cases(self, function_signature: str, function_docstring: str = None) -> Optional[str]:
        """
        Generate test cases for a specific function using Groq
        
        Args:
            function_signature: The function signature to test
            function_docstring: Optional docstring for context
            
        Returns:
            Generated test cases as string, or None if failed
        """
        prompt = f"""Generate complete pytest test functions for this Python function.

FUNCTION TO TEST:
{function_signature}
{f'DOCSTRING: {function_docstring}' if function_docstring else ''}

REQUIREMENTS:
1. Generate 3 complete test functions with full implementations
2. Include proper assertions and pytest.raises blocks
3. Use realistic test data
4. Each function must be complete and executable

Generate these functions:
- test_FUNCNAME_normal_cases() with @pytest.mark.parametrize
- test_FUNCNAME_edge_cases() with boundary conditions
- test_FUNCNAME_error_cases() with exception handling

Return only the complete Python test functions:"""
        
        return self.generate_content(prompt)
    
    def is_configured(self) -> bool:
        """Check if the client is properly configured"""
        return bool(self.api_key and self.model_name)
    
    def test_connection(self) -> bool:
        """Test the connection to Groq API"""
        try:
            test_prompt = "Write a simple Python function that returns 'Hello World'"
            response = self.generate_content(test_prompt)
            return response is not None and len(response) > 10
        except Exception:
            return False
    
    def get_available_models(self) -> list:
        """Get list of available Groq models"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []