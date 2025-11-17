"""
Job Creation Script - Refactored
Creates multiple jobs via JobTrekPro API with configurable parameters.
"""
import requests
import random
import time
import uuid
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


# Job tag colors (hex codes)
TAG_COLORS = [
    "#0055ff", "#ff0000", "#00cc00", "#ffaa00",
    "#cc00ff", "#00cccc", "#ff6600", "#0099ff",
    "#ff0066", "#9900ff", "#00ff99", "#ff9900"
]


# Random name lists
FIRST_NAMES = [
    "John", "Sarah", "Michael", "Emma", "David", "Lisa", "James", "Maria",
    "Robert", "Jennifer", "William", "Linda", "Richard", "Patricia", "Joseph",
    "Elizabeth", "Thomas", "Susan", "Christopher", "Jessica", "Daniel", "Karen",
    "Matthew", "Nancy", "Anthony", "Betty", "Mark", "Helen", "Donald", "Sandra"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White",
    "Harris", "Clark", "Lewis", "Robinson", "Walker", "Young", "Hall"
]


@dataclass
class JobConfig:
    """Configuration for job creation"""
    api_url: str = "https://api.jobtrekpro.com/api/jobs"
    admin_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIyMmMyZjA2Ny03OGJhLTQ1NmQtODU2Yy1mMmMzNzc4YmNjNWUiLCJlbWFpbCI6InRlc3RAeW9wbWFpbC5jb20iLCJyb2xlIjoib3duZXIiLCJpYXQiOjE3NjMwMjkwMDQsImV4cCI6MTc2MzExNTQwNH0.ohdkrHCQS8WDSFYCkrIW7vlCFdVwZ4lttUXgf61jM8A"
    client_id: str = "d16fe772-a0de-42bc-9689-793d00c54f8e"
    contractor_id: str = "64ea2b3b-7d99-4756-99fe-4d1ee9c68353"
    rate_limit_delay: float = 0.1
    request_timeout: int = 10


@dataclass
class Service:
    """Service details"""
    name: str
    description: str
    duration: int
    base_price: int
    total_price: int

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "duration": self.duration,
            "basePrice": self.base_price,
            "totalPrice": self.total_price,
            "serviceId": str(uuid.uuid4())
        }


@dataclass
class JobPayload:
    """Job creation payload"""
    client_id: str
    contractor_id: str
    client_first_name: str
    client_last_name: str
    title: str
    description: str
    duration_hours: int
    job_date: str
    job_time: str
    location_address: str
    requested_service: str
    total_price: int
    services: List[Service]
    job_tag: Optional[str] = None

    def to_dict(self) -> dict:
        tag = self.job_tag or random.choice(TAG_COLORS)

        return {
            "clientId": self.client_id,
            "clientFirstName": self.client_first_name,
            "clientLastName": self.client_last_name,
            "title": self.title,
            "description": self.description,
            "durationHours": self.duration_hours,
            "jobDate": self.job_date,
            "jobTime": self.job_time,
            "jobTag": tag,
            "locationAddress": self.location_address,
            "requestedService": self.requested_service,
            "totalPrice": self.total_price,
            "selectedTags": [tag],
            "candidateContractorIds": [self.contractor_id],
            "priorityContractorIds": [self.contractor_id],
            "services": [s.to_dict() for s in self.services]
        }


class JobCreator:
    """Handles job creation via API"""

    def __init__(self, config: JobConfig):
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {config.admin_token}",
            "Content-Type": "application/json"
        }
        self.stats = {"success": 0, "failed": 0}

    def create_default_job_payload(self) -> JobPayload:
        """Creates a default job payload with cleaning service and random client name"""
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        cleaning_service = Service(
            name="cleaning",
            description=f"Clean the property for {first_name} {last_name}",
            duration=random.randint(1, 4),
            base_price=random.randint(50, 150),
            total_price=random.randint(100, 300)
        )

        return JobPayload(
            client_id=self.config.client_id,
            contractor_id=self.config.contractor_id,
            client_first_name=first_name,
            client_last_name=last_name,
            title=f"Cleaning job for {first_name} {last_name}",
            description=f"Professional cleaning service requested by {first_name} {last_name}",
            duration_hours=cleaning_service.duration,
            job_date="2025-11-15",
            job_time=f"{random.randint(8, 16):02d}:00",
            location_address=f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Pine'])} Street",
            requested_service="cleaning",
            total_price=cleaning_service.total_price,
            services=[cleaning_service]
        )

    def create_job(self, payload: JobPayload, job_number: int) -> bool:
        """
        Creates a single job via API

        Args:
            payload: Job payload to send
            job_number: Job number for logging

        Returns:
            True if successful, False otherwise
        """
        try:
            response = requests.post(
                self.config.api_url,
                json=payload.to_dict(),
                headers=self.headers,
                timeout=self.config.request_timeout
            )

            if response.status_code in [200, 201]:
                self.stats["success"] += 1
                tag_color = payload.to_dict()['jobTag']
                print(
                    f"[{job_number}] ✅ Created job: '{payload.title}' (tag: {tag_color})")
                return True
            else:
                self.stats["failed"] += 1
                print(
                    f"[{job_number}] ❌ Failed ({response.status_code}): {response.text}")
                return False

        except requests.exceptions.RequestException as e:
            self.stats["failed"] += 1
            print(f"[{job_number}] ⚠️ Request error: {e}")
            return False
        except Exception as e:
            self.stats["failed"] += 1
            print(f"[{job_number}] ⚠️ Unexpected error: {e}")
            return False

    def create_multiple_jobs(self, count: int, payload_generator=None) -> dict:
        """
        Creates multiple jobs

        Args:
            count: Number of jobs to create
            payload_generator: Optional function that returns JobPayload

        Returns:
            Dictionary with success and failed counts
        """
        self.stats = {"success": 0, "failed": 0}

        for i in range(1, count + 1):
            payload = payload_generator(
                i) if payload_generator else self.create_default_job_payload()
            self.create_job(payload, i)

            if i < count:  # Don't delay after last job
                time.sleep(self.config.rate_limit_delay)

        print(
            f"\n✅ Success: {self.stats['success']} | ❌ Failed: {self.stats['failed']}")
        return self.stats


def main():
    """Main entry point"""
    config = JobConfig()
    creator = JobCreator(config)

    # Create 5 jobs with default payload
    creator.create_multiple_jobs(10)


if __name__ == "__main__":
    main()
