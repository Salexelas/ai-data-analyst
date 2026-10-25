import os
import pandas as pd
import streamlit as st
from ui.services.relationship_service import RelationshipService

DATA_PATH = "data"

def render_relationship_panel():

    active_datasets = (
        st.session_state.get(
            "active_datasets",
            []
        )
    )

    if len(active_datasets) < 2:
        return

    st.markdown(
        "### 🔗 Dataset Relationships"
    )

    st.session_state.setdefault(
        "dataset_relations",
        []
    )

    left_dataset = st.selectbox(
        "Left Dataset",
        active_datasets
    )

    right_dataset = st.selectbox(
        "Right Dataset",
        [
            ds
            for ds in active_datasets
            if ds != left_dataset
        ]
    )

    left_columns = pd.read_csv(
        os.path.join(
            DATA_PATH,
            left_dataset
        ),
        nrows=1
    ).columns.tolist()

    right_columns = pd.read_csv(
        os.path.join(
            DATA_PATH,
            right_dataset
        ),
        nrows=1
    ).columns.tolist()

    left_column = st.selectbox(
        "Left Column",
        left_columns
    )

    right_column = st.selectbox(
        "Right Column",
        right_columns
    )

    if st.button(
        "Add Relationship"
    ):

        RelationshipService.add_relationship(
            st.session_state[
                "dataset_relations"
            ],
            left_dataset,
            left_column,
            right_dataset,
            right_column
        )

        st.rerun()