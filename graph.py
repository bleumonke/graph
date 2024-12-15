from model import mistral
from langgraph.graph import StateGraph, START, END
from dataclasses import dataclass
from typing import Optional
import uuid

llm = mistral("ministral-3b-2410")

@dataclass
class GraphSchema:
    question: str
    answer: Optional[str] = None
    function: Optional[str] = None
    id: str = str(uuid.uuid4())

@dataclass
class GraphRequest:
    question: str
    url: Optional[str] = None

@dataclass
class GraphResponse:
    answer: str
    id: str
    function: Optional[str] = None

graph_builder = StateGraph(state_schema=GraphSchema,input=GraphRequest,output=GraphResponse)

def processRequest(request: GraphRequest):
    print(f"Processing request: {request}")
    return request
    
def detectRequestType(request: GraphRequest):
    print(f"Detecting request type: {request}")
    if request.url:
        return "chatFile"
    return "chat"

def chat(request: GraphSchema):
    answer = llm.invoke(request.question).content
    return GraphSchema(question=request.question, answer=answer, function="chat")

def chat_with_file(request: GraphSchema):
    answer = llm.invoke(request.question).content
    return GraphSchema(question=request.question, answer=answer, function="chat_with_file")

def prepareResponse(schema: GraphSchema):
    response = GraphResponse(answer=schema.answer, id=schema.id, function=schema.function)
    return response

graph_builder.add_node("processRequest", processRequest)
graph_builder.add_node("chat", chat)
graph_builder.add_node("chatFile", chat_with_file)
graph_builder.add_node("prepareResponse", prepareResponse)

graph_builder.add_edge(START, "processRequest")
graph_builder.add_conditional_edges("processRequest", detectRequestType)
graph_builder.add_edge("chat", "prepareResponse")
graph_builder.add_edge("chatFile", "prepareResponse")
graph_builder.add_edge("prepareResponse", END)

graph = graph_builder.compile()

response = graph.invoke({"question": "Hello, how are you?"})
print(response)

