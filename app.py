import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    file_path = "ECD_Termly_monitoring_tool_-_Focus_Districts_-_all_versions_-_labels_-_2026-03-10-05-13-40.xlsx"

    try:
        df = pd.read_excel(file_path, sheet_name="Sheet1")
    except FileNotFoundError:
        st.error(f"Excel file not found: {file_path}")
        st.stop()
    except Exception as e:
        st.error(f"Error reading Excel: {e}")
        st.stop()

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    return df


def find_column(columns, possible_names):
    """
    Return the first matching column from a list of possible names.
    Matching is case-insensitive.
    """
    col_map = {c.lower().strip(): c for c in columns}
    for name in possible_names:
        if name.lower().strip() in col_map:
            return col_map[name.lower().strip()]
    return None


st.set_page_config(page_title="Mubende ECD Dashboard", layout="wide")
st.title("Mubende District ECD Centres Monitoring Dashboard")

df = load_data()

# Show available columns for debugging
with st.expander("Show detected columns"):
    st.write(df.columns.tolist())

# Try to detect important columns
subcounty_col = find_column(df.columns, [
    "Sub County",
    "Sub county",
    "SubCounty"
])

centre_col = find_column(df.columns, [
    "ECD Centre",
    "Ecd Centre",
    "Centre Name",
    "School Name"
])

licensing_col = find_column(df.columns, [
    "Is the licensing status of this ECCE centre",
    "Is the licensing status of this ECCE center",
    "Licensing status",
    "License status",
    "Is the licensing status of this centre"
])

# Enrollment columns
boys_cols = [col for col in df.columns if "Boys_Total_" in col]
girls_cols = [col for col in df.columns if "Girls_Total_" in col]

df["Total_Enrollment"] = df[boys_cols + girls_cols].sum(axis=1, skipna=True) if (boys_cols or girls_cols) else 0

# Attendance columns
attend_cols = [col for col in df.columns if "attending" in col.lower()]
df["Total_Attending"] = df[attend_cols].sum(axis=1, skipna=True) if attend_cols else 0

df["Attendance_Rate_%"] = (
    df["Total_Attending"] / df["Total_Enrollment"].replace(0, pd.NA) * 100
).round(1)

# Validate only the truly necessary columns
missing = []
if subcounty_col is None:
    missing.append("Sub County")
if centre_col is None:
    missing.append("ECD Centre")

if missing:
    st.error(f"Missing required column(s): {', '.join(missing)}")
    st.stop()

# Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total ECD Centres", f"{len(df):,}")
col2.metric("Total Children Enrolled", f"{int(df['Total_Enrollment'].sum()):,}")

avg_att = df["Attendance_Rate_%"].dropna().mean()
col3.metric("Average Attendance Rate", f"{avg_att:.1f}%" if pd.notna(avg_att) else "N/A")

if licensing_col:
    licensed_count = (
        df[licensing_col]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("licensed")
        .sum()
    )
    col4.metric("Licensed Centres", f"{licensed_count:,}")
else:
    col4.metric("Licensed Centres", "N/A")

# Centres by Sub-County
st.subheader("Centres by Sub-County")
subcounty_df = (
    df[subcounty_col]
    .fillna("Unknown")
    .value_counts()
    .rename_axis(subcounty_col)
    .reset_index(name="Number of Centres")
)

fig_bar = px.bar(
    subcounty_df,
    x=subcounty_col,
    y="Number of Centres",
    title="ECD Centres per Sub-County",
    color="Number of Centres"
)
st.plotly_chart(fig_bar, use_container_width=True)

# Licensing chart
if licensing_col:
    st.subheader("Licensing Status Breakdown")
    pie_df = df.copy()
    pie_df[licensing_col] = pie_df[licensing_col].fillna("Unknown")

    fig_pie = px.pie(
        pie_df,
        names=licensing_col,
        title="Distribution by Licensing Status"
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("Licensing column not found, so the licensing chart was skipped.")

# Top 10 centres
st.subheader("Top 10 Centres by Enrollment")

top10_cols = [centre_col, subcounty_col, "Total_Enrollment", "Attendance_Rate_%"]
if licensing_col:
    top10_cols.append(licensing_col)

top10 = (
    df[top10_cols]
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

st.markdown("---")
st.caption("Data: ECD Termly Monitoring Tool – Mubende Focus Districts")
