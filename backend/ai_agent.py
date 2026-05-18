from langchain_core.tools import tool
from tools import query_medgemma, call_emergency

@tool
def ask_mental_health_specialist(query: str) ->str:
    """
    Generate a therapeutic response using medgemma model.
    Use this for all general user queries , mental health questions, emotional concerns.
    or to offer empathetic, evedence based guidance in a conversational tone.

    """
    return query_medgemma(query)

@tool
def emergency_call_tool(phone: str) ->str:
    """
    Place an emergency  call  to the safety helpline's phone number via Twilio.
    Use this only if the user express suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    return call_emergency(phone)

@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}, {location}:\n"
        "- Dr. Ayesha Kapoor - +1 (555) 123-4567\n"
        "- Dr. James Patel - +1 (555) 987-6543\n"
        "- MindCare Counseling Center - +1 (555) 222-3333"
    )

# create an AI agent and link to backend
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from config import GROQ_API_KEY

tools=[ask_mental_health_specialist, emergency_call_tool,find_nearby_therapists_by_location]
llm = ChatGroq(
    
    model_name="openai/gpt-oss-20b",
    temperature=0.2,
    api_key= GROQ_API_KEY
)
graph = create_agent(llm, tools=tools)

SYSTEM_PROMPT ="""
You are an empathetic AI therapist assistant supporting mental health conversations with warmth and clinical accuracy.
You have access to two tools:

1.`ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with theraputic guidance.
2.`emergency_call_tool`:Use this immediately if the user expresses suicidal thoughts, self-harm intensions,or is in crisis.

Always prioritize user safety, validation and helpful action.
Respond kindly, clearly and supportively.
"""


def parse_response(stream):

    tool_called_name = None
    final_response = None

    for s in stream:

        print("STREAM:", s)

        # MODEL RESPONSE
        if "model" in s:

            messages = s["model"]["messages"]

            if messages:

                final_response = messages[-1].content

        # TOOL RESPONSE
        if "tools" in s:

            messages = s["tools"]["messages"]

            if messages:

                tool_called_name = messages[-1].name

    return tool_called_name, final_response

# if __name__== "__main__":
#     while True:
#         user_input= input("User:")
#         print(f"Received user input: {user_input[:200]}...")
#         inputs = {"messages":[("system", SYSTEM_PROMPT),("user", user_input)]}
#         stream = graph.stream(inputs, stream_mode="updates")
#         for s in stream:
#             print(s)