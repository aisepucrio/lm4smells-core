from enum import Enum

class PromptType(str, Enum):
    zero_shot_chain_of_thought = "zero-shot-chain-of-thought"
    zero_shot = "zero-shot"

