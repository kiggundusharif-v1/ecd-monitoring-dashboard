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
        st.write("Available columns:")
        st.write(df.columns.tolist())
        st.stop()
    return None

def yes_share(df, col):
    if col is None:
        return np.nan
    s = df[col].astype(str).str.strip().str.lower()
    return s.eq("yes").mean()

def count_yes(df, col):
    if col is None:
        return 0
    s = df[col].astype(str).str.strip().str.lower()
    return int(s.eq("yes").sum())

def yes_no_counts(df, col):
    if col is None:
        return pd.DataFrame(columns=["Response", "Centres"])
    s = df[col].astype(str).str.strip().str.title()
    s = s.replace({"Nan": "Unknown", "": "Unknown"})
    out = s.value_counts(dropna=False).reset_index()
    out.columns = ["Response", "Centres"]
    return out

def category_counts(df, col, value_name="Centres"):
    if col is None:
        return pd.DataFrame(columns=["Category", value_name])
    s = df[col].astype(str).str.strip()
    s = s.replace({"": "Unknown", "nan": "Unknown", "NaN": "Unknown"})
    out = s.value_counts(dropna=False).reset_index()
    out.columns = ["Category", value_name]
    return out

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

sne_presence_col = find_col(df, [
    "Does the ECCE centre have children with Special Needs (SNEs)?"
], required=False)

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

materials_cols = {
    "Story books": find_col(df, ["Are story books available?", "Story books available"], required=False),
    "Toys": find_col(df, ["Are toys available?", "Toys available"], required=False),
    "Outdoor play materials": find_col(df, ["Are outdoor play materials available?", "Outdoor play materials available"], required=False),
    "Indoor play materials": find_col(df, ["Are indoor play materials available?", "Indoor play materials available"], required=False),
    "Teaching aids": find_col(df, ["Are teaching aids available?", "Teaching aids available"], required=False),
}

feeding_source_col = find_col(df, [
    "What is the source of food for school feeding?",
    "Main source of food for school feeding",
    "Source of school feeding"
], required=False)

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
df["Registered_or_Licensed_Flag"] = df[lic_col].astype(str).str.strip().str.lower().isin(["licensed", "registered"]).astype(int)

if trained_cg_male_col or trained_cg_female_col:
    df["Trained_Caregivers_Total"] = (
        (num(df[trained_cg_male_col]) if trained_cg_male_col else 0) +
        (num(df[trained_cg_female_col]) if trained_cg_female_col else 0)
    )
else:
    df["Trained_Caregivers_Total"] = 0

if qualified_cg_male_col or qualified_cg_female_col:
    df["Qualified_Caregivers_Total"] = (
        (num(df[qualified_cg_male_col]) if qualified_cg_male_col else 0) +
        (num(df[qualified_cg_female_col]) if qualified_cg_female_col else 0)
    )
else:
    df["Qualified_Caregivers_Total"] = 0

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
    lic_df = category_counts(f, lic_col)
    lic_df.columns = ["Licensing Status", "Centres"]
    st.plotly_chart(px.bar(lic_df, x="Licensing Status", y="Centres", title="Licensing Status"), use_container_width=True)

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
    c1.plotly_chart(px.bar(category_counts(f, lic_col), x="Category", y="Centres", title="ECD Centre Status"), use_container_width=True)
    c2.plotly_chart(px.bar(yes_no_counts(f, attached_col), x="Response", y="Centres", title="Attachment to Primary"), use_container_width=True)

with tab3:
    r1, r2, r3 = st.columns(3)
    r1.plotly_chart(px.bar(yes_no_counts(f, deworm_col), x="Response", y="Centres", title="Deworming"), use_container_width=True)
    r2.plotly_chart(px.bar(yes_no_counts(f, meal_col), x="Response", y="Centres", title="Hot Meal Program"), use_container_width=True)
    r3.plotly_chart(px.bar(yes_no_counts(f, lang_col), x="Response", y="Centres", title="Local Language Teaching"), use_container_width=True)

    r4, r5, r6 = st.columns(3)
    r4.plotly_chart(px.bar(yes_no_counts(f, vacc_col), x="Response", y="Centres", title="Vaccination / Immunization"), use_container_width=True)
    r5.plotly_chart(px.bar(yes_no_counts(f, growth_col), x="Response", y="Centres", title="Growth Monitoring"), use_container_width=True)
    r6.plotly_chart(px.bar(yes_no_counts(f, parenting_col), x="Response", y="Centres", title="Parenting Education"), use_container_width=True)

    r7, r8 = st.columns(2)
    r7.plotly_chart(px.bar(yes_no_counts(f, referral_col), x="Response", y="Centres", title="Referral Services"), use_container_width=True)
    r8.plotly_chart(px.bar(yes_no_counts(f, birthreg_col), x="Response", y="Centres", title="Birth Registration Support"), use_container_width=True)

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

    c3.plotly_chart(px.bar(yes_no_counts(f, salary_col), x="Response", y="Centres", title="Centres that Pay Caregivers"), use_container_width=True)

with tab5:
    available_materials = {k: v for k, v in materials_cols.items() if v is not None}
    if available_materials:
        mat_df = pd.DataFrame({
            "Material": list(available_materials.keys()),
            "Yes %": [yes_share(f, col) for col in available_materials.values()]
        }).dropna()
        fig = px.bar(mat_df, x="Material", y="Yes %", title="Learning and Play Materials")
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        items = list(available_materials.items())
        for i, (label, col) in enumerate(items[:3]):
            [m1, m2, m3][i].plotly_chart(px.bar(yes_no_counts(f, col), x="Response", y="Centres", title=label), use_container_width=True)
        if len(items) > 3:
            n1, n2 = st.columns(2)
            for i, (label, col) in enumerate(items[3:5]):
                [n1, n2][i].plotly_chart(px.bar(yes_no_counts(f, col), x="Response", y="Centres", title=label), use_container_width=True)
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
        feed_src_df = category_counts(f, feeding_source_col)
        c2.plotly_chart(px.bar(feed_src_df, x="Category", y="Centres", title="Source of School Feeding"), use_container_width=True)

with tab7:
    c1, c2 = st.columns(2)

    if water_col:
        water_df = category_counts(f, water_col)
        c1.plotly_chart(px.bar(water_df, x="Category", y="Centres", title="Drinking Water Source"), use_container_width=True)

    wash_summary = pd.DataFrame({
        "Indicator": ["Handwashing", "Toilets / Latrines", "Accessible for SNEs"],
        "Percent": [
            yes_share(f, handwash_col),
            yes_share(f, toilet_col),
            yes_share(f, accessible_col)
        ]
    }).dropna()
    if len(wash_summary):
        fig = px.bar(wash_summary, x="Indicator", y="Percent", title="WASH Coverage Summary")
        fig.update_yaxes(tickformat=".0%")
        c2.plotly_chart(fig, use_container_width=True)

    w1, w2, w3 = st.columns(3)
    w1.plotly_chart(px.bar(yes_no_counts(f, handwash_col), x="Response", y="Centres", title="Handwashing Facilities"), use_container_width=True)
    w2.plotly_chart(px.bar(yes_no_counts(f, toilet_col), x="Response", y="Centres", title="Toilets / Latrines"), use_container_width=True)
    w3.plotly_chart(px.bar(yes_no_counts(f, accessible_col), x="Response", y="Centres", title="Accessible Facilities for SNEs"), use_container_width=True)

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

    record_items = {
        "Attendance Register": register_col,
        "Lesson Plans": lesson_col,
        "Learning Framework": framework_col,
        "Log Book": logbook_col,
        "Inventory Book": inventory_col,
        "Correspondence Book": correspondence_col,
        "Assessment Records": assessment_col,
        "Scheme of Work": scheme_col,
        "Timetable / Routine": timetable_col,
        "Income & Expenditure Books": income_exp_col,
    }

    cols = st.columns(2)
    i = 0
    for label, col in record_items.items():
        if col is not None:
            cols[i % 2].plotly_chart(
                px.bar(yes_no_counts(f, col), x="Response", y="Centres", title=label),
                use_container_width=True
            )
            i += 1

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
