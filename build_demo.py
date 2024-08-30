#!/usr/bin/env python

import os
import yt_dlp
import whisper
import textwrap

from langchain_openai import OpenAI, ChatOpenAI

from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.mapreduce import MapReduceChain
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DeepLake

os.environ["OPENAI_API_KEY"] = "<your OpenAI key>"
os.environ['ACTIVELOOP_TOKEN'] = "<your activeloop toke>"
os.environ['USER_AGENT'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"


class VideoSummarizer:
    def __init__(self, 
                 urls=[], 
                 pdfs=[], 
                 job_id='hv', 
                 whisper_model="base", 
                 embed_model="text-embedding-ada-002",
                 aloid="jpgai", 
                 aldsn="hv_youtube_summarizer", overwrite=False):
        self.urls = urls
        self.pdfs = pdfs
        self.job_id = job_id
        self.video_info = []
        self.whisper_model = whisper.load_model(whisper_model)
        self.transcriptions = []
        self.docs = None
        self.embeddings = OpenAIEmbeddings(model=embed_model)
        self.llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
        self.activeloop_org_id = aloid 
        self.activeloop_dataset_name = aldsn
        self.dataset_path = f"hub://{self.activeloop_org_id}/{self.activeloop_dataset_name}"
        self.db = DeepLake(dataset_path=self.dataset_path, embedding=self.embeddings, overwrite=overwrite)
        self.distance_metric = 'cos'
        self.k = 4
        self.prompt_template = """Use the following pieces of transcripts from a video to answer the 
                                  question in bullet points and summarized. If you don't know the answer, 
                                  just say that you don't know, don't try to make up an answer.

                                  {context}

                                  Question: {question}
                                  Summarized answer in bullter points:"""

    def download(self):
        for i, url in enumerate(self.urls):
            temp_file = f'./{self.job_id}_{i}.mp4'
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
                'outtmpl': temp_file,
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(url, download=True)
                title = result.get('title', "")
                author = result.get('uploader', "")
            self.video_info.append((temp_file, title, author))
        return self.video_info

    def transcribe(self):
        for video in self.video_info:
            result = self.whisper_model.transcribe(video[0])
            self.transcriptions.append(result['text'])

    def process_pdfs(self):
        if self.pdfs:
            for p in self.pdfs:
                document_loader = PyPDFLoader(file_path=p)
                document = document_loader.load()
                for d in document:
                    self.docs.append(Document(page_content=d.page_content.replace('\x00', '')))
            
    def process_text(self):
        if len(self.transcriptions) > 0:
            text = "\n".join(self.transcriptions)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"]
            )
            texts = text_splitter.split_text(text)
            self.docs = [Document(page_content=t) for t in texts]
        else:
           print("Error: No transcriptions. Transcribe a video first.") 

    def to_vectordb(self):
        if self.docs:    
            self.db.add_documents(self.docs)
        else:
            print("Error: No docs defined")

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
    
    def summarize(self):
        if self.docs: 
            chain = load_summarize_chain(self.llm, chain_type="map_reduce")
            output_summary = chain.invoke(self.docs)
            return output_summary
        else:
            print("Error: No docs defined")


if __name__ == "__main__":
    urls=["https://youtu.be/CA5IHvV9kWs?si=pESCy2GMn9bRJYGy", 
          "https://youtu.be/3mNcwr-OqKY?si=7AnO7l81JpFDfd-0",
          "https://youtu.be/2I6YoBrgdwg?si=E1XedQrhBRegBkRw", 
          "https://youtu.be/UjYR4TwBnUk?si=ABCOBr9euwOjIdfP", 
          "https://youtu.be/ttM5COuvHuQ?si=DebzSof4p14LnuEm", 
          "https://youtu.be/NfhiX0DXMcE?si=--nWycFowfrZEUAY"]  
    
    pdfs = ["./smart-spaces-video-intelligence-solution-profile.pdf", 
            "./Smart-City-Operational-Intelligence-for-Smarter-Communities-Solution-Brief-3.pdf", 
            "./industry_roundtable_report_issue_0.pdf"]

    vs = VideoSummarizer(urls=urls, pdfs=pdfs, job_id="hv", overwrite=True)
    vs.download()
    vs.transcribe()
    vs.process_text()
    vs.process_pdfs()
    vs.to_vectordb()


