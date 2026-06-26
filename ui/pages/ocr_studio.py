import streamlit as st

from services.ocr_pipeline import OCRPipeline


def render_ocr_studio():

    st.title("📷 OCR Studio (Advanced)")

    uploaded_file = st.file_uploader(
        "Upload file",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if not uploaded_file:
        return

    # =========================
    # OCR STEP
    # =========================
    if st.button("Run OCR"):

        with st.spinner("Processing OCR..."):

            text = OCRPipeline.extract(uploaded_file)
            st.session_state["ocr_text"] = text

    text = st.session_state.get("ocr_text")

    if not text:
        return

    # =========================
    # EDITABLE TEXT
    # =========================
    editable_text = st.text_area(
        "Edit extracted text",
        value=text,
        height=300
    )

    # =========================
    # ADVANCED INPUTS
    # =========================
    context = st.text_input(
        "Context (domain / type of document)"
    )

    columns = st.text_input(
        "Columns (comma separated)"
    )

    examples = st.text_area(
        "Examples (optional)"
    )

    # =========================
    # GENERATE DATASET
    # =========================
    if st.button("Generate dataset"):

        df = OCRPipeline.build_dataframe(
            raw_text=editable_text,
            columns=columns,
            context=context,
            examples=examples,
            llm=st.session_state["llm"]
        )

        st.session_state["ocr_df"] = df

    # =========================
    # PREVIEW + VALIDATION
    # =========================
    df = st.session_state.get("ocr_df")

    if df is None:
        return

    edited_df = st.data_editor(
        df,
        width="stretch",
        num_rows="dynamic"
    )

    errors = OCRPipeline.validate(edited_df)

    if errors:
        for e in errors:
            st.error(e)
        return

    st.success("Dataset valid ✔")

    # =========================
    # SAVE
    # =========================
    if st.button("Save dataset"):

        result = OCRPipeline.save(
            edited_df,
            prefix="ocr_studio"
        )

        st.success(result["dataset_id"])
        st.rerun()