import streamlit as st
import os
from connectors.factory import create_connector

DATA_PATH = "data"


def render_datasets():

    st.title("📚 Gestión de Datasets")

    if not os.path.exists(DATA_PATH):
        st.info("No hay datasets todavía")
        return

    files = os.listdir(DATA_PATH)

    if not files:
        st.info("No hay datasets guardados")
        return

    for file in files:

        file_path = os.path.join(DATA_PATH, file)

        col1, col2, col3 = st.columns([4, 1, 1])

        # -------------------------
        # 📄 Nombre
        # -------------------------
        with col1:
            st.write(f"📄 {file}")

            if "file_path" in st.session_state and st.session_state["file_path"] == file_path:
                st.caption("🟢 Activo")

        # -------------------------
        # ▶️ CARGAR
        # -------------------------
        with col2:
            if st.button("Cargar", key=f"load_{file}"):

                file_type = "csv" if file.endswith(".csv") else "excel"

                connector = create_connector(file_type, {"file_path": file_path})

                st.session_state["connector"] = connector
                st.session_state["file_path"] = file_path

                st.success(f"Dataset activo: {file}")
                st.rerun()

        # -------------------------
        # 🗑️ ELIMINAR
        # -------------------------
        with col3:
            if st.button("🗑️", key=f"delete_{file}"):

                os.remove(file_path)

                if st.session_state.get("file_path") == file_path:
                    st.session_state.pop("connector", None)
                    st.session_state.pop("file_path", None)

                st.warning(f"{file} eliminado")
                st.rerun()

        # -------------------------
        # 👀 PREVIEW
        # -------------------------
        with st.expander(f"Preview: {file}"):

            try:
                file_type = "csv" if file.endswith(".csv") else "excel"
                connector = create_connector(file_type, {"file_path": file_path})

                preview = connector.preview()

                st.dataframe(preview, use_container_width=True)

            except Exception as e:
                st.error(f"Error preview: {e}")