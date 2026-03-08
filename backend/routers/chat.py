from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from ..models.database import get_db, ChatMessage, Workspace, Paper, User
from ..routers.auth import get_current_user
from ..utils.research_assistant import (
    answer_research_question,
    summarize_paper,
    compare_papers,
    extract_key_findings,
)

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    workspace_id: int
    message: str


class CompareRequest(BaseModel):
    workspace_id: int
    paper_ids: List[int]


# ── 1. Main chat endpoint ─────────────────────────────────────────────────────
@router.post("/")
def chat(req: ChatRequest, db: Session = Depends(get_db),
         current_user: User = Depends(get_current_user)):
    ws = db.query(Workspace).filter(
        Workspace.id == req.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")

    papers = db.query(Paper).filter(Paper.workspace_id == req.workspace_id).all()
    history_rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.workspace_id == req.workspace_id)
        .order_by(ChatMessage.timestamp).all()
    )
    history = [{"role": r.role, "content": r.content} for r in history_rows]
    answer = answer_research_question(req.message, papers, history)

    db.add(ChatMessage(role="user", content=req.message, workspace_id=req.workspace_id))
    db.add(ChatMessage(role="assistant", content=answer, workspace_id=req.workspace_id))
    db.commit()
    return {"response": answer}


# ── 2. Summarize a single paper ───────────────────────────────────────────────
@router.get("/summarize/{paper_id}")
def summarize(paper_id: int, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    summary = summarize_paper(paper)
    return {"paper_id": paper_id, "title": paper.title, "summary": summary}


# ── 3. Compare multiple papers ────────────────────────────────────────────────
@router.post("/compare")
def compare(req: CompareRequest, db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    papers = db.query(Paper).filter(Paper.id.in_(req.paper_ids)).all()
    if len(papers) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 paper IDs")
    result = compare_papers(papers)
    return {"comparison": result}


# ── 4. Extract key findings from a paper ─────────────────────────────────────
@router.get("/findings/{paper_id}")
def findings(paper_id: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    extracted = extract_key_findings(paper)
    return {"paper_id": paper_id, "title": paper.title, "findings": extracted}


# ── 5. Get chat history ───────────────────────────────────────────────────────
@router.get("/{workspace_id}/history")
def get_history(workspace_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    msgs = (
        db.query(ChatMessage)
        .filter(ChatMessage.workspace_id == workspace_id)
        .order_by(ChatMessage.timestamp).all()
    )
    return [{"role": m.role, "content": m.content, "timestamp": str(m.timestamp)} for m in msgs]


# ── 6. Clear chat history ─────────────────────────────────────────────────────
@router.delete("/{workspace_id}/history")
def clear_history(workspace_id: int, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db.query(ChatMessage).filter(ChatMessage.workspace_id == workspace_id).delete()
    db.commit()
    return {"message": "Chat history cleared"}
