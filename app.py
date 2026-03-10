import streamlit as st
import pandas as pd
import plotly.express as px

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

    # Clean column names
    df.columns = df.columns.str.strip().str.replace(r"\s+", " ", regex=True)

    # Calculate useful totals
    boys_cols = [col for col in df.columns if "Boys_Total_" in col]
    girls_cols = [col for col in df.columns if "Girls_Total_" in col]

    if not boys_cols and not girls_cols:
        st.warning("No enrollment columns found matching 'Boys_Total_' or 'Girls_Total_'.")

    df["Total_Enrollment"] = df[boys_cols + girls_cols].sum(axis=1, skipna=True) if (boys_cols or girls_cols) else 0

    attend_cols = [col for col in df.columns if "attending" in col.lower()]
    if not attend_cols:
        st.warning("No attendance columns found containing 'attending'.")

    df["Total_Attending"] = df[attend_cols].sum(axis=1, skipna=True) if attend_cols else 0

    df["Attendance_Rate_%"] = (
        df["Total_Attending"] / df["Total_Enrollment"].replace(0, pd.NA) * 100
    ).round(1)

    return df


# Page config
st.set_page_config(page_title="Mubende ECD Dashboard", layout="wide")

st.title("Mubende District ECD Centres Monitoring Dashboard")

df = load_data()

# Column names used in the dashboard
subcounty_col = "Sub County"
licensing_col = "Is the licensing status of this ECCE centre"
centre_col = "ECD Centre"

# Validate required columns
required_cols = [subcounty_col, licensing_col, centre_col]
missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Missing required column(s): {', '.join(missing_cols)}")
    st.stop()

# Key summary metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total ECD Centres", f"{len(df):,}")
col2.metric("Total Children Enrolled", f"{int(df['Total_Enrollment'].sum()):,}")

avg_attendance = df["Attendance_Rate_%"].dropna().mean()
col3.metric("Average Attendance Rate", f"{avg_attendance:.1f}%" if pd.notna(avg_attendance) else "N/A")

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

# Licensing Status Breakdown
st.subheader("Licensing Status Breakdown")

licensing_plot_df = df.copy()
licensing_plot_df[licensing_col] = licensing_plot_df[licensing_col].fillna("Unknown")

fig_pie = px.pie(
    licensing_plot_df,
    names=licensing_col,
    title="Distribution by Licensing Status"
)
st.plotly_chart(fig_pie, use_container_width=True)

# Top 10 Centres by Enrollment
st.subheader("Top 10 Centres by Enrollment")

top10_cols = [centre_col, subcounty_col, "Total_Enrollment", "Attendance_Rate_%", licensing_col]
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
