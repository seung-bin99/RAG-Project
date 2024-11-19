# RAG-Project
## 반려동물 관련 pdf 문서 기반 RAG 챗봇
### RAG 기술 기반 pdf 내용을 검색, 질의응답(QA) 구현하는 챗봇

### Process
#### chat.py
- Ollama 라이브러리를 이용해서 등록한 EEVE모델 가져옴
- 한국어 문장 임베딩을 위한 jhgan/ko-sroberta-multitask 모델을 설정
- PDF 파일의 텍스트를 PyPDFLoader로 추출해 청크로 분할
- 추출한 내용을 langchain을 이용해서 임베딩하여 벡터화한 다음 FAISS 벡터 저장소에 저장
- 벡터 저장소 로드
- 유사도 높은 문서를 추출하기 위해 retriever 설정
- 챗봇의 응답을 정의하기 위한 프롬프트 설정
- 문서 내용을 포맷팅하여 문자열 변환 함수 정의
- Retriever, 프롬프트, 모델 및 출력 파서를 연결하여 최종 RAG 체인 생성

#### server.py
- FastAPI를 사용하여 웹 애플리케이션을 구성하고 CORS 설정을 통해 다양한 출처에서의 요청 허용
- 루트 URL 리다이렉션 설정
- 메시지 데이터 모델링
- LangServe와 연동 : 챗봇의 기능을 API 엔드포인트로 노출하고, 피드백 기능과 공개 트레이스 링크 활성화
- 서버 실행 : FastAPI 서버를 실행하여 클라이언트의 요청을 처리

#### 서버 배포
- Ngrok를 활용해 배포함으로써 외부 접근 허용

### Ollama 모델 등록
![ollama 모델 등록](https://github.com/user-attachments/assets/9a36450e-05e9-4243-8527-5efbdfc298eb)

### 서버 실행 코드
![서버 코드](https://github.com/user-attachments/assets/72d77932-712b-4b11-8ce9-e6b7d1fc33fa)


### RAG 기반 반려동물 챗봇 구현
![챗 체인](https://github.com/user-attachments/assets/17d52ef1-d9c1-4726-89df-e6c574def4a1)

### 모델 선정
- 모델 크기와 사용자 Local 환경 고려해 llama3-ko와 EEVE 모델 중 한국어 답변 우수했던 야놀자 EEVE LLM 모델 선정
- 한국어 임베딩 모델 성능 테스트 자료 참고해 BGE-M3 임베딩 모델 선정

### 챗봇 URL(채팅챗)
[**펫 케어 봇**](https://brave-martin-endlessly.ngrok-free.app/chat/playground/)

# 참고 자료
1. [**EEVE LLM 논문 리뷰**](https://fornewchallenge.tistory.com/entry/AI-%EB%85%BC%EB%AC%B8-%EC%98%AC%ED%95%B4%EC%9D%98-%ED%95%9C%EA%B5%AD%EC%96%B4-LLM%EC%97%90-%EC%84%A0%EC%A0%95%EB%90%9C-%EC%95%BC%EB%86%80%EC%9E%90-%EC%96%B8%EC%96%B4-%EB%AA%A8%EB%8D%B8-EEVE)
2. [**BGE-M3 임베딩 모델 논문 리뷰**](https://introduce-ai.tistory.com/entry/%EB%85%BC%EB%AC%B8-%EB%A6%AC%EB%B7%B0-BGE-M3-Embedding-Multi-Lingual-Multi-Functionality-Multi-Granularity-Text-Embeddings-Through-Self-Knowledge-Distillation)
2. [**한국어 임베딩 모델 성능 비교 테스트 결과**](https://steemit.com/kr-dev/@anpigon/20240604t162445271z)


### 사용 모델
> 1. [**야놀자 EEVE모델**](https://huggingface.co/heegyu/EEVE-Korean-Instruct-10.8B-v1.0-GGUF)
> 2. [**BAAI/bge-m3 임베딩 모델**](https://huggingface.co/BAAI/bge-m3)

### 버전
1. `LangChain version: 0.2.12`
2. `Python version: 3.12.4`
3. `LangServe version: 0.2.2`
