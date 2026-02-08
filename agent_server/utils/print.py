from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

def debug_print_messages(messages):
    print("\n================= AGENT TRACE =================")

    for msg in messages:
        if isinstance(msg, HumanMessage):
            print("\n👤 USER:")
            print(msg.content)

        elif isinstance(msg, AIMessage):
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    print("\n🤖 LLM → TOOL CALL:")
                    print(f"Tool: {tc['name']}")
                    print(f"Args: {tc['args']}")
            elif msg.content:
                print("\n🤖 LLM FINAL RESPONSE:")
                print(msg.content)

        elif isinstance(msg, ToolMessage):
            print("\n🔧 TOOL RESPONSE:")
            # trim long JSON
            content = msg.content
            if len(content) > 500:
                content = content[:500] + "..."
            print(content)

    print("\n===============================================\n")
