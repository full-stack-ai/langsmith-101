from langchain_community.document_loaders import PyPDFLoader

pdf_file_path = "data/pdf/Learning_Python.pdf"
loader = PyPDFLoader(pdf_file_path)

pages = loader.load_and_split()
len(pages)