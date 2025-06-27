from app.core.db import get_db
from app.schemas import issue as schemas
from app.services import issue as services
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


@router.post("/", response_model=schemas.Issue)
def create_issue(issue: schemas.IssueCreate, db: Session = Depends(get_db)):
    return services.create_issue(db=db, issue=issue)


@router.get("/", response_model=List[schemas.Issue])
def get_issues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_issues(db=db, skip=skip, limit=limit)


@router.get("/{issue_id}", response_model=schemas.Issue)
def get_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = services.get_issue(db=db, issue_id=issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.put("/{issue_id}", response_model=schemas.Issue)
def update_issue(issue_id: int, issue_update: schemas.IssueCreate, db: Session = Depends(get_db)):
    issue = services.update_issue(db=db, issue_id=issue_id, issue_update=issue_update)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.delete("/{issue_id}", response_model=schemas.Issue)
def delete_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = services.delete_issue(db=db, issue_id=issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.post("/{issue_id}/subissues/", response_model=schemas.SubIssue)
def create_sub_issue(issue_id: int, sub_issue: schemas.SubIssueCreate, db: Session = Depends(get_db)):
    issue = services.get_issue(db=db, issue_id=issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Parent Issue not found")
    return services.create_sub_issue(db=db, sub_issue=sub_issue, issue_id=issue_id)


@router.get("/{issue_id}/subissues/", response_model=List[schemas.SubIssue])
def get_sub_issues_by_issue(issue_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parent_issue = services.get_issue(db=db, issue_id=issue_id)
    if not parent_issue:
        raise HTTPException(status_code=404, detail="Parent Issue not found")
    sub_issues = services.get_sub_issues_by_issue(db=db, issue_id=issue_id, skip=skip, limit=limit)
    return sub_issues


@router.put("/{issue_id}/subissues/{sub_issue_id}", response_model=schemas.SubIssue)
def update_sub_issue_endpoint(sub_issue_id: int, sub_issue_update: schemas.SubIssueCreate, db: Session = Depends(get_db)):
    db_sub_issue = services.update_sub_issue(
        db=db, 
        sub_issue_id=sub_issue_id, 
        sub_issue_update=sub_issue_update
    )
    if db_sub_issue is None:
        raise HTTPException(status_code=404, detail="SubIssue not found")
    return db_sub_issue


@router.delete(
    "/{issue_id}/subissues/{sub_issue_id}", 
    response_model=schemas.SubIssue)
def delete_sub_issue(sub_issue_id: int, db: Session = Depends(get_db)):
    db_sub_issue = services.delete_sub_issue(db=db, sub_issue_id=sub_issue_id)
    if db_sub_issue is None:
        raise HTTPException(status_code=404, detail="SubIssue not found")
    return db_sub_issue