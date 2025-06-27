from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# Schemas for SubIssue model
class SubIssueBase(BaseModel):
    description: str
    solution: str
    sample_response: str
    references: Optional[str] = None


class SubIssueCreate(SubIssueBase):
    pass


class SubIssueUpdate(SubIssueBase):
    description: Optional[str] = None
    solution: Optional[str] = None
    sample_response: Optional[str] = None
    references: Optional[str] = None


class SubIssue(SubIssueBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Schemas for Issue model
class IssueBase(BaseModel):
    service_name: str
    description: str
    mcp_url: str


class IssueCreate(IssueBase):
    pass


class IssueUpdate(IssueBase):
    service_name: Optional[str] = None
    description: Optional[str] = None
    mcp_url: Optional[str] = None


class Issue(IssueBase):
    id: int
    sub_issues: List[SubIssue] = []

    model_config = ConfigDict(from_attributes=True)