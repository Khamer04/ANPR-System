import streamlit as st
from lnpr import process_video
import tempfile

st.set_page_config(page_title="ANPR System", layout="wide")
st.title("🚗 Automatic Number Plate Recognition – Stolen Vehicle Detection")

video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

if video:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(video.read())
        path = tmp.name

    st.video(video)

    if st.button("Start Detection"):
        with st.spinner("Processing..."):
            matches = process_video(path)

        if matches:
            st.error("🚨 Stolen Vehicles Detected!")
            for plate, details in matches:
                st.write(f"**Plate:** {plate}")
                st.write(details)
                st.divider()
        else:
            st.success("✅ No stolen vehicles found")
