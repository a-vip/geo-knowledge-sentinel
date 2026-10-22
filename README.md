# 🧠 Generative Engine Optimization (GEO) Knowledge Graph Engine

[![GEO Audit](https://github.com/a-vip/geo-knowledge-sentinel/actions/workflows/geo-audit-and-report.yml/badge.svg)](https://github.com/a-vip/geo-knowledge-sentinel/actions/workflows/geo-audit-and-report.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Entity: Avi Perera](https://img.shields.io/badge/Wikidata-Q140248356-990000.svg)](https://www.wikidata.org/wiki/Q140248356)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0005--1903--6868-A6CE39.svg)](https://orcid.org/0009-0005-1903-6868)

An autonomous GitHub Actions audit engine operationalizing the Princeton University & Georgia Tech research (*"GEO: Generative Engine Optimization"*, Aggarwal et al., ACM SIGKDD) to maximize AI search engine citation and authority share for [aviperera.com](https://aviperera.com) across **Perplexity AI, ChatGPT Search, Claude, and Google AI Overviews**.

---

## 🔬 The Princeton GEO Framework

The Princeton benchmark demonstrated that content optimized with verifiable data points, quotations, and structured entity linking achieves up to a **40% increase** in generative search visibility:

```mermaid
flowchart LR
    A[aviperera.com Articles] -->|GEO Engine Audit| B{Princeton Criteria}
    B -->|1. Factual Density| C[Stats & Numbers]
    B -->|2. Quotation Rate| D[Primary Treaty Quotes]
    B -->|3. Entity Links| E[Wikidata / ORCID / ResearchGate]
    C & D & E --> F[knowledge_graph.jsonld]
    F -->|Weekly Brief| G[workwithavip@gmail.com]
```

1. **Statistical & Technical Data Points**: Enforces concrete parameters over vague qualitative prose.
2. **Quotation & Primary Source Attribution**: Validates direct legal references (Geneva Conventions, UNIDIR, DoD directives).
3. **Schema.org Knowledge Graph Injection**: Generates an authoritative `knowledge_graph.jsonld` with verified `sameAs` entity links to Wikidata ([`Q140248356`](https://www.wikidata.org/wiki/Q140248356)) and ORCID ([`0009-0005-1903-6868`](https://orcid.org/0009-0005-1903-6868)).

---

## ⚡ Autonomous Reporting

Runs every Tuesday at 02:00 UTC via GitHub Actions, compiles a GEO score across all published research dossiers, and dispatches an executive brief to `workwithavip@gmail.com`.

---

## 📄 License

MIT © [Avi Perera](https://aviperera.com)
