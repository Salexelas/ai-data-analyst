import streamlit as st
from semantic.semantic_layer import build_semantic_layer
from semantic.utils import save_semantic_layer

def render_semantic():

    st.title("🧠 Capa Semántica")

    if "connector" not in st.session_state:
        st.warning("Primero cargá un dataset")
        return

    connector = st.session_state["connector"]
    columns = list(connector.preview().columns)

    # -------------------------
    # INIT SI NO EXISTE
    # -------------------------
    if "semantic_layer" not in st.session_state or st.session_state["semantic_layer"] is None:

        st.session_state["semantic_layer"] = build_semantic_layer(columns)

    sl = st.session_state["semantic_layer"]

    tabs = st.tabs([
        "🔤 Aliases",
        "📊 Métricas",
        "🧪 Test"
    ])

    # -------------------------
    # 🔤 ALIASES
    # -------------------------
    with tabs[0]:

        st.subheader("Aliases por columna")

        for col in columns:

            current = sl["aliases"].get(col, [])

            key = f"alias_{col}"

            if key not in st.session_state:
                st.session_state[key] = ", ".join(current)

            value = st.text_input(f"{col}", key=key)

            sl["aliases"][col] = [v.strip() for v in value.split(",") if v]

    # -------------------------
    # 📊 METRICS
    # -------------------------
    with tabs[1]:

        st.subheader("Métricas")

        for k, v in list(sl["metrics"].items()):

            key = f"metric_{k}"

            if key not in st.session_state:
                st.session_state[key] = v

            new_val = st.text_input(k, key=key)
            sl["metrics"][k] = new_val

        st.markdown("### ➕ Nueva métrica")

        new_name = st.text_input("Nombre métrica")
        new_expr = st.text_input("SQL")

        if st.button("Agregar métrica"):
            if new_name and new_expr:
                sl["metrics"][new_name] = new_expr
                st.success(f"✅ {new_name} agregada")

    # -------------------------
    # 🧪 TEST (simple)
    # -------------------------
    with tabs[2]:

        st.subheader("Test rápido")

        st.json(sl)

    # -------------------------
    # SAVE
    # -------------------------
    if st.button("💾 Guardar capa semántica"):

        save_semantic_layer(
            st.session_state["dataset_id"],
            sl
        )

        st.success("✅ Guardado")

    # persistencia final
    st.session_state["semantic_layer"] = sl