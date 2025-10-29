import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
import os
from dotenv import load_dotenv
from pdf2image import convert_from_bytes
import io
import pytesseract


load_dotenv()


def get_text_from_pdf(files):
    full_text = ""

    for file in files:
        try:
            pdf_data = file.read()
            reader = PdfReader(io.BytesIO(pdf_data))

            for i, page in enumerate(reader.pages):
                content = page.extract_text()

                if content and content.strip():
                    full_text += content + "\n"
                else:
                    try:
                        image_pages = convert_from_bytes(pdf_data, start=i + 1, end=i + 1)
                        for img in image_pages:
                            full_text += pytesseract.image_to_string(img) + "\n"
                    except Exception as err:
                        print(f"OCR failed on page {i + 1}: {err}")

        except Exception as e:
            print(f"Error reading PDF: {e}")

    return full_text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    return splitter.split_text(text)


def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store


def get_conversation_chain(vectorstore):
    prompt_template = """
    You are a helpful assistant that summarizes and answers questions based on the provided context.

    If the question asks for a summary, use the context to generate a concise and accurate summary.
    If information is missing, make your best attempt based on context — do not just say "I don't know".

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o-mini",
        temperature=0
    )

    retriever = vectorstore.as_retriever()

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=False
    )

    return chain


def get_user_input(user_que):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_que, k=4)
    chain = get_conversation_chain(new_db)
    resp = chain.run(input_documents=docs, query=user_que)
    return resp


st.set_page_config(page_title="PDF Q&A bot", layout="wide")
st.title("PDF Chatbot")

with st.sidebar:
    st.header("Upload PDF Files")
    multiple_pdfs = st.file_uploader("Upload PDFs:", type=["pdf"], accept_multiple_files=True)
    if st.button("Process PDFs") and multiple_pdfs:
        with st.spinner("Processing PDFs..."):
            raw_text = get_text_from_pdf(multiple_pdfs)
            chunks = get_text_chunks(raw_text)
            get_vector_store(chunks)
            st.success("PDF processed. ask questions.")

st.subheader("Ask a Question")
user_que = st.text_input("Type your question based on uploaded PDFs:")

if user_que:
    with st.spinner("Thinking..."):
        resp = get_user_input(user_que)
        st.markdown(" Answer:")
        st.write(resp)
