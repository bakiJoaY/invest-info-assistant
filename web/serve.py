from langserve import add_routes
from fastapi import FastAPI

from vector_store.qdrant import init_vector_database
from vector_store.qdrant import save_vector
from data.data import init_hot_stock_concept

from langchain_community.chat_models.tongyi import ChatTongyi
from langgraph.graph import MessagesState, StateGraph
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from tool.tools import retrieveHottestConcept, retrieveConceptInfo

from langgraph.graph import END
from langgraph.prebuilt import ToolNode, tools_condition



init_vector_database()
docList = init_hot_stock_concept()
save_vector(docList)


# build chain
llm = ChatTongyi(
    model="qwen-max",
    api_key="your_api_key",
    temperature=0.1,
    top_p=0.9,
    top_k=50,
)
# 第一步，先接受用户的提问，用户问的问题可能与股票无关，例如打招呼，此时不查询向量库。
def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieveHottestConcept, retrieveConceptInfo])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}

# 第二步，通过tool的api查询所需要的数据。
tools = ToolNode([retrieveHottestConcept, retrieveConceptInfo])

# 第三步，如果使用了tool接口，则处理响应
def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]
    print('tool_messages:\n')
    print(tool_messages)
    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "你是一个证券市场的消息人士，由于市场消息每天都在变化，所以请使用以下最新信息来回答用户的提问。"
        "\n\n"
        f"{docs_content}"
    )
    print('state detail:\n')
    print(state)
    print(state['messages'])
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = llm.invoke(prompt)
    return {"messages": [response]}

graphNode = StateGraph(MessagesState)
# 构造workflow
graphNode.add_node(query_or_respond)
graphNode.add_node(tools)
graphNode.add_node(generate)

graphNode.set_entry_point("query_or_respond")
graphNode.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)
graphNode.add_edge("tools", "generate")
graphNode.add_edge("generate", END)


graph = graphNode.compile()



app = FastAPI(title="LangChain Demo")


chain = graph
add_routes(app, chain, path="/runApp")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)

