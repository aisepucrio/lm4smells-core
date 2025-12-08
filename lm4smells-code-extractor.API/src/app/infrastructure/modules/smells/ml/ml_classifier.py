from __future__ import annotations

import os
from typing import Any, Dict, List

from application.dtos.enums.ml_model import MLModel
from domain.entities.ml_classification import MLClassification
from infrastructure.config.settings import settings
from pycaret.classification import load_model as pycaret_load_model
from pycaret.classification import predict_model as pycaret_predict_model
import pandas as pd


class MLClassifier:
    def classify_methods(
        self,
        task_id: str,
        extraction_results: List[Dict[str, Any]],
        ml_model: MLModel,
        analyse_type: str,
    ) -> List[MLClassification]:
        return self._classify_elements(task_id, extraction_results, ml_model, analyse_type, element_type='method')

    def classify_classes(
        self,
        task_id: str,
        extraction_results: List[Dict[str, Any]],
        ml_model: MLModel,
        analyse_type: str,
    ) -> List[MLClassification]:
        return self._classify_elements(task_id, extraction_results, ml_model, analyse_type, element_type='class')

    def _classify_elements(
        self,
        task_id: str,
        extraction_results: List[Dict[str, Any]],
        ml_model: MLModel,
        analyse_type: str,
        *,
        element_type: str,
    ) -> List[MLClassification]:
        classifications: List[MLClassification] = []

        model_path = self._choose_models(analyse_type.value, ml_model)
        model = pycaret_load_model(model_path)

        for result in extraction_results:
            metrics: Dict[str, Any] = result.get("code_metric", {}) or {}
            data = pd.DataFrame([metrics])

            pred_df = pycaret_predict_model(model, data=data, verbose=False)

            prediction = pred_df["prediction_label"].iloc[0]
            
            if "prediction_score" in pred_df.columns:
                confidence = float(pred_df["prediction_score"].iloc[0])
            else:
                try:
                    conf_raw = model.decision_function(data)[0]
                    confidence = float(abs(conf_raw))
                except Exception:
                    confidence = 0.0

            classifications.append(
                MLClassification(
                    id=task_id,
                    file_name=result.get('file_name', ''),
                    classification=str(prediction),
                    model_used=f'ML_{ml_model.value}',
                    element_name=self._get_element_name(result, element_type),
                    element_type=element_type,
                    confidence_score=confidence,
                    metrics=metrics,
                )
            )

        return classifications

    def _get_element_name(self, result: Dict[str, Any], element_type: str) -> str:
        """Extract element name from result."""
        if element_type == 'class':
            return result.get('class_name', '')
        return result.get('method_name', '')
    

    def _long_method(self, ml_model: MLModel):
        match ml_model:
            case MLModel.LGBM:
                return settings.lgbm_lm_model
            case MLModel.KNN:
                return settings.knn_lm_model
            case MLModel.LDA:
                return settings.lda_lm_model
            case MLModel.RIDGE:
                return settings.ridge_lm_model
            case MLModel.SGD:
                return settings.sgd_lm_model
            case _:
                raise ValueError(f"Unsupported ML model for long method: {ml_model}")

    def _long_parameter_list(self, ml_model: MLModel):
        match ml_model:
            case MLModel.GAUSSIAN:
                return settings.gaussian_lpl_model
            case MLModel.KNN:
                return settings.knn_lpl_model
            case MLModel.LGBM:
                return settings.lgbm_lpl_model
            case MLModel.QDA:
                return settings.qda_lpl_model
            case MLModel.SGD:
                return settings.sgd_lpl_model
            case _:
                raise ValueError(f"Unsupported ML model for long parameter list: {ml_model}")

    def _large_class(self, ml_model: MLModel):
        match ml_model:
            case MLModel.LGBM:
                return settings.lgbm_lc_model
            case MLModel.KNN:
                return settings.knn_lc_model
            case MLModel.LDA:
                return settings.lda_lc_model
            case MLModel.RIDGE:
                return settings.ridge_lc_model
            case MLModel.IR:
                return settings.ir_lc_model
            case _:
                raise ValueError(f"Unsupported ML model for large class: {ml_model}")



    def _choose_models(self, analyse_type: str, ml_model: MLModel):
        if analyse_type == "long-method":
            return self._long_method(ml_model)
        
        if analyse_type == "long-parameter-list":
            return self._long_parameter_list(ml_model)
        
        if analyse_type == "large-class":
            return self._large_class(ml_model)
