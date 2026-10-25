import streamlit as st

from services.ocr_pipeline import OCRPipeline


def render_ocr_panel():

    st.subheader("📷 OCR (Simple Mode)")

    uploaded_file = st.file_uploader(
        "Upload image",
        type=["png", "jpg", "jpeg"]
    )

    if not uploaded_file:
        return

    if st.button("Process image"):

        with st.spinner("Reading image..."):
            st.session_state["ocr_text"] = OCRPipeline.extract(
                uploaded_file
            )

    text = st.session_state.get("ocr_text")

    if not text:
        return

    st.text_area(
        "Detected text",
        value=text,
        height=250
    )

    columns = st.text_input(
        "Columns (comma separated)"
    )

    generate_dataset(
        text,
        columns
    )

    preview_dataset()


def generate_dataset(
    text,
    columns
):

    if not st.button("Generate dataset"):
        return

    st.session_state["ocr_df"] = OCRPipeline.build_dataframe(
        raw_text=text,
        columns=columns,
        context="",
        examples="",
        llm=st.session_state["llm"]
    )


def preview_dataset():

    df = st.session_state.get("ocr_df")

    if df is None:
        return

    edited_df = st.data_editor(
        df,
        width="stretch",
        num_rows="dynamic"
    )

    errors = OCRPipeline.validate(
        edited_df
    )

    if errors:
        for error in errors:
            st.error(error)
        return

    st.success("Dataset valid ✔")

    if not st.button("Save dataset"):
        return

    result = OCRPipeline.save(
        edited_df,
        prefix="ocr_simple"
    )

    st.success(result["dataset_id"])
    st.rerun()