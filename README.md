Live: https://nodenavigator.onrender.com
# NodeNavigator

> A game-engine code guide that shows where every millisecond of an answer goes.

## Problem

Godot is a large open-source game engine with thousands of source files and class reference files, making it difficult for developers to quickly locate the implementation behind a particular engine behavior. Gameplay programmers often need answers about callbacks, signals, physics, rendering, and other engine internals while coding. Searching manually across a large codebase takes time and interrupts development flow. NodeNavigator helps developers ask questions in natural language, find relevant source files, and understand the answer while tracking the latency of each processing stage.

## Who it is for

Gameplay programmers at indie game studios, particularly developers working with Godot who need to understand engine internals, debug behavior, and locate relevant C++ source files quickly.

## Signature feature

A per-answer timing strip that displays the milliseconds spent on embedding, search, re-ranking, and LLM generation, helping developers identify bottlenecks and understand the performance of every answer.

## Hardest problem (my interview story)

The hardest problem is building an observability system that traces every question through the complete retrieval and answer-generation pipeline. Each stage needs accurate timing so I can identify the slowest component and optimize it without sacrificing answer relevance. My target is a p95 end-to-end response latency below 2.5 seconds, with per-stage traces available for 100% of requests. I also plan to connect a natural-language data analyst that generates safe, read-only SQL queries against Godot GitHub issues and pull requests, linking the results to relevant engine source files.

## Dataset

| Source | Link | Documents | Pages | Licence / terms |
|---|---|---:|---|---|
| Godot Engine source code and class reference | [github.com/godotengine/godot](https://github.com/godotengine/godot) | Target: 8,400+ source and reference files | Not applicable | MIT licence; verify individual files and third-party components |
| Godot GitHub issues and pull requests | [github.com/godotengine/godot/issues](https://github.com/godotengine/godot/issues) | To be determined from the public GitHub API dataset | Not applicable | GitHub API terms; respect applicable rate limits and content licences |

## 10 real questions

See [docs/QUESTIONS.md](docs/QUESTIONS.md).

Example questions:

1. How does a Node's `_process` callback get called each frame?
2. Where are signals connected and emitted in the core code?
3. Which file implements the 2D physics body collision response?
4. How does the scene tree handle adding and removing nodes?
5. Where is the main game loop implemented?
6. How does Godot dispatch input events to nodes?
7. Which files implement 2D rendering?
8. How does the engine load and instantiate a scene?
9. Which engine area has the most open bugs this quarter?
10. Which source files are related to the most frequently reported open issues?

## Performance target

**Target:** p95 end-to-end response latency below 2.5 seconds, with per-stage timing traces for 100% of requests.

The target should be validated using measured results and a representative test set.

## Run it
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                                 # Windows: copy .env.example .env
uvicorn app.main:app --reload
curl localhost:8000/health
```

## Live link
<Added in Week 2>
