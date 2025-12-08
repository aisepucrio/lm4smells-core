"""
Keras 3.x model loader for backward compatibility.
This module handles the complexity of loading Keras 3.x models in Keras 2.x/TensorFlow 2.x environments.
"""
from __future__ import annotations

import json
import os
import tempfile
import zipfile
from typing import Any, Dict

import tensorflow as tf


@tf.keras.utils.register_keras_serializable(package="Custom", name="CastToFloat32")
class CastToFloat32Layer(tf.keras.layers.Layer):
    """Custom layer to cast inputs to float32."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def call(self, inputs, *args, **kwargs):
        return tf.cast(inputs, tf.float32)

    def get_config(self) -> Dict[str, Any]:
        return super().get_config()


def load_keras3_model(model_path: str) -> tf.keras.Model:
    """
    Load a Keras 3.x model from a .keras archive file.

    Args:
        model_path: Path to the .keras model file

    Returns:
        Loaded Keras model

    Raises:
        RuntimeError: If model loading fails
    """
    try:
        # First, try standard loading
        return tf.keras.models.load_model(
            model_path,
            custom_objects={'CastToFloat32': CastToFloat32Layer},
            compile=False
        )
    except (OSError, Exception):
        # Fall back to manual loading for Keras 3.x format
        pass

    if not (model_path.lower().endswith('.keras') and zipfile.is_zipfile(model_path)):
        raise RuntimeError(f"Cannot load model from {model_path}")

    return _load_from_keras3_archive(model_path)


def _load_from_keras3_archive(archive_path: str) -> tf.keras.Model:
    """Load model from Keras 3.x .keras archive format."""
    import h5py

    # Extract config and weights
    try:
        with zipfile.ZipFile(archive_path, 'r') as archive:
            config_bytes = archive.read('config.json')
            weights_bytes = archive.read('model.weights.h5')
    except KeyError as exc:
        raise RuntimeError(f'Invalid Keras archive: missing {exc}') from exc

    config = json.loads(config_bytes.decode('utf-8'))

    # Build model from config
    model = _build_model_from_config(config)

    # Load weights
    with tempfile.NamedTemporaryFile(suffix='.h5', delete=False) as tmp_file:
        tmp_file.write(weights_bytes)
        weights_path = tmp_file.name

    try:
        with h5py.File(weights_path, 'r') as h5_file:
            _load_weights(model, h5_file)
    finally:
        try:
            os.remove(weights_path)
        except OSError:
            pass

    return model


def _build_model_from_config(config: Dict[str, Any]) -> tf.keras.Model:
    """Build Keras model from configuration."""
    layers_config = config.get('config', {}).get('layers', [])
    if not layers_config:
        raise RuntimeError("No layers found in model config")

    # Build layers
    layers_dict = {}
    for layer_data in layers_config:
        layer_class = layer_data.get('class_name')
        layer_name = layer_data.get('name')
        layer_config = _clean_layer_config(layer_data.get('config', {}), layer_class)

        if layer_class == 'InputLayer':
            shape = layer_config.get('batch_shape', [None, 4])
            input_shape = shape[1:] if isinstance(shape, list) and len(shape) > 1 else [4]
            layers_dict[layer_name] = tf.keras.Input(shape=input_shape, name=layer_name)
        elif layer_class == 'CastToFloat32':
            layers_dict[layer_name] = CastToFloat32Layer(name=layer_name)
        elif hasattr(tf.keras.layers, layer_class):
            layer_cls = getattr(tf.keras.layers, layer_class)
            layers_dict[layer_name] = layer_cls(**layer_config)
        else:
            raise RuntimeError(f"Unknown layer: {layer_class}")

    # Connect layers
    x = None
    for layer_data in layers_config:
        layer_name = layer_data.get('name')
        layer_class = layer_data.get('class_name')
        layer = layers_dict[layer_name]

        if layer_class == 'InputLayer':
            x = layer
        elif x is not None:
            x = layer(x)

    # Create model
    input_layer = layers_config[0]['name']
    return tf.keras.Model(inputs=layers_dict[input_layer], outputs=x)


def _clean_layer_config(config: Dict[str, Any], layer_class: str) -> Dict[str, Any]:
    """Clean layer config by removing incompatible parameters."""
    cleaned = config.copy()
    cleaned.pop('batch_shape', None)
    cleaned.pop('batch_input_shape', None)

    if 'dtype' in cleaned and isinstance(cleaned['dtype'], dict):
        cleaned['dtype'] = 'float32'

    if layer_class == 'BatchNormalization':
        cleaned.pop('synchronized', None)

    return cleaned


def _load_weights(model: tf.keras.Model, h5_file) -> None:
    """Load weights from Keras 3.x H5 format."""
    if 'layers' not in h5_file.keys():
        return

    layers_group = h5_file['layers']

    for layer in model.layers:
        if len(layer.weights) == 0:
            continue

        if layer.name not in layers_group:
            continue

        layer_group = layers_group[layer.name]
        if 'vars' not in layer_group:
            continue

        vars_group = layer_group['vars']
        weight_values = []

        for i in range(len(layer.weights)):
            if str(i) in vars_group:
                weight_values.append(vars_group[str(i)][()])

        if weight_values:
            try:
                layer.set_weights(weight_values)
            except Exception:
                pass 
