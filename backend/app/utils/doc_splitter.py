from langchain.text_splitter import RecursiveCharacterTextSplitter



splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=25)


def file_split(file_path:str):
    if file_path.endswith(".pdf"):
        from langchain_community.document_loaders import PyMuPDFLoader
        pdf_loader = PyMuPDFLoader(file_path=file_path)
        pages = pdf_loader.load()
        chunks = splitter.split_documents(pages)
    return chunks


        

