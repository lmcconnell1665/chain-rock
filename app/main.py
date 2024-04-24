from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
model_kwargs = {
    "max_tokens": 2048,
    "temperature": 0.1,
    "top_k": 250,
    "top_p": 1,
    "stop_sequences": ["\n\nHuman"],
}

app = FastAPI()

async def stream_chain(human_question: str):

    # imit the model
    llm = ChatBedrock(
        model_id=model_id,
        model_kwargs=model_kwargs,
        region_name='us-east-1',
        streaming=True
    )

    # setup the messages
    system_prompt = "You are a helpful assistant that loves {topic}."
    human_template = "{text}"

    # format the messages as <USER> and <ASST>
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_template)
    ])

    # add the needed input variables
    prompt.format_messages(topic="OSHA", text=human_question)

    # create the chain
    chain = prompt | llm | StrOutputParser()

    async for chunk in chain.astream({}):
        print(chunk, end="", flush=True)
        yield chunk


@app.post("/stream")
async def stream_response(question: str):
    """Streaming endpoint for the LangChain chain."""
    return StreamingResponse(stream_chain(question),  media_type='text/event-stream')
