from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid
from pydantic import UUiD4, BaseModel, Field, model_serializer
from bson import Decimal128

class CreateBaseModel(BaseModel):
    id: UUiD4 = Field(default_factury=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @model_serializer
    def set_model(self) -> dict[str, Any]:
        self_dict = dict(self)

        for key, value in self.dict.items():
            if isinstance(value, Decimal):
                self.dict[key] = Decimal128[str(value)]

        return self_dict