# test_llm.py - Run this to test your new LLM setup
from src.utils.llm_setup import llm

def test_llm():
    test_prompt = '''
    You are a reflective journaling assistant.
    User just wrote: "I had a really great day at work today. My project was successful and my team was supportive.".
    Sentiment detected: positive.
    No past entries found.
    
    Based on this, give an empathetic reflection.
    Suggest patterns or insight if relevant.
    '''
    
    print("Testing LLM...")
    print(f"LLM type: {type(llm)}")
    print(f"LLM object: {llm}")
    
    try:
        response = llm.invoke(test_prompt)
        print("\n" + "="*50)
        print("LLM RESPONSE:")
        print("="*50)
        print(response)
        print("="*50)
        print("\n✅ LLM is working correctly!")
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")

if __name__ == "__main__":
    test_llm()