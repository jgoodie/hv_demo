# Unstructured Data Summarization and Intelligent Search
------------------------------------------------------------------------------

<img width="875" alt="Screenshot 2024-08-30 at 12 40 18 PM" src="https://github.com/user-attachments/assets/20cd2f1b-7917-4a2a-8f96-4e58d583b0ca">



This demo shows how organizations can utilize intelligent data retrieval methods such as retrieval augmented generation (RAG) to improve customer satisfaction and reduce support costs while enabling employes to be more efficient when search for specific information. Specifially this demo shows how orgizations can implement multi-modal search to enable them to gain insights not just from textual data, but from audio, video, image, and other unstructured data formats.

This demo utilizes the following technology from:

* OpenAI to create text embeddings, audio/video transcription, and large language model (LLM) support
* Deeplake to store the vector embeddings and enable similary or semantic search
* LangChain to allow developers to create applications powered by large language models.

<img width="828" alt="Screenshot 2024-08-30 at 12 46 44 PM" src="https://github.com/user-attachments/assets/e5f1538b-a417-4a8e-8b0f-92753ef77025">

------------------------------------------------------------------------------
To run this demo, you will first need to create accounts and obtain API keys for both products:
* Activeloop: https://www.activeloop.ai/
* OpenAI: https://platform.openai.com/docs/overview

For each file add your OpenAI key and Activeloop token.
* build_demo.py
* manage_vector_data.py
* rag_query.py
* vector_query.py

os.environ["OPENAI_API_KEY"] = "<your OpenAI key>"
os.environ['ACTIVELOOP_TOKEN'] = "<your activeloop toke>"



