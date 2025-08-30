from enum import Enum

class LMModels(str, Enum):
    gemma2_2b = "gemma2:2b"
    gpt_4o_mini = "gpt-4o-mini"
    mistral_latest = "mistral:latest"
    deepseek1_5b="deepseek-r1:1.5b"
    qwen2_5_coder_1_5b="qwen2.5-coder:1.5b"
    gpt_4o      = "gpt-4o"
    codellama_7b="codellama:7b"