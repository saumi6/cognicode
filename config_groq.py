import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the test generator with Groq support"""
    
    # Gemini API settings (existing)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # Groq API settings (new)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-20b')
    
    # LLM Provider selection
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq').lower()  # 'groq' or 'gemini'
    
    # Test generation settings
    MAX_TEST_CASES = int(os.getenv('MAX_TEST_CASES', '10'))
    INCLUDE_EDGE_CASES = os.getenv('INCLUDE_EDGE_CASES', 'true').lower() == 'true'
    INCLUDE_ERROR_CASES = os.getenv('INCLUDE_ERROR_CASES', 'true').lower() == 'true'
    
    # Output settings
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'generated_tests')
    VERBOSE = os.getenv('VERBOSE', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present based on selected provider"""
        if cls.LLM_PROVIDER == 'groq':
            if not cls.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required when using Groq. Please set it in your .env file.")
            if len(cls.GROQ_API_KEY) < 20:
                raise ValueError("GROQ_API_KEY appears to be invalid (too short).")
        elif cls.LLM_PROVIDER == 'gemini':
            if not cls.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is required when using Gemini. Please set it in your .env file.")
            if len(cls.GEMINI_API_KEY) < 20:
                raise ValueError("GEMINI_API_KEY appears to be invalid (too short).")
        else:
            raise ValueError(f"Unknown LLM_PROVIDER: {cls.LLM_PROVIDER}. Use 'groq' or 'gemini'.")
        
        return True
    
    @classmethod
    def get_env_template(cls):
        """Get template for .env file with both providers"""
        return """# LLM Provider Selection
LLM_PROVIDER=groq

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# Gemini API Configuration (alternative)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Test Generation Settings
MAX_TEST_CASES=10
INCLUDE_EDGE_CASES=true
INCLUDE_ERROR_CASES=true

# Output Settings
OUTPUT_DIR=generated_tests
VERBOSE=false
"""