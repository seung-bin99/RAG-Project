from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from langserve.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from chat import rag_chain

app = FastAPI()


# FastAPI 애플리케이션에서 Cross-Origin Resource Sharing(CORS) 설정을 관리하는 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], # 모든 출처의 요청 허용
    allow_credentials = True, # 교차 출처 요청에 대해 쿠키가 지원되어야 함
    allow_methods = ["*"], # 교차 출처 요청에 허용되어야 하는 HTTP 메소드 목록
    allow_headers = ["*"], # 교차 출처 요청에 대해 지원되어야 하는 HTTP 요청 헤더 목록
    expose_headers = ["*"], # 브라우저에서 액세스할 수 있어야 하는 응답 헤더
)
    
# 루트 URL("/")에 GET 요청이 왔을 경우 "/chat/playground"로 리다이렉트
@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/chat/playground")


# 메세지 데이터를 효과적으로 모델링하고 유효성 검사와 데이터 관리 기능 제공
class Input(BaseModel):
    """Input for the chat endpoint."""  # Input 클래스 용도
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description = "the messages representing the current converation." # Field 설명 추가
    )


# 채팅 체인(chat_chain)에 접근할 수 있도록 "/chat"라는 경로(URL)로 라우팅
# 피드백 엔드포인트, 공개 트레이스 링크 엔드포인트를 활성화하며, 이 엔드포인트의 유형을 "chat"으로 설정
add_routes(app, 
           rag_chain.with_types(input_type=Input),
           path="/chat",
           enable_feedback_endpoint=True,
           enable_public_trace_link_endpoint=True,
           playground_type="chat"
           )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
