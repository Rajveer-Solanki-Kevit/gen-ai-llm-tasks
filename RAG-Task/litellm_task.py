import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
from pdf2image import convert_from_bytes
import io
import pytesseract
import litellm


load_dotenv()


os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY", "")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY", "")
os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")
litellm.success_callback = ["langfuse"]
litellm.failure_callback = ["langfuse"]


def get_text_from_pdf(multiple_pdfs):
    text = ""
    for pdf in multiple_pdfs:
        pdf_bytes = pdf.read()
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))

        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()

            if page_text and page_text.strip():
                text += page_text + "\n"
            else:
                try:
                    images = convert_from_bytes(pdf_bytes, first_page=page_num + 1, last_page=page_num + 1)
                    for image in images:
                        img_text = pytesseract.image_to_string(image)
                        if img_text.strip():
                            text += img_text + "\n"
                except Exception as e:
                    print(f"OCR failed on page {page_num + 1}: {e}")

    if not text.strip():
        print("No text extracted from PDF.")
    return text


def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
    return splitter.split_text(text)


def get_vector_store(text_chunks):
    if not text_chunks:
        raise ValueError("No text chunks found.")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    persist_directory = "chroma_db"

    vector_store = Chroma.from_texts(
        texts=text_chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vector_store.persist()
    return vector_store


def get_user_input(user_que):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    persist_directory = "chroma_db"

    db = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    docs = db.similarity_search(user_que, k=4)
    context = "\n\n".join([d.page_content for d in docs])

    response = litellm.completion(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that answers questions based on PDF content."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_que}"}
        ]
    )

    answer = response["choices"][0]["message"]["content"]
    return answer



st.set_page_config(page_title="PDF Q&A Bot", layout="wide")
st.title("PDF Chatbot")

with st.sidebar:
    st.header("Upload PDF Files")
    multiple_pdfs = st.file_uploader("Upload PDFs:", type=["pdf"], accept_multiple_files=True)

    if st.button("Process PDFs") and multiple_pdfs:
        with st.spinner("Processing PDFs..."):
            raw_text = get_text_from_pdf(multiple_pdfs)
            chunks = get_text_chunks(raw_text)
            get_vector_store(chunks)
            st.success("PDF processed successfully! You can now ask questions.")

st.subheader("Ask a Question")
user_que = st.text_input("Type your question based on uploaded PDFs:")

if user_que:
    with st.spinner("Thinking..."):
        resp = get_user_input(user_que)
        st.markdown("### Answer:")
        st.write(resp)
