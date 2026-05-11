import streamlit as st
import os

from connectors.factory import create_connector

DATA_PATH = "data"


# =========================
# HELPERS
# =========================

def detect_file_type(file):

    if file.endswith(".csv"):
        return "csv"

    elif file.endswith(".xlsx"):
        return "excel"

    return None


def load_dataset(file, file_path):

    file_type = detect_file_type(file)

    if not file_type:
        raise ValueError(
            "Formato no soportado"
        )

    connector = create_connector(
        file_type,
        {"file_path": file_path}
    )

    st.session_state["connector"] = connector

    st.session_state["file_path"] = file_path

    st.session_state["dataset_id"] = file

    return connector


# =========================
# PAGE
# =========================

def render_datasets():

    st.title("📚 Gestión de Datasets")

    # -------------------------
    # VALIDATE FOLDER
    # -------------------------
    if not os.path.exists(DATA_PATH):

        st.info(
            "No hay datasets todavía"
        )

        return

    # -------------------------
    # FILES
    # -------------------------
    files = sorted(
        os.listdir(DATA_PATH),
        reverse=True
    )

    if not files:

        st.info(
            "No hay datasets guardados"
        )

        return

    st.markdown("---")

    # -------------------------
    # LOOP
    # -------------------------
    for file in files:

        file_path = os.path.join(
            DATA_PATH,
            file
        )

        # 🔥 5 columnas ahora
        col1, col2, col3, col4, col5 = st.columns(
            [4, 1, 1, 1, 1]
        )

        # ==================================================
        # FILE NAME
        # ==================================================
        with col1:

            st.write(f"📄 {file}")

            current_file = st.session_state.get(
                "file_path"
            )

            if current_file == file_path:

                st.caption(
                    "🟢 Dataset activo"
                )

        # ==================================================
        # LOAD
        # ==================================================
        with col2:

            if st.button(
                "Cargar",
                key=f"load_{file}"
            ):

                try:

                    load_dataset(
                        file,
                        file_path
                    )

                    st.success(
                        f"✅ Dataset activo: {file}"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Error cargando dataset: {e}"
                    )

        # ==================================================
        # EDIT
        # ==================================================
        with col3:

            if st.button(
                "Editar",
                key=f"edit_{file}"
            ):

                try:

                    load_dataset(
                        file,
                        file_path
                    )

                    st.session_state.page = (
                        "dataset_editor"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Error editor: {e}"
                    )

        # ==================================================
        # INFO
        # ==================================================
        with col4:

            if st.button(
                "📊 Info",
                key=f"info_{file}"
            ):

                try:

                    load_dataset(
                        file,
                        file_path
                    )

                    st.session_state.page = (
                        "dataset_info"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Error info: {e}"
                    )

        # ==================================================
        # DELETE
        # ==================================================
        with col5:

            if st.button(
                "🗑️",
                key=f"delete_{file}"
            ):

                try:

                    os.remove(file_path)

                    current_file = st.session_state.get(
                        "file_path"
                    )

                    if current_file == file_path:

                        st.session_state["connector"] = None

                        st.session_state["file_path"] = None

                        st.session_state["dataset_id"] = None

                        st.session_state[
                            "semantic_layer"
                        ] = None

                    st.warning(
                        f"🗑️ {file} eliminado"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Error eliminando: {e}"
                    )

        # ==================================================
        # PREVIEW
        # ==================================================
        with st.expander(
            f"Preview: {file}"
        ):

            try:

                connector = create_connector(
                    detect_file_type(file),
                    {"file_path": file_path}
                )

                preview = connector.preview()

                st.dataframe(
                    preview,
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"Error preview: {e}"
                )