from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers.langchain import wait_for_all_tracers
from langchain.callbacks.tracers import LangChainTracer
from langsmith import Client

client = Client()

tracer = LangChainTracer(project_name="new-project-langsmith-101")
import uuid
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a truthful AI assistant,"),
        ("user", "{input}")
    ])

llm_model = ChatOpenAI(temperature=0)

output_parser = StrOutputParser()

chain = (prompt | llm_model | output_parser).with_config(
    {
        "tags": ["openai-chat", "simple-chain"],
        "metadata": {"user_id": str(uuid.uuid4())},
        "run_name": "chat-openai-chain"
    })

try:
    response = chain.invoke({"input":"What is the best way to work with Large Language Models?"},
                 config= {"callbacks": [tracer]},
            #  {"tags": ["openai-chat", "simple-chain"],
            #   "metadata": {"user_id": str(uuid.uuid4())}}
              )
    
    client.create_feedback(
        run_id=response["__run"].run_id,
        key="user-rating",
        score=0.8,
        comment="The response was helpful."
    )
finally:
    wait_for_all_tracers()
