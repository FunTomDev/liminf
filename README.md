# Liminf

Liminf is a platform designed for students of the **Faculty of Mathematics and Information Science (MiNI)** at the **Warsaw University of Technology (PW)**. It serves as a central hub for easily storing and sharing notes, materials, problems, and curriculum-related information.

## ⚠️ Project Status

- **Deprecated:** This project is currently deprecated. A new version is being developed based on **Django Rest Framework (DRF)**.
- **Showcase:** This repository serves as a showcase of the original architecture and logic. Local installation is not recommended.
- **Availability:** The live website may not be accessible as it depends on a **Supabase** database that might currently be suspended.

## 🚀 Technology Stack & Architecture

The project follows a modified Django MVT (Model-View-Template) architecture, integrating modern frontend tooling.

- **Backend:** [Django](https://www.djangoproject.com/) (Python)
- **Database:** [PostgreSQL](https://www.postgresql.org/) (hosted on [Supabase](https://supabase.com/))
- **Frontend Tooling:** [Vite](https://vitejs.dev/) with [Tailwind CSS](https://tailwindcss.com/)
- **Frontend Integration:** [django-vite](https://github.com/mrbin702/django-vite)
- **File Storage:** S3-compatible storage via Supabase Storage
- **Dependency Management:** [Poetry](https://python-poetry.org/)

## 🏗️ Backend Structure

The backend is organized into specialized Django applications, each handling a distinct part of the platform's ecosystem:

```text
backend/
│
├── app/ — Project Heart
│   └── Core settings, URL routing, ASGI/WSGI configurations, and global middleware.
│
├── curriculum/ — Educational Backbone
│   └── Manages the hierarchy of learning: Semesters → Subjects → Topics. Acts as the primary organizational structure for all content.
│
├── materials/ — Knowledge Repository
│   └── Handles storage and categorization of study materials, including student-made notes, research articles, and official faculty resources.
│
├── problems/ — Exercise Database
│   └── A collection of academic problems categorized by status (unsolved, solved, verified), linked to specific curriculum topics.
│
├── submissions/ — Community Solutions
│   └── Manages user-contributed solutions to problems, featuring a voting system (upvotes/downvotes) to highlight helpful answers.
│
├── users/ — Identity & Permissions
│   └── Custom User model with specialized roles (Student, Contributor, Editor, Admin) and dynamic vocative name generation.
│
├── attachments/ — Generic Media Handling
│   └── A flexible, generic attachment system allowing files to be linked to any model in the system via ContentTypes.
│
├── forums/ — Discussion Space
│   └── A module intended for student discussions and collaborative problem-solving.
│
└── pages/ — Interface & Layout
    └── Manages general-purpose views, landing pages, and the overall static structure of the website.
```

---

*Note: This project is archived and maintained for portfolio purposes.*
