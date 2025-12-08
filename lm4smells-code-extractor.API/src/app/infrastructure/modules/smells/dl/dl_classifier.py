"""Deep Learning classifier for code smell detection."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Tuple

import numpy as np
from application.dtos.enums.dl_model import DLModel
from domain.entities.dl_classification import DLClassification
from infrastructure.config.settings import settings

from .keras3_loader import load_keras3_model


class DLClassifier:
    """Classifier using deep learning models for code smell detection."""

    # Features used by the DL model (after correlation filtering)
    FEATURE_ORDER = [
        'raw_sloc',
        'raw_multi',
        'raw_single_comments',
        'hal_func_N2',
    ]

    def __init__(self) -> None:
        """Initialize the DL classifier by loading the model."""
        self.dl_model = load_keras3_model(settings.dl_model)
        self.model_labels = self._load_labels(settings.dl_model)
        print(f'[OK] DL model loaded from {settings.dl_model}')

    def classify_methods(
        self,
        task_id: str,
        extraction_results: List[Dict[str, Any]],
        dl_model: DLModel,
    ) -> List[DLClassification]:
        """Classify methods using the DL model."""
        return self._classify_elements(task_id, extraction_results, dl_model, element_type='method')

    def classify_classes(
        self,
        task_id: str,
        extraction_results: List[Dict[str, Any]],
        dl_model: DLModel,
    ) -> List[DLClassification]:
        """Classify classes using the DL model."""
        return self._classify_elements(task_id, extraction_results, dl_model, element_type='class')

    def _classify_elements(
        self,
        task_id: str,
        extraction_results: List[Dict[str, Any]],
        dl_model: DLModel,
        *,
        element_type: str,
    ) -> List[DLClassification]:
        """Classify code elements (methods or classes)."""
        classifications: List[DLClassification] = []
        total = len(extraction_results)

        print(f"[DL Classifier] Classifying {total} {element_type}(s)...")

        for idx, result in enumerate(extraction_results, 1):
            metrics = result.get('code_metric', {}) or {}
            features = self._prepare_features(metrics)
            label, confidence = self._predict(features)

            if idx % 10 == 0 or idx == total:
                print(f"[DL Classifier] Progress: {idx}/{total} {element_type}(s) classified")

            classifications.append(
                DLClassification(
                    id=task_id,
                    file_name=result.get('file_name', ''),
                    classification=label,
                    model_used=f'DL_Keras',
                    element_name=self._get_element_name(result, element_type),
                    element_type=element_type,
                    confidence_score=confidence,
                    metrics=metrics,
                    raw_code=result.get('code', ''),
                )
            )

        print(f"[DL Classifier] Completed: {total} {element_type}(s) classified")
        return classifications

    def _prepare_features(self, metrics: Dict[str, Any]) -> Dict[str, float]:
        """Extract and prepare the 4 features needed by the model."""
        return {
            'raw_sloc': float(metrics.get('raw_sloc', metrics.get('sloc', metrics.get('loc', 0)))),
            'raw_multi': float(metrics.get('raw_multi', metrics.get('multi', 0))),
            'raw_single_comments': float(metrics.get('raw_single_comments', 0)),
            # Ensure we read the correct Halstead N2 key as mapped by the DTO layer
            'hal_func_N2': float(metrics.get('hal_func_N2', metrics.get('N2', metrics.get('n2', 0)))),
        }

    def _predict(self, features: Dict[str, float]) -> Tuple[str, float]:
        """Make prediction using the DL model."""
        vector = [features[key] for key in self.FEATURE_ORDER]
        data = np.array([vector], dtype=float)

        predictions = self.dl_model.predict(data, verbose=0)
        probabilities = predictions[0]

        if not (0.99 <= probabilities.sum() <= 1.01):
            exp_preds = np.exp(probabilities - np.max(probabilities))
            probabilities = exp_preds / exp_preds.sum()

        label_index = int(np.argmax(probabilities))
        confidence = float(probabilities[label_index])
        label = self._get_label(label_index)

        if not hasattr(self, '_low_confidence_warned') and confidence < 0.5:
            print(f"[WARN] Low confidence prediction detected ({confidence:.2%}). "
                  f"This may indicate the model needs retraining with more data or better features.")
            self._low_confidence_warned = True

        return label, confidence

    def _get_element_name(self, result: Dict[str, Any], element_type: str) -> str:
        """Extract element name from result."""
        if element_type == 'class':
            return result.get('class_name', '')
        return result.get('method_name', '')

    def _get_label(self, index: int) -> str:
        """Get label name from index."""
        if 0 <= index < len(self.model_labels):
            return self.model_labels[index]
        return str(index)

    def _resolve_model_path(self) -> str:
        """Resolve the model file path."""
        if not settings.dl_model:
            raise ValueError('DL model path not configured in settings')

        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, '..', '..', '..', '..', 'models', 'dl', settings.dl_model)
        model_path = os.path.normpath(model_path)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f'DL model not found at: {model_path}')

        return model_path

    def _load_labels(self, model_path: str) -> List[str]:
        """Load label names from labels.json file."""
        model_dir = os.path.dirname(model_path)
        labels_path = os.path.join(model_dir, 'labels.json')

        if os.path.exists(labels_path):
            try:
                with open(labels_path, 'r', encoding='utf-8') as f:
                    labels = json.load(f)
                    if isinstance(labels, list):
                        return labels
            except Exception as e:
                print(f'[WARN] Failed to load labels from {labels_path}: {e}')

        return ['long-method', 'long-parameter-list', 'non-long-method', 'non-long-parameter-list']
