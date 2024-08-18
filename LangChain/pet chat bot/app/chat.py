#!/usr/bin/env python
# coding: utf-8

import os
import warnings
warnings.filterwarnings('ignore')


# **모델 불러오기(야놀자 EEVE 모델 사용 - 올해의 한국어 모델**

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks.manager import CallbackManager

# Ollama를 이용해 로컬에서 LLM 실행
model = ChatOllama(model='EEVE-Korean-10.8B')

callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])


# **임베딩 모델 설정(BAAI/bge-m3모델사용)**
# **- 한국어 문장 임베딩 모델 성능 비교 결과, 높은 성능 가짐**
# **HuggingFace Embedding**
from langchain.embeddings import HuggingFaceEmbeddings
# 문장을 임베딩으로 변환 후, 벡터 저장소에 저장
embedding_model = HuggingFaceEmbeddings(
    model_name='BAAI/bge-m3',
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings':False}
)


# **Text Splitter**
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
# 문서를 문장으로 분리
def load_split_doc(loaders):
    # 청크 크기 500, 각 청크 50자씩 겹치도록 청크 분할
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, 
                                                   chunk_overlap=50)
    docs = []

    for loader in loaders:
        pages = loader.load_and_split()
        splits = text_splitter.split_documents(pages)
        docs.extend(splits)

    return docs


loaders = [
    PyPDFLoader('./pet pdf/국내 반려동물 테마시설 시장 트렌드 및 동향.pdf'),
    PyPDFLoader('./pet pdf/반려동물보험시장의 현황과 과제.pdf'),
    PyPDFLoader('./pet pdf/동물보호법.pdf')
]
docs = load_split_doc(loaders)


# **벡터스토어 불러오기**
from langchain_community.vectorstores import FAISS

# load db
vectorstore = FAISS.load_local(
    './db/faiss', 
    embedding_model,
    allow_dangerous_deserialization=True  # 안전하다고 확신할 경우에만 True로 설정
)


# **Retriever 생성**
# 유사도 높은 3개 추출
retriever = vectorstore.as_retriever(search_kwargs={'k': 3})


# **LangChain**
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# Prompt 생성
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            친절한 챗봇으로서 상대방의 요청에 최대한 자세하고 친절하게 답하자. 너의 이름은 '펫 케어 봇' 이야. 모든 대답은 한국어(Korean)으로 대답해줘.:
            \n\n
            {context}",
            """
        ),
        ("human", "{question}"),
    ]
)

def format_docs(docs):
    return '\n\n'.join([d.page_content for d in docs])

# RAG Chain 연결
rag_chain = (
    {'context': retriever | format_docs, 'question': RunnablePassthrough()}
    | prompt # prompt : LLM 설정
    | model  # model : LLM 종류
    | StrOutputParser() # 채팅을 문자열로 변환하는 간단한 출력 구문 분석기
)

