from infrastructure.repositories.ml_classification_repository import MLClassificationRepository

class HandleMlCodesUseCase:
    def __init__(self):
        self.repository = MLClassificationRepository()

    def execute(self):
        try:
            classifications = self.repository.get_all()
            return {
                "message": "ML codes retrieved successfully",
                "data": classifications,
                "count": len(classifications)
            }
        except Exception as e:
            return {
                "message": f"Error retrieving ML codes: {str(e)}",
                "data": [],
                "count": 0
            }

    def get_by_file_name(self, file_name: str):
        try:
            classifications = self.repository.get_by_file_name(file_name)
            return {
                "message": f"ML codes for file '{file_name}' retrieved successfully",
                "data": classifications,
                "count": len(classifications)
            }
        except Exception as e:
            return {
                "message": f"Error retrieving ML codes for file '{file_name}': {str(e)}",
                "data": [],
                "count": 0
            }