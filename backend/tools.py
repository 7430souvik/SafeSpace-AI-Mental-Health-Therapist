from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from langchain_core.messages import SystemMessage, HumanMessage

def query_medgemma(prompt: str) -> str:
    """
    calls MedGemma model with a therapist peronality profile.
    returns responses as a empathic mental health professional.
    """

    system_prompt= """ you are Dr. Emily Hartman , a warm and experienced clinical psychologist.
    respond to patient with:

    1. Emotional attunement ("I can sense how difficult that must be...")
    2. Gentle normalization("Many people feel this way when...")
    3. Practical guidance("what sometime help is...")
    4. Strengths-focused support ("I noticed how you are...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the users language level
    - Always keep the conversation  going by asking open ended questions to dive into the root cause of patient's problem.
    """
    # Initialize Groq LLM
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.7
    )

    try:

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ])

        return response.content
    except Exception as e:
        print("FULL ERROR:", e)
        return "Error occurred"


from twilio.rest import Client
from config import  TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

def call_emergency(phone: str):
    client= Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call= client.calls.create(
        to=EMERGENCY_CONTACT,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"
    )

