import csv
from pathlib import Path

OUT = Path("/home/claude/p/ai-governance-comparator/data/governance_matrix.csv")

HEADER = ["dimension", "category", "EU", "United States", "India", "United Kingdom", "notes"]

ROWS = [
    ["Primary instrument", "Structure",
     "AI Act (Regulation 2024/1689), binding horizontal law",
     "No comprehensive federal statute; sectoral rules, executive actions, NIST frameworks",
     "India AI Governance Guidelines (MeitY, Nov 2025); no standalone AI act",
     "No standalone AI act; regulator-led under existing law",
     "The EU is the outlier in having one binding horizontal instrument."],

    ["Legal bindingness", "Structure",
     "Binding regulation with penalties",
     "Mixed: voluntary frameworks plus binding sectoral rules and procurement conditions",
     "Guidance and principles applying existing statutes",
     "Voluntary guidance plus existing sectoral regulators",
     "Bindingness is the sharpest axis of divergence."],

    ["Core approach", "Structure",
     "Risk-tiered prohibition and obligation",
     "Innovation-first, standards and measurement led",
     "Light-touch, pro-innovation, principles-based",
     "Context-specific, pro-innovation, regulator-led",
     ""],

    ["Central coordinating body", "Institutions",
     "AI Office (European Commission)",
     "CAISI (Center for AI Standards and Innovation), within NIST",
     "AI Governance Group (AIGG) with a Technology and Policy Expert Committee",
     "AI Security Institute (AISI)",
     ""],

    ["Safety institute", "Institutions",
     "AI Office plus Scientific Panel",
     "CAISI",
     "IndiaAI Safety Institute",
     "AI Security Institute",
     "All four have a technical evaluation body, but their mandates differ substantially."],

    ["Risk classification", "Substance",
     "Four tiers: unacceptable, high, limited, minimal",
     "No formal statutory tiering; NIST RMF provides a voluntary taxonomy",
     "Principles-based, no formal statutory tiers",
     "Sector regulators apply their own risk judgements",
     ""],

    ["Prohibited practices", "Substance",
     "Yes, Article 5, applicable since February 2025",
     "No general federal prohibitions on AI practices as such",
     "No standalone prohibitions; existing criminal and consumer law applies",
     "No standalone prohibitions",
     ""],

    ["GPAI / foundation model rules", "Substance",
     "Yes. GPAI obligations applicable from August 2025; Commission enforcement powers from August 2026",
     "Voluntary commitments plus pre-deployment testing agreements with some developers",
     "No GPAI-specific obligations",
     "Voluntary agreements with frontier developers",
     ""],

    ["Transparency duties", "Substance",
     "Article 50 duties, applicable August 2026",
     "Sectoral disclosure rules; no general federal AI transparency mandate",
     "Transparency is a guiding principle rather than a separately enforced duty",
     "Expected via existing consumer and data protection law",
     ""],

    ["Third-party evaluation", "Evaluation",
     "Conformity assessment required for high-risk systems",
     "Voluntary. CAISI evaluates under agreements; no accreditation regime for evaluators",
     "IndiaAI Safety Institute role still being defined",
     "AISI conducts evaluations; no mandatory third-party regime",
     "No jurisdiction currently accredits AI evaluators. This is the open gap."],

    ["Evaluation standards", "Evaluation",
     "Harmonised standards under development via CEN-CENELEC",
     "NIST AI RMF, the GenAI Profile, and draft practices for automated benchmark evaluations",
     "Adopting international standards rather than authoring its own",
     "AISI publishes evaluation methods; no binding standard",
     ""],

    ["Compute thresholds", "Substance",
     "A FLOP threshold is used to presume systemic risk for GPAI models",
     "Reporting thresholds have featured in executive actions; status varies by administration",
     "No compute thresholds",
     "No compute thresholds",
     ""],

    ["Open-weight treatment", "Substance",
     "Partial exemptions for free and open-source models, subject to conditions",
     "Generally permissive; actively debated in policy circles",
     "Explicitly supportive of open innovation and domestic model development",
     "Permissive",
     ""],

    ["Enforcement penalties", "Enforcement",
     "Up to 7 percent of global turnover or EUR 35m for prohibited practices",
     "Sectoral enforcement by the FTC and others under existing authority",
     "Existing sectoral penalties; no AI-specific penalty regime",
     "Existing regulator powers",
     ""],

    ["Extraterritorial reach", "Enforcement",
     "Yes. Applies to providers placing systems on the EU market",
     "Primarily domestic, though export controls reach abroad",
     "Primarily domestic",
     "Primarily domestic",
     ""],

    ["Key timeline", "Timeline",
     "Prohibitions Feb 2025; GPAI Aug 2025; transparency and GPAI enforcement Aug 2026; high-risk Dec 2027 and Aug 2028",
     "Shifts with administration; no fixed statutory schedule",
     "Guidelines issued November 2025; implementation ongoing",
     "Ongoing; no fixed statutory schedule",
     "EU high-risk deadlines were pushed back by the Digital Omnibus (Reg. 2026/1744, in force 27 July 2026)."],

    ["Innovation posture", "Posture",
     "Regulate first and adjust later; criticised for compliance burden",
     "Deregulatory and competitiveness-focused in current posture",
     "Explicitly pro-innovation; avoids pre-emptive restriction",
     "Pro-innovation; avoids early statutory constraint",
     ""],

    ["Global South relevance", "Posture",
     "High compliance cost may deter adoption as a template",
     "Limited direct transferability",
     "High. Positions India as a reference model for jurisdictions weighing EU-style rules against flexibility",
     "Moderate",
     "This row is the analytical payoff of the comparison."],
]

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(HEADER)
    w.writerows(ROWS)

print(f"wrote {len(ROWS)} rows")
