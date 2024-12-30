from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv
load_dotenv()

company=input("enter company name :")

web_search_agent = Agent(
    name = "Web Search Agent",
    role="Search the web for the information",
    model=Groq(id ="llama3-groq-70b-8192-tool-use-preview"),
    tools = [DuckDuckGo()],
    instructions = ["Always include sources"],
    show_tools_calls=True,
    markdown=True,
)

# financial agent
finance_agent = Agent(
    name="Finance AI Agent",
    model = Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[
        YFinanceTools(stock_price=True,analyst_recommendations=True, stock_fundamentals=True,
                      company_news=True),

    ],
    instructions=["Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,

)

multi_ai_agent=Agent(
    model = Groq(id="llama3-groq-70b-8192-tool-use-preview"), #--> if your not mention here model then by dafault it will consider openai model
    team=[web_search_agent,finance_agent],
    instructions=["Always include sources","use tables to display the data"],
    show_tool_calls=True,
    markdown=True,

)
multi_ai_agent.print_response(f"summarize analyst recommendation and share the latest news for {company}",stream=True)
