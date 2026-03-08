from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import httpx
from ..models.database import get_db, Paper, Workspace, User
from ..routers.auth import get_current_user

router = APIRouter(prefix="/papers", tags=["papers"])


# ── Schemas ───────────────────────────────────────────────────────────────────
class PaperImport(BaseModel):
    title: str
    authors: str
    abstract: str
    url: str
    published_date: str
    workspace_id: int


class WorkspaceCreate(BaseModel):
    name: str


# ── Workspace routes ──────────────────────────────────────────────────────────
@router.post("/workspaces", status_code=201)
def create_workspace(data: WorkspaceCreate, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    ws = Workspace(name=data.name, owner_id=current_user.id)
    db.add(ws)
    db.commit()
    db.refresh(ws)
    return {"id": ws.id, "name": ws.name}


@router.get("/workspaces")
def list_workspaces(db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    workspaces = db.query(Workspace).filter(Workspace.owner_id == current_user.id).all()
    return [{"id": w.id, "name": w.name} for w in workspaces]


@router.get("/workspaces/{workspace_id}/papers")
def list_papers(workspace_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    papers = db.query(Paper).filter(Paper.workspace_id == workspace_id).all()
    return [
        {"id": p.id, "title": p.title, "authors": p.authors,
         "abstract": p.abstract, "url": p.url, "published_date": p.published_date}
        for p in papers
    ]


# ── Search route (uses arXiv public API) ─────────────────────────────────────
@router.get("/search")
async def search_papers(query: str, max_results: int = 10,
                        current_user: User = Depends(get_current_user)):
    url = "https://export.arxiv.org/api/query"
    params = {"search_query": f"all:{query}", "start": 0, "max_results": max_results}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)

    # Simple XML parse without lxml
    import xml.etree.ElementTree as ET
    root = ET.fromstring(resp.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    results = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", "", ns).strip().replace("\n", " ")
        abstract = entry.findtext("atom:summary", "", ns).strip().replace("\n", " ")
        published = entry.findtext("atom:published", "", ns)[:10]
        link_el = entry.find("atom:id", ns)
        link = link_el.text if link_el is not None else ""
        authors = ", ".join(
            a.findtext("atom:name", "", ns)
            for a in entry.findall("atom:author", ns)
        )
        results.append({
            "title": title, "authors": authors, "abstract": abstract,
            "url": link, "published_date": published
        })
    return results


# ── Import paper into workspace ───────────────────────────────────────────────
@router.post("/import", status_code=201)
def import_paper(data: PaperImport, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    ws = db.query(Workspace).filter(
        Workspace.id == data.workspace_id,
        Workspace.owner_id == current_user.id
    ).first()
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    paper = Paper(
        title=data.title, authors=data.authors, abstract=data.abstract,
        url=data.url, published_date=data.published_date, workspace_id=data.workspace_id
    )
    db.add(paper)
    db.commit()
    return {"message": "Paper imported successfully"}


# ── Delete paper ──────────────────────────────────────────────────────────────
@router.delete("/{paper_id}")
def delete_paper(paper_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    db.delete(paper)
    db.commit()
    return {"message": "Paper deleted"}
