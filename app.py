import io
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="ECD Monitoring Dashboard", layout="wide")
st.title("ECD Monitoring Dashboard")
st.caption("Upload an ECCE monitoring Excel file to explore access, quality, inclusion, infrastructure, health, nutrition, governance, and data quality.")
# Cache data loading for better performance
@st.cache_data
def load_data():
    file_path = "ECD_Termly_monitoring_tool_-_Focus_Districts_-_all_versions_-_labels_-_2026-03-10-05-13-40.xlsx"
    try:
        df = pd.read_excel(file_path, sheet_name="Sheet1")
    except FileNotFoundError:
        st.error(f"Excel file not found: {file_path}\nMake sure the file is in the same folder as app.py")
        st.stop()
    except Exception as e:
        st.error(f"Error reading Excel: {e}")
        st.stop()
def num(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)

def find_col(df, candidates, required=True):
    for c in candidates:
        if c in df.columns:
            return c
    if required:
        st.error("A required column is missing.")
        st.write("Checked names:", candidates)
        st.write("Available columns:", df.columns.tolist())
        st.stop()
    return None

def yes_flag(df, candidates):
    col = find_col(df, candidates, required=False)
    if col is None:
        return pd.Series([np.nan] * len(df), index=df.index), None
    return df[col].astype(str).str.strip().str.lower().eq("yes").astype(float), col

@st.cache_data
def load_data(file_bytes, filename):
    if filename.lower().endswith(".csv"):
        return pd.read_csv(io.BytesIO(file_bytes))
    return pd.read_excel(io.BytesIO(file_bytes))

uploaded = st.file_uploader("Upload Excel or CSV", type=["xlsx", "xls", "csv"])
if not uploaded:
    st.info("Upload your monitoring file to begin.")
    st.stop()

df = load_data(uploaded.getvalue(), uploaded.name).copy()

district_col = find_col(df, ["District"])
subcounty_col = find_col(df, ["Sub County", "Subcounty", "Sub-county"])
parish_col = find_col(df, ["Parish"])
centre_col = find_col(df, ["ECD Centre", "ECCE Centre", "Centre Name"])

lat_col = find_col(df, ["_Record the ECD Centre Location_latitude", "latitude", "Latitude"], required=False)
lon_col = find_col(df, ["_Record the ECD Centre Location_longitude", "longitude", "Longitude"], required=False)

lic_col = find_col(df, [
    "What is the licensing status of this ECCE centre",
    "Is the licensing status of this ECCE centre",
    "Licensing status",
])

boys_baby = find_col(df, ["Boys_Total_Baby"])
boys_mid = find_col(df, ["Boys_Total_Mid"])
boys_top = find_col(df, ["Boys_Total_Top"])
boys_day = find_col(df, ["Boys_Total_Day"])

girls_baby = find_col(df, ["Girls_Total_Baby"])
girls_mid = find_col(df, ["Girls_Total_Mid"])
girls_top = find_col(df, ["Girls_Total_Top"])
girls_day = find_col(df, ["Girls_Total_Day"])

att_cols = [
    find_col(df, ["Number of learners attending in baby class - Boys"]),
    find_col(df, ["Number of learners attending in baby class - Girls"]),
    find_col(df, ["Number of learners attending in Middle class - Boys"]),
    find_col(df, ["Number of learners attending in Middle class - Girls"]),
    find_col(df, ["Number of learners attending in Top class - Boys"]),
    find_col(df, ["Number of learners attending in Top class - Girls"]),
    find_col(df, ["Number of learners attending in the day centre - Boys"]),
    find_col(df, ["Number of learners attending in the day center - Girls", "Number of learners attending in the day centre - Girls"]),
]

male_cg = find_col(df, ["Number of Caregivers  Males", "Number of Caregivers Males"])
female_cg = find_col(df, ["Number of Caregivers - Females", "Number of Caregivers Females"])

lesson_plan_flag, _ = yes_flag(df, [
    "Are lesson plans available for all caregivers?",
    "Does each caregiver have lesson plans?",
    "Lesson plans available",
])

framework_flag, _ = yes_flag(df, [
    "Does the ECCE centre use the learning framework?",
    "Is the learning framework available and being used?",
    "Learning framework available",
])

register_flag, _ = yes_flag(df, [
    "Does the ECCE centre have updated attendance register?",
    "Updated attendance register",
])

logbook_flag, _ = yes_flag(df, [
    "Does the ECCE centre have updated log book?",
    "Updated log book",
])

inventory_flag, _ = yes_flag(df, [
    "Does the ECCE centre have updated inventory book?",
    "Updated inventory book",
])

cmc_flag, _ = yes_flag(df, ["Does the ECCE centre have Centre Management Committee (CMC)?"])
meal_flag, _ = yes_flag(df, ["Does the ECCE provide hot midday meals to learners?"])
lang_flag, _ = yes_flag(df, ["Does the ECCE centre teach learners using local languages?"])
aff_flag, _ = yes_flag(df, ["Is the ECCE centre attached or affiliated to a Primary School"])
sne_flag, _ = yes_flag(df, ["Does the ECCE centre have children with Special Needs (SNEs)?"])
deworm_flag, _ = yes_flag(df, [
    "Were children dewormed in this term?",
    "Does the ECCE centre provide deworming services?",
    "Deworming service provided"
])

community_flag, _ = yes_flag(df, [
    "Is the community involved in supporting the ECCE centre?",
    "Community involvement",
])

water_col = find_col(df, [
    "Main source of drinking water for Children in the ECCE centre",
    "Main source of drinking water"
], required=False)

founder_col = find_col(df, ["Who founded this ECCE centre?"], required=False)

infra_map = {
    "Permanent Classrooms": ["Where does the ECCE hold their daily lessons?/Permanent Classrooms"],
    "Temporary Classrooms": ["Where does the ECCE hold their daily lessons?/Temporary Classrooms"],
    "Under Tree Shade": ["Where does the ECCE hold their daily lessons?/Under Tree Shade"],
    "Open Space": ["Where does the ECCE hold their daily lessons?/Open Space"],
}
infra_cols = {}
for label, candidates in infra_map.items():
    c = find_col(df, candidates, required=False)
    if c:
        infra_cols[label] = c

handwash_flag, _ = yes_flag(df, [
    "Are there handwashing facilities at the ECCE centre?",
    "Handwashing facilities available",
])

toilet_flag, _ = yes_flag(df, [
    "Does the ECCE centre have latrines/toilets for children?",
    "Toilets available for children",
])

accessible_flag, _ = yes_flag(df, [
    "Are facilities accessible for children with special needs?",
    "Accessible facilities for SNEs",
])

df["Total_Boys_Enrolled"] = num(df[boys_baby]) + num(df[boys_mid]) + num(df[boys_top]) + num(df[boys_day])
df["Total_Girls_Enrolled"] = num(df[girls_baby]) + num(df[girls_mid]) + num(df[girls_top]) + num(df[girls_day])
df["Total_Enrollment"] = df["Total_Boys_Enrolled"] + df["Total_Girls_Enrolled"]
df["Total_Attendance"] = df[att_cols].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1)
df["Caregivers_Total"] = num(df[male_cg]) + num(df[female_cg])
df["Attendance_Rate"] = np.where(df["Total_Enrollment"] > 0, df["Total_Attendance"] / df["Total_Enrollment"], np.nan)
df["Learners_per_Caregiver"] = np.where(df["Caregivers_Total"] > 0, df["Total_Enrollment"] / df["Caregivers_Total"], np.nan)
df["Licensed_Flag"] = df[lic_col].astype(str).str.strip().str.lower().eq("licensed").astype(float)
df["Registered_or_Licensed_Flag"] = df[lic_col].astype(str).str.strip().str.lower().isin(["licensed", "registered"]).astype(float)

for name, series in {
    "CMC_Flag": cmc_flag,
    "Hot_Meal_Flag": meal_flag,
    "Local_Language_Flag": lang_flag,
    "Affiliated_Flag": aff_flag,
    "SNE_Flag": sne_flag,
    "Lesson_Plan_Flag": lesson_plan_flag,
    "Framework_Flag": framework_flag,
    "Register_Flag": register_flag,
    "Logbook_Flag": logbook_flag,
    "Inventory_Flag": inventory_flag,
    "Deworm_Flag": deworm_flag,
    "Community_Flag": community_flag,
    "Handwash_Flag": handwash_flag,
    "Toilet_Flag": toilet_flag,
    "Accessible_Flag": accessible_flag,
}.items():
    df[name] = series

orphan_cols = [c for c in [
    "Number of Orphans in baby class  - Boys",
    "Number of Orphans in baby class - Girls",
    "Number of Orphans in  Middle class - Boys",
    "Number of Orphans in Middle class -  Girls",
    "Number of Orphans in Top class -  Boys",
    "Number of Orphans in Top class -  Girls",
    "Number of Orphans in the day care centre -  Boys",
    "Number of Orphans in the day care centre -  Girls",
] if c in df.columns]
df["Total_Orphans"] = df[orphan_cols].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1) if orphan_cols else 0

refugee_cols = [c for c in df.columns if "refugee" in c.lower()]
df["Refugee_Count"] = df[refugee_cols].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1) if refugee_cols else 0

districts = sorted([x for x in df[district_col].dropna().unique().tolist()])
with st.sidebar:
    st.header("Filters")
    selected_districts = st.multiselect("District", districts, default=districts)
    subs = sorted(df[df[district_col].isin(selected_districts)][subcounty_col].dropna().unique().tolist()) if selected_districts else []
    selected_subs = st.multiselect("Sub County", subs, default=subs)
    include_zero_attendance = st.checkbox("Include zero-attendance centres", value=True)

f = df.copy()
if selected_districts:
    f = f[f[district_col].isin(selected_districts)]
if selected_subs:
    f = f[f[subcounty_col].isin(selected_subs)]
if not include_zero_attendance:
    f = f[f["Total_Attendance"] > 0]

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

def pct(series):
    val = pd.to_numeric(series, errors="coerce").dropna()
    return float(val.mean()) if len(val) else np.nan

centres = len(f)
enrollment = int(f["Total_Enrollment"].sum())
attendance = int(f["Total_Attendance"].sum())
caregivers = int(f["Caregivers_Total"].sum())
attendance_rate = attendance / enrollment if enrollment else np.nan
licensed_pct = pct(f["Licensed_Flag"])

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Centres", f"{centres:,}")
c2.metric("Enrollment", f"{enrollment:,}")
c3.metric("Attendance", f"{attendance:,}")
c4.metric("Attendance Rate", f"{attendance_rate:.1%}" if pd.notna(attendance_rate) else "—")
c5.metric("Caregivers", f"{caregivers:,}")
c6.metric("Licensed %", f"{licensed_pct:.1%}" if pd.notna(licensed_pct) else "—")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Executive Overview",
    "Access & Scale",
    "Quality & Readiness",
    "Inclusion",
    "Infrastructure & WASH",
    "Health, Governance & Data Quality"
])

with tab1:
    st.subheader("Priority insights")
    insights = []
    if pd.notna(licensed_pct):
        insights.append(f"Licensed centres: {licensed_pct:.1%}")
    if pd.notna(pct(f['Affiliated_Flag'])):
        insights.append(f"Affiliated to primary schools: {pct(f['Affiliated_Flag']):.1%}")
    if pd.notna(pct(f['Local_Language_Flag'])):
        insights.append(f"Teach using local languages: {pct(f['Local_Language_Flag']):.1%}")
    if pd.notna(pct(f['CMC_Flag'])):
        insights.append(f"Centres with CMC: {pct(f['CMC_Flag']):.1%}")
    if (f["Total_Attendance"] == 0).sum() > 0:
        insights.append(f"Centres with zero attendance recorded: {(f['Total_Attendance'] == 0).sum():,}")
    for item in insights:
        st.write("•", item)

    e1, e2 = st.columns(2)

    lic_df = f[lic_col].fillna("Unknown").value_counts().reset_index()
    lic_df.columns = ["Licensing Status", "Centres"]
    e1.plotly_chart(px.bar(lic_df, x="Licensing Status", y="Centres", title="Licensing Status"), use_container_width=True)

    class_df = pd.DataFrame({
        "Class": ["Baby", "Middle", "Top", "Day Care"],
        "Boys": [int(num(f[boys_baby]).sum()), int(num(f[boys_mid]).sum()), int(num(f[boys_top]).sum()), int(num(f[boys_day]).sum())],
        "Girls": [int(num(f[girls_baby]).sum()), int(num(f[girls_mid]).sum()), int(num(f[girls_top]).sum()), int(num(f[girls_day]).sum())],
    })
    class_long = class_df.melt(id_vars="Class", var_name="Sex", value_name="Enrollment")
    e2.plotly_chart(px.bar(class_long, x="Class", y="Enrollment", color="Sex", barmode="stack", title="Boys vs Girls by Class"), use_container_width=True)

    kpi_sub = (
        f.groupby(subcounty_col)
        .agg(
            Centres=(centre_col, "count"),
            Enrollment=("Total_Enrollment", "sum"),
            Attendance=("Total_Attendance", "sum"),
            Caregivers=("Caregivers_Total", "sum"),
            Licensed=("Licensed_Flag", "mean"),
            CMC=("CMC_Flag", "mean"),
        )
        .reset_index()
    )
    kpi_sub["Attendance Rate"] = np.where(kpi_sub["Enrollment"] > 0, kpi_sub["Attendance"] / kpi_sub["Enrollment"], np.nan)
    kpi_sub["Learners per Caregiver"] = np.where(kpi_sub["Caregivers"] > 0, kpi_sub["Enrollment"] / kpi_sub["Caregivers"], np.nan)
    heat = kpi_sub[[subcounty_col, "Enrollment", "Attendance Rate", "Learners per Caregiver", "Licensed", "CMC"]].copy()
    heat = heat.set_index(subcounty_col)
    heat.columns = ["Enrollment", "Attendance Rate", "Learners/Caregiver", "Licensed %", "CMC %"]

    if len(heat):
        heat_norm = heat.copy()
        for col in heat_norm.columns:
            s = pd.to_numeric(heat_norm[col], errors="coerce")
            if s.max() != s.min():
                heat_norm[col] = (s - s.min()) / (s.max() - s.min())
            else:
                heat_norm[col] = 0.5
        fig_heat = px.imshow(
            heat_norm.T,
            aspect="auto",
            labels=dict(x="Sub County", y="KPI", color="Relative Value"),
            title="Sub-county vs Key KPIs Heatmap"
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        st.dataframe(heat.reset_index(), use_container_width=True)

with tab2:
    a1, a2 = st.columns(2)
    sub_enr = f.groupby(subcounty_col, dropna=False)["Total_Enrollment"].sum().sort_values(ascending=False).reset_index()
    a1.plotly_chart(px.bar(sub_enr, x=subcounty_col, y="Total_Enrollment", title="Enrollment by Sub County"), use_container_width=True)

    sub_att = (
        f.groupby(subcounty_col, dropna=False)
        .agg(Enrollment=("Total_Enrollment", "sum"), Attendance=("Total_Attendance", "sum"))
        .reset_index()
    )
    sub_att["Attendance Rate"] = np.where(sub_att["Enrollment"] > 0, sub_att["Attendance"] / sub_att["Enrollment"], np.nan)
    fig_att = px.bar(sub_att.sort_values("Attendance Rate", ascending=False), x=subcounty_col, y="Attendance Rate", title="Attendance Rate by Sub County")
    fig_att.update_yaxes(tickformat=".0%")
    a2.plotly_chart(fig_att, use_container_width=True)

    a3, a4 = st.columns(2)
    caregiver_df = (
        f.groupby(subcounty_col, dropna=False)
        .agg(Enrollment=("Total_Enrollment", "sum"), Caregivers=("Caregivers_Total", "sum"))
        .reset_index()
    )
    caregiver_df["Learners per Caregiver"] = np.where(caregiver_df["Caregivers"] > 0, caregiver_df["Enrollment"] / caregiver_df["Caregivers"], np.nan)
    a3.plotly_chart(px.bar(caregiver_df.sort_values("Learners per Caregiver", ascending=False), x=subcounty_col, y="Learners per Caregiver", title="Learner-to-Caregiver Ratio by Sub County"), use_container_width=True)

    if lat_col and lon_col:
        map_df = f[[centre_col, district_col, subcounty_col, parish_col, "Total_Enrollment", lat_col, lon_col]].copy()
        map_df = map_df.dropna(subset=[lat_col, lon_col])
        if len(map_df):
            fig_map = px.scatter_mapbox(
                map_df,
                lat=lat_col,
                lon=lon_col,
                hover_name=centre_col,
                hover_data={district_col: True, subcounty_col: True, parish_col: True, "Total_Enrollment": True},
                size="Total_Enrollment",
                zoom=8,
                title="Map of Centres"
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=50, b=0))
            a4.plotly_chart(fig_map, use_container_width=True)
        else:
            a4.info("No GPS coordinates available after filtering.")
    else:
        a4.info("GPS fields not found in this file.")

with tab3:
    q1, q2 = st.columns(2)

    quality_df = pd.DataFrame({
        "Indicator": ["Licensed", "Registered or Licensed", "Lesson Plans", "Learning Framework", "Updated Attendance Register", "Updated Log Book", "Updated Inventory Book"],
        "Percent": [
            pct(f["Licensed_Flag"]),
            pct(f["Registered_or_Licensed_Flag"]),
            pct(f["Lesson_Plan_Flag"]),
            pct(f["Framework_Flag"]),
            pct(f["Register_Flag"]),
            pct(f["Logbook_Flag"]),
            pct(f["Inventory_Flag"]),
        ]
    }).dropna()
    fig_quality = px.bar(quality_df, x="Indicator", y="Percent", title="Quality and Readiness Indicators")
    fig_quality.update_yaxes(tickformat=".0%")
    q1.plotly_chart(fig_quality, use_container_width=True)

    if founder_col:
        founder_df = f[founder_col].fillna("Unknown").value_counts().reset_index()
        founder_df.columns = ["Founder", "Centres"]
        q2.plotly_chart(px.bar(founder_df, x="Founder", y="Centres", title="Founder / Ownership"), use_container_width=True)

    sub_quality = (
        f.groupby(subcounty_col)
        .agg(
            Licensed=("Licensed_Flag", "mean"),
            Lesson_Plans=("Lesson_Plan_Flag", "mean"),
            Framework=("Framework_Flag", "mean"),
            Register=("Register_Flag", "mean"),
            Logbook=("Logbook_Flag", "mean"),
            Inventory=("Inventory_Flag", "mean"),
        )
        .reset_index()
    )
    st.dataframe(sub_quality, use_container_width=True)

with tab4:
    i1, i2 = st.columns(2)

    inclusion_df = pd.DataFrame({
        "Indicator": ["SNE Presence", "Local Language Teaching"],
        "Percent": [pct(f["SNE_Flag"]), pct(f["Local_Language_Flag"])]
    }).dropna()
    if len(inclusion_df):
        fig_inc = px.bar(inclusion_df, x="Indicator", y="Percent", title="Inclusion Indicators")
        fig_inc.update_yaxes(tickformat=".0%")
        i1.plotly_chart(fig_inc, use_container_width=True)

    totals_df = pd.DataFrame({
        "Metric": ["Orphans", "Refugees"],
        "Count": [int(f["Total_Orphans"].sum()), int(f["Refugee_Count"].sum())]
    })
    i2.plotly_chart(px.bar(totals_df, x="Metric", y="Count", title="Vulnerability Counts"), use_container_width=True)

    sub_inc = (
        f.groupby(subcounty_col)
        .agg(
            Centres=(centre_col, "count"),
            SNE_Presence=("SNE_Flag", "mean"),
            Local_Language=("Local_Language_Flag", "mean"),
            Orphans=("Total_Orphans", "sum"),
            Refugees=("Refugee_Count", "sum"),
        )
        .reset_index()
    )
    st.dataframe(sub_inc, use_container_width=True)

with tab5:
    w1, w2 = st.columns(2)

    if infra_cols:
        infra_df = pd.DataFrame({
            "Setting": list(infra_cols.keys()),
            "Centres": [int(pd.to_numeric(f[col], errors="coerce").fillna(0).sum()) for col in infra_cols.values()]
        })
        w1.plotly_chart(px.bar(infra_df, x="Setting", y="Centres", title="Permanent vs Temporary Classrooms"), use_container_width=True)
    else:
        w1.info("Infrastructure lesson-setting fields not found.")

    if water_col:
        water_df = f[water_col].fillna("Unknown").value_counts().reset_index()
        water_df.columns = ["Water Source", "Centres"]
        w2.plotly_chart(px.bar(water_df, x="Water Source", y="Centres", title="Water Sources"), use_container_width=True)
    else:
        w2.info("Water-source field not found.")

    wash_df = pd.DataFrame({
        "Indicator": ["Handwashing", "Toilets", "Accessible Facilities for SNEs"],
        "Percent": [pct(f["Handwash_Flag"]), pct(f["Toilet_Flag"]), pct(f["Accessible_Flag"])]
    }).dropna()
    if len(wash_df):
        fig_wash = px.bar(wash_df, x="Indicator", y="Percent", title="WASH and Accessibility Indicators")
        fig_wash.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_wash, use_container_width=True)

with tab6:
    h1, h2 = st.columns(2)

    gov_df = pd.DataFrame({
        "Indicator": ["Deworming", "Hot Meal Program", "CMC Availability", "Community Involvement", "Affiliated to Primary"],
        "Percent": [
            pct(f["Deworm_Flag"]),
            pct(f["Hot_Meal_Flag"]),
            pct(f["CMC_Flag"]),
            pct(f["Community_Flag"]),
            pct(f["Affiliated_Flag"]),
        ]
    }).dropna()
    fig_gov = px.bar(gov_df, x="Indicator", y="Percent", title="Health, Nutrition and Governance Indicators")
    fig_gov.update_yaxes(tickformat=".0%")
    h1.plotly_chart(fig_gov, use_container_width=True)

    dq = pd.DataFrame({
        "Check": [
            "Missing centre names",
            "Missing sub-county",
            "Missing parish",
            "Missing latitude",
            "Missing longitude",
            "Centres with zero enrollment",
            "Centres with zero attendance",
            "Centres with zero caregivers",
            "Duplicate centre/parish/sub-county rows",
            "Attendance greater than enrollment",
        ],
        "Count": [
            int(f[centre_col].isna().sum()),
            int(f[subcounty_col].isna().sum()),
            int(f[parish_col].isna().sum()),
            int(f[lat_col].isna().sum()) if lat_col else np.nan,
            int(f[lon_col].isna().sum()) if lon_col else np.nan,
            int((f["Total_Enrollment"] == 0).sum()),
            int((f["Total_Attendance"] == 0).sum()),
            int((f["Caregivers_Total"] == 0).sum()),
            int(f.duplicated(subset=[centre_col, parish_col, subcounty_col], keep=False).sum()),
            int((f["Total_Attendance"] > f["Total_Enrollment"]).sum()),
        ]
    })
    h2.dataframe(dq, use_container_width=True)

    st.subheader("Flagged records for review")
    dup_mask = f.duplicated(subset=[centre_col, parish_col, subcounty_col], keep=False)
    flagged = f.loc[
        (f["Total_Attendance"] == 0) | (f["Caregivers_Total"] == 0) | dup_mask,
        [c for c in [district_col, subcounty_col, parish_col, centre_col, "Total_Enrollment", "Total_Attendance", "Caregivers_Total", lic_col] if c in f.columns]
    ].copy()
    st.dataframe(flagged, use_container_width=True)

    st.download_button(
        "Download filtered records as CSV",
        data=f.to_csv(index=False).encode("utf-8"),
        file_name="ecd_filtered_records.csv",
        mime="text/csv",
    )

