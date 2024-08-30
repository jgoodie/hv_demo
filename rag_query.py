#!/usr/bin/env python

import os
import textwrap

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain_community.vectorstores import DeepLake

os.environ["OPENAI_API_KEY"] = "<your OpenAI key>"
os.environ['ACTIVELOOP_TOKEN'] = "<your activeloop token>"
os.environ['USER_AGENT'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"

class RAGQuery:
    def __init__(self,  
                 embed_model="text-embedding-ada-002",
                 aloid="jpgai", 
                 aldsn="hv_youtube_summarizer", 
                 k = 4,
                 overwrite=False):
        self.embeddings = OpenAIEmbeddings(model=embed_model)
        self.llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
        self.activeloop_org_id = aloid 
        self.activeloop_dataset_name = aldsn
        self.dataset_path = f"hub://{self.activeloop_org_id}/{self.activeloop_dataset_name}"
        self.db = DeepLake(dataset_path=self.dataset_path, embedding=self.embeddings, overwrite=overwrite)
        self.distance_metric = 'cos'
        self.k = k
        self.prompt_template = """Use the following pieces of transcripts from a video to answer the 
                                  question in bullet points and summarized. If you don't know the answer, 
                                  just say that you don't know, don't try to make up an answer.

                                  {context}

                                  Question: {question}
                                  Summarized answer in bullter points:"""


    def query(self, q="Summarize the mentions of smart cities according to Hitachi Vantara"):
        retriever = self.db.as_retriever()
        retriever.search_kwargs['distance_metric'] = self.distance_metric
        retriever.search_kwargs['k'] = self.k
        PROMPT = PromptTemplate(template=self.prompt_template, input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": PROMPT}
        qa = RetrievalQA.from_chain_type(llm=self.llm,
                                 chain_type="stuff",
                                 retriever=retriever,
                                 chain_type_kwargs=chain_type_kwargs)
        return qa.invoke(q)
    

if __name__ == "__main__":
    rq = RAGQuery(k=10, overwrite=False)
    print()
    while True:
        q = input('QUERY:')
        print()
        if q == "quit":
            break
        result = rq.query(q=q)
        print(result['result'])
        print()
    




