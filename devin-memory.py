#!/usr/bin/env python3
"""
codey's Memory System v2
========================
SQLite + nomic-embed-text (via Ollama) for semantic memory.
No Qdrant, no Mem0 — just embeddings stored alongside text in SQLite.
Cosine similarity search done in Python.

Usage:
    python3 codey-memory.py add "Andrew suggested the promises.md system" --category relationship --person "Andrew Grantham"
    python3 codey-memory.py search "What do I know about Andrew?"
    python3 codey-memory.py search "trading portfolio" --limit 3
    python3 codey-memory.py person "Estevo"
    python3 codey-memory.py list
    python3 codey-memory.py count
    python3 codey-memory.py load seed-memories.txt
    python3 codey-memory.py startup
    python3 codey-memory.py delete <id>
"""

import sys
import os
import json
import argparse
import time
import sqlite3
import struct
import math
import requests

DB_PATH = "/home/themapsmith/codexProjects/codey-memories.db"
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            category TEXT DEFAULT 'general',
            person TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            embedding BLOB NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_person ON memories(person)")
    conn.commit()
    return conn

def embed(text):
    """Get embedding from Ollama nomic-embed-text."""
    resp = requests.post(f"{OLLAMA_URL}/api/embeddings", json={
        "model": EMBED_MODEL,
        "prompt": text
    }, timeout=30)
    resp.raise_for_status()
    vec = resp.json()["embedding"]
    return vec

def vec_to_bytes(vec):
    return struct.pack(f'{len(vec)}f', *vec)

def bytes_to_vec(b):
    n = len(b) // 4
    return struct.unpack(f'{n}f', b)

def cosine_sim(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

def add_memory(text, category="general", person=""):
    conn = get_db()
    vec = embed(text)
    conn.execute(
        "INSERT INTO memories (text, category, person, created_at, embedding) VALUES (?, ?, ?, ?, ?)",
        (text, category, person, time.strftime("%Y-%m-%dT%H:%M:%S"), vec_to_bytes(vec))
    )
    conn.commit()
    last_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return last_id

def search_memory(query, limit=5, category=None, person=None):
    conn = get_db()
    query_vec = embed(query)

    # Build SQL filter
    where = []
    params = []
    if category:
        where.append("category = ?")
        params.append(category)
    if person:
        where.append("person = ?")
        params.append(person)

    sql = "SELECT id, text, category, person, created_at, embedding FROM memories"
    if where:
        sql += " WHERE " + " AND ".join(where)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    # Score by cosine similarity
    scored = []
    for row in rows:
        rid, text, cat, per, created, emb_bytes = row
        emb = bytes_to_vec(emb_bytes)
        score = cosine_sim(query_vec, emb)
        scored.append({
            "id": rid,
            "text": text,
            "category": cat,
            "person": per,
            "created_at": created,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]

def list_memories(category=None):
    conn = get_db()
    if category:
        rows = conn.execute(
            "SELECT id, text, category, person, created_at FROM memories WHERE category = ? ORDER BY id",
            (category,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, text, category, person, created_at FROM memories ORDER BY id"
        ).fetchall()
    conn.close()
    return rows

def count_memories():
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
    conn.close()
    return count

def delete_memory(mem_id):
    conn = get_db()
    conn.execute("DELETE FROM memories WHERE id = ?", (mem_id,))
    conn.commit()
    conn.close()

def startup_context():
    """Get essential startup context across multiple query categories."""
    queries = [
        "active conversations, who needs replies, recent emails",
        "open promises and commitments I owe people",
        "trading portfolio status, bots, equity, P&L",
        "important recent events, milestones, breakthroughs",
        "creative projects in progress, writing, games",
        "key relationships and personality notes",
        "standing rules and instructions",
    ]

    seen_ids = set()
    context = []
    for q in queries:
        results = search_memory(q, limit=3)
        for r in results:
            if r["id"] not in seen_ids:
                seen_ids.add(r["id"])
                context.append(r)

    context.sort(key=lambda x: x["score"], reverse=True)
    return context

def main():
    parser = argparse.ArgumentParser(description="codey's Memory System v2")
    subparsers = parser.add_subparsers(dest="command")

    add_p = subparsers.add_parser("add", help="Add a memory")
    add_p.add_argument("text")
    add_p.add_argument("--category", default="general")
    add_p.add_argument("--person", default="")

    search_p = subparsers.add_parser("search", help="Search memories")
    search_p.add_argument("query")
    search_p.add_argument("--limit", type=int, default=5)
    search_p.add_argument("--category", default=None)
    search_p.add_argument("--person", default=None)

    person_p = subparsers.add_parser("person", help="Search by person")
    person_p.add_argument("name")

    subparsers.add_parser("list", help="List all memories")
    subparsers.add_parser("count", help="Count memories")

    load_p = subparsers.add_parser("load", help="Load from file")
    load_p.add_argument("file")

    subparsers.add_parser("startup", help="Get startup context")

    del_p = subparsers.add_parser("delete", help="Delete a memory by ID")
    del_p.add_argument("id", type=int)

    args = parser.parse_args()

    if args.command == "add":
        mid = add_memory(args.text, args.category, args.person)
        print(f"Added memory #{mid}")

    elif args.command == "search":
        results = search_memory(args.query, limit=args.limit, category=args.category, person=args.person)
        for r in results:
            meta = f" [{r['category']}]" if r['category'] else ""
            meta += f" (re: {r['person']})" if r['person'] else ""
            print(f"[{r['score']:.3f}] #{r['id']}{meta} {r['text']}")

    elif args.command == "person":
        # First try filtered by person field
        results = search_memory(f"What do I know about {args.name}?", limit=10, person=args.name)
        if not results:
            results = search_memory(args.name, limit=10)
        for r in results:
            print(f"[{r['score']:.3f}] {r['text']}")

    elif args.command == "list":
        rows = list_memories()
        for r in rows:
            rid, text, cat, person, created = r
            meta = f" [{cat}]" if cat else ""
            meta += f" (re: {person})" if person else ""
            print(f"#{rid}{meta} {text} ({created})")

    elif args.command == "count":
        print(f"Total memories: {count_memories()}")

    elif args.command == "load":
        with open(args.file) as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        print(f"Loading {len(lines)} memories...")
        for i, line in enumerate(lines):
            parts = line.split(" | ")
            text = parts[0]
            category = "general"
            person = ""
            for p in parts[1:]:
                if p.startswith("category="):
                    category = p.split("=", 1)[1]
                elif p.startswith("person="):
                    person = p.split("=", 1)[1]
            mid = add_memory(text, category, person)
            print(f"  [{i+1}/{len(lines)}] #{mid} {text[:70]}...")
        print(f"Done! {len(lines)} memories loaded.")

    elif args.command == "startup":
        context = startup_context()
        print(f"Startup context ({len(context)} unique memories):\n")
        for c in context:
            print(f"[{c['score']:.3f}] {c['text']}")

    elif args.command == "delete":
        delete_memory(args.id)
        print(f"Deleted memory #{args.id}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
