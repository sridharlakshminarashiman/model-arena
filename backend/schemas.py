from enum import Enum
from typing import Optional
from pydantic import BaseModel

class Category(str, Enum):
    '''Valid ticket categories.
    Inherting from str means Pydantic serializes this to a plain string in JSON.'''
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    SHIPPING = "shipping"
    OTHER = "other"

class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ClassificationOutput(BaseModel):
    '''The structured JSON output we expect from the model.
    This is what we parse the raw model response into.'''
    category: Category
    urgency: Urgency
    recommendation_action: str

class ModelResult(BaseModel):
    '''One model's attempt at classifying one support ticket
    output is optional because we may not be able to parse the model's raw response into structured JSON. 
    But we still want to keep the raw response from the model - the latency, and what it actually said.'''
    model_name: str
    latency_ms: float
    raw_response: str
    valid: bool
    output: Optional[ClassificationOutput] = None

class RunRequest(BaseModel):
    '''What the front-end sends when trigeering a battle.
    ground_truth is optional - you may not always have a cerified answer.'''
    ticket_text: str
    ground_truth: Optional[ClassificationOutput]= None

# # Tesing my Schema
# if __name__=="__main__":
#     # this should succeed
#     result = ModelResult(
#         model_name = "qwen3:8b,",
#         latency_ms = 1234.5,
#         raw_response = '{"category": "billing", "urgency": "high", "recommendation_action": "Escalate"}',
#         valid = True,
#         output = ClassificationOutput(
#             category=Category.BILLING,
#             urgency=Urgency.HIGH,
#             recommendation_action="Escalate to billing team immediately"
#         )
#     )
#     print("Valid results", result.model_name, result.output.category)
#     print("JSON:", result.model_dump_json(indent=2))