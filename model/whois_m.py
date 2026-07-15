from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class Whois(BaseModel):
    domain_name: str
    registrar: Optional[str] = None
    registrar_url: Optional[str] = None
    reseller: Optional[str] = None
    whois_server: Optional[str] = None
    referral_url: Optional[str] = None
    updated_date: Optional[datetime] = None
    creation_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    name_servers: list[str] = [] 
    status: list[str] = []
    emails: list[EmailStr] = []
    dnssec: Optional[str] = None
    name: Optional[str] = None
    org: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    registrant_postal_code: Optional[str] = None
    country: Optional[str] = None
    tech_name: Optional[str] = None
    tech_org: Optional[str] = None
    admin_name: Optional[str] = None
    admin_org: Optional[str] = None

    #we take the last date
    @field_validator("updated_date", "creation_date", "expiration_date", mode="before")
    @classmethod
    def extract_last_date(cls, val) :
        if isinstance(val, list):
            return val[-1]
        return val
    
    # dynamiclly handles the values
    @field_validator("status", "emails", mode="before")
    @classmethod
    def set_status(cls, value):
        if isinstance(value, str):  # if we get single value we cast it to a list
            return [value]
        return value
    
    @field_validator("registrar_url", "org", "address", "city", "registrant_postal_code", mode="before")
    @classmethod
    def set_list_field(cls, value):
        if isinstance(value, list):
            return value[-1] if value else None # if we get a list we return the last element
        return value
    
    