import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 100000, chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks,embedding = embeddings)
    vector_store.save_local("faiss_index")
    


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context,
    make sure to provide all the details, if the answer is not in provided context just say, 
    "Answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer: 
    """
    
    model = ChatGoogleGenerativeAI(model = "gemini-pro", temperature=0.5)
    
    prompt = PromptTemplate(template= prompt_template, input_variables=["context","question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt = prompt)
    return chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization = True)
    docs = new_db.similarity_search(user_question)
    
    chain = get_conversational_chain()
    
    response = chain({"input_documents": docs, "question": user_question})
    
    st.write("Reply:", response["output_text"])
    
def main():
    st.set_page_config("Chat bot")
    st.header("chat Bot By ajeet")
    
    
    user_info = {}
    user_question = st.text_input("Ask a question related to the pdf")
    contact = ["contact", "call"]
    for contacts in contact:
        if contacts in user_question.lower():
            st.subheader("Contact Form")
            user_info["name"] = st.text_input("Name")
            user_info["phone_number"] = st.text_input("Phone")
            user_info["email"] = st.text_input("Email")
            user_wants_call = st.button("Request Call")
            if user_wants_call:
                if all(value for value in user_info.values()):
                    st.write(f"Calling {user_info['name']} at {user_info['phone_number']}")

    
    if user_question:
        user_input(user_question)
        
    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your pdf files and click on submit button.", accept_multiple_files=True)
        if st.button("Submit And Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")
                
            
if __name__ == "__main__":
    main()
         