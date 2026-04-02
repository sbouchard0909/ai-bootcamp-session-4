"""
Slalom Capabilities Management System API

A FastAPI application that enables Slalom consultants to register their
capabilities and manage consulting expertise across the organization.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import os
from pathlib import Path

app = FastAPI(
    title="Slalom Capabilities Management API",
    description="API for managing consulting capabilities and consultant expertise",
)

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(current_dir, "static")),
    name="static",
)

# In-memory capabilities database
capabilities = {
    "Cloud Architecture": {
        "description": "Design and implement scalable cloud solutions using AWS, Azure, and GCP",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["AWS Solutions Architect", "Azure Architect Expert"],
        "industry_verticals": ["Healthcare", "Financial Services", "Retail"],
        "capacity": 40,  # hours per week available across team
        "consultants": ["alice.smith@slalom.com", "bob.johnson@slalom.com"],
    },
    "Data Analytics": {
        "description": "Advanced data analysis, visualization, and machine learning solutions",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": [
            "Tableau Desktop Specialist",
            "Power BI Expert",
            "Google Analytics",
        ],
        "industry_verticals": ["Retail", "Healthcare", "Manufacturing"],
        "capacity": 35,
        "consultants": ["emma.davis@slalom.com", "sophia.wilson@slalom.com"],
    },
    "DevOps Engineering": {
        "description": "CI/CD pipeline design, infrastructure automation, and containerization",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": [
            "Docker Certified Associate",
            "Kubernetes Admin",
            "Jenkins Certified",
        ],
        "industry_verticals": ["Technology", "Financial Services"],
        "capacity": 30,
        "consultants": ["john.brown@slalom.com", "olivia.taylor@slalom.com"],
    },
    "Digital Strategy": {
        "description": "Digital transformation planning and strategic technology roadmaps",
        "practice_area": "Strategy",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": [
            "Digital Transformation Certificate",
            "Agile Certified Practitioner",
        ],
        "industry_verticals": ["Healthcare", "Financial Services", "Government"],
        "capacity": 25,
        "consultants": ["liam.anderson@slalom.com", "noah.martinez@slalom.com"],
    },
    "Change Management": {
        "description": "Organizational change leadership and adoption strategies",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Prosci Certified", "Lean Six Sigma Black Belt"],
        "industry_verticals": ["Healthcare", "Manufacturing", "Government"],
        "capacity": 20,
        "consultants": ["ava.garcia@slalom.com", "mia.rodriguez@slalom.com"],
    },
    "UX/UI Design": {
        "description": "User experience design and digital product innovation",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": [
            "Adobe Certified Expert",
            "Google UX Design Certificate",
        ],
        "industry_verticals": ["Retail", "Healthcare", "Technology"],
        "capacity": 30,
        "consultants": ["amelia.lee@slalom.com", "harper.white@slalom.com"],
    },
    "Cybersecurity": {
        "description": "Information security strategy, risk assessment, and compliance",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["CISSP", "CISM", "CompTIA Security+"],
        "industry_verticals": ["Financial Services", "Healthcare", "Government"],
        "capacity": 25,
        "consultants": ["ella.clark@slalom.com", "scarlett.lewis@slalom.com"],
    },
    "Business Intelligence": {
        "description": "Enterprise reporting, data warehousing, and business analytics",
        "practice_area": "Technology",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": ["Microsoft BI Certification", "Qlik Sense Certified"],
        "industry_verticals": ["Retail", "Manufacturing", "Financial Services"],
        "capacity": 35,
        "consultants": ["james.walker@slalom.com", "benjamin.hall@slalom.com"],
    },
    "Agile Coaching": {
        "description": "Agile transformation and team coaching for scaled delivery",
        "practice_area": "Operations",
        "skill_levels": ["Emerging", "Proficient", "Advanced", "Expert"],
        "certifications": [
            "Certified Scrum Master",
            "SAFe Agilist",
            "ICAgile Certified",
        ],
        "industry_verticals": ["Technology", "Financial Services", "Healthcare"],
        "capacity": 20,
        "consultants": ["charlotte.young@slalom.com", "henry.king@slalom.com"],
    },
}

# In-memory per-consultant skill profiles keyed by consultant email.
# Each profile currently stores a simple list of capability names so it can
# be easily extended later with proficiency, evidence, and history.
consultant_profiles: dict[str, dict] = {}


def _initialize_consultant_profiles_from_capabilities() -> None:
    """Seed consultant skill profiles from existing capability assignments."""
    for capability_name, details in capabilities.items():
        for email in details.get("consultants", []):
            profile = consultant_profiles.setdefault(email, {"skills": []})
            if capability_name not in profile["skills"]:
                profile["skills"].append(capability_name)


_initialize_consultant_profiles_from_capabilities()


class ConsultantSkillAssignment(BaseModel):
    capability_name: str


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/capabilities")
def get_capabilities():
    return capabilities


@app.post("/capabilities/{capability_name}/register")
def register_for_capability(capability_name: str, email: str):
    """Register a consultant for a capability."""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    capability = capabilities[capability_name]

    # Validate consultant is not already registered
    if email in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is already registered for this capability",
        )

    # Add consultant to capability
    capability["consultants"].append(email)

    # Ensure consultant profile is kept in sync
    profile = consultant_profiles.setdefault(email, {"skills": []})
    if capability_name not in profile["skills"]:
        profile["skills"].append(capability_name)

    return {"message": f"Registered {email} for {capability_name}"}


@app.delete("/capabilities/{capability_name}/unregister")
def unregister_from_capability(capability_name: str, email: str):
    """Unregister a consultant from a capability."""
    # Validate capability exists
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    capability = capabilities[capability_name]

    # Validate consultant is registered
    if email not in capability["consultants"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant is not registered for this capability",
        )

    # Remove consultant from capability
    capability["consultants"].remove(email)

    # Keep consultant profile in sync
    profile = consultant_profiles.get(email)
    if profile and capability_name in profile.get("skills", []):
        profile["skills"].remove(capability_name)

    return {"message": f"Unregistered {email} from {capability_name}"}


@app.get("/consultants/{email}/skills")
def get_consultant_skills(email: str):
    """Get the list of capabilities associated with a consultant profile."""
    profile = consultant_profiles.get(email, {"skills": []})
    return {"consultant": email, "skills": profile["skills"]}


@app.post("/consultants/{email}/skills")
def add_consultant_skill(email: str, assignment: ConsultantSkillAssignment):
    """Add a capability to a consultant's skill profile."""
    capability_name = assignment.capability_name

    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    profile = consultant_profiles.setdefault(email, {"skills": []})

    if capability_name in profile["skills"]:
        raise HTTPException(
            status_code=400,
            detail="Consultant already has this capability in their profile",
        )

    # Add to consultant profile
    profile["skills"].append(capability_name)

    # Ensure capability-level view stays in sync
    capability = capabilities[capability_name]
    if email not in capability["consultants"]:
        capability["consultants"].append(email)

    return {"message": f"Added {capability_name} to {email}'s skill profile"}


@app.delete("/consultants/{email}/skills/{capability_name}")
def remove_consultant_skill(email: str, capability_name: str):
    """Remove a capability from a consultant's skill profile."""
    if capability_name not in capabilities:
        raise HTTPException(status_code=404, detail="Capability not found")

    profile = consultant_profiles.get(email)
    if not profile or capability_name not in profile.get("skills", []):
        raise HTTPException(
            status_code=400,
            detail="Consultant does not have this capability in their profile",
        )

    # Remove from consultant profile
    profile["skills"].remove(capability_name)

    # Keep capability-level view in sync
    capability = capabilities[capability_name]
    if email in capability["consultants"]:
        capability["consultants"].remove(email)

    return {
        "message": f"Removed {capability_name} from {email}'s skill profile",
    }
