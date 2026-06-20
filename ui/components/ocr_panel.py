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

    # =========================
    # OCR STEP
    # =========================
    if st.button("Process image"):

        with st.spinner("Reading image..."):

            text = OCRPipeline.extract(uploaded_file)
            st.session_state["ocr_text"] = text

    text = st.session_state.get("ocr_text")

    if not text:
        return

    st.text_area(
        "Detected text",
        value=text,
        height=250
    )

    # =========================
    # SIMPLE INPUT
    # =========================
    columns = st.text_input(
        "Columns (comma separated)"
    )

    if st.button("Generate dataset"):

        df = OCRPipeline.build_dataframe(
            raw_text=text,
            columns=columns,
            context="",
            examples="",
            llm=st.session_state["llm"]
        )

        st.session_state["ocr_df"] = df

    # =========================
    # PREVIEW + SAVE
    # =========================
    df = st.session_state.get("ocr_df")

    if df is None:
        return

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    errors = OCRPipeline.validate(edited_df)

    if errors:
        for e in errors:
            st.error(e)
        return

    st.success("Dataset valid ✔")

    if st.button("Save dataset"):

        result = OCRPipeline.save(edited_df, prefix="ocr_simple")

        st.success(result["dataset_id"])
        st.rerun()