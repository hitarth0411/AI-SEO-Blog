# AI Blog Writing Agent

An AI-powered blog generation platform that automates the complete blog writing workflow using intelligent AI agents, SEO optimization, and automation pipelines.

The platform helps users generate high-quality, SEO-friendly blogs in minutes by combining AI research, structured content planning, and automated content generation.

---

# Features

* AI-powered blog generation
* SEO optimized content creation
* Automated research and planning
* Multi-agent AI workflow
* Blog regeneration
* Authentication system
* Chat history management
* PDF/Word export
* Workflow automation using n8n
* Responsive modern UI

---

# Tech Stack

## Frontend

* React.js
* TypeScript

## Backend

* Python
* FastAPI

## Database

* MongoDB

## AI & Automation

* LangChain
* LangGraph
* Groq API
* n8n

---

# Project Overview

This project was built to simplify and automate content creation using AI-powered workflows. The application combines modern frontend technologies, backend APIs, and AI orchestration to generate SEO-friendly blogs efficiently.

The system supports intelligent research, structured blog generation, backend workflow automation, and scalable AI integration while maintaining a clean and user-friendly experience.

---

# Demo Screenshots

## Home Page

![Home Page](screenshots/home.png)

---

## Sign In Page

![Sign In](screenshots/signIn.png)

---

## Generated Blog Output
![Generated Blog](screenshots/Blog_Generation_1.png)
![Generated Blog](screenshots/Blog_Generation_2.png)

---

# Export Support

The platform supports exporting generated blogs into downloadable formats:

- PDF Export
- Word (.docx) Export

## Sample Export Files

- [Download Sample PDF](exports/Output.pdf)
- [Download Sample Word File](exports/Sample_generated_blog.docx)

---

# Local Setup Guide

## Clone Repository

```bash
git clone https://github.com/hitarth0411/ai-seo-blog-agent.git
cd ai-seo-blog-agent
```

---

# Backend Setup

## Navigate to Backend

```bash
cd backend
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file inside backend folder and add:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=ai_blog_agent
```

## Run Backend Server

```bash
uvicorn main:app --reload
```

Alternatively, from the repository root:

```bash
uvicorn main:app --app-dir backend --reload
```

Backend will run on:

```text
http://localhost:8000
```

---

# Frontend Setup

## Navigate to Frontend

```bash
cd frontend
```

## Install Dependencies

```bash
npm install
```

## Start Frontend

```bash
npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```

---

# Database Setup

Install and start MongoDB locally, or create a MongoDB Atlas cluster. Set
`MONGODB_URI` in `backend/.env` to the local connection string or Atlas URI.
`MONGODB_DATABASE` selects the database; MongoDB creates it on the first write.

---

# Run Full Application

1. Start MongoDB
2. Run Backend Server
3. Run Frontend Server
4. Open browser:

```text
http://localhost:5173
```

---

# Future Improvements

* AI image generation
* Multi-language support
* Advanced SEO scoring
* Cloud deployment
* Team collaboration features
