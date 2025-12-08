from typing import Any, Dict, List
from fastapi import UploadFile
from application.dtos.enums.dl_model import DLModel
from application.dtos.enums.extract_type import ExtractType


class DLOperationInput:
    def __init__(self, file_contents: List[str], file_names: List[str], extract_type: ExtractType, analyse_type, dl_model: DLModel, task_id: str):
        self.file_contents = file_contents
        self.file_names = file_names
        self.extract_type = extract_type
        self.analyse_type = analyse_type
        self.dl_model = dl_model
        self.programming_language = ["python"] * len(file_names)
        self.task_id = task_id

    @classmethod
    async def process_files(
        cls,
        files: List[UploadFile],
        extract_type: ExtractType,
        analyse_type,
        dl_model: DLModel,
        task_id
    ):
        raw_file_content = [await file.read() for file in files]
        decoded_file_content = [content.decode("utf-8") for content in raw_file_content]
        file_names = [file.filename for file in files]

        return cls(
            file_contents=decoded_file_content,
            file_names=file_names,
            extract_type=extract_type,
            analyse_type=analyse_type,
            dl_model=dl_model,
            task_id=task_id
        )

    @property
    def respective_codes(self) -> List[Dict[str, str]]:
        return [
            {
                "file_name": fname,
                "code": fcode,
                "programming_language": planguage,
            }
            for fname, fcode, planguage in zip(self.file_names, self.file_contents, self.programming_language)
        ]

    @staticmethod
    def map_metrics_to_dl_input(extraction_results: List[Dict[str, Any]]) -> None:
        """Map extracted metrics to DL model input format (same as ML format)."""
        for result in extraction_results:
            metrics = result.get('code_metric', {}) or {}

            raw = metrics.get('raw', {}) or {}
            if isinstance(raw, dict) and 'sloc' not in raw:
                raw = raw.get('-', next(iter(raw.values()), {}))

            hal = metrics.get('hal') or {}
            if isinstance(hal, dict):
                hal = hal.get('-', {})
                hal_total = hal.get('total', {})
            else:
                hal_total = {}

            mapped = {
                'raw_sloc': raw.get('sloc', 0),
                'raw_multi': raw.get('multi', 0),
                'raw_blank': raw.get('blank', 0),
                'raw_single_comments': raw.get('single_comments', raw.get('comments', 0)),
                'hal_func_N2': hal_total.get('N2', hal_total.get('n2', 0)),
                'hal_func_vocabulary': hal_total.get('vocabulary', 0),
                'hal_func_length': hal_total.get('length', 0),
                'hal_func_calculated_length': hal_total.get('calculated_length', 0),
                'hal_func_volume': hal_total.get('volume', 0),
                'hal_func_difficulty': hal_total.get('difficulty', 0),
                'hal_func_effort': hal_total.get('effort', 0),
                'hal_func_time': hal_total.get('time', 0),
                'hal_func_bugs': hal_total.get('bugs', 0),
            }

            result['code_metric'] = mapped
