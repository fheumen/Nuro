import os
from typing import Dict, List, Any

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

# from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Pinecone
import pinecone

from consts import INDEX_NAME

print(INDEX_NAME)
# pinecone.init(api_key="f0358c1e-0404-4344-8e87-1120495ea92e", environment="gcp-starter")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []) -> Any:
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    docsearch = Pinecone.from_existing_index(
        embedding=embeddings, index_name=INDEX_NAME
    )
    chat = ChatOpenAI(verbose=True, temperature=0)
    # qa = RetrievalQA.from_chain_type(
    #     llm=chat,
    #     chain_type="stuff",
    #     retriever=docsearch.as_retriever(),
    #     return_source_documents=True,
    # )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=docsearch.as_retriever(), return_source_documents=True
    )

    #return qa({"query": query, "chat_history": chat_history})
    return qa({"question": query, "chat_history": chat_history})


if __name__ == "__main__":
    query = "What is the treatment duration of Pembrolizumab? Give me a 15 word answer for begginer"
    print(run_llm(query))
