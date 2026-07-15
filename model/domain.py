from pydantic import BaseModel, field_validator
import re 

DOMAIN_RE = re.compile(
    r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))+$"  #domain name pattern for validation of a domain 
)

class Domain(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_domain(cls, dom):
        if not DOMAIN_RE.match(dom):
            raise ValueError("Not valid Doamin")
        return dom.lower()
