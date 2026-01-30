"""
Example string utility functions for testing the pytest generator
This file contains various string manipulation functions
"""

import re
from typing import List, Dict, Optional

def reverse_string(text: str) -> str:
    """
    Reverse a string.
    
    Args:
        text: The string to reverse
        
    Returns:
        The reversed string
    """
    return text[::-1]

def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Check if a string is a palindrome.
    
    Args:
        text: The string to check
        ignore_case: Whether to ignore case differences
        ignore_spaces: Whether to ignore spaces and punctuation
        
    Returns:
        True if the string is a palindrome, False otherwise
    """
    processed_text = text
    
    if ignore_spaces:
        processed_text = re.sub(r'[^a-zA-Z0-9]', '', processed_text)
    
    if ignore_case:
        processed_text = processed_text.lower()
    
    return processed_text == processed_text[::-1]

def count_words(text: str) -> int:
    """
    Count the number of words in a string.
    
    Args:
        text: The text to count words in
        
    Returns:
        The number of words
    """
    if not text.strip():
        return 0
    return len(text.split())

def count_characters(text: str, include_spaces: bool = True) -> Dict[str, int]:
    """
    Count the frequency of each character in a string.
    
    Args:
        text: The text to analyze
        include_spaces: Whether to include spaces in the count
        
    Returns:
        Dictionary with character frequencies
    """
    char_count = {}
    
    for char in text:
        if not include_spaces and char == ' ':
            continue
        char_count[char] = char_count.get(char, 0) + 1
    
    return char_count

def capitalize_words(text: str, force_lower_rest: bool = True) -> str:
    """
    Capitalize the first letter of each word.
    
    Args:
        text: The text to capitalize
        force_lower_rest: Whether to force other letters to lowercase
        
    Returns:
        The text with capitalized words
    """
    if not text:
        return text
    
    words = text.split()
    capitalized_words = []
    
    for word in words:
        if word:
            if force_lower_rest:
                capitalized_word = word[0].upper() + word[1:].lower()
            else:
                capitalized_word = word[0].upper() + word[1:]
            capitalized_words.append(capitalized_word)
    
    return ' '.join(capitalized_words)

def remove_duplicates(text: str, preserve_order: bool = True) -> str:
    """
    Remove duplicate characters from a string.
    
    Args:
        text: The input string
        preserve_order: Whether to preserve the order of first occurrence
        
    Returns:
        String with duplicate characters removed
    """
    if preserve_order:
        seen = set()
        result = []
        for char in text:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)
    else:
        return ''.join(set(text))

def find_longest_word(text: str) -> Optional[str]:
    """
    Find the longest word in a string.
    
    Args:
        text: The text to search
        
    Returns:
        The longest word, or None if no words found
    """
    if not text.strip():
        return None
    
    words = text.split()
    longest_word = max(words, key=len)
    return longest_word

def extract_numbers(text: str) -> List[float]:
    """
    Extract all numbers from a string.
    
    Args:
        text: The text to extract numbers from
        
    Returns:
        List of numbers found in the text
    """
    # Pattern to match integers and floats (including negative)
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    
    numbers = []
    for match in matches:
        if '.' in match:
            numbers.append(float(match))
        else:
            numbers.append(float(int(match)))
    
    return numbers

def replace_multiple(text: str, replacements: Dict[str, str]) -> str:
    """
    Replace multiple substrings in a text based on a dictionary.
    
    Args:
        text: The original text
        replacements: Dictionary mapping old substrings to new ones
        
    Returns:
        Text with all replacements made
    """
    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result

def is_anagram(str1: str, str2: str, ignore_case: bool = True) -> bool:
    """
    Check if two strings are anagrams of each other.
    
    Args:
        str1: First string
        str2: Second string
        ignore_case: Whether to ignore case differences
        
    Returns:
        True if the strings are anagrams, False otherwise
    """
    # Remove spaces and convert to lowercase if specified
    processed_str1 = str1.replace(' ', '')
    processed_str2 = str2.replace(' ', '')
    
    if ignore_case:
        processed_str1 = processed_str1.lower()
        processed_str2 = processed_str2.lower()
    
    # Check if sorted characters are equal
    return sorted(processed_str1) == sorted(processed_str2)

def compress_string(text: str) -> str:
    """
    Compress a string by replacing consecutive identical characters with character + count.
    Example: "aaabbc" -> "a3b2c1"
    
    Args:
        text: The string to compress
        
    Returns:
        The compressed string
    """
    if not text:
        return text
    
    compressed = []
    current_char = text[0]
    count = 1
    
    for i in range(1, len(text)):
        if text[i] == current_char:
            count += 1
        else:
            compressed.append(current_char + str(count))
            current_char = text[i]
            count = 1
    
    # Add the last group
    compressed.append(current_char + str(count))
    
    # Return original if compression doesn't reduce length
    compressed_str = ''.join(compressed)
    return compressed_str if len(compressed_str) < len(text) else text

def validate_email(email: str) -> bool:
    """
    Validate if a string is a valid email address.
    
    Args:
        email: The email address to validate
        
    Returns:
        True if valid email format, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def extract_urls(text: str) -> List[str]:
    """
    Extract all URLs from a text.
    
    Args:
        text: The text to extract URLs from
        
    Returns:
        List of URLs found in the text
    """
    url_pattern = r'https?://[^\s<>"]{2,}'
    return re.findall(url_pattern, text)

def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length and add a suffix.
    
    Args:
        text: The string to truncate
        max_length: Maximum allowed length
        suffix: Suffix to add when truncating
        
    Returns:
        The truncated string
        
    Raises:
        ValueError: If max_length is less than the length of suffix
    """
    if max_length < len(suffix):
        raise ValueError("max_length must be at least as long as the suffix")
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix