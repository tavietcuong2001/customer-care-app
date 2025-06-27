from app.models import issue as models
from app.schemas import issue as schemas
from sqlalchemy.orm import Session


def create_issue(db: Session, issue: schemas.IssueCreate):
    issue = models.Issue(**issue.model_dump())
    db.add(issue)
    db.commit()
    db.refresh(issue)
    return issue


def get_issues(db: Session, skip: int, limit: int):
    return db.query(models.Issue).offset(skip).limit(limit).all()


def get_issue(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id == issue_id).first()


def update_issue(db: Session, issue_id: int, issue_update: schemas.IssueUpdate):
    issue = get_issue(db, issue_id)
    if not issue:
        return None

    update_data = issue_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(issue, key, value)

    db.commit()
    db.refresh(issue)
    
    return issue


def delete_issue(db: Session, issue_id: int):
    issue = get_issue(db, issue_id)
    if not issue:
        return None

    db.delete(issue)
    db.commit()
    
    return issue


def create_sub_issue(db: Session, sub_issue: schemas.SubIssueCreate, issue_id: int):
    sub_issue = models.SubIssue(**sub_issue.model_dump(), issue_id=issue_id)
    db.add(sub_issue)
    db.commit()
    db.refresh(sub_issue)
    return sub_issue


def get_sub_issue(db: Session, sub_issue_id: int):
    return db.query(models.SubIssue).filter(models.SubIssue.id == sub_issue_id).first()


def get_sub_issues_by_issue(db: Session, issue_id: int, skip: int, limit: int):
    return db.query(models.SubIssue).filter(models.SubIssue.issue_id == issue_id).offset(skip).limit(limit).all()


def update_sub_issue(db: Session, sub_issue_id: int, sub_issue_update: schemas.SubIssueCreate):
    sub_issue = get_sub_issue(db, sub_issue_id=sub_issue_id)
    if not sub_issue:
        return None

    update_data = sub_issue_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sub_issue, key, value)
    
    db.add(sub_issue)
    db.commit()
    db.refresh(sub_issue)
    return sub_issue


def delete_sub_issue(db: Session, sub_issue_id: int):
    sub_issue = get_sub_issue(db, sub_issue_id=sub_issue_id)
    if not sub_issue:
        return None
        
    db.delete(sub_issue)
    db.commit()
    return sub_issue