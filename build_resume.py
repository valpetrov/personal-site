"""Generate Val Petrov's professional resume as a PDF."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Palette — distilled from the site's dark theme into a refined light edition.
INK = HexColor("#1a1d24")
SUBINK = HexColor("#4a4d54")
MUTED = HexColor("#8a8b8e")
ACCENT = HexColor("#b8923b")
ACCENT_SOFT = HexColor("#c9a84c")
HAIR = HexColor("#dcd9d2")
BG_SOFT = HexColor("#f7f4ee")
PAPER = HexColor("#fdfcf8")

SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_I = "Times-Italic"
SANS = "Helvetica"
SANS_B = "Helvetica-Bold"
MONO = "Courier"
MONO_B = "Courier-Bold"

PAGE_W, PAGE_H = LETTER
MARGIN_L = 0.45 * inch
MARGIN_R = 0.45 * inch
MARGIN_T = 0.42 * inch
MARGIN_B = 0.42 * inch

SIDEBAR_W = 2.10 * inch  # left sidebar
GUTTER = 0.28 * inch
MAIN_X = MARGIN_L + SIDEBAR_W + GUTTER
MAIN_W = PAGE_W - MAIN_X - MARGIN_R


def draw_background(c):
    # Sidebar background (soft cream).
    c.setFillColor(BG_SOFT)
    c.rect(0, 0, MARGIN_L + SIDEBAR_W + GUTTER / 2, PAGE_H, fill=1, stroke=0)
    # Main panel.
    c.setFillColor(PAPER)
    c.rect(MARGIN_L + SIDEBAR_W + GUTTER / 2, 0, PAGE_W - (MARGIN_L + SIDEBAR_W + GUTTER / 2), PAGE_H, fill=1, stroke=0)
    # Accent stripe down the divider.
    c.setFillColor(ACCENT)
    c.rect(MARGIN_L + SIDEBAR_W + GUTTER / 2 - 1, 0, 2, PAGE_H, fill=1, stroke=0)


def draw_header(c):
    """Name block at the top of the main column."""
    y = PAGE_H - MARGIN_T - 6
    # Tiny label
    c.setFillColor(ACCENT)
    c.setFont(MONO_B, 6.8)
    c.drawString(MAIN_X, y, "AGENTIC ENGINEER  ·  NEW YORK, NY")
    # Hairline under label
    y -= 7
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.6)
    c.line(MAIN_X, y, MAIN_X + 70, y)

    # Name — large serif
    y -= 34
    c.setFillColor(INK)
    c.setFont(SERIF_B, 28)
    c.drawString(MAIN_X, y, "Val Petrov")

    # Tagline — italic serif with gold em-style on "agents"
    y -= 18
    c.setFont(SERIF_I, 11.5)
    c.setFillColor(SUBINK)
    text = "Building autonomous "
    c.drawString(MAIN_X, y, text)
    w = c.stringWidth(text, SERIF_I, 11.5)
    c.setFillColor(ACCENT)
    c.drawString(MAIN_X + w, y, "agents")
    w2 = c.stringWidth("agents", SERIF_I, 11.5)
    c.setFillColor(SUBINK)
    c.drawString(MAIN_X + w + w2, y, " that move industries.")

    # Decorative thin rule
    y -= 10
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.5)
    c.line(MAIN_X, y, MAIN_X + MAIN_W, y)
    return y - 11


def draw_sidebar_section_title(c, y, title):
    c.setFillColor(ACCENT)
    c.setFont(MONO_B, 7)
    c.drawString(MARGIN_L, y, title.upper())
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.5)
    c.line(MARGIN_L, y - 3.5, MARGIN_L + 16, y - 3.5)
    return y - 14


def draw_main_section_title(c, y, title):
    c.setFillColor(ACCENT)
    c.setFont(MONO_B, 7)
    c.drawString(MAIN_X, y, title.upper())
    # Hairline extending to the right
    tw = c.stringWidth(title.upper(), MONO_B, 7)
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.4)
    c.line(MAIN_X + tw + 8, y + 2.5, MAIN_X + MAIN_W, y + 2.5)
    return y - 12


def wrap(c, text, font, size, width):
    """Word-wrap text to a max pixel width. Returns a list of lines."""
    words = text.split()
    if not words:
        return [""]
    lines = []
    cur = words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if c.stringWidth(trial, font, size) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def draw_paragraph(c, x, y, text, font, size, leading, width, color=SUBINK):
    c.setFillColor(color)
    c.setFont(font, size)
    for line in wrap(c, text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def draw_sidebar(c):
    y = PAGE_H - MARGIN_T - 6

    # ===== CONTACT =====
    y = draw_sidebar_section_title(c, y, "Contact")
    for label, value in [
        ("Email", "val.petrov@gmail.com"),
        ("Phone", "(646) 470-4361"),
        ("LinkedIn", "linkedin.com/in/valpetrov"),
        ("Location", "New York, NY"),
    ]:
        c.setFillColor(INK)
        c.setFont(SANS_B, 7.4)
        c.drawString(MARGIN_L, y, label.upper())
        c.setFillColor(SUBINK)
        c.setFont(SANS, 8)
        c.drawString(MARGIN_L, y - 9.5, value)
        y -= 23

    # ===== SKILLS =====
    y = draw_sidebar_section_title(c, y, "Expertise")

    skill_groups = [
        ("AI & Agentic", [
            "LLM Agents",
            "Multi-Agent Orchestration",
            "RAG Pipelines",
            "Tool Use / Function Calling",
            "Prompt Engineering",
            "LangChain / LangGraph",
            "Vector Databases",
        ]),
        ("LLM Platforms", [
            "OpenAI API",
            "Claude / Anthropic API",
            "Hugging Face",
            "Pinecone · ChromaDB",
        ]),
        ("Languages", [
            "Python · Kotlin · Java",
            "TypeScript · C# · SQL",
        ]),
        ("Infrastructure & Data", [
            "Apache Kafka · Databricks",
            "Redis · SQL Server",
            "Hadoop / HDFS · Delta Lake",
        ]),
        ("Domain Background", [
            "FinTech / Wall Street",
            "Security Master",
            "Portfolio Management",
            "Real-Time Systems",
        ]),
        ("Leadership", [
            "Team Building",
            "Systems Architecture",
            "Agile · Hiring · Mentoring",
        ]),
    ]

    for title, items in skill_groups:
        c.setFillColor(INK)
        c.setFont(SANS_B, 7.6)
        c.drawString(MARGIN_L, y, title)
        # Small accent dot
        c.setFillColor(ACCENT)
        c.circle(MARGIN_L - 6, y + 2.5, 1.2, fill=1, stroke=0)
        y -= 9.5
        c.setFillColor(SUBINK)
        c.setFont(SANS, 7.4)
        for item in items:
            c.drawString(MARGIN_L, y, item)
            y -= 9
        y -= 4.5

    # ===== EDUCATION =====
    y = draw_sidebar_section_title(c, y, "Education")
    c.setFillColor(INK)
    c.setFont(SERIF_B, 9.5)
    c.drawString(MARGIN_L, y, "B.S. Computer Eng.")
    y -= 11
    c.setFillColor(ACCENT)
    c.setFont(SANS_B, 7.6)
    c.drawString(MARGIN_L, y, "University of Waterloo")
    y -= 10
    c.setFillColor(MUTED)
    c.setFont(MONO, 7)
    c.drawString(MARGIN_L, y, "Ontario · Class of 2008")
    y -= 10
    c.setFillColor(SUBINK)
    c.setFont(SANS, 7.6)
    c.drawString(MARGIN_L, y, "GPA: ")
    c.setFillColor(ACCENT)
    c.setFont(SANS_B, 7.6)
    c.drawString(MARGIN_L + 20, y, "3.7 / 4.0")
    y -= 18

    # ===== METRICS =====
    y = draw_sidebar_section_title(c, y, "Snapshot")

    metrics = [
        ("14+", "Years in distributed systems"),
        ("5", "Tier-1 Wall Street firms"),
        ("8+", "Engineers led on PMS"),
        ("6M+", "Txns/day at sub-sec latency"),
    ]
    for big, label in metrics:
        c.setFillColor(ACCENT)
        c.setFont(SERIF_B, 14)
        c.drawString(MARGIN_L, y, big)
        bw = c.stringWidth(big, SERIF_B, 14)
        c.setFillColor(SUBINK)
        c.setFont(SANS, 7)
        label_x = MARGIN_L + bw + 5
        max_label_w = SIDEBAR_W - bw - 5
        for i, line in enumerate(wrap(c, label, SANS, 7, max_label_w)):
            c.drawString(label_x, y + 3 - i * 8, line)
        y -= 18


def draw_skill_pill(c, x, y, text):
    pad_x = 4
    pad_y = 1.8
    w = c.stringWidth(text, MONO_B, 6.2) + pad_x * 2
    h = 7.5 + pad_y * 2
    c.setFillColor(HexColor("#f1ead7"))
    c.setStrokeColor(HexColor("#e2d6a8"))
    c.setLineWidth(0.3)
    c.roundRect(x, y - pad_y, w, h, 2, fill=1, stroke=1)
    c.setFillColor(ACCENT)
    c.setFont(MONO_B, 6.2)
    c.drawString(x + pad_x, y + 1.5, text)
    return w


def draw_skill_pills(c, x, y, pills, max_width):
    row_x = x
    for p in pills:
        w = c.stringWidth(p, MONO_B, 6.2) + 8
        if row_x + w > x + max_width:
            row_x = x
            y -= 12
        draw_skill_pill(c, row_x, y, p)
        row_x += w + 3
    return y - 11


def draw_experience_item(c, y, date, title, company, desc, tech):
    # Date marker — small monospaced label with bullet
    c.setFillColor(ACCENT)
    c.circle(MAIN_X - 7, y + 2.5, 1.6, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont(MONO, 6.6)
    c.drawString(MAIN_X, y, date.upper())
    y -= 10

    # Title
    c.setFillColor(INK)
    c.setFont(SERIF_B, 10.5)
    c.drawString(MAIN_X, y, title)
    y -= 11

    # Company
    c.setFillColor(ACCENT)
    c.setFont(SANS_B, 7.8)
    c.drawString(MAIN_X, y, company)
    y -= 9.5

    # Description
    y = draw_paragraph(c, MAIN_X, y, desc, SANS, 7.8, 9.8, MAIN_W, SUBINK)
    y -= 1

    # Tech pills
    if tech:
        y = draw_skill_pills(c, MAIN_X, y, tech, MAIN_W)
    return y - 5


def draw_main(c, y):
    # ===== SUMMARY =====
    y = draw_main_section_title(c, y, "Profile")
    summary = (
        "Agentic Engineer with 14+ years architecting mission-critical distributed systems for "
        "top-tier Wall Street firms — now focused on autonomous AI agents, LLM-powered workflows, "
        "and multi-agent orchestration. Deep expertise across real-time data pipelines, platform "
        "architecture, and team leadership. I build systems — and agents — that reason, act, and ship."
    )
    y = draw_paragraph(c, MAIN_X, y, summary, SANS, 8, 10.5, MAIN_W, INK)
    y -= 6

    # ===== EXPERIENCE =====
    y = draw_main_section_title(c, y, "Experience")

    experiences = [
        {
            "date": "Apr 2025 — Present",
            "title": "Tech Lead — Macro Technology",
            "company": "Point72  ·  New York",
            "desc": (
                "Leading technology for the macro investment platform. Orchestrating Murex migration "
                "with end-to-end ownership of trade booking, straight-through processing, and "
                "reconciliation across a distributed financial data stack."
            ),
            "tech": ["Murex", "C#", ".NET", "Python 3.14", "SQL Server", "Sybase", "Kafka", "Databricks"],
        },
        {
            "date": "Nov 2022 — Jan 2025",
            "title": "Data Warehouse Lead — Security Master",
            "company": "Centiva Capital  ·  New York",
            "desc": (
                "Designed and built the firm's new security master from the ground up. Architected "
                "authorization services, instrument creation pipelines, and vendor data integrations "
                "(Bloomberg Sanctions, Corporate Actions, Pricing). Led sprints, hiring, and onboarding."
            ),
            "tech": ["Python 3.11", "SQL Server", "Databricks", "Git"],
        },
        {
            "date": "Jul 2018 — Nov 2022",
            "title": "Software Engineering Lead — Portfolio Management",
            "company": "Schonfeld  ·  New York",
            "desc": (
                "Led a team of 8 engineers delivering an in-house PMS processing 6M+ transactions/day "
                "with sub-second latency. Built security master validation pipelines and a scalable "
                "Kafka-based architecture. Spearheaded Agile practices and mentored the team."
            ),
            "tech": ["Kotlin", "Java 8/11", "Kafka", "MySQL", "Redis", "kdb+"],
        },
        {
            "date": "Jan 2017 — Jul 2018",
            "title": "Senior Software Developer — Middle Office",
            "company": "Millennium Partners  ·  New York",
            "desc": (
                "Developed invoicing, expense, and document management systems. Consolidated T+1 PMS "
                "PnL reporting; implemented a Kafka & Python POC for T-0 PnL delivery; reduced "
                "redundant Murex trade data by 88% via SQL optimization."
            ),
            "tech": ["C# 7", ".NET 4.0", "Kafka", "Python", "RabbitMQ"],
        },
        {
            "date": "Mar 2015 — May 2016",
            "title": "Senior Software Developer — Big Data Platform",
            "company": "Bloomberg L.P.  ·  New York",
            "desc": (
                "Built RESTful services for file storage and retrieval. Architected Big Data solutions "
                "using Hadoop HDFS and Solr handling hundreds of millions of messages daily. "
                "Engineered schema-driven extraction and search services."
            ),
            "tech": ["Java", "Hadoop", "HBase", "Solr", "Python", "Flask"],
        },
        {
            "date": "Mar 2011 — Mar 2015",
            "title": "Senior Software Developer — MBS Structuring & Analytics",
            "company": "Bloomberg L.P.  ·  New York",
            "desc": (
                "Built domain-rich GUI applications for Mortgage-Backed Securities structuring using "
                ".NET and WPF. Developed distributed server-side services, authored custom controls, "
                "and invented a novel concurrency control solution for improved throughput."
            ),
            "tech": ["C#", "WPF", ".NET", "C++"],
        },
        {
            "date": "Sep 2010 — Mar 2011",
            "title": "Software Engineer — Director",
            "company": "Trading Machines  ·  Stamford, CT",
            "desc": (
                "Led front-end GUI development for 90+ trading forms across 7+ applications. Managed "
                "multicast traffic consistency and built proprietary libraries for back-office "
                "functions. Coordinated market data feeds from OPRA, CTA, UTP, and direct exchanges."
            ),
            "tech": ["C#", "WinForms", "C++", "Perl", "FIX Protocol"],
        },
    ]

    for exp in experiences:
        # Page-break safety: if not enough room for a full block, start new page.
        if y < MARGIN_B + 110:
            draw_footer(c)
            c.showPage()
            draw_background(c)
            # Continue main column on new page, no header — but a continuation label
            y = PAGE_H - MARGIN_T - 8
            c.setFillColor(ACCENT)
            c.setFont(MONO_B, 7)
            c.drawString(MAIN_X, y, "VAL PETROV  ·  EXPERIENCE (CONT.)")
            y -= 8
            c.setStrokeColor(ACCENT)
            c.line(MAIN_X, y, MAIN_X + 70, y)
            y -= 22
            # Redraw sidebar header continuation
            sy = PAGE_H - MARGIN_T - 8
            c.setFillColor(ACCENT)
            c.setFont(MONO_B, 7)
            c.drawString(MARGIN_L, sy, "VAL PETROV")
            sy -= 8
            c.line(MARGIN_L, sy, MARGIN_L + 18, sy)
            sy -= 14
            c.setFillColor(INK)
            c.setFont(SERIF_B, 14)
            c.drawString(MARGIN_L, sy, "Agentic Engineer")
            sy -= 14
            c.setFillColor(SUBINK)
            c.setFont(SANS, 8)
            c.drawString(MARGIN_L, sy, "val.petrov@gmail.com")
            sy -= 10
            c.drawString(MARGIN_L, sy, "(646) 470-4361")
            sy -= 10
            c.drawString(MARGIN_L, sy, "linkedin.com/in/valpetrov")
        y = draw_experience_item(c, y, exp["date"], exp["title"], exp["company"], exp["desc"], exp["tech"])

    return y


def draw_footer(c):
    y = MARGIN_B - 12
    c.setStrokeColor(HAIR)
    c.setLineWidth(0.4)
    c.line(MARGIN_L, y + 18, PAGE_W - MARGIN_R, y + 18)
    c.setFillColor(MUTED)
    c.setFont(MONO, 6.5)
    c.drawString(MARGIN_L, y + 6, "VAL PETROV  ·  AGENTIC ENGINEER  ·  NEW YORK, NY")
    text = "val.petrov@gmail.com  ·  (646) 470-4361  ·  linkedin.com/in/valpetrov"
    tw = c.stringWidth(text, MONO, 6.5)
    c.drawString(PAGE_W - MARGIN_R - tw, y + 6, text)


def build(out_path="val-petrov-resume.pdf"):
    c = canvas.Canvas(out_path, pagesize=LETTER)
    c.setTitle("Val Petrov — Resume")
    c.setAuthor("Val Petrov")
    c.setSubject("Resume — Agentic Engineer")

    draw_background(c)
    draw_sidebar(c)
    y_after_header = draw_header(c)
    draw_main(c, y_after_header)
    draw_footer(c)
    c.save()
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    build()
