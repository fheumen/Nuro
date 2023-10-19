import os
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import pinecone

from consts import INDEX_NAME

# pinecone.init(api_key="f0358c1e-0404-4344-8e87-1120495ea92e", environment="gcp-starter")
pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)


def ingest_docs() -> None:
    loader = PyPDFDirectoryLoader(
        "C:\\Users\\heume\\OneDrive\\MachineLearning\\Gen AI\\Nuro\\Data\\HTA Reports\\UK",
    )
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    documents = text_splitter.split_documents(documents)
    print(f"Splitted into {len(documents)} chunks")

    #### Changing the Source path
    # for doc in documents:
    #     old_path = doc.metadata["source"]
    #     new_url = old_path.replace("langchain-docs", "https:/")
    #     doc.metadata.update({"source":new_url})

    print(f"Going to insert {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("****** Added to Pinecone vectorstore vector")

    # qa = RetrievalQA.from_chain_type(
    #     llm=OpenAI(),
    #     chain_type="stuff",
    #     retriever=docsearch.as_retriever(),
    #     return_source_documents=True,
    # )
    #
    # # query = "What is a vector DB? Give me a 15 word answer for begginer"
    # # query = "What is a Pembrolizumab? Give me a 15 word answer for begginer"
    # query = "What is the treatment duration of Pembrolizumab? Give me a 15 word answer for begginer"
    # result = qa({"query": query})
    #
    # print(result)

    # print(document)
if __name__ == "__main__":
    ingest_docs()