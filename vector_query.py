#!/usr/bin/env python

import os
import textwrap

from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DeepLake

os.environ["OPENAI_API_KEY"] = "<your OpenAI key>"
os.environ['ACTIVELOOP_TOKEN'] = "<your activeloop token>"
os.environ['USER_AGENT'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"


aloid="jpgai" 
aldsn="hv_youtube_summarizer"

activeloop_org_id = aloid 
activeloop_dataset_name = aldsn
vector_store_path = f"hub://{activeloop_org_id}/{activeloop_dataset_name}"
embedding_function = OpenAIEmbeddings(model = 'text-embedding-ada-002')

# Re-load the vector store
db = DeepLake(dataset_path = vector_store_path, embedding = embedding_function, read_only = True)

if __name__ == "__main__":
    print()
    while True:
        q = input('QUERY:')
        print()
        if q == "quit":
            break
        query_docs = db.similarity_search(query = q, k=2)
        for d in query_docs:
            print(textwrap.fill(d.page_content, width=100))
            print()
        print()
