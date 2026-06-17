import os
import mammoth
from langchain.schema import Document
from langchain.document_loaders import PyMuPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from logger_files.logger import error_logger, warning_logger

def load_documents(resume_folder):
    documents = []
    for filename in os.listdir(resume_folder):
        path = os.path.join(resume_folder, filename)
        loader = None

        try:
            if filename.endswith(".pdf"):
                loader = PyMuPDFLoader(path)

            elif filename.endswith(".txt"):
                loader = TextLoader(path)

            elif filename.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(path)

            elif filename.endswith(".doc"):
                try:
                    import win32com.client
                    word = win32com.client.Dispatch("Word.Application")
                    word.Visible = False
                    doc = word.Documents.Open(path)
                    text = doc.Content.Text
                    doc.Close()
                    word.Quit()
                    documents.append(Document(page_content=text))
                except Exception as e:
                    error_logger.error(f"Failed to load {filename}: {e}")
                continue

            elif filename.endswith(".tmp"):
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    documents.append(Document(page_content=text))
                continue

            else:
                warning_logger.warning(f"Skipped unsupported file: {filename}")
                continue

            docs = loader.load()
            documents.extend(docs)

        except Exception as e:
            error_logger.error(f"Failed to load {filename}: {e}")

    return documents