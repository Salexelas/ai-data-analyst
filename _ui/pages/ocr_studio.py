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

    if st.button("Run OCR"):

        with st.spinner("Processing OCR..."):
            st.session_state["ocr_text"] = OCRPipeline.extract(
                uploaded_file
            )

    text = st.session_state.get("ocr_text")

    if not text:
        return

    editable_text = st.text_area(
        "Edit extracted text",
        value=text,
        height=300
    )

    context = st.text_input(
        "Context (domain / type of document)"
    )

    columns = st.text_input(
        "Columns (comma separated)"
    )

    examples = st.text_area(
        "Examples (optional)"
    )

    generate_dataset(
        editable_text,
        columns,
        context,
        examples
    )

    preview_dataset()


def generate_dataset(
    editable_text,
    columns,
    context,
    examples
):

    if not st.button("Generate dataset"):
        return

    st.session_state["ocr_df"] = OCRPipeline.build_dataframe(
        raw_text=editable_text,
        columns=columns,
        context=context,
        examples=examples,
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

    errors = OCRPipeline.validate(edited_df)

    if errors:
        for error in errors:
            st.error(error)
        return

    st.success("Dataset valid ✔")

    if not st.button("Save dataset"):
        return

    result = OCRPipeline.save(
        edited_df,
        prefix="ocr_studio"
    )

    st.success(result["dataset_id"])
    st.rerun()