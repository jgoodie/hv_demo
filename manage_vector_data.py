#!/usr/bin/env python

import os
import argparse

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DeepLake
from langchain_community.document_loaders import PyPDFLoader

os.environ["OPENAI_API_KEY"] = "<your OpenAI key>"
os.environ['ACTIVELOOP_TOKEN'] = "<your activeloop token>"
os.environ['USER_AGENT'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--add", help="add vector embeddings")
    group.add_argument("-d", "--delete", help="delete vector embeddings")
    args = parser.parse_args()

    aloid="jpgai" 
    aldsn="hv_youtube_summarizer"
    activeloop_org_id = aloid 
    activeloop_dataset_name = aldsn
    vector_store_path = f"hub://{activeloop_org_id}/{activeloop_dataset_name}"
    embedding_function = OpenAIEmbeddings(model = 'text-embedding-ada-002')
    db = DeepLake(dataset_path = vector_store_path, embedding = embedding_function, read_only = False)

    if args.add:
        document_loader = PyPDFLoader(file_path=args.add)
        document = document_loader.load()
        db.add_documents(document)
    
    if args.delete: 
        db.delete(filter={'metadata': {'source': args.delete}})



