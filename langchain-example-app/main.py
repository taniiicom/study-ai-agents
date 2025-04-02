import os
from dotenv import load_dotenv
from weather_agent import WeatherAgent

def main():
    # Load environment variables
    load_dotenv()
    
    # Get OpenAI API key
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable is not set")
        return

    # Create the weather agent
    agent = WeatherAgent(openai_api_key)
    
    print("Weather Assistant (type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        # Check for quit command
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
            
        if not user_input:
            continue
            
        try:
            # Get response from agent
            response = agent.run(user_input)
            print("\nAssistant:", response)
            
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()