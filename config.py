import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings for the test generator"""
    
    # Gemini API configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-pro')
    
    # Test generation settings
    MAX_TEST_CASES = int(os.getenv('MAX_TEST_CASES', '10'))
    INCLUDE_EDGE_CASES = os.getenv('INCLUDE_EDGE_CASES', 'true').lower() == 'true'
    INCLUDE_ERROR_CASES = os.getenv('INCLUDE_ERROR_CASES', 'true').lower() == 'true'
    
    # Output settings
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'generated_tests')
    VERBOSE = os.getenv('VERBOSE', 'false').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        return True