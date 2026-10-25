import streamlit as st

from semantic.semantic_layer import build_semantic_layer
from semantic.utils import save_semantic_layer


def render_aliases(columns, sl):

    st.subheader("Aliases por columna")

    for col in columns:

        current = sl["aliases"].get(col, [])

        key = f"alias_{col}"

        if key not in st.session_state:
            st.session_state[key] = ", ".join(current)

        value = st.text_input(
            col,
            key=key,
        )

        sl["aliases"][col] = [
            v.strip()
            for v in value.split(",")
            if v
        ]


def session_text_input(label, key, default):

    st.session_state.setdefault(
        key,
        default,
    )

    return st.text_input(
        label,
        key=key,
    )


def render_metrics(sl):

    st.subheader("Métricas")

    for name, value in sl["metrics"].items():

        sl["metrics"][name] = session_text_input(
            name,
            f"metric_{name}",
            value,
        )

    st.markdown("### ➕ Nueva métrica")

    new_name = st.text_input(
        "Nombre métrica"
    )

    new_expr = st.text_input(
        "SQL"
    )

    if (
        st.button("Agregar métrica")
        and new_name
        and new_expr
    ):
        sl["metrics"][new_name] = new_expr

        st.success(
            f"✅ {new_name} agregada"
        )


def render_semantic():

    st.title("🧠 Capa Semántica")

    if "connector" not in st.session_state:
        st.warning("Primero cargá un dataset")
        return

    connector = st.session_state["connector"]
    columns = list(connector.preview().columns)

    if (
        "semantic_layer" not in st.session_state
        or st.session_state["semantic_layer"] is None
    ):
        st.session_state["semantic_layer"] = (
            build_semantic_layer(columns)
        )

    sl = st.session_state["semantic_layer"]

    tabs = st.tabs(
        [
            "🔤 Aliases",
            "📊 Métricas",
            "🧪 Test",
        ]
    )

    with tabs[0]:
        render_aliases(
            columns,
            sl,
        )

    with tabs[1]:
        render_metrics(sl)

    with tabs[2]:

        st.subheader("Test rápido")

        st.json(sl)

    if st.button("💾 Guardar capa semántica"):

        save_semantic_layer(
            st.session_state["dataset_id"],
            sl,
        )

        st.success("✅ Guardado")

    st.session_state["semantic_layer"] = sl