import re
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="FootLens Analytics", page_icon="⚽", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:radial-gradient(circle at 75% 0%,#17434a 0,#0a1424 38%,#070d17 78%);color:#edf3ff}
.block-container{max-width:1500px;padding-top:1.5rem;padding-bottom:3rem}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.03em}
.hero{padding:clamp(28px,5vw,68px);border:1px solid #ffffff24;border-radius:28px;background:linear-gradient(120deg,#0c182bf5,#0b4549ed);box-shadow:0 25px 80px #0005;margin:8px 0 24px}
.eyebrow{color:#6ef0bb;text-transform:uppercase;letter-spacing:.18em;font-size:.75rem;font-weight:700}
.hero h1{font-size:clamp(2.8rem,7vw,5.8rem);line-height:.98;margin:.55rem 0 1.1rem;color:#fff}
.hero h1 span{color:#6ef0bb}
.hero-copy{max-width:720px;color:#c1cde2;font-size:1.08rem;line-height:1.75}
.pills{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
.pill{border:1px solid #ffffff26;background:#ffffff0b;border-radius:999px;padding:9px 14px;color:#dce8fb;font-size:.85rem}
.feature{height:100%;min-height:160px;background:linear-gradient(145deg,#132137f5,#0c1727f5);border:1px solid #ffffff18;border-radius:18px;padding:22px}
.feature h3{color:#fff;font-size:1.1rem}.feature p{color:#aebbd2;font-size:.91rem;line-height:1.6}
.kpi{background:linear-gradient(145deg,#14233af5,#0b1626f5);border:1px solid #ffffff1c;border-radius:16px;padding:18px;min-height:100px}
.kpi-label{color:#9baecb;font-size:.78rem;font-weight:700}.kpi-value{color:#fff;font-size:1.7rem;font-weight:700;margin-top:7px}.kpi-note{color:#6ef0bb;font-size:.75rem}
.insight{background:#101e31e8;border:1px solid #ffffff18;border-left:3px solid #6ef0bb;border-radius:12px;padding:15px;margin-bottom:10px;color:#dbe6f7}
.footer{border-top:1px solid #ffffff1a;margin-top:35px;padding-top:18px;color:#8798b5;font-size:.82rem}
.stButton>button{border-radius:12px;border:1px solid #6ef0bb;background:#6ef0bb;color:#071321;font-weight:800;padding:.72rem 1.2rem}
.stButton>button:hover{background:#9af7d0;color:#071321}
div[data-testid="stMetric"]{background:#101e31;border:1px solid #ffffff1c;padding:14px;border-radius:14px}
div[data-testid="stTabs"] button{color:#c7d3e8}div[data-testid="stTabs"] button[aria-selected="true"]{color:#6ef0bb!important;border-bottom-color:#6ef0bb!important}
</style>
""", unsafe_allow_html=True)

ALIASES = {
    "player":["player","player_name","name","footballer","athlete"],
    "team":["team","club","club_name","team_name"],
    "result":["result","match_result","outcome","match_outcome"],
    "injury_start":["injury_start","injury_start_date","start_date","injury_date","date_of_injury"],
    "injury_end":["injury_end","injury_end_date","end_date","recovery_date","return_date"],
    "rating":["rating","performance_rating","player_rating","match_rating","average_rating"],
    "age":["age","player_age"],
    "injury_type":["injury_type","injury","injury_name","injury_category","type_of_injury"],
    "goals":["goals","goal","goals_scored"],
    "season":["season","year","season_year"],
    "match_date":["match_date","date","game_date","fixture_date"],
}
PREFERRED_FILES = ["football_data.csv","football_data.xlsx","football_data.xls","football_dataset.csv","football_dataset.xlsx","data.csv","data.xlsx"]

def norm(s):
    s = re.sub(r"[^a-z0-9]+", "_", str(s).strip().lower())
    return s.strip("_")

def find_dataset():
    for name in PREFERRED_FILES:
        if Path(name).is_file():
            return Path(name)
    candidates = sorted([p for p in Path(".").glob("*") if p.is_file() and p.suffix.lower() in [".csv",".xlsx",".xls"] and p.name != "requirements.txt"])
    return candidates[0] if candidates else None

@st.cache_data(show_spinner=False)
def read_file(name, mtime):
    p = Path(name)
    if p.suffix.lower() == ".csv":
        try: return pd.read_csv(p)
        except UnicodeDecodeError: return pd.read_csv(p, encoding="latin-1")
    return pd.read_excel(p)

def prepare(raw):
    df = raw.copy()
    df.columns = [norm(c) for c in df.columns]
    ren = {}
    for target, choices in ALIASES.items():
        if target not in df.columns:
            for c in choices:
                if norm(c) in df.columns:
                    ren[norm(c)] = target
                    break
    df = df.rename(columns=ren)
    for c, default in [("player","Unknown Player"),("team","Unknown Team"),("injury_type","Unspecified"),("result","Unknown")]:
        if c not in df: df[c] = default
        df[c] = df[c].fillna(default).astype(str).replace({"nan":default,"":default})
    for c in ["injury_start","injury_end","match_date"]:
        if c in df: df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in ["rating","age","goals"]:
        if c in df: df[c] = pd.to_numeric(df[c].astype(str).str.replace(",","",regex=False), errors="coerce")
    if "injury_start" in df and "injury_end" in df:
        df["injury_days"] = (df["injury_end"]-df["injury_start"]).dt.days.clip(lower=0)
    else: df["injury_days"] = np.nan
    if "injury_start" in df:
        df["injury_month"] = df["injury_start"].dt.month_name()
        df["injury_month_num"] = df["injury_start"].dt.month
        df["injury_year"] = df["injury_start"].dt.year
    else:
        df["injury_month"],df["injury_month_num"],df["injury_year"] = "Unknown",np.nan,np.nan
    if "season" not in df: df["season"] = df["injury_year"].fillna("Unknown").astype(str)
    result = df["result"].str.strip().str.lower()
    df["match_points"] = np.select([result.isin(["w","win","won","victory","3"]),result.isin(["d","draw","drawn","tie","1"]),result.isin(["l","loss","lost","defeat","0"])],[3,1,0],default=np.nan)
    duration = pd.to_numeric(df["injury_days"],errors="coerce").fillna(0).clip(lower=0)
    ref = max(float(duration.quantile(.95)) if len(duration) else 1,1)
    duration_part = (duration/ref).clip(0,1)
    if "rating" in df and df["rating"].notna().any():
        avg = df["rating"].mean()
        rating_part = ((avg-df["rating"].fillna(avg))/max(abs(avg),1)).clip(-1,1)
        rating_part = (rating_part+1)/2
    else: rating_part = pd.Series(.5,index=df.index)
    df["injury_impact_index"] = ((.6*duration_part+.4*rating_part)*100).round(1)
    return df

def plot_style(fig, height=400):
    fig.update_layout(height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#d8e4f5",family="DM Sans"),title_font=dict(color="#f4f7ff",size=17),margin=dict(l=15,r=15,t=60,b=15),legend=dict(bgcolor="rgba(0,0,0,0)"),xaxis=dict(gridcolor="#ffffff14"),yaxis=dict(gridcolor="#ffffff14"))
    return fig

def section(label,title,sub=None):
    st.markdown(f'<div class="eyebrow" style="margin:20px 0 8px">{label}</div><h2 style="margin-top:0;color:#f4f7ff">{title}</h2>',unsafe_allow_html=True)
    if sub: st.markdown(f'<p style="color:#a6b4d0;margin-top:-6px">{sub}</p>',unsafe_allow_html=True)

def landing(name, df, columns):
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">Football intelligence · Data-driven decisions</div>
      <h1>FOOTLENS<br><span>ANALYTICS.</span></h1>
      <p class="hero-copy">A smarter view of the game. Explore player injuries, recovery patterns and team performance through an interactive analytics experience built to turn raw football data into meaningful insights.</p>
      <div class="pills"><span class="pill">⚽ Injury intelligence</span><span class="pill">📈 Performance analytics</span><span class="pill">🧠 Decision support</span></div>
    </div>""",unsafe_allow_html=True)
    a,b=st.columns([1.1,1],gap="large")
    with a:
        section("THE PLATFORM","See beyond the scoreline.","FootLens brings injury records and performance information together in one clear workspace, helping users explore patterns that may otherwise be difficult to spot.")
        if st.button("ENTER DASHBOARD  →",use_container_width=True):
            st.session_state["entered"] = True
            st.rerun()
        st.caption("Interactive analytics · Filterable charts · Downloadable results")
    with b:
        st.markdown("""<div class="feature" style="min-height:100%">
        <div class="eyebrow">Your match-day intelligence hub</div><div style="font-size:3.2rem;margin:20px 0">⚽ 📊</div>
        <h3 style="font-size:1.5rem">From raw data to clearer decisions.</h3>
        <p>Monitor injury volume, compare clubs, examine recovery durations and explore player ratings using interactive visualisations.</p>
        <div class="pills"><span class="pill">01 Discover patterns</span><span class="pill">02 Compare teams</span><span class="pill">03 Track recovery</span><span class="pill">04 Export findings</span></div></div>""",unsafe_allow_html=True)
    st.markdown('<div class="eyebrow" style="margin:28px 0 12px">BUILT FOR EXPLORATION</div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for col,icon,title,desc in zip(cols,["🩹","📈","🏟️","🏆"],["Injury intelligence","Performance trends","Team comparison","Player insights"],["Explore injury types, duration and monthly patterns.","Review ratings and available match-result information.","Compare club injury burden and affected-player counts.","Explore player summaries and performance peaks."]):
        with col: st.markdown(f'<div class="feature"><div style="font-size:1.7rem">{icon}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown(f'<div class="footer">DATA SOURCE READY · <b style="color:#6ef0bb">{name}</b> · {len(df):,} records · {columns} columns<br>FootLens Analytics | Artificial Intelligence · Interactive Football Analytics</div>',unsafe_allow_html=True)

path=find_dataset()
if path is None:
    st.markdown('<div class="hero"><div class="eyebrow">Football intelligence</div><h1>FOOTLENS<br><span>ANALYTICS.</span></h1><p class="hero-copy">Your interactive football injury and performance dashboard.</p></div>',unsafe_allow_html=True)
    st.error("Dataset not found. Upload your CSV or Excel dataset to the same GitHub repository as app.py.")
    st.markdown("Recommended filename: `football_data.csv`")
    st.code("FootLens-Analytics/\\n├── app.py\\n├── football_data.csv\\n├── requirements.txt\\n└── README.md")
    st.stop()
try:
    raw=read_file(str(path),path.stat().st_mtime)
    df=prepare(raw)
except Exception as e:
    st.error(f"Could not load {path.name}: {e}")
    st.stop()
if df.empty:
    st.error("The dataset contains no records.")
    st.stop()

if "entered" not in st.session_state: st.session_state["entered"]=False
if not st.session_state["entered"]:
    landing(path.name,df,len(raw.columns))
    st.stop()

with st.sidebar:
    st.markdown("## ⚽ FootLens")
    st.caption("ANALYTICS WORKSPACE")
    if st.button("← Back to Home",use_container_width=True):
        st.session_state["entered"]=False
        st.rerun()
    st.divider()
    teams=st.multiselect("Teams / clubs",sorted(df["team"].unique()),default=sorted(df["team"].unique()))
    players=st.multiselect("Players",sorted(df["player"].unique()),default=sorted(df["player"].unique()))
    injuries=st.multiselect("Injury types",sorted(df["injury_type"].unique()),default=sorted(df["injury_type"].unique()))
    filtered=df[df["team"].isin(teams)&df["player"].isin(players)&df["injury_type"].isin(injuries)].copy()
    if "injury_start" in filtered and filtered["injury_start"].notna().any():
        low,high=filtered["injury_start"].min().date(),filtered["injury_start"].max().date()
        dates=st.date_input("Injury date range",value=(low,high),min_value=low,max_value=high)
        if isinstance(dates,(tuple,list)) and len(dates)==2:
            filtered=filtered[filtered["injury_start"].dt.date.between(dates[0],dates[1])]
    st.divider()
    st.caption(f"Dataset: {path.name}")

section("FOOTBALL INTELLIGENCE","Executive overview","A live summary of the selected records. Findings depend on the quality and coverage of the supplied dataset.")
if filtered.empty:
    st.warning("No records match these filters. Change one or more filters in the sidebar.")
    st.stop()
kpis=st.columns(5)
metrics=[("INJURY RECORDS",f"{len(filtered):,}","Filtered records"),("PLAYERS",f"{filtered.player.nunique():,}","Unique players"),("CLUBS",f"{filtered.team.nunique():,}","Unique teams"),("AVG. RECOVERY",f"{filtered.injury_days.mean():.1f} days" if filtered.injury_days.notna().any() else "N/A","Where dates are available"),("AVG. IMPACT INDEX",f"{filtered.injury_impact_index.mean():.1f}" if filtered.injury_impact_index.notna().any() else "N/A","Project-defined measure")]
for col,(label,value,note) in zip(kpis,metrics):
    with col: st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',unsafe_allow_html=True)

section("QUICK READ","Signals from the selected data")
insights=[]
if filtered.injury_days.notna().any():
    r=filtered.loc[filtered.injury_days.idxmax()]; insights.append(f"Longest recorded injury: **{r.player}** — {r.injury_days:.0f} days.")
tc=filtered.team.value_counts(); ic=filtered.injury_type.value_counts()
if len(tc): insights.append(f"Highest injury-record count: **{tc.index[0]}** ({tc.iloc[0]} records).")
if len(ic): insights.append(f"Most frequent injury category: **{ic.index[0]}** ({ic.iloc[0]} records).")
if "rating" in filtered and filtered.rating.notna().any(): insights.append(f"Mean recorded performance rating: **{filtered.rating.mean():.2f}**.")
if filtered.match_points.notna().any(): insights.append(f"Mean match points in available result records: **{filtered.match_points.mean():.2f}**.")
for start in range(0,len(insights),3):
    cols=st.columns(3)
    for col,txt in zip(cols,insights[start:start+3]):
        with col: st.markdown(f'<div class="insight">✦ {txt}</div>',unsafe_allow_html=True)

tabs=st.tabs(["📈 Performance","🩹 Injury intelligence","🏆 Players & comebacks","🏟️ Team analysis","📋 Data & methodology"])
with tabs[0]:
    section("PERFORMANCE LAB","Performance impact analysis")
    c1,c2=st.columns(2)
    with c1:
        s=filtered.groupby("injury_type",as_index=False).agg(mean_impact=("injury_impact_index","mean"),cases=("injury_type","size")).sort_values("mean_impact",ascending=False).head(12)
        f=px.bar(s.sort_values("mean_impact"),x="mean_impact",y="injury_type",orientation="h",text="mean_impact",hover_data=["cases"],title="Injury categories by average impact index",labels={"mean_impact":"Average impact index","injury_type":"Injury type"})
        f.update_traces(texttemplate="%{text:.1f}",textposition="outside",marker_color="#4ee0ad")
        st.plotly_chart(plot_style(f,430),use_container_width=True)
    with c2:
        if "age" in filtered and filtered.age.notna().any():
            f=px.scatter(filtered.dropna(subset=["age"]),x="age",y="injury_impact_index",color="team",hover_name="player",hover_data=["injury_type","injury_days"],title="Player age vs injury impact",labels={"age":"Age","injury_impact_index":"Impact index"})
            st.plotly_chart(plot_style(f,430),use_container_width=True)
        else: st.info("Age data is not available.")
    if "rating" in filtered and filtered.rating.notna().any() and "match_date" in filtered and filtered.match_date.notna().any():
        f=px.line(filtered.dropna(subset=["rating","match_date"]).sort_values("match_date"),x="match_date",y="rating",color="player",markers=True,hover_data=["team","injury_type"],title="Recorded player ratings over time")
        st.plotly_chart(plot_style(f,430),use_container_width=True)
    else: st.info("Include performance ratings and a Match Date column to show a player-rating timeline.")

with tabs[1]:
    section("INJURY MONITOR","Patterns, duration and concentration")
    c1,c2=st.columns(2)
    with c1:
        m=filtered.dropna(subset=["injury_month_num"]).groupby(["injury_month_num","injury_month"]).size().reset_index(name="cases").sort_values("injury_month_num")
        if len(m):
            f=px.line(m,x="injury_month",y="cases",markers=True,title="Monthly injury-record trend",labels={"injury_month":"Month","cases":"Records"}); f.update_traces(line_color="#4ee0ad",marker_size=8); st.plotly_chart(plot_style(f),use_container_width=True)
        else: st.info("Injury start dates are needed for monthly trends.")
    with c2:
        heat=pd.crosstab(filtered.team,filtered.injury_month)
        order=["January","February","March","April","May","June","July","August","September","October","November","December"]
        months=[m for m in order if m in heat.columns]
        if months:
            f=px.imshow(heat[months],aspect="auto",text_auto=True,title="Injury records by club and month",labels={"x":"Month","y":"Club","color":"Records"},color_continuous_scale=["#11243b","#1b8c76","#80f0c2"]); st.plotly_chart(plot_style(f),use_container_width=True)
        else: st.info("Month information is unavailable.")
    if filtered.injury_days.notna().any():
        c1,c2=st.columns(2)
        with c1:
            f=px.histogram(filtered.dropna(subset=["injury_days"]),x="injury_days",nbins=20,marginal="box",title="Recovery duration distribution",labels={"injury_days":"Duration (days)"}); f.update_traces(marker_color="#4ee0ad"); st.plotly_chart(plot_style(f),use_container_width=True)
        with c2:
            long=filtered.dropna(subset=["injury_days"]).nlargest(10,"injury_days").sort_values("injury_days")
            f=px.bar(long,x="injury_days",y="player",color="team",orientation="h",hover_data=["injury_type"],title="10 longest recorded injury durations",labels={"injury_days":"Days","player":"Player"}); st.plotly_chart(plot_style(f),use_container_width=True)
    else: st.info("Both injury start and end dates are required to calculate duration.")

with tabs[2]:
    section("PLAYER SPOTLIGHT","Player summaries and performance peaks")
    if "rating" in filtered and filtered.rating.notna().any():
        ps=filtered.groupby("player",as_index=False).agg(records=("player","size"),avg_rating=("rating","mean"),best_rating=("rating","max"),avg_impact=("injury_impact_index","mean"),avg_recovery_days=("injury_days","mean"))
        ps["peak_above_average_pct"]=((ps.best_rating-ps.avg_rating)/ps.avg_rating.replace(0,np.nan)*100).replace([np.inf,-np.inf],np.nan)
        top=ps.dropna(subset=["peak_above_average_pct"]).nlargest(10,"peak_above_average_pct").sort_values("peak_above_average_pct")
        if len(top):
            f=px.bar(top,x="peak_above_average_pct",y="player",orientation="h",text="peak_above_average_pct",title="Performance-peak leaderboard (simplified score)",labels={"peak_above_average_pct":"Peak above average (%)"}); f.update_traces(texttemplate="%{text:.1f}%",textposition="outside",marker_color="#4ee0ad"); st.plotly_chart(plot_style(f,430),use_container_width=True)
        st.markdown("#### Player summary table"); st.dataframe(ps.round(2).sort_values("avg_impact",ascending=False),use_container_width=True,hide_index=True)
        st.caption("This simplified score compares maximum and average recorded ratings. It does not prove recovery or medical comeback.")
    else: st.info("A performance-rating column is needed for player summaries.")

with tabs[3]:
    section("CLUB INTELLIGENCE","Team-level comparison")
    ts=filtered.groupby("team",as_index=False).agg(injury_records=("team","size"),players_affected=("player","nunique"),avg_recovery_days=("injury_days","mean"),avg_impact=("injury_impact_index","mean")).sort_values("injury_records",ascending=False)
    c1,c2=st.columns(2)
    with c1:
        f=px.bar(ts.sort_values("injury_records"),x="injury_records",y="team",orientation="h",text="injury_records",title="Injury records by club",labels={"injury_records":"Records","team":"Club"}); f.update_traces(marker_color="#4ee0ad"); st.plotly_chart(plot_style(f,420),use_container_width=True)
    with c2:
        f=px.scatter(ts,x="injury_records",y="avg_impact",size="players_affected",color="team",hover_data=["avg_recovery_days"],title="Club injury volume vs average impact",labels={"injury_records":"Injury records","avg_impact":"Average impact index"}); st.plotly_chart(plot_style(f,420),use_container_width=True)
    st.dataframe(ts.round(2),use_container_width=True,hide_index=True)
    rc=filtered.result.astype(str).value_counts().reset_index(); rc.columns=["result","records"]
    f=px.pie(rc,names="result",values="records",hole=.55,title="Recorded match-result distribution",color_discrete_sequence=["#4ee0ad","#4e83e0","#f4bd61","#bd8cff"]); st.plotly_chart(plot_style(f,390),use_container_width=True)

with tabs[4]:
    section("DATA WORKSPACE","Data quality, methods and export")
    a,b,c=st.columns(3); a.metric("Original records",f"{len(raw):,}"); b.metric("Filtered records",f"{len(filtered):,}"); c.metric("Dataset columns",len(raw.columns))
    st.markdown("#### Cleaning and feature engineering")
    for item in ["Column names are normalised and common aliases are recognised.","Available injury and match dates are converted to datetime values.","Age, goals and performance ratings are converted to numeric values where available.","Missing text values are replaced with readable placeholders.","Injury duration is calculated when start and end dates exist.","Month and year features are derived from injury dates.","A project-defined Injury Impact Index is calculated for exploratory comparison.","Recognisable win/draw/loss results are mapped to 3/1/0 match points."]:
        st.markdown("- "+item)
    st.markdown("#### Five business questions")
    for i,q in enumerate(["Which injury categories have the highest average project-defined impact index?","What win/draw/loss pattern appears in the available match-result records?","How do recorded player ratings vary over time?","Are there months or clubs with higher concentrations of recorded injuries?","Which clubs and players show the largest recorded injury burden or performance peaks?"],1): st.markdown(f"**Q{i}.** {q}")
    st.markdown("#### Data preview"); st.dataframe(filtered.head(200),use_container_width=True,hide_index=True)
    st.download_button("⬇️ Download filtered analysis as CSV",data=filtered.to_csv(index=False).encode("utf-8"),file_name="footlens_filtered_data.csv",mime="text/csv")
    st.info("The Injury Impact Index is a project-defined exploratory measure, not a medical score. Patterns or associations in this dataset do not establish causation.")

st.markdown('<div class="footer">FOOTLENS ANALYTICS · Artificial Intelligence · Football injury & performance exploration<br>Use findings as exploratory analysis and verify data definitions before making decisions.</div>',unsafe_allow_html=True)
