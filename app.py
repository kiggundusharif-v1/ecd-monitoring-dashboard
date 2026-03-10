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
    df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
    
    # Calculate useful totals
    boys_cols = [col for col in df.columns if 'Boys_Total_' in col]
    girls_cols = [col for col in df.columns if 'Girls_Total_' in col]
    df['Total_Enrollment'] = df[boys_cols + girls_cols].sum(axis=1, skipna=True)
    
    attend_cols = [col for col in df.columns if 'attending' in col.lower()]
    df['Total_Attending'] = df[attend_cols].sum(axis=1, skipna=True)
    
    df['Attendance_Rate_%'] = (df['Total_Attending'] / df['Total_Enrollment'].replace(0, pd.NA) * 100).round(1)
    
    return df

# ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mubende ECD Dashboard", layout="wide")

st.title("Mubende District ECD Centres Monitoring Dashboard")

df = load_data()

# Key summary metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total ECD Centres", len(df))
col2.metric("Total Children Enrolled", f"{int(df['Total_Enrollment'].sum()):,}")
col3.metric("Average Attendance Rate", f"{df['Attendance_Rate_%'].mean():.1f}%")
col4.metric("Licensed Centres", f"{(df['What is the licensing status of this ECCE centre'] == 'Licensed').sum()}")

st.subheader("Centres by Sub-County")
subcounty_df = df['Sub County'].value_counts().reset_index(name='Number of Centres')
fig_bar = px.bar(subcounty_df, x='Sub County', y='Number of Centres', 
                 title="ECD Centres per Sub-County",
                 color='Number of Centres')
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("Licensing Status Breakdown")
fig_pie = px.pie(df, names='What is the licensing status of this ECCE centre',
                 title="Distribution by Licensing Status")
st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("Top 10 Centres by Enrollment")
top10 = df[['ECD Centre', 'Sub County', 'Total_Enrollment', 'Attendance_Rate_%', 
            'Is the licensing status of this ECCE centre']]\
        .sort_values('Total_Enrollment', ascending=False)\
        .head(10)\
        .reset_index(drop=True)

st.dataframe(
    top10.style.format({
        'Total_Enrollment': '{:,.0f}',
        'Attendance_Rate_%': '{:.1f}%'
    }).set_properties(**{'text-align': 'center'}),
    use_container_width=True
)

st.markdown("---")

st.caption("Data: ECD Termly Monitoring Tool – Mubende Focus Districts")
