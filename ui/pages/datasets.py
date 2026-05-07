import streamlit as st
import os

from connectors.factory import create_connector

DATA_PATH = "data"


def render_datasets():

    st.title("📚 Gestión de Datasets")

    # -------------------------
    # VALIDATE DATA FOLDER
    # -------------------------
    if not os.path.exists(DATA_PATH):

        st.info("No hay datasets todavía")
        return

    # -------------------------
    # FILES
    # -------------------------
    files = os.listdir(DATA_PATH)

    if not files:

        st.info("No hay datasets guardados")
        return

    # -------------------------
    # DATASETS LOOP
    # -------------------------
    for file in files:

        file_path = os.path.join(DATA_PATH, file)

        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

        # ==================================================
        # 📄 FILE NAME
        # ==================================================
        with col1:

            st.write(f"📄 {file}")

            current_file = st.session_state.get("file_path")

            if current_file == file_path:

                st.caption("🟢 Dataset activo")

        # ==================================================
        # ▶️ LOAD DATASET
        # ==================================================
        with col2:

            if st.button(
                "Cargar",
                key=f"load_{file}"
            ):

                try:

                    # -------------------------
                    # Detect type
                    # -------------------------
                    if file.endswith(".csv"):

                        file_type = "csv"

                    elif file.endswith(".xlsx"):

                        file_type = "excel"

                    else:

                        st.error("Formato no soportado")
                        st.stop()

                    # -------------------------
                    # Create connector
                    # -------------------------
                    connector = create_connector(
                        file_type,
                        {"file_path": file_path}
                    )

                    # -------------------------
                    # Session state
                    # -------------------------
                    st.session_state["connector"] = connector
                    st.session_state["file_path"] = file_path
                    st.session_state["dataset_id"] = file

                    st.success(f"✅ Dataset activo: {file}")

                    st.rerun()

                except Exception as e:

                    st.error(f"Error cargando dataset: {e}")

        # ==================================================
        # ✏️ EDIT DATASET
        # ==================================================
        with col3:

            if st.button(
                "Editar",
                key=f"edit_{file}"
            ):

                try:

                    # -------------------------
                    # Detect type
                    # -------------------------
                    if file.endswith(".csv"):

                        file_type = "csv"

                    elif file.endswith(".xlsx"):

                        file_type = "excel"

                    else:

                        st.error("Formato no soportado")
                        st.stop()

                    # -------------------------
                    # Create connector
                    # -------------------------
                    connector = create_connector(
                        file_type,
                        {"file_path": file_path}
                    )

                    # -------------------------
                    # Session state
                    # -------------------------
                    st.session_state["connector"] = connector
                    st.session_state["file_path"] = file_path
                    st.session_state["dataset_id"] = file

                    # ⚠️ change page
                    st.session_state.page = "dataset_editor"

                    st.rerun()

                except Exception as e:

                    st.error(f"Error abriendo editor: {e}")

        # ==================================================
        # 🗑️ DELETE DATASET
        # ==================================================
        with col4:

            if st.button(
                "🗑️",
                key=f"delete_{file}"
            ):

                try:

                    os.remove(file_path)

                    # -------------------------
                    # Clear active dataset
                    # -------------------------
                    current_file = st.session_state.get("file_path")

                    if current_file == file_path:

                        st.session_state["connector"] = None
                        st.session_state["file_path"] = None
                        st.session_state["dataset_id"] = None
                        st.session_state["semantic_layer"] = None

                    st.warning(f"🗑️ {file} eliminado")

                    st.rerun()

                except Exception as e:

                    st.error(f"Error eliminando dataset: {e}")

        # ==================================================
        # 👀 PREVIEW
        # ==================================================
        with st.expander(f"Preview: {file}"):

            try:

                # -------------------------
                # Detect type
                # -------------------------
                if file.endswith(".csv"):

                    file_type = "csv"

                elif file.endswith(".xlsx"):

                    file_type = "excel"

                else:

                    st.error("Formato no soportado")
                    continue

                # -------------------------
                # Connector
                # -------------------------
                connector = create_connector(
                    file_type,
                    {"file_path": file_path}
                )

                preview = connector.preview()

                st.dataframe(
                    preview,
                    use_container_width=True
                )

            except Exception as e:

                st.error(f"Error preview: {e}")