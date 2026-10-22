#!/usr/bin/env python3
"""
geo_engine.py
Autonomous Generative Engine Optimization (GEO) & Knowledge Graph Engine for aviperera.com.
Operationalizes the Princeton / Georgia Tech research (Aggarwal et al., ACM SIGKDD)
to maximize AI search engine citation frequency (Perplexity, ChatGPT, Claude, Google AI Overviews).
"""

import os
import sys
import json
import html
import re
import urllib.request
import smtplib
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WP_API = "https://aviperera.com/wp-json/wp/v2/posts?per_page=100&_fields=id,slug,link,title,content,excerpt,date_gmt,modified_gmt"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
TARGET_EMAIL = "workwithavip@gmail.com"

AVI_PERERA_SAMEAS = [
    "https://www.wikidata.org/wiki/Q140248356",
    "https://orcid.org/0009-0005-1903-6868",
    "https://www.researchgate.net/profile/Avi-Perera",
    "https://www.linkedin.com/in/avi-perera",
    "https://bsky.app/profile/aviperera.bsky.social",
    "https://x.com/aviperera_"
]

def clean_html(text: str) -> str:
    clean = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(clean).strip()

def score_geo_readiness(title: str, content: str) -> dict:
    """Scores content against the Princeton GEO framework: Stats, Quotations, and Citations."""
    clean = clean_html(content)
    words = clean.split()
    word_count = len(words)
    
    # 1. Statistical / Technical Data Points (numbers, percentages, dimensions, years)
    stats_matches = re.findall(r"\b(?:\d+(?:\.\d+)?%?|\$\d+(?:\.\d+)?|\d{4})\b", clean)
    stats_density = (len(stats_matches) / max(word_count, 1)) * 100

    # 2. Quotation / Primary Source Attribution
    quotes = re.findall(r"[\"“][^\"”]{15,}[\"”]|<blockquote", content)
    has_quotes = len(quotes) > 0

    # 3. Legal / Academic Citations (treaties, conventions, protocols)
    citations = re.findall(r"\b(geneva|article\s+\d+|unidir|protocol\s+[i|iv|v]+|dod\s+directive|icrc|meaningful human control)\b", clean, re.IGNORECASE)
    has_authoritative_citations = len(citations) > 0

    score = 0
    if stats_density >= 2.0:
        score += 35
    elif stats_density >= 1.0:
        score += 20
        
    if has_quotes:
        score += 30
    if has_authoritative_citations:
        score += 35

    return {
        "score": min(score, 100),
        "word_count": word_count,
        "stats_count": len(stats_matches),
        "quote_count": len(quotes),
        "citation_count": len(citations)
    }

def build_knowledge_graph(posts: list) -> dict:
    """Generates unified Schema.org JSON-LD Knowledge Graph."""
    author_entity = {
        "@type": "Person",
        "@id": "https://aviperera.com/#avi-perera",
        "name": "Avi Perera",
        "jobTitle": "AI Governance Researcher & International Lawyer",
        "worksFor": {
            "@type": "Organization",
            "name": "Sovereign Intelligence Dashboard"
        },
        "url": "https://aviperera.com",
        "sameAs": AVI_PERERA_SAMEAS
    }

    graph_nodes = [author_entity]

    for p in posts:
        title = html.unescape(p.get("title", {}).get("rendered", "")).strip()
        link = p.get("link", "").strip()
        date_gmt = p.get("date_gmt", "")
        raw_excerpt = p.get("excerpt", {}).get("rendered", "")
        description = clean_html(raw_excerpt) if raw_excerpt else title

        article_node = {
            "@type": "TechArticle",
            "@id": f"{link}#article",
            "headline": title,
            "description": description[:200],
            "url": link,
            "datePublished": date_gmt,
            "author": {"@id": "https://aviperera.com/#avi-perera"},
            "publisher": {"@id": "https://aviperera.com/#avi-perera"},
            "inLanguage": "en-GB",
            "mainEntityOfPage": link
        }
        graph_nodes.append(article_node)

    return {
        "@context": "https://schema.org",
        "@graph": graph_nodes
    }

def send_weekly_report(plain_text: str, html_content: str, subject: str):
    smtp_host = os.getenv("SMTP_HOST") or "smtp.gmail.com"
    port_val = os.getenv("SMTP_PORT", "").strip()
    smtp_port = int(port_val) if port_val.isdigit() else 587
    smtp_user = os.getenv("SMTP_USERNAME", "").strip()
    smtp_pass = os.getenv("SMTP_PASSWORD", "").strip()

    if smtp_user and smtp_pass:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"Avi Perera GEO Sentinel <{smtp_user}>"
            msg["To"] = TARGET_EMAIL
            msg.attach(MIMEText(plain_text, "plain"))
            msg.attach(MIMEText(html_content, "html"))
            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, TARGET_EMAIL, msg.as_string())
            print(f"[OK] GEO report successfully emailed to {TARGET_EMAIL}")
            return
        except Exception as e:
            print(f"[!] SMTP failed: {e}")

    # Fallback to GitHub Issue dispatch
    gh_token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if gh_token:
        try:
            cmd = [
                "gh", "issue", "create",
                "--title", subject,
                "--body", f"{plain_text}\n\n---\n*Delivered autonomously to {TARGET_EMAIL} via GitHub Actions.*"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"[OK] Report issue dispatched: {res.stdout.strip()}")
            else:
                print(f"[i] Issue note: {res.stderr.strip()}")
        except Exception as e:
            print(f"[i] Issue note: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GEOSentinelBot/1.0; +https://aviperera.com)"}
    
    print("[*] Ingesting posts for Generative Engine Optimization audit...")
    try:
        req = urllib.request.Request(WP_API, headers=headers)
        with urllib.request.urlopen(req, timeout=25) as resp:
            posts = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[!] Fetch failed: {e}")
        return 1

    total_score = 0
    high_readiness = 0
    audited_posts = []

    for p in posts:
        title = html.unescape(p.get("title", {}).get("rendered", "")).strip()
        link = p.get("link", "").strip()
        content = p.get("content", {}).get("rendered", "")
        metrics = score_geo_readiness(title, content)
        total_score += metrics["score"]
        if metrics["score"] >= 70:
            high_readiness += 1
        audited_posts.append({"title": title, "link": link, **metrics})

    avg_score = round(total_score / max(len(posts), 1), 1)
    print(f"[OK] Evaluated {len(posts)} articles. Average GEO Readiness Score: {avg_score}/100")

    # Generate Knowledge Graph JSON-LD
    kg = build_knowledge_graph(posts)
    kg_path = os.path.join(OUTPUT_DIR, "knowledge_graph.jsonld")
    with open(kg_path, "w", encoding="utf-8") as f:
        json.dump(kg, f, indent=2, ensure_ascii=False)
    print(f"[OK] Unified Knowledge Graph exported to {kg_path}")

    # Prepare Reports
    now_str = datetime.now(timezone.utc).strftime("%B %d, %Y")
    subject = f"🧠 Weekly GEO & Knowledge Graph Brief: aviperera.com ({now_str})"
    
    plain_text = f"""Avi Perera — Weekly GEO (Generative Engine Optimization) Audit
Generated: {now_str} | Target: https://aviperera.com

=== Princeton GEO Metric Results ===
- Total Articles Evaluated: {len(posts)}
- Average AI Citation Score: {avg_score} / 100
- Highly Extractable Dossiers (Score >= 70): {high_readiness}
- Schema.org Entity Graph: Active (6 Wikidata, ORCID & ResearchGate sameAs nodes)

=== Top 5 AI-Search Optimised Dossiers ===
"""
    top_5 = sorted(audited_posts, key=lambda x: x["score"], reverse=True)[:5]
    for i, it in enumerate(top_5, 1):
        plain_text += f"{i}. {it['title']} (Score: {it['score']}/100) — {it['link']}\n"

    html_content = f"""
    <html>
    <body style="font-family: -apple-system, sans-serif; line-height: 1.6; color: #1e293b; max-width: 650px; margin: 0 auto; padding: 24px;">
        <div style="background: linear-gradient(135deg, #1e1b4b, #312e81); color: #f8fafc; padding: 24px; border-radius: 12px; margin-bottom: 24px;">
            <h1 style="margin: 0 0 8px 0; font-size: 22px;">Generative Engine Optimization (GEO) Brief</h1>
            <p style="margin: 0; font-size: 14px; opacity: 0.85;">Princeton Research Benchmark Audit • {now_str}</p>
        </div>
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
            <h2 style="font-size: 16px; margin-top: 0; color: #4338ca;">🎯 Princeton GEO Metric Health</h2>
            <p><strong>Average AI Citation Score:</strong> <span style="font-size: 20px; font-weight: bold; color: #10b981;">{avg_score} / 100</span></p>
            <p><strong>Dossiers with High AI Extractability:</strong> {high_readiness} of {len(posts)}</p>
            <p style="font-size: 13px; color: #64748b;">Unified Schema.org Knowledge Graph generated with sameAs links to Wikidata (Q140248356) and ORCID.</p>
        </div>
        <div style="text-align: center; font-size: 12px; color: #94a3b8; margin-top: 32px;">
            <p>Dispatched autonomously to {TARGET_EMAIL} by GitHub Actions.</p>
        </div>
    </body>
    </html>
    """

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(f"## {subject}\n\n```text\n{plain_text}\n```\n")

    send_weekly_report(plain_text, html_content, subject)
    return 0

if __name__ == "__main__":
    sys.exit(main())
