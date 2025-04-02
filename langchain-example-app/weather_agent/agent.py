from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from .tools import WeatherTool

class WeatherAgent:
    def __init__(self, openai_api_key: str):
        # Initialize the tool
        self.weather_tool = WeatherTool()
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            api_key=openai_api_key
        )

        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful weather assistant that provides accurate weather information.

Your primary function is to help users get weather details for specific locations. When responding:
- Always ask for a location if none is provided
- If the location name isn't in English, please translate it
- If giving a location with multiple parts (e.g. "New York, NY"), use the most relevant part (e.g. "New York")
- Include relevant details like humidity, wind conditions, and precipitation
- Keep responses concise but informative

Use the get_weather tool to fetch current weather data."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])

        # Create the agent
        self.agent = create_openai_functions_agent(
            llm=self.llm,
            prompt=prompt,
            tools=[self.weather_tool]
        )

        # Create the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=[self.weather_tool],
            verbose=True
        )

    def run(self, input_text: str) -> str:
        """
        Run the weather agent with the given input text.
        
        Args:
            input_text (str): The user's input text/question
            
        Returns:
            str: The agent's response
        """
        return self.agent_executor.invoke(
            {
                "input": input_text,
                "chat_history": []
            }
        )["output"]