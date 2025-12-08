from infrastructure.repositories.dl_classification_repository import DLClassificationRepository

class HandleDlCodesUseCase:
    def __init__(self):
        self.repository = DLClassificationRepository()

    def execute(self):
        try:
            classifications = self.repository.get_all()
            return {
                "message": "DL codes retrieved successfully",
                "data": classifications,
                "count": len(classifications)
            }
        except Exception as e:
            return {
                "message": f"Error retrieving DL codes: {str(e)}",
                "data": [],
                "count": 0
            }

    def get_by_file_name(self, file_name: str):
        try:
            classifications = self.repository.get_by_file_name(file_name)
            return {
                "message": f"DL codes for file '{file_name}' retrieved successfully",
                "data": classifications,
                "count": len(classifications)
            }
        except Exception as e:
            return {
                "message": f"Error retrieving DL codes for file '{file_name}': {str(e)}",
                "data": [],
                "count": 0
            }