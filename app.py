import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="ECD Monitoring Dashboard", layout="wide")
st.title("ECD Monitoring Dashboard")

file_url = "https://raw.githubusercontent.com/kiggundusharif-v1/ecd-monitoring-dashboard/main/ECD_Termly_monitoring_tool_-_Focus_Districts_-_all_versions_-_labels_-_2026-03-10-05-13-40.xlsx"

@st.cache_data
def load_data(url):
    return pd.read_excel(url)

def num(series):
    return pd.to_numeric(series, errors="coerce").fillna(0)

def find_col(df, names, required=True):
    for name in names:
        if name in df.columns:
            return name
    if required:
        st.error(f"Missing required column. Checked: {names}")
        st.write(df.columns.tolist())
        st.stop()
    return None

def yes_share(df, col):
    if col is None:
        return np.nan
    return df[col].astype(str).str.strip().str.lower().eq("yes").mean()

def count_yes(df, col):
    if col is None:
        return 0
    return int(df[col].astype(str).str.strip().str.lower().eq("yes").sum())

try:
    df = load_data(file_url)
except Exception as e:
    st.error("Could not load the Excel file from GitHub.")
    st.code(str(e))
    st.stop()

# ---------------- COLUMN MAPPING ----------------
district_col = find_col(df, ["District"])
subcounty_col = find_col(df, ["Sub County", "Subcounty", "Sub-county"])
parish_col = find_col(df, ["Parish"])
centre_col = find_col(df, ["ECD Centre", "ECCE Centre", "Centre Name"])

lic_col = find_col(df, [
    "What is the licensing status of this ECCE centre",
    "Is the licensing status of this ECCE centre",
    "Licensing status"
])

attached_col = find_col(df, [
    "Is the ECCE centre attached or affiliated to a Primary School"
], required=False)

lang_col = find_col(df, [
    "Does the ECCE centre teach learners using local languages?"
], required=False)

cmc_col = find_col(df, [
    "Does the ECCE centre have Centre Management Committee (CMC)?"
], required=False)

meal_col = find_col(df, [
    "Does the ECCE provide hot midday meals to learners?"
], required=False)

deworm_col = find_col(df, [
    "Does the ECCE centre provide deworming services?",
    "Were children dewormed in this term?",
    "Deworming service provided"
], required=False)

salary_col = find_col(df, [
    "Does the ECCE centre pay salaries to Caregivers?",
    "Does the ECCE centre pay salary/stipend to caregivers?",
    "Do caregivers receive salary/stipend?"
], required=False)

water_col = find_col(df, [
    "Main source of drinking water for Children in the ECCE centre",
    "Main source of drinking water"
], required=False)

handwash_col = find_col(df, [
    "Are there handwashing facilities at the ECCE centre?",
    "Handwashing facilities available"
], required=False)

toilet_col = find_col(df, [
    "Does the ECCE centre have latrines/toilets for children?",
    "Toilets available for children"
], required=False)

accessible_col = find_col(df, [
    "Are facilities accessible for children with special needs?",
    "Accessible facilities for SNEs"
], required=False)

lesson_col = find_col(df, [
    "Are lesson plans available for all caregivers?",
    "Does each caregiver have lesson plans?",
    "Lesson plans available"
], required=False)

framework_col = find_col(df, [
    "Does the ECCE centre use the learning framework?",
    "Is the learning framework available and being used?",
    "Learning framework available"
], required=False)

register_col = find_col(df, [
    "Does the ECCE centre have updated attendance register?",
    "Updated attendance register"
], required=False)

logbook_col = find_col(df, [
    "Does the ECCE centre have updated log book?",
    "Updated log book"
], required=False)

inventory_col = find_col(df, [
    "Does the ECCE centre have updated inventory book?",
    "Updated inventory book"
], required=False)

correspondence_col = find_col(df, [
    "Does the ECCE centre have updated correspondence book?",
    "Updated correspondence book"
], required=False)

assessment_col = find_col(df, [
    "Does the ECCE centre have children's assessment records?",
    "Children's assessment records"
], required=False)

scheme_col = find_col(df, [
    "Does the ECCE centre have updated scheme of work?",
    "Updated scheme of work"
], required=False)

timetable_col = find_col(df, [
    "Does the ECCE centre have clearly designed timetable/routine?",
    "Clearly designed timetable/routine"
], required=False)

income_exp_col = find_col(df, [
    "Does the ECCE centre have updated income and expenditure books?",
    "Income and expenditure books"
], required=False)

sne_col = find_col(df, [
    "Does the ECCE centre have children with Special Needs (SNEs)?"
], required=False)

# caregiver quality
trained_cg_male_col = find_col(df, [
    "Number of trained caregivers - Males",
    "Number of trained Caregivers - Males"
], required=False)

trained_cg_female_col = find_col(df, [
    "Number of trained caregivers - Females",
    "Number of trained Caregivers - Females"
], required=False)

qualified_cg_male_col = find_col(df, [
    "Number of qualified caregivers - Males",
    "Number of qualified Caregivers - Males"
], required=False)

qualified_cg_female_col = find_col(df, [
    "Number of qualified caregivers - Females",
    "Number of qualified Caregivers - Females"
], required=False)

# learning/play materials
materials_cols = {
    "Story books": find_col(df, ["Are story books available?", "Story books available"], required=False),
    "Toys": find_col(df, ["Are toys available?", "Toys available"], required=False),
    "Outdoor play materials": find_col(df, ["Are outdoor play materials available?", "Outdoor play materials available"], required=False),
    "Indoor play materials": find_col(df, ["Are indoor play materials available?", "Indoor play materials available"], required=False),
    "Teaching aids": find_col(df, ["Are teaching aids available?", "Teaching aids available"], required=False),
}

# school feeding source
feeding_source_col = find_col(df, [
    "What is the source of food for school feeding?",
    "Main source of food for school feeding",
    "Source of school feeding"
], required=False)

# IECD services
vacc_col = find_col(df, [
    "Does the ECCE centre support immunization/vaccination services?",
    "Vaccination services provided",
    "Immunization services provided"
], required=False)

growth_col = find_col(df, [
    "Does the ECCE centre support growth monitoring services?",
    "Growth monitoring provided"
], required=False)

parenting_col = find_col(df, [
    "Does the ECCE centre provide parenting education/support?",
    "Parenting education/support provided"
], required=False)

referral_col = find_col(df, [
    "Does the ECCE centre refer children for health/social support services?",
    "Referral services provided"
], required=False)

birthreg_col = find_col(df, [
    "Does the ECCE centre support birth registration services?",
    "Birth registration support"
], required=False)

lat_col = find_col(df, ["_Record the ECD Centre Location_latitude", "latitude", "Latitude"], required=False)
lon_col = find_col(df, ["_Record the ECD Centre Location_longitude", "longitude", "Longitude"], required=False)

# ---------------- DERIVED METRICS ----------------
boys_baby = find_col(df, ["Boys_Total_Baby"])
boys_mid = find_col(df, ["Boys_Total_Mid"])
boys_top = find_col(df, ["Boys_Total_Top"])
boys_day = find_col(df, ["Boys_Total_Day"])

girls_baby = find_col(df, ["Girls_Total_Baby"])
girls_mid = find_col(df, ["Girls_Total_Mid"])
girls_top = find_col(df, ["Girls_Total_Top"])
girls_day = find_col(df, ["Girls_Total_Day"])

df["Total_Boys_Enrolled"] = (
    num(df[boys_baby]) + num(df[boys_mid]) + num(df[boys_top]) + num(df[boys_day])
)
df["Total_Girls_Enrolled"] = (
    num(df[girls_baby]) + num(df[girls_mid]) + num(df[girls_top]) + num(df[girls_day])
)
df["Total_Enrollment"] = df["Total_Boys_Enrolled"] + df["Total_Girls_Enrolled"]

attendance_cols = [
    find_col(df, ["Number of learners attending in baby class - Boys"]),
    find_col(df, ["Number of learners attending in baby class - Girls"]),
    find_col(df, ["Number of learners attending in Middle class - Boys"]),
    find_col(df, ["Number of learners attending in Middle class - Girls"]),
    find_col(df, ["Number of learners attending in Top class - Boys"]),
    find_col(df, ["Number of learners attending in Top class - Girls"]),
    find_col(df, ["Number of learners attending in the day centre - Boys"]),
    find_col(df, ["Number of learners attending in the day center - Girls", "Number of learners attending in the day centre - Girls"])
]
df["Total_Attendance"] = df[attendance_cols].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1)

male_cg = find_col(df, ["Number of Caregivers  Males", "Number of Caregivers Males"])
female_cg = find_col(df, ["Number of Caregivers - Females", "Number of Caregivers Females"])
df["Caregivers_Total"] = num(df[male_cg]) + num(df[female_cg])

df["Attendance_Rate"] = np.where(df["Total_Enrollment"] > 0, df["Total_Attendance"] / df["Total_Enrollment"], np.nan)
df["Learners_per_Caregiver"] = np.where(df["Caregivers_Total"] > 0, df["Total_Enrollment"] / df["Caregivers_Total"], np.nan)
df["Licensed_Flag"] = df[lic_col].astype(str).str.strip().str.lower().eq("licensed").astype(int)

trained_total = 0
if trained_cg_male_col:
    trained_total += num(df[trained_cg_male_col])
if trained_cg_female_col:
    trained_total += num(df[trained_cg_female_col])
df["Trained_Caregivers_Total"] = trained_total if isinstance(trained_total, pd.Series) else 0

qualified_total = 0
if qualified_cg_male_col:
    qualified_total += num(df[qualified_cg_male_col])
if qualified_cg_female_col:
    qualified_total += num(df[qualified_cg_female_col])
df["Qualified_Caregivers_Total"] = qualified_total if isinstance(qualified_total, pd.Series) else 0

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

# SNE enrolment totals
sne_cols = [c for c in df.columns if "special needs" in c.lower() or "sne" in c.lower()]
sne_count_cols = [c for c in sne_cols if any(x in c.lower() for x in ["number", "boys", "girls", "baby", "middle", "top", "day"])]
df["SNE_Enrollment_Total"] = df[sne_count_cols].apply(pd.to_numeric, errors="coerce").fillna(0).sum(axis=1) if sne_count_cols else 0

# ---------------- FILTERS ----------------
districts = sorted(df[district_col].dropna().unique().tolist())
selected_districts = st.sidebar.multiselect("District", districts, default=districts)

subs = sorted(df[df[district_col].isin(selected_districts)][subcounty_col].dropna().unique().tolist()) if selected_districts else []
selected_subs = st.sidebar.multiselect("Sub County", subs, default=subs)

f = df.copy()
if selected_districts:
    f = f[f[district_col].isin(selected_districts)]
if selected_subs:
    f = f[f[subcounty_col].isin(selected_subs)]

if f.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# ---------------- EXECUTIVE SUMMARY ----------------
centres = len(f)
enrollment = int(f["Total_Enrollment"].sum())
attendance = int(f["Total_Attendance"].sum())
caregivers = int(f["Caregivers_Total"].sum())
attendance_rate = attendance / enrollment if enrollment else np.nan
licensed_pct = f["Licensed_Flag"].mean()

st.subheader("Executive Summary")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Centres", f"{centres:,}")
k2.metric("Enrollment", f"{enrollment:,}")
k3.metric("Attendance Rate", f"{attendance_rate:.1%}" if pd.notna(attendance_rate) else "—")
k4.metric("Caregivers", f"{caregivers:,}")
k5.metric("Licensed %", f"{licensed_pct:.1%}" if pd.notna(licensed_pct) else "—")

s1, s2 = st.columns(2)

with s1:
    lic_df = f[lic_col].fillna("Unknown").value_counts().reset_index()
    lic_df.columns = ["Licensing Status", "Centres"]
    st.plotly_chart(px.pie(lic_df, names="Licensing Status", values="Centres", title="ECD Centre Status"), use_container_width=True)

with s2:
    summary_df = pd.DataFrame({
        "Indicator": [
            "Attached to Primary",
            "Local Language Teaching",
            "CMC Availability",
            "Hot Meals",
            "Deworming",
            "Updated Register",
            "Lesson Plans",
            "Learning Framework"
        ],
        "Percent": [
            yes_share(f, attached_col),
            yes_share(f, lang_col),
            yes_share(f, cmc_col),
            yes_share(f, meal_col),
            yes_share(f, deworm_col),
            yes_share(f, register_col),
            yes_share(f, lesson_col),
            yes_share(f, framework_col),
        ]
    }).dropna()
    fig = px.bar(summary_df, x="Indicator", y="Percent", title="Key Coverage Percentages")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Enrolment",
    "Centre Status",
    "IECD Services",
    "Caregivers",
    "Learning & Play Materials",
    "Infrastructure",
    "WASH",
    "Records"
])

with tab1:
    c1, c2, c3 = st.columns(3)

    class_df = pd.DataFrame({
        "Class": ["Day Care", "Baby Class", "Middle Class", "Top Class"],
        "Female": [
            int(num(f[girls_day]).sum()),
            int(num(f[girls_baby]).sum()),
            int(num(f[girls_mid]).sum()),
            int(num(f[girls_top]).sum()),
        ],
        "Male": [
            int(num(f[boys_day]).sum()),
            int(num(f[boys_baby]).sum()),
            int(num(f[boys_mid]).sum()),
            int(num(f[boys_top]).sum()),
        ],
    })
    class_long = class_df.melt(id_vars="Class", var_name="Sex", value_name="Enrollment")
    c1.plotly_chart(px.bar(class_long, x="Class", y="Enrollment", color="Sex", barmode="group", title="Enrolment by Class and Sex"), use_container_width=True)

    sex_df = pd.DataFrame({
        "Sex": ["Female", "Male"],
        "Enrollment": [int(f["Total_Girls_Enrolled"].sum()), int(f["Total_Boys_Enrolled"].sum())]
    })
    c2.plotly_chart(px.pie(sex_df, names="Sex", values="Enrollment", title="Enrolment by Sex"), use_container_width=True)

    sne_df = pd.DataFrame({
        "Metric": ["SNE Enrolment", "Orphans", "Refugees"],
        "Count": [
            int(f["SNE_Enrollment_Total"].sum()),
            int(f["Total_Orphans"].sum()),
            int(f["Refugee_Count"].sum())
        ]
    })
    c3.plotly_chart(px.bar(sne_df, x="Metric", y="Count", title="Inclusion Enrolment"), use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)

    status_df = f[lic_col].fillna("Unknown").value_counts().reset_index()
    status_df.columns = ["Status", "Centres"]
    c1.plotly_chart(px.bar(status_df, x="Status", y="Centres", title="ECD Centre Status"), use_container_width=True)

    attach_df = pd.DataFrame({
        "Indicator": ["Attached to Primary", "Not Attached"],
        "Value": [
            count_yes(f, attached_col),
            len(f) - count_yes(f, attached_col)
        ]
    })
    c2.plotly_chart(px.pie(attach_df, names="Indicator", values="Value", title="Attachment to Primary"), use_container_width=True)

with tab3:
    iecd_df = pd.DataFrame({
        "Service": [
            "Deworming",
            "Hot Meal Program",
            "Local Language",
            "Vaccination / Immunization",
            "Growth Monitoring",
            "Parenting Education",
            "Referral Services",
            "Birth Registration Support"
        ],
        "Percent": [
            yes_share(f, deworm_col),
            yes_share(f, meal_col),
            yes_share(f, lang_col),
            yes_share(f, vacc_col),
            yes_share(f, growth_col),
            yes_share(f, parenting_col),
            yes_share(f, referral_col),
            yes_share(f, birthreg_col),
        ]
    }).dropna()

    fig = px.bar(iecd_df, x="Service", y="Percent", title="IECD Services")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    c1, c2, c3 = st.columns(3)

    cg_sex = pd.DataFrame({
        "Sex": ["Female", "Male"],
        "Caregivers": [
            int(num(f[female_cg]).sum()),
            int(num(f[male_cg]).sum())
        ]
    })
    c1.plotly_chart(px.bar(cg_sex, x="Sex", y="Caregivers", title="Caregivers by Sex"), use_container_width=True)

    trained_qualified_df = pd.DataFrame({
        "Category": ["Trained Caregivers", "Qualified Caregivers"],
        "Count": [
            int(num(f["Trained_Caregivers_Total"]).sum()),
            int(num(f["Qualified_Caregivers_Total"]).sum())
        ]
    })
    c2.plotly_chart(px.bar(trained_qualified_df, x="Category", y="Count", title="Trained and Qualified Caregivers"), use_container_width=True)

    salary_df = pd.DataFrame({
        "Indicator": ["Salary/Stipend"],
        "Percent": [yes_share(f, salary_col)]
    }).dropna()
    fig = px.bar(salary_df, x="Indicator", y="Percent", title="Centres that Pay Caregivers")
    fig.update_yaxes(tickformat=".0%")
    c3.plotly_chart(fig, use_container_width=True)

with tab5:
    available_materials = {k: v for k, v in materials_cols.items() if v is not None}
    if available_materials:
        mat_df = pd.DataFrame({
            "Material": list(available_materials.keys()),
            "Percent": [yes_share(f, col) for col in available_materials.values()]
        }).dropna()
        fig = px.bar(mat_df, x="Material", y="Percent", title="Learning and Play Materials")
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Learning and play materials columns were not found in this file.")

with tab6:
    c1, c2 = st.columns(2)

    infra = {}
    for label, colname in {
        "Permanent": "Where does the ECCE hold their daily lessons?/Permanent Classrooms",
        "Temporary": "Where does the ECCE hold their daily lessons?/Temporary Classrooms",
        "Under Tree Shade": "Where does the ECCE hold their daily lessons?/Under Tree Shade",
        "Open Space": "Where does the ECCE hold their daily lessons?/Open Space",
    }.items():
        if colname in f.columns:
            infra[label] = int(pd.to_numeric(f[colname], errors="coerce").fillna(0).sum())

    if infra:
        infra_df = pd.DataFrame({"Type": list(infra.keys()), "Centres": list(infra.values())})
        c1.plotly_chart(px.bar(infra_df, x="Type", y="Centres", title="Learning Spaces"), use_container_width=True)

    if feeding_source_col:
        feed_src_df = f[feeding_source_col].fillna("Unknown").value_counts().reset_index()
        feed_src_df.columns = ["Source", "Centres"]
        c2.plotly_chart(px.bar(feed_src_df, x="Source", y="Centres", title="Source of School Feeding"), use_container_width=True)

with tab7:
    c1, c2 = st.columns(2)

    if water_col:
        water_df = f[water_col].fillna("Unknown").value_counts().reset_index()
        water_df.columns = ["Water Source", "Centres"]
        c1.plotly_chart(px.bar(water_df, x="Water Source", y="Centres", title="Drinking Water Source"), use_container_width=True)

    wash_df = pd.DataFrame({
        "Indicator": [
            "Handwashing Facilities",
            "Toilets / Latrines",
            "Accessible Facilities for SNEs"
        ],
        "Percent": [
            yes_share(f, handwash_col),
            yes_share(f, toilet_col),
            yes_share(f, accessible_col)
        ]
    }).dropna()
    fig = px.bar(wash_df, x="Indicator", y="Percent", title="WASH Details")
    fig.update_yaxes(tickformat=".0%")
    c2.plotly_chart(fig, use_container_width=True)

with tab8:
    records_df = pd.DataFrame({
        "Record": [
            "Attendance Register",
            "Lesson Plans",
            "Learning Framework",
            "Log Book",
            "Inventory Book",
            "Correspondence Book",
            "Assessment Records",
            "Scheme of Work",
            "Timetable / Routine",
            "Income & Expenditure Books"
        ],
        "Percent": [
            yes_share(f, register_col),
            yes_share(f, lesson_col),
            yes_share(f, framework_col),
            yes_share(f, logbook_col),
            yes_share(f, inventory_col),
            yes_share(f, correspondence_col),
            yes_share(f, assessment_col),
            yes_share(f, scheme_col),
            yes_share(f, timetable_col),
            yes_share(f, income_exp_col),
        ]
    }).dropna()

    fig = px.bar(records_df, x="Record", y="Percent", title="Availability of Records")
    fig.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Data Quality")
    dq = pd.DataFrame({
        "Check": [
            "Missing centre names",
            "Missing sub-county",
            "Missing parish",
            "Centres with zero enrollment",
            "Centres with zero attendance",
            "Centres with zero caregivers",
        ],
        "Count": [
            int(f[centre_col].isna().sum()),
            int(f[subcounty_col].isna().sum()),
            int(f[parish_col].isna().sum()),
            int((f["Total_Enrollment"] == 0).sum()),
            int((f["Total_Attendance"] == 0).sum()),
            int((f["Caregivers_Total"] == 0).sum()),
        ]
    })
    st.dataframe(dq, use_container_width=True)
