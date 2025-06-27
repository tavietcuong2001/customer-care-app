from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db import Base


class Issue(Base):
    __tablename__ = 'issues'
    
    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    mcp_url = Column(String(255), nullable=False)

    sub_issues = relationship("SubIssue", back_populates="parent_issue", cascade="all, delete-orphan")


class SubIssue(Base):
    __tablename__ = 'sub_issues'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    solution = Column(Text, nullable=False)
    sample_response = Column(Text, nullable=False)
    references = Column(Text, nullable=True)
    issue_id = Column(Integer, ForeignKey('issues.id'), nullable=False)

    parent_issue = relationship("Issue", back_populates="sub_issues")