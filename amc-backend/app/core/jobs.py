"""Background job system for async task processing."""
from typing import Optional, Dict, Any
import asyncio
from datetime import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text


class BackgroundJob:
    """Background job for async task processing."""
    
    def __init__(
        self,
        job_id: str,
        job_type: str,
        payload: Dict[str, Any],
        retry_count: int = 0,
        max_retries: int = 3
    ):
        self.job_id = job_id
        self.job_type = job_type
        self.payload = payload
        self.retry_count = retry_count
        self.max_retries = max_retries
        self.created_at = datetime.utcnow()
        self.completed_at: Optional[datetime] = None
        self.error: Optional[str] = None
        self.result: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'job_id': self.job_id,
            'job_type': self.job_type,
            'payload': self.payload,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error': self.error,
            'result': self.result
        }


class JobQueue:
    """Simple in-memory job queue for async task processing.
    
    For production, this should be replaced with Redis/RQ/Celery.
    This is a minimal implementation that works without external dependencies.
    """
    
    def __init__(self):
        self.jobs: Dict[str, BackgroundJob] = {}
        self.processing = False
    
    def add_job(self, job: BackgroundJob) -> str:
        """Add a job to the queue."""
        self.jobs[job.job_id] = job
        return job.job_id
    
    def get_job(self, job_id: str) -> Optional[BackgroundJob]:
        """Get a job by ID."""
        return self.jobs.get(job_id)
    
    def complete_job(self, job_id: str, result: Optional[Dict[str, Any]] = None):
        """Mark a job as complete."""
        if job_id in self.jobs:
            self.jobs[job_id].completed_at = datetime.utcnow()
            self.jobs[job_id].result = result
    
    def fail_job(self, job_id: str, error: str):
        """Mark a job as failed."""
        if job_id in self.jobs:
            self.jobs[job_id].completed_at = datetime.utcnow()
            self.jobs[job_id].error = error
    
    def get_pending_jobs(self, job_type: Optional[str] = None) -> list[BackgroundJob]:
        """Get all pending jobs of a type."""
        pending = [
            job for job in self.jobs.values()
            if job.completed_at is None
        ]
        
        if job_type:
            pending = [job for job in pending if job.job_type == job_type]
        
        return pending
    
    def cleanup_completed(self, older_than_hours: int = 24) -> int:
        """Remove completed jobs older than specified hours."""
        cutoff = datetime.utcnow()
        cutoff = cutoff.replace(hour=cutoff.hour - older_than_hours)
        
        to_remove = [
            job_id for job_id, job in self.jobs.items()
            if job.completed_at and job.completed_at < cutoff
        ]
        
        for job_id in to_remove:
            del self.jobs[job_id]
        
        return len(to_remove)


# Global job queue instance
_job_queue = JobQueue()


def get_job_queue() -> JobQueue:
    """Get the global job queue instance."""
    return _job_queue
