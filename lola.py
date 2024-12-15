from model import mistral
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langgraph.graph import MessagesState, StateGraph, START, END

llm = mistral("ministral-3b-2410")

@tool
def get_loan_infromation(loan_number: int) -> dict:
    """Get loan information from a loan number."""
    return {
        "123456":{
            "monthly_payment": 100,
            "principal": 10000,
            "rate": 5,
            "term": 60,
        },
        "1010101":{
            "monthly_payment": 200,
            "principal": 2000,
            "rate": 5,
            "term": 360,
        },
    }


@tool
def unpaid_balance(principal: int, rate: float, term: int, month: int) -> float:
    """Calculate the unpaid balance on a loan."""
    rate = rate / 100 / 12
    return principal * ((1 + rate) ** term - (1 + rate) ** month) / ((1 + rate) ** term - 1)

@tool
def monthly_payment(principal: int, rate: float, term: int) -> float:
    """Calculate the monthly payment on a loan."""
    rate = rate / 100 / 12
    return principal * rate / (1 - (1 + rate) ** -term)

tools = [get_loan_infromation]
llm_with_tools = llm.bind_tools(tools)


def reasoner(state:MessagesState):
    print(f"Reasoner state: {state}")
    sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing some calculations on set of inputs. if no relevant tools are available, ask the user for more information.")
    response = {"messages":[llm_with_tools.invoke([sys_msg] + state["messages"])]}
    print(f"Reasoner response: {response}")
    return response

builder = StateGraph(MessagesState)
builder.add_node("reasoner", reasoner)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START, "reasoner")
builder.add_conditional_edges("reasoner", tools_condition)
builder.add_edge("tools", "reasoner")
builder.add_edge("reasoner", END)

graph = builder.compile()

messages = graph.invoke({"messages":[HumanMessage(content="what is the monthly payment for loan 1010101?")]})
for message in messages["messages"]:
    print(f"Type: {message.type}, Content: {message.content}")