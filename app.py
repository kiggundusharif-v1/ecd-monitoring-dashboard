import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------
st.set_page_config(page_title="Mubende ECD Monitoring Dashboard", layout="wide")
st.title("Mubende District ECD Centres Monitoring Dashboard")
st.caption("Data: ECD Termly Monitoring Tool – Mubende Focus Districts")


# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def clean_columns(df):
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    return df


def to_num(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)


def safe_col(df, col_name, default=None):
    if col_name in df.columns:
        return df[col_name]
    return pd.Series([default] * len(df), index=df.index)


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    file_path = "ECD_Termly_monitoring_tool_-_Focus_Districts_-_all_versions_-_labels_-_2026-03-10-05-13-40.xlsx"
    df = pd.read_excel(file_path, sheet_name="Sheet1")
    df = clean_columns(df)
    return df


df = load_data()

# ---------------------------------------------------
# IMPORTANT COLUMNS
# ---------------------------------------------------
district_col = "District"
subcounty_col = "Sub County"
parish_col = "Parish"
centre_col = "ECD Centre"
licensing_col = "What is the licensing status of this ECCE centre"
attached_col = "Is the ECCE centre attached or affiliated to a Primary School"

# attendance
attendance_cols = [
    "Number of learners attending in baby class - Boys",
    "Number of learners attending in baby class - Girls",
    "Number of learners attending in Middle class - Boys",
    "Number of learners attending in Middle class - Girls",
    "Number of learners attending in Top class - Boys",
    "Number of learners attending in Top class - Girls",
    "Number of learners attending in the day centre - Boys",
    "Number of learners attending in the day center - Girls",
]

# enrollment
enrollment_cols = [
    "Boys_Total_Baby", "Girls_Total_Baby",
    "Boys_Total_Mid", "Girls_Total_Mid",
    "Boys_Total_Top", "Girls_Total_Top",
    "Boys_Total_DayCare", "Girls_Total_DayCare"
]

# caregivers
caregiver_cols = [
    "Number of Caregivers  Males",
    "Number of Caregivers - Females",
]

trained_cols = [
    "Number of trained caregivers with Diploma in Early Childhood Education - Males",
    "Number of trained caregivers with Diploma in Early Childhood Education - Females",
    "Number of trained caregivers with Certificate in Nursery Teaching - Males",
    "Number of trained caregivers with Certificate in Nursery Teaching - Females",
    "Number of Qualified caregivers with Bachelor’s degree and above - Males",
    "Number of Qualified caregivers with Bachelor’s degree and above - Females",
    "Number of Qualified caregivers with Diploma in Primary Education (Grade V) - Males",
    "Number of Qualified caregivers with Diploma in Primary Education (Grade V) - Females",
    "Number of Qualified caregivers who are Grade III teachers - Males",
    "Number of Qualified caregivers who are Grade III teachers - Females",
    "Number of Qualified caregivers who are SNE Trained teachers - Males",
    "Number of Qualified caregivers who are SNE Trained teachers- Females",
    "Number of trained/Qualified caregivers with other trainings - Females",
    "Number of trained caregivers/Qualified with other trainings - Males",
    "Number of SNE trained caregivers/Qualified - Male",
    "Number of SNE trained caregivers/Qualified - Female",
]

# infrastructure / governance
handwash_col = "How many hand-washing facilities are at the ECCE centre?"
cmc_col = "Does the ECCE centre have Centre Management Committee (CMC)?"
cmc_meetings_col = "How many CMC meetings were held this term?"
lesson_plan_col = "Do all caregivers/teachers have lesson plans for the days taught"
timetable_col = "Is there a clearly designed timetable"
attendance_register_col = "Is there an UPDATED attendance register"
midday_meal_col = "Does the ECCE provide hot midday meals to learners?"
snack_system_col = "Is there a system to ensure that learners take a mid-morning snack?"
water_source_col = "What is the main source of DRINKING WATER for this ECCE centre?"
water_distance_col = "What is the distance to the main source of water for drinking?"
fence_gate_col = "Does the ECCE centre have the following/Intruder proof fence with a gate"
fence_no_gate_col = "Does the ECCE centre have the following/Intruder proof fence without a gate"
temp_class_col = "Where does the ECCE hold their daily lessons?/Temporary Classrooms"
open_space_col = "Where does the ECCE hold their daily lessons?/In an open space"
under_tree_col = "Where does the ECCE hold their daily lessons?/Under tree shade"


# ---------------------------------------------------
# PREP DATA
# ---------------------------------------------------
for col in enrollment_cols + attendance_cols + caregiver_cols + trained_cols + [
    handwash_col, cmc_meetings_col, fence_gate_col, fence_no_gate_col,
    temp_class_col, open_space_col, under_tree_col
]:
    if col in df.columns:
        df[col] = to_num(df[col])

df["Total_Enrollment"] = df[[c for c in enrollment_cols if c in df.columns]].sum(axis=1)
df["Total_Attending"] = df[[c for c in attendance_cols if c in df.columns]].sum(axis=1)
df["Attendance_Rate_%"] = (
    df["Total_Attending"] / df["Total_Enrollment"].replace(0, np.nan) * 100
).round(1)

df["Total_Caregivers"] = df[[c for c in caregiver_cols if c in df.columns]].sum(axis=1)
df["Total_Trained_Qualified"] = df[[c for c in trained_cols if c in df.columns]].sum(axis=1)
df["Learner_Caregiver_Ratio"] = (
    df["Total_Enrollment"] / df["Total_Caregivers"].replace(0, np.nan)
).round(1)

# ---------------------------------------------------
# ISSUE FLAGS
# ---------------------------------------------------
df["Issue_Unlicensed"] = safe_col(df, licensing_col, "").astype(str).str.strip().str.lower().ne("licensed")
df["Issue_Low_Attendance"] = df["Attendance_Rate_%"].fillna(0) < 75
df["Issue_High_Learner_Caregiver_Ratio"] = df["Learner_Caregiver_Ratio"].fillna(0) > 25
df["Issue_No_Handwashing"] = safe_col(df, handwash_col, 0).fillna(0).eq(0)
df["Issue_No_CMC"] = safe_col(df, cmc_col, "").astype(str).str.strip().str.lower().eq("no")
df["Issue_No_Lesson_Plans"] = safe_col(df, lesson_plan_col, "").astype(str).str.strip().str.lower().eq("no")
df["Issue_No_Timetable"] = safe_col(df, timetable_col, "").astype(str).str.strip().str.lower().eq("no")
df["Issue_No_Attendance_Register"] = safe_col(df, attendance_register_col, "").astype(str).str.strip().str.lower().eq("no")
df["Issue_No_Midday_Meal"] = safe_col(df, midday_meal_col, "").astype(str).str.strip().str.lower().eq("no")
df["Issue_No_Snack_System"] = safe_col(df, snack_system_col, "").astype(str).str.strip().str.lower().eq("no")
df["Issue_Unsafe_Water"] = safe_col(df, water_source_col, "").isin(["Unprotected well/spring", "Surface water"])
df["Issue_Water_Far"] = safe_col(df, water_distance_col, "").eq("More than 500m from the ECCE centre")
df["Issue_No_Fence"] = ~(
    safe_col(df, fence_gate_col, 0).fillna(0).eq(1) |
    safe_col(df, fence_no_gate_col, 0).fillna(0).eq(1)
)
df["Issue_Temporary_or_Open_Learning_Space"] = (
    safe_col(df, temp_class_col, 0).fillna(0).eq(1) |
    safe_col(df, open_space_col, 0).fillna(0).eq(1) |
    safe_col(df, under_tree_col, 0).fillna(0).eq(1)
)

issue_cols = [
    "Issue_Unlicensed",
    "Issue_Low_Attendance",
    "Issue_High_Learner_Caregiver_Ratio",
    "Issue_No_Handwashing",
    "Issue_No_CMC",
    "Issue_No_Lesson_Plans",
    "Issue_No_Timetable",
    "Issue_No_Attendance_Register",
    "Issue_No_Midday_Meal",
    "Issue_No_Snack_System",
    "Issue_Unsafe_Water",
    "Issue_Water_Far",
    "Issue_No_Fence",
    "Issue_Temporary_or_Open_Learning_Space",
]

df["Issue_Count"] = df[issue_cols].sum(axis=1)

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Filters")

districts = ["All"] + sorted(df[district_col].dropna().astype(str).unique().tolist()) if district_col in df.columns else ["All"]
selected_district = st.sidebar.selectbox("District", districts)

filtered_df = df.copy()

if selected_district != "All":
    filtered_df = filtered_df[filtered_df[district_col].astype(str) == selected_district]

subcounties = ["All"] + sorted(filtered_df[subcounty_col].dropna().astype(str).unique().tolist()) if subcounty_col in filtered_df.columns else ["All"]
selected_subcounty = st.sidebar.selectbox("Sub County", subcounties)

if selected_subcounty != "All":
    filtered_df = filtered_df[filtered_df[subcounty_col].astype(str) == selected_subcounty]

show_only_high_risk = st.sidebar.checkbox("Show only high-risk centres (4+ issues)", value=False)
if show_only_high_risk:
    filtered_df = filtered_df[filtered_df["Issue_Count"] >= 4]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("ECD Centres", f"{len(filtered_df):,}")
c2.metric("Children Enrolled", f"{int(filtered_df['Total_Enrollment'].sum()):,}")
c3.metric("Avg Attendance", f"{filtered_df['Attendance_Rate_%'].mean():.1f}%")
c4.metric("Licensed Centres", f"{(filtered_df[licensing_col].astype(str).str.strip().str.lower() == 'licensed').sum():,}")
c5.metric("High-Risk Centres", f"{(filtered_df['Issue_Count'] >= 4).sum():,}")

# ---------------------------------------------------
# ISSUE SUMMARY
# ---------------------------------------------------
st.subheader("Key Issues Summary")

issue_summary = pd.DataFrame({
    "Issue": [
        "Unlicensed centres",
        "Low attendance (<75%)",
        "High learner-caregiver ratio (>25)",
        "No handwashing facility",
        "No CMC",
        "No lesson plans",
        "No timetable",
        "No attendance register",
        "No hot midday meal",
        "No snack system",
        "Unsafe water source",
        "Water source farther than 500m",
        "No intruder-proof fence",
        "Temporary/open learning space"
    ],
    "Count": [
        filtered_df["Issue_Unlicensed"].sum(),
        filtered_df["Issue_Low_Attendance"].sum(),
        filtered_df["Issue_High_Learner_Caregiver_Ratio"].sum(),
        filtered_df["Issue_No_Handwashing"].sum(),
        filtered_df["Issue_No_CMC"].sum(),
        filtered_df["Issue_No_Lesson_Plans"].sum(),
        filtered_df["Issue_No_Timetable"].sum(),
        filtered_df["Issue_No_Attendance_Register"].sum(),
        filtered_df["Issue_No_Midday_Meal"].sum(),
        filtered_df["Issue_No_Snack_System"].sum(),
        filtered_df["Issue_Unsafe_Water"].sum(),
        filtered_df["Issue_Water_Far"].sum(),
        filtered_df["Issue_No_Fence"].sum(),
        filtered_df["Issue_Temporary_or_Open_Learning_Space"].sum(),
    ]
})

issue_summary["Rate %"] = (issue_summary["Count"] / max(len(filtered_df), 1) * 100).round(1)
issue_summary = issue_summary.sort_values("Count", ascending=False)

fig_issues = px.bar(
    issue_summary,
    x="Count",
    y="Issue",
    orientation="h",
    text="Rate %",
    title="Most Common Issues Across Centres"
)
st.plotly_chart(fig_issues, use_container_width=True)

# ---------------------------------------------------
# SUB-COUNTY RISK VIEW
# ---------------------------------------------------
st.subheader("Top Sub-Counties by Average Number of Issues")

subcounty_risk = (
    filtered_df.groupby(subcounty_col, dropna=False)
    .agg(
        Centres=(centre_col, "count"),
        Avg_Issues=("Issue_Count", "mean"),
        Total_Enrollment=("Total_Enrollment", "sum")
    )
    .reset_index()
    .sort_values("Avg_Issues", ascending=False)
)

fig_subcounty_risk = px.bar(
    subcounty_risk,
    x=subcounty_col,
    y="Avg_Issues",
    hover_data=["Centres", "Total_Enrollment"],
    title="Average Issues per Centre by Sub-County"
)
st.plotly_chart(fig_subcounty_risk, use_container_width=True)

# ---------------------------------------------------
# LICENSING STATUS
# ---------------------------------------------------
st.subheader("Licensing Status Breakdown")
license_df = filtered_df.copy()
license_df[licensing_col] = license_df[licensing_col].fillna("Unknown")

fig_pie = px.pie(
    license_df,
    names=licensing_col,
    title="Distribution by Licensing Status"
)
st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------
# ATTENDANCE VS ENROLLMENT
# ---------------------------------------------------
st.subheader("Attendance vs Enrollment")

scatter_df = filtered_df[[centre_col, subcounty_col, "Total_Enrollment", "Total_Attending", "Attendance_Rate_%", "Issue_Count"]].copy()

fig_scatter = px.scatter(
    scatter_df,
    x="Total_Enrollment",
    y="Attendance_Rate_%",
    size="Issue_Count",
    hover_name=centre_col,
    hover_data=[subcounty_col, "Total_Attending"],
    title="Attendance Rate vs Total Enrollment"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------
# HIGH-RISK CENTRES TABLE
# ---------------------------------------------------
st.subheader("Priority Centres Requiring Follow-up")

priority_df = filtered_df[
    [
        centre_col,
        district_col,
        subcounty_col,
        parish_col,
        licensing_col,
        "Total_Enrollment",
        "Attendance_Rate_%",
        "Total_Caregivers",
        "Learner_Caregiver_Ratio",
        "Issue_Count",
        "Issue_Unlicensed",
        "Issue_Low_Attendance",
        "Issue_High_Learner_Caregiver_Ratio",
        "Issue_No_Handwashing",
        "Issue_No_CMC",
        "Issue_No_Lesson_Plans",
        "Issue_No_Midday_Meal",
        "Issue_No_Fence",
    ]
].copy()

priority_df = priority_df.sort_values(
    by=["Issue_Count", "Total_Enrollment"],
    ascending=[False, False]
)

st.dataframe(
    priority_df.style.format({
        "Total_Enrollment": "{:,.0f}",
        "Attendance_Rate_%": "{:.1f}%",
        "Learner_Caregiver_Ratio": "{:.1f}"
    }),
    use_container_width=True,
    height=500
)

# ---------------------------------------------------
# TOP 10 CENTRES BY ENROLLMENT
# ---------------------------------------------------
st.subheader("Top 10 Centres by Enrollment")

top10 = (
    filtered_df[
        [
            centre_col,
            subcounty_col,
            licensing_col,
            "Total_Enrollment",
            "Attendance_Rate_%",
            "Issue_Count"
        ]
    ]
    .sort_values("Total_Enrollment", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

st.dataframe(
    top10.style.format({
        "Total_Enrollment": "{:,.0f}",
        "Attendance_Rate_%": "{:.1f}%"
    }),
    use_container_width=True
)

# ---------------------------------------------------
# OPTIONAL RAW DATA
# ---------------------------------------------------
with st.expander("Show cleaned raw data"):
    st.dataframe(filtered_df, use_container_width=True)
