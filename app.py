import streamlit as st

from data_parser import load_match_data, get_match_list
from report_generator import generate_report

st.set_page_config(
    page_title="BKFC Match Report Generator",
    layout="wide"
)

st.title("⚽ Brooklyn FC Match Report Generator")

st.markdown("Upload BKFC + Opponent season files to generate a match report.")

# ── Uploads ─────────────────────────────
bkfc_file = st.file_uploader("Upload BKFC Season File", type=["xlsx"])
opp_file = st.file_uploader("Upload Opponent Season File", type=["xlsx"])

data = None

# Both files must be uploaded before processing begins
if bkfc_file and opp_file:
    try:
        # Extract available matches from the BKFC tracking file
        match_options = get_match_list(bkfc_file)
        
        if match_options:
            # Dynamically default the selection index to the newest match (bottom of the sheet)
            latest_match_idx = len(match_options) - 1
            
            selected_match = st.selectbox(
                "Select Match to Generate Report For",
                options=match_options,
                index=latest_match_idx,
                format_func=lambda x: x["label"]
            )
            
            # Load your data dynamically based on the match picked
            data = load_match_data(bkfc_file, opp_file, match_row_idx=selected_match["index"])
        else:
            # Fallback configuration if matches aren't successfully parsed
            data = load_match_data(bkfc_file, opp_file)
            
    except Exception as e:
        st.error(f"Failed to automatically process spreadsheet structure: {e}")
        data = None

    if data:
        st.success(
            f"Detected Match: BKFC vs {data['opponent_name']}"
        )

        st.write("**Match Info**")
        st.write(f"Date: {data['match_date']}")
        st.write(f"Competition: {data['competition']}")
        st.write(f"Score: {data['score']}")

        confirm = st.checkbox("I confirm this match is correct")

        if confirm:
            if st.button("Generate Report"):

                output_file = "BKFC_Match_Report.pptx"

                with st.spinner("Generating PowerPoint..."):
                    generate_report(data)

                with open(output_file, "rb") as f:
                    st.download_button(
                        "Download PowerPoint",
                        f,
                        file_name=output_file,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                    )
