# Unstructured Data Summarization and Intelligent Search
------------------------------------------------------------------------------

<img width="875" alt="Screenshot 2024-08-30 at 12 40 18 PM" src="https://github.com/user-attachments/assets/20cd2f1b-7917-4a2a-8f96-4e58d583b0ca">



This demo shows how organizations can utilize intelligent data retrieval methods such as retrieval augmented generation (RAG) to improve customer satisfaction and reduce support costs while enabling employees to be more efficient when searching for specific information. Specifially this demo shows how orgizations can implement multi-modal search to enable them to gain insights not just from textual data, but from audio, video, image, and other unstructured data formats.

This demo utilizes the following technology from:

* OpenAI to create text embeddings, audio/video transcription, and large language model (LLM) support
* Deeplake to store the vector embeddings and enable similary or semantic search
* LangChain to allow developers to create applications powered by large language models.

<img width="828" alt="Screenshot 2024-08-30 at 12 46 44 PM" src="https://github.com/user-attachments/assets/e5f1538b-a417-4a8e-8b0f-92753ef77025">

------------------------------------------------------------------------------
Before running this demo, you will first need to create accounts and obtain API keys for both OpenAI's API and Activeloop:
* Activeloop: https://www.activeloop.ai/
* OpenAI: https://platform.openai.com/docs/overview

For each file add your OpenAI key and Activeloop token.
* `build_demo.py`
* `manage_vector_data.py`
* `rag_query.py`
* `vector_query.py`
  
```
os.environ["OPENAI_API_KEY"] = "<your OpenAI key>"
os.environ['ACTIVELOOP_TOKEN'] = "<your activeloop toke>"
```

After adding your OpenAI key and Activeloop token, make sure to change the activeloop ID and dataset name you want to create/use.
Check the following files:
* `build_demo.py`
* `manage_vector_data.py`
* `rag_query.py`
* `vector_query.py`

```
aloid="<your activeloop id>",
aldsn="<a dataset name of your choosing>"
```

**Python Dependencies:**

* `yt_dlp`
* `whisper`
* `textwrap`
* `langchain`
* `langchain_openai`
* `langchain_community`

**To build the demo:**
1. Make sure to update the list of Youtube videos that will be transcribed. Look at the `build_demo.py` file and update the list called `urls`.
The current list of videos point to Hitachi Vantara marketing materials around smart cities. If you want to use a different set of videos, simply edit this list to point to something else.

```
 urls=["https://youtu.be/CA5IHvV9kWs?si=pESCy2GMn9bRJYGy", 
        "https://youtu.be/3mNcwr-OqKY?si=7AnO7l81JpFDfd-0",
        "https://youtu.be/2I6YoBrgdwg?si=E1XedQrhBRegBkRw", 
        "https://youtu.be/UjYR4TwBnUk?si=ABCOBr9euwOjIdfP", 
        "https://youtu.be/ttM5COuvHuQ?si=DebzSof4p14LnuEm", 
        "https://youtu.be/NfhiX0DXMcE?si=--nWycFowfrZEUAY"]
```

2. To demonstrate multi-modal search you can have the `build_demo.py` ingest a set of PDF files. To include PDF data, simply download some PDFs into the directory where `build_demo.py` will be run and update the `pdfs` list in `build_demo.py` to point to local files:
```
pdfs = ["./smart-spaces-video-intelligence-solution-profile.pdf", 
        "./Smart-City-Operational-Intelligence-for-Smarter-Communities-Solution-Brief-3.pdf", 
        "./industry_roundtable_report_issue_0.pdf"]
```
3. Finally, simply run `build_demo.py` to build the demo. This process will take a while as the script downloads the YouTube content, transcribes the videos and processes any PDF content. The script will automatically create the document embeddings and upload them to Deeplake.

**To run the demo:**

To run the demo and query the data, simply run the `rag_query.py` script. 
At the QUERY prompt, type your questions about the data. The query will be sent to deeplake and will return the top 4 semantically similar results. OpenAI will then take those results and return a coherent response.

**To update the vector embeddings to simulate new content being added:**

To simulate changing data (i.e. a company releases a new product and associated product manuals), you can simply add new vector embeddings with the `manage_vector_data.py` script. With this script you can ingest new PDF data or delete recently added PDF data. 

NOTE: This script cannot manage the data from the initial demo build script as it does not include the metadata necessary for the `manage_vector_data.py` - the `build_demo.py` script needs to be improved to include metadata.

* To add new PDF vector embeddings, simply run: `manage_vector_data.py -a ./My-New-Product-Manual.pdf`
* To delete a PDF vector embedding, simply run: `manage_vector_data.py -d ./My-New-Product-Manual.pdf`

Once the new data has been added to the vector DB, you can re-run the `rag_query.py` script with relevant questions about the new content to demonstrate how easy it is for RAG to handle new data without the need for finetuning a model.

  **To demonstrate how the LLM takes the document chucks from the vector DB and stitches them into a coherant response**

You might get the question about why LLMs are even necessary if the Vector DB is simply returning all the necessary information. To demostrate why an LLM is needed, you can show how the vector DB only returns snippets of the relevent document by runing the `vector_query.py` script. To drive the point home, re-run the `rag_query.py` script with the same query to see the difference in response.

