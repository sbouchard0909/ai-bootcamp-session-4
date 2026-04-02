# Slalom Capabilities Management API

<p align="center">
  <img src="https://colby-timm.github.io/images/byte-teacher.png" alt="Byte Teacher" width="200" />
</p>

A FastAPI application that enables Slalom consultants to register their capabilities and manage consulting expertise across the organization.

## Features

- View all available consulting capabilities
- Register consultant expertise and availability
- Track skill levels and certifications
- Manage capability capacity and team assignments
- Maintain per-consultant skill profiles linked to capabilities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc
   - Capabilities Dashboard: http://localhost:8000/

## API Endpoints

| Method | Endpoint                                                                                 | Description                                                          |
| ------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| GET    | `/capabilities`                                                                         | Get all capabilities with details and current consultant assignments |
| POST   | `/capabilities/{capability_name}/register?email=consultant@slalom.com`                  | Register consultant for a capability                                 |
| DELETE | `/capabilities/{capability_name}/unregister?email=consultant@slalom.com`                | Unregister consultant from a capability                              |
| GET    | `/consultants/{email}/skills`                                                            | Get a consultant's skill profile (list of capabilities)              |
| POST   | `/consultants/{email}/skills` (JSON body: `{ "capability_name": "Cloud Architecture" }`) | Add a capability to a consultant's skill profile                     |
| DELETE | `/consultants/{email}/skills/{capability_name}`                                         | Remove a capability from a consultant's skill profile                |

## Data Model

The application uses a consulting-focused data model:

1. **Capabilities** - Uses capability name as identifier:
   - Description of the consulting capability
   - Skill levels (Emerging, Proficient, Advanced, Expert)
   - Practice area (Strategy, Technology, Operations)
   - Industry verticals served
   - Required certifications
   - List of consultant emails registered
   - Available capacity (hours per week)
   - Geographic location preferences

2. **Consultants** - Uses email as identifier:
   - Name
   - Practice area
   - Skill level
   - Certifications
   - Availability
   - **Skill profile**: list of capability identifiers (with structure designed to later support proficiency, evidence, and history)

All data is currently stored in memory for this learning exercise. In a production environment, this would be backed by a robust database system.

## Future Enhancements

This exercise will guide you through implementing:
- Capability maturity assessments
- Intelligent team matching algorithms  
- Analytics dashboards for practice leads
- Integration with project management systems
- Advanced search and filtering capabilities
