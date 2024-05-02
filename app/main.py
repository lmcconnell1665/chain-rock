from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_aws import ChatBedrock
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

    # format the messages as <USER> and <ASST>
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that loves {topic} and can answer any questions related to this topic."),
        ("human", "{text}"),
    ])

    # create the chain
    chain = prompt_template | llm | StrOutputParser()

    async for chunk in chain.astream({"topic": "OSHA", "text": human_question}):
        print(chunk, end="", flush=True)
        yield chunk

@app.post("/stream")
async def stream_response(question: str):
    """Streaming endpoint for the LangChain chain."""
    return StreamingResponse(stream_chain(question),  media_type='text/event-stream')

@app.get("/")
def hello():
    return {"message": "Hello from Chain"}