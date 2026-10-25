from ui.core.chat_session import (
    DatasetRelationship
)


class RelationshipService:

    @staticmethod
    def add_relationship(
        relations: list,
        left_dataset: str,
        left_column: str,
        right_dataset: str,
        right_column: str
    ):

        relations.append(
            DatasetRelationship(
                left_dataset=left_dataset,
                left_column=left_column,
                right_dataset=right_dataset,
                right_column=right_column
            )
        )