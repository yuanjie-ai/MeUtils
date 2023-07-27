#
# from .chinese_text_splitter import *
#
#
#
# from langchain.text_splitter import RecursiveCharacterTextSplitter
#
#
from langchain.text_splitter import RecursiveCharacterTextSplitter
textsplitter = RecursiveCharacterTextSplitter(separators=["。"], chunk_overlap=10, chunk_size=100)
