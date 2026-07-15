from pydantic import BaseModel, ConfigDict, field_validator, Field

class DnsRecords(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    domain_name: str
    a: list[str] = Field(default_factory=list, alias="A")
    aaaa: list[str] = Field(default_factory=list, alias="AAAA")
    ns: list[str] = Field(default_factory=list, alias="NS")
    txt: list[str] = Field(default_factory=list, alias="TXT")
    mx: list[str] = Field(default_factory=list, alias="MX")
    cname: list[str] = Field(default_factory=list, alias="CNAME")

    @field_validator("txt", mode="before")
    @classmethod
    def parse_txt(cls, value):
        if value is None:
            return []
        return [v.strip('"') for v in value]
    
    @field_validator("a", "aaaa", "ns", "txt", "mx", "cname", mode="before")
    @classmethod
    def none_to_list(cls, value):
        return [] if value is None else value