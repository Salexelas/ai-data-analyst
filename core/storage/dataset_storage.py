import os

DATA_PATH = "data"

os.makedirs(
    DATA_PATH,
    exist_ok=True
)


class DatasetStorage:

    @staticmethod
    def list_available():

        if not os.path.exists(DATA_PATH):
            return []

        return sorted(
            os.listdir(DATA_PATH)
        )

    @staticmethod
    def get_path(
        dataset_name: str
    ):

        return os.path.join(
            DATA_PATH,
            dataset_name
        )

    @staticmethod
    def save_uploaded_file(
        uploaded_file
    ):

        file_path = os.path.join(
            DATA_PATH,
            uploaded_file.name
        )

        with open(
            file_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )

        return file_path

    @staticmethod
    def save_dataframe(
        dataframe,
        filename
    ):

        file_path = os.path.join(
            DATA_PATH,
            filename
        )

        dataframe.to_csv(
            file_path,
            index=False
        )

        return file_path