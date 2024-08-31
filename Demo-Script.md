### Title Slide/Slide 1

Hi this is <YOUR NAME> and I want to talk to you about how organizations can gain deeper insights from their unstructured data by using intelligent data retrieval techniques.

### Slide 2

If you look around most organizations, you’ll probably discover that finding necessary information to help complete a task can take longer than it should. 

Products like Microsoft Sharepoint are great for storing or sharing information but when faced with finding the necessary and relevant information is you’re 
left sorting through multiple sources of information.

From a customer perspective, we have a similar problem – finding support information from product manuals and support forms results in the same sort problems 
of having to deal with various documents and forum discussions.

Given these vast and varied sources of information, how does an organization synthesis that data to provide intelligent insights and provide customer value?

### Slide 3

For many organization, the solution is to simply punt to built in search functionality of whatever product is hosting their documents. 
Or course this doesn’t solve the problem because not users are left having to utilize multiple different search features and products that simply don’t talk 
to each other and rely on simple keywork searches. 
To make matters worse, simple search leaves users with a list of documents and users must extract and combine the relevant information themselves.

### Slide 4

One way organizations may try to solve this problem is to finetune a foundational model on their mountain product and support manuals and implement some 
kind of chat system.

The problem with this is approach is that finetuning foundational models can be impractical due to the time and recourses needed to retrain a model.

Additionally, finetuning an LLM could end up being costly simply due to the changing nature of organizational data. 

For example, customer support forums are actively changing sources of data, and organizations constantly release new products and product updates which generates 
new sources of data. 
Given the rapidly changing nature of organizational data, finetuning models becomes hugely problematic. Of course, this makes no mention of the newly finetuned 
LLM potential hallucinating an incorrect response to a product support case.

So what is the solution? How can customers solve this problem of needing to provide accurate and relevant information to customers and employees?

### Slide 5

To solve this problem, organizations can take advantage of the power of vector embedding and vector databases. 

Vector embeddings are a way to convert words and sentences and other data into numbers that capture their meaning and relationships.

By utilizing a vector database, organizations can store these vector representations of their data, then issue queries to identify the most semantically similar 
pieces of information.

Finally, by combining Large Language Models with the results of these semantic queries, the LLMs can craft a coherent and concise response to the use user query.

By combining not just text but also audio, video and image based data, this approach enables more complex data retrieval that is not limited to keywords and 
synonyms and can deliver a true multi-modal search experience.

### Slide 6

* _Talk to the work flow on how the user sends a query and that the query is sent to the Vector DB where a similarity search is run against the vector embedding_
* _Talk about how the Vector DB returns the top K number of similar text segments and how the LLM creates a coherent response from the text snippets_

### Slide 7

RAG can pull relevant information from various documents or databases and synthesize this information into a single, concise answer.  
This is particularly useful when the required information is scattered across multiple sources. 
Utilizing RAG pipelines with audio/video transcription as well as OCR technologies can help organizations gain deeper insights that traditional methods may miss.

Contextual Understanding: RAG doesn't just retrieve documents; it understands the context of the query and generates a response that directly addresses the user's needs. 
It can combine information from multiple sources to create a coherent, context-aware answer. This can greatly increase customer satisfaction and help drive down support costs. 

### Slide 8

Real-Time and Up-to-Date Information: As organizational data grows and changes, RAG can retrieve and generate responses based on the most recent information available. 
This is crucial for support teams when new products releases and they need to find the latest product information.

Improved User Experience: RAG provides a more intuitive and seamless user experience by allowing users to interact with the system in a conversational manner. 
It reduces the effort needed to extract useful information, making the retrieval process more efficient and user-friendly.

### Slide 9

Separator Slide


### Slide 10

The technologies used in this solution include:
* OpenAI for the audio/video transcriptions, document embeddings and LLM
* Deeplake is a cloud based vector datastore designed to explicitly to store any data (pdfs, vectors, audio, videos, etc.) for AI use cases.
* LangChain is a framework for developing applications powered by large language models (LLMs). LangChain helps to simplify every stage of the LLM application lifecycle

### Slide 11

Now you may be thinking, “My organization has a mandate to not use cloud services due to costs or regulatory requirements”

While not shown in this demo, on-prem customers that are faced with this dilemma can easily modify this solution to utilize off the shelf open-source tools that can run on-premises.
That technology stack might look like:
* Text embedding models downloaded from Huggingface
* Huggingface’s Speech2TextProcessor for audio/video transcriptions 
* Postgres pgvector extension for vector similarity search
* Lanchain to help glue it all together.

### Slide 12
In this demo, I’ll show how we can take multi-modal information such as video and PDF data to create an intelligent RAG pipeline that will allow employees and customers to query multiple data sources to quickly gain relevant and accurate information.

In this workflow, OpenAI handles the video transcription using the Whisper model and langchain handles the text extraction from the PDFs.
We then take the text from our videos and PDF files and transform it into vector embeddings which are then loaded into the Deeplake vector data store.

Once that’s completed, users are able to query the service. The User query comes in and sent to the Vector DB to run a similarity search which will then return the top K results. In this demo, we return the top 4 similar results from our vector database. 

The LLM, in this case OpenAI’s GPT-4o, takes the document snippets returned from the vector DB and stitches a coherent and accurate response for the user.

### Slide 13
Quickly, this is what an on-premises workflow might look like. 
Notice that the actual workflow has not changed; we have simply swapped out cloud-based services in favor of open source models that can be run locally on-prem.

### Slide 14
For this demo, we pull 6 different videos and 3 PDFs relating to Hitachi Vantara’s smart city initiatives.

### Slide 15
_Run the demo_

1. Run the build_demo.py script
    1. This script is the ingestion pipepline.
        - It will download the youtube content
        - It will then begin transcribing the videos
        - After the videos are complete, it will extract the text from the PDF files
        - Finally, it will create the document embeddings and place them into the Vector DB
2. Run the vectory_query.py script to show how we can query the vector DB and show that we still need the LLM to craft a coherent response.
3. Run the rag_query.py script to show how the LLM provides a relevant, coherent and concise response to the use.
4. Run the manage_vector_data.py script and add a new PDF to the vector DB
    1. This will take a new PDF, extract the text, create new document embeddings and add them to the vector DB 
6. Run the rag_query.py script again and ask some questions relevant to the new document to demonstrate how our RAG pipeline can handle the introduction of new data.

### Slide 16
_this is a place holder to show the output of the demo if you can't run the demo_

### Slide 17

Separator Slide

### Slide 18

Final comments, 

LLMs by themselves are really limiting for use cases where organization need targeted and relevant responses to employee and customer questions.

Finetuning an LLM becomes problematic due to the rate of data change within an organization.

Finetuned LLMs run the risk of potentially hallucinating a response that may not be accurate.

RAG solves these problems by feeding the LLM the correct and relevant information while drastically lowering the possibility of hallucinations.

The vector DB is the linchpin in this solution. The Vector DB with it’s embeddings help provide the relevant information to a user's query while 
the LLM stitches together a coherent response. 

The vector database with help from the LLM are the future to building next generation multi-modal search applications that will help lower 
support costs and increase customer satisfaction in solving their support issues.

_Make sure to open up the conversation to discussion_

### Slide 19

Thank you Slide

### Slides 20-26

_Additional slides just in case the extra technical folks want to dig into the code or discuss implementation techniques_










