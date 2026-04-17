import streamlit as st

from semantic.semantic_layer import build_semantic_layer, merge_semantic_layers
from semantic.semantic_agent import generate_semantic_suggestions
from semantic.utils import (
    save_semantic_layer,
    list_semantic_files,
    load_semantic_file
)

def render_semantic_ui(connector):

    preview = connector.preview()
    columns = list(preview.columns)

    st.subheader("🧠 Columnas")
    st.write(columns)

    st.subheader("📊 Tipos")
    st.write(preview.dtypes)

    # -------------------------
    # MULTI SEMANTIC
    # -------------------------

    st.subheader("🧠 Usar Semantic Layers existentes")

    semantic_files = list_semantic_files()

    if semantic_files:

        col1, col2 = st.columns(2)

        with col1:
            sem1_name = st.selectbox("Semantic 1", ["None"] + semantic_files)

        with col2:
            sem2_name = st.selectbox("Semantic 2", ["None"] + semantic_files)

        if st.button("📥 Aplicar Semantic Layers"):

            sem1 = load_semantic_file(sem1_name) if sem1_name != "None" else None
            sem2 = load_semantic_file(sem2_name) if sem2_name != "None" else None

            merged = merge_semantic_layers(sem1, sem2)

            st.session_state["semantic_layer"] = merged

            st.success("✅ Semantic layers aplicadas")
            st.json(merged)

    # -------------------------
    # GENERAR
    # -------------------------

    st.subheader("✨ Generar nueva semántica")

    if st.button("Generar automáticamente"):
        raw = generate_semantic_suggestions(columns,st.session_state["llm"])

        st.session_state["semantic_layer"] = build_semantic_layer(
            columns,
            raw.get("aliases"),
            raw.get("metrics")
        )

        st.success("✅ Generada")

    # -------------------------
    # EDITAR
    # -------------------------

    if "semantic_layer" in st.session_state:

        sl = st.session_state["semantic_layer"]

        st.write("### 🔤 Aliases")
        st.json(sl["aliases"])

        st.write("### 📊 Métricas")
        st.json(sl["metrics"])

        st.write("### ✏️ Editar Aliases")

        for col in columns:
            current = sl["aliases"].get(col, [])
            key_name = f"alias_{col}"

            if key_name not in st.session_state:
                st.session_state[key_name] = ", ".join(current)

            value = st.text_input(col, key=key_name)
            sl["aliases"][col] = [v.strip() for v in value.split(",") if v]

        st.write("### ✏️ Editar Métricas")

        for k, v in list(sl["metrics"].items()):
            key_name = f"metric_{k}"

            if key_name not in st.session_state:
                st.session_state[key_name] = v

            new_val = st.text_input(k, key=key_name)
            sl["metrics"][k] = new_val

        # AGREGAR
        st.write("### ➕ Nueva Métrica")

        new_name = st.text_input("Nombre")
        new_expr = st.text_input("SQL")

        if st.button("Agregar métrica"):
            if new_name and new_expr:
                sl["metrics"][new_name] = new_expr
                st.success(f"✅ {new_name} agregada")

        # GUARDAR
        if st.button("💾 Guardar capa semántica"):
            save_semantic_layer(
                st.session_state["dataset_id"],
                sl
            )
            st.success("✅ Guardado")

        st.session_state["semantic_layer"] = sl