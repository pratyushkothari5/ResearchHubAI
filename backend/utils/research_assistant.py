# code for research assistant logic

"""
research_assistant.py
Activity 5.1 — AI Agent Implementation and Context Management

Functions:
  1. answer_research_question  — core RAG-based Q&A
  2. summarize_paper           — auto-summarize a single paper
  3. compare_papers            — structured comparison across multiple papers
  4. extract_key_findings      — pull methodology, results, conclusion
  5. build_smart_context       — context memory manager (trims old history smartly)
"""

from .vector_db import find_relevant_papers
from .groq_client import chat_with_groq


# ── 1. Core Q&A ───────────────────────────────────────────────────────────────
def answer_research_question(query: str, all_papers: list, chat_history: list) -> str:
    """
    Find relevant papers using vector similarity and answer the user's
    research question using Groq LLM with full context.
    """
    relevant = find_relevant_papers(query, all_papers, top_k=3)
    context = _build_paper_context(relevant)

    system_prompt = (
        "You are ResearchHub AI, an expert research assistant. "
        "You help researchers understand academic papers. "
        "Use the provided paper context to answer questions accurately and concisely. "
        "If the context doesn't cover the question, say so honestly.\n\n"
        f"PAPER CONTEXT:\n{context}"
    )

    trimmed_history = build_smart_context(chat_history, max_messages=6)
    messages = [{"role": "system", "content": system_prompt}]
    messages += trimmed_history
    messages.append({"role": "user", "content": query})

    return chat_with_groq(messages)


# ── 2. Paper Summarization ────────────────────────────────────────────────────
def summarize_paper(paper) -> str:
    """
    Auto-generate a concise summary of a single paper.
    Called when a paper is imported into a workspace.
    """
    prompt = f"""Summarize this research paper in 3-5 clear sentences for a researcher.
Focus on: what problem it solves, what method it uses, and what the key result is.

Title: {paper.title}
Authors: {paper.authors}
Abstract: {paper.abstract}

Write the summary in plain English. Do not use bullet points."""

    messages = [
        {"role": "system", "content": "You are a scientific summarization expert. Be concise and accurate."},
        {"role": "user", "content": prompt}
    ]
    return chat_with_groq(messages)


# ── 3. Cross-Paper Comparison ─────────────────────────────────────────────────
def compare_papers(papers: list) -> str:
    """
    Generate a structured comparison across multiple papers.
    Useful when a researcher asks 'how do these papers differ?'
    """
    if len(papers) < 2:
        return "Need at least 2 papers to compare."

    paper_list = ""
    for i, p in enumerate(papers, 1):
        paper_list += f"\nPaper {i}: {p.title}\nAuthors: {p.authors}\nAbstract: {p.abstract}\n"

    prompt = f"""Compare these {len(papers)} research papers across these dimensions:
1. Problem they solve
2. Methodology / approach used
3. Key results / contributions
4. Limitations mentioned

Papers:
{paper_list}

Format your response as a clear structured comparison. Be specific and cite paper numbers."""

    messages = [
        {"role": "system", "content": "You are an expert research analyst specializing in comparing academic papers."},
        {"role": "user", "content": prompt}
    ]
    return chat_with_groq(messages)


# ── 4. Key Findings Extraction ────────────────────────────────────────────────
def extract_key_findings(paper) -> dict:
    """
    Extract structured key findings from a paper's abstract.
    Returns a dict with: problem, method, result, contribution.
    """
    prompt = f"""Extract key information from this paper.
Respond ONLY with a JSON object with exactly these 4 keys:
- "problem": what problem does this paper address? (1 sentence)
- "method": what technique or approach do they use? (1 sentence)
- "result": what is the main result or achievement? (1 sentence)
- "contribution": why does this matter to the field? (1 sentence)

Title: {paper.title}
Abstract: {paper.abstract}

Return only valid JSON, no extra text."""

    messages = [
        {"role": "system", "content": "You extract structured information from research papers. Always respond with valid JSON only."},
        {"role": "user", "content": prompt}
    ]
    response = chat_with_groq(messages)

    import json
    try:
        clean = response.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except json.JSONDecodeError:
        return {
            "problem": "Could not extract",
            "method": "Could not extract",
            "result": "Could not extract",
            "contribution": response
        }


# ── 5. Smart Context Memory Manager ──────────────────────────────────────────
def build_smart_context(chat_history: list, max_messages: int = 6) -> list:
    """
    Intelligently trim chat history to avoid token overflow.

    Strategy:
    - Always keep the first message (establishes conversation topic)
    - Always keep the last N most recent messages
    - Drop middle messages if history is too long
    """
    if len(chat_history) <= max_messages:
        return chat_history

    first = chat_history[0]
    recent = chat_history[-(max_messages - 1):]

    if first in recent:
        return recent

    return [first] + recent


# ── Internal Helper ───────────────────────────────────────────────────────────
def _build_paper_context(papers: list) -> str:
    """Format paper objects into a readable context string for the LLM."""
    if not papers:
        return "No papers available in this workspace."
    context = ""
    for i, p in enumerate(papers, 1):
        context += f"\n[Paper {i}]\nTitle: {p.title}\nAuthors: {p.authors}\nAbstract: {p.abstract}\n"
    return context
