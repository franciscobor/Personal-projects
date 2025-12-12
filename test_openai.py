#!/usr/bin/env python3
"""
Simple test script to verify OpenAI API key connection.
"""

import os
import sys
from openai import OpenAI

def test_openai_connection(api_key=None):
    """Test OpenAI API connection with the provided or environment API key."""
    
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("ERROR: No API key provided or OPENAI_API_KEY environment variable not set.")
        return False
    
    print(f"API Key (first 20 chars): {api_key[:20]}...")
    print("Creating OpenAI client...")
    
    try:
        client = OpenAI(api_key=api_key)
        
        print("\nTesting API connection...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Say 'Success' in one word only."}
            ],
            max_tokens=10,
            timeout=30  # Add explicit timeout
        )
        
        print("SUCCESS! OpenAI connection works.")
        print(f"Model response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check that your API key is valid at https://platform.openai.com/account/api-keys")
        print("2. Verify internet connection and network access to api.openai.com")
        print("3. Ensure your OpenAI account has available credits/quota")
        print("4. Check for API rate limiting or quota issues")
        return False


if __name__ == "__main__":
    # Read API key from secrets or environment
    import streamlit as st
    
    try:
        # Try to load from Streamlit secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        print("Loaded API key from Streamlit secrets")
    except:
        # Fall back to environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("Loaded API key from OPENAI_API_KEY environment variable")
    
    success = test_openai_connection(api_key)
    sys.exit(0 if success else 1)
