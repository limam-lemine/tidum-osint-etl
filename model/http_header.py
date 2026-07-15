from datetime import datetime
from email.utils import parsedate_to_datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional


class Header(BaseModel):
    
    model_config = ConfigDict(populate_by_name=True)

    location: Optional[str] = None
    #since http headers uses '-' and python attributes dont, we use Field() to alias them 
    content_type: Optional[str] = Field(None, alias="content-type")
    content_security_policy_report_only: Optional[str] = Field(None, alias="content-security-policy-report-only")
    date : Optional[datetime] = None
    expires: Optional[str] = None
    cache_control: Optional[str] = Field(None, alias="cache-control")
    server: Optional[str] = None
    content_length: Optional[str] = Field(None, alias="content-length")
    x_xss_protection: Optional[str] = Field(None, alias="x-xss-protection")
    x_frame_options: Optional[str] = Field(None, alias="x-frame-options")
    alt_svc: Optional[str] = Field(None, alias="alt-svc")

    #redirection history
    final_url: Optional[str] = None
    nbr_redirection: int = 0

    #convert to datetime
    @field_validator("date", mode="before")
    @classmethod
    def parse_to_datetime(cls, val):
        if isinstance(val, str):
            return parsedate_to_datetime(val)
        return val