"""
AI Governance Comparator.

A structured side-by-side of how four jurisdictions approach the same
regulatory questions, plus a divergence score showing where they agree
and where they split.

Run:     streamlit run app.py
Deploy:  see DEPLOY.md
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="AI Governance Comparator", layout="wide",
                   initial_sidebar_state="expanded")

DATA = Path(__file__).parent / "data"
JURISDICTIONS = ["EU", "United States", "India", "United Kingdom"]


@st.cache_data
def load():
    m = pd.read_csv(DATA / "governance_matrix.csv")
    s = pd.read_csv(DATA / "sources.csv")
    return m, s


matrix, sources = load()

st.title("AI Governance Comparator")
st.caption(
    "How the EU, US, India and UK answer the same regulatory questions differently. "
    "Compiled September 2026 from primary sources. Verify against the originals "
    "listed under Sources before citing."
)

# ---------------- sidebar ----------------
st.sidebar.header("Filters")
cats = sorted(matrix["category"].unique())
sel_cats = st.sidebar.multiselect("Category", cats, default=cats)
sel_juris = st.sidebar.multiselect("Jurisdictions", JURISDICTIONS, default=JURISDICTIONS)
if not sel_juris:
    st.warning("Select at least one jurisdiction.")
    st.stop()

view = matrix[matrix["category"].isin(sel_cats)]

# ---------------- divergence ----------------
def divergence_score(row, juris):
    """Crude but honest: how many distinct positions exist across the
    selected jurisdictions for this dimension. Normalised 0-1. Text is
    compared after lowercasing and trimming, so near-identical wording
    counts as agreement only if it is actually identical."""
    vals = [str(row[j]).strip().lower() for j in juris if j in row.index]
    if len(vals) <= 1:
        return 0.0
    return (len(set(vals)) - 1) / (len(vals) - 1)


view = view.copy()
view["divergence"] = view.apply(lambda r: divergence_score(r, sel_juris), axis=1)

c1, c2, c3 = st.columns(3)
c1.metric("Dimensions compared", len(view))
c2.metric("Jurisdictions", len(sel_juris))
c3.metric("Fully divergent dimensions", int((view["divergence"] == 1.0).sum()),
          help="Every selected jurisdiction takes a different position.")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Side by side", "Divergence map", "By dimension", "Sources"]
)

# ---------------- tab 1 ----------------
with tab1:
    st.subheader("Side-by-side comparison")
    disp = view[["dimension", "category"] + sel_juris].copy()
    st.dataframe(
        disp, width='stretch', hide_index=True,
        column_config={
            "dimension": st.column_config.TextColumn("Dimension", width="medium"),
            "category": st.column_config.TextColumn("Category", width="small"),
            **{j: st.column_config.TextColumn(j, width="large") for j in sel_juris},
        },
    )
    st.caption("Scroll horizontally to read full cell text, or use the 'By dimension' tab.")

# ---------------- tab 2 ----------------
with tab2:
    st.subheader("Where do they actually disagree?")
    st.write(
        "Divergence of 1.0 means every selected jurisdiction takes a distinct "
        "position on that dimension. 0.0 means they all align. This is a text-"
        "distinctness measure, not a judgement about which approach is better."
    )
    plot_df = view[["dimension", "category", "divergence"]].sort_values("divergence")
    fig = px.bar(
        plot_df, x="divergence", y="dimension", color="category",
        orientation="h", height=max(400, 26 * len(plot_df)),
        labels={"divergence": "Divergence (0 = aligned, 1 = all differ)",
                "dimension": ""},
    )
    fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), legend_title_text="")
    st.plotly_chart(fig, width='stretch')

    high = plot_df[plot_df["divergence"] >= 0.99]["dimension"].tolist()
    if high:
        st.info(
            "**Fully divergent:** " + ", ".join(high) +
            ". These are the dimensions where an international standard would be "
            "hardest to negotiate, and where a comparative memo has the most to say."
        )

# ---------------- tab 3 ----------------
with tab3:
    st.subheader("Read one dimension in full")
    dim = st.selectbox("Dimension", view["dimension"].tolist())
    row = view[view["dimension"] == dim].iloc[0]
    st.markdown(f"**Category:** {row['category']}  |  "
                f"**Divergence:** {row['divergence']:.2f}")
    cols = st.columns(len(sel_juris))
    for col, j in zip(cols, sel_juris):
        with col:
            st.markdown(f"##### {j}")
            st.write(row[j])
    if isinstance(row.get("notes"), str) and row["notes"].strip():
        st.info(row["notes"])

# ---------------- tab 4 ----------------
with tab4:
    st.subheader("Sources")
    st.write(
        "Every claim in this comparison traces to a primary source below. "
        "AI governance moves quickly; check the date column and verify before citing."
    )
    st.dataframe(
        sources, width='stretch', hide_index=True,
        column_config={"url": st.column_config.LinkColumn("Link")},
    )
    st.caption(
        "Known limitation: the divergence score compares text distinctness, not "
        "substantive policy distance. Two jurisdictions could reach similar outcomes "
        "through differently-worded mechanisms and score as divergent. Treat it as a "
        "prompt for reading the rows, not as a finding."
    )

st.divider()
st.caption("Built by Rishikesh Nair · Data and methodology open in the repo")
