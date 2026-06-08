# ResuMess 🤯

## "Because your resume is a mess — let’s fix it automatically."

---

## 1. Overview

**ResuMess** is an end-to-end career document automation platform for building, updating, optimizing, previewing, and exporting resumes, CVs, and SOPs.

The core idea is simple:

1. Keep one authoritative, user-specific context space
2. Ingest a job description or company context
3. Retrieve the right facts and evidence
4. Rewrite content with ATS-aware phrasing
5. Render the result in LaTeX
6. Preview, download, and iterate instantly

---

## 2. Problem

Applying to jobs is chaotic:

* You keep editing the same resume again and again
* Skills need constant reordering
* Project descriptions need reframing per JD
* LaTeX resumes break for no reason
* ATS systems silently reject you

**ResuMess solves this chaos.**

---

## 3. Core Idea

Instead of editing documents repeatedly, users maintain a **personalized context space** of their:

* Skills
* Projects
* Experience
* Achievements
* Writing samples
* Links and portfolios

This user-specific space is the long-term source of truth for every future output, including:

* Resumes
* CVs
* SOPs
* Cover letters
* LinkedIn posts
* Portfolio website content

The retrieval layer will be implemented using PageIndex or a vectorless RAG approach so the system can work with structured, traceable context instead of only raw embeddings.

ResuMess then:

1. Reads a Job Description
2. Selects relevant content
3. Rewrites and optimizes it
4. Generates a polished LaTeX resume
5. Compiles + previews it
6. Provides download options
7. Evaluates ATS compatibility

---

## 4. Features

### 🧩 Personalized User Context Layer

* Separate schema per user
* Modular sections:

  * Skills (tagged + weighted)
  * Projects (impact, metrics, tech stack)
  * Experience
  * Achievements
  * Notes and reusable facts
  * Company-specific context
* Easily editable and reusable
* Designed as the long-term knowledge base for all future document generation tasks

---

### 🎯 JD-Aware Resume Generation

* Extracts keywords and requirements from JD
* Reorders skills based on relevance
* Selects best-fit projects
* Aligns content with role expectations
* Uses the JD plus company context to produce a more targeted draft
* Can recommend missing skills or additions that improve shortlist probability

---

### ✍️ Intelligent Rewriting

* Converts descriptions into:

  * Impact-driven bullet points
  * Quantified achievements
  * ATS-friendly phrasing
* Maintains factual correctness
* Reuses user-specific evidence from the personal context layer

---

### 📄 LaTeX Automation Engine

* Uses predefined templates
* Generates clean LaTeX code
* Detects and fixes common errors
* Compiles to PDF automatically
* Integrates an in-platform LaTeX viewer
* Supports downloadable output from the platform itself

---

### 📊 ATS Optimization

* Scores resume based on:

  * Keyword match
  * Structure
  * Completeness
* Suggests improvements:

  * Missing skills
  * Weak phrasing
  * Better alignment
* Uses ATS rules and template-aware checks
* Will initially support Jake's template

---

### ⚡ Real-Time Preview

* Live LaTeX + PDF view
* Instant updates on edits
* Download PDF and source artifacts directly from the platform

---

### 🔁 Version Control

* Save multiple resume versions
* Compare outputs
* Experiment with variations

---

## 5. Branching & Delivery Plan

The project should be developed through dedicated feature branches, reviewed independently, and merged one by one.

### Suggested branch structure

* `main` — stable production-ready code
* `feature/ui` — frontend shell, editor, preview, and navigation
* `feature/user-context-space` — personalized context store and retrieval layer
* `feature/jd-intelligence` — JD parsing, keyword extraction, and company-aware drafting
* `feature/latex-engine` — LaTeX generation, compilation, preview, and downloads
* `feature/ats-checker` — ATS rules, scoring, and template checks
* `feature/template-integration` — Jake's template and future template support
* `feature/versioning` — resume variants, history, compare, and rollback
* `feature/sop-cover-letter` — SOP and cover letter generation from the same context

### Workflow

1. Create the feature branch
2. Build the feature in isolation
3. Review against scope and quality checks
4. Merge into `main` only after approval
5. Move to the next branch

This keeps the UI separate from backend intelligence and allows focused ownership per feature.

## 5. System Architecture

### Frontend

* Resume editor
* JD input interface
* Live preview panel
* LaTeX render preview and downloads

### Feature-focused UI branch

The UI should stay on a dedicated branch so frontend work can progress independently from retrieval, ATS, and generation logic.

### Backend

* Resume generation API
* JD parsing module
* Content rewriting engine
* ATS scoring system
* User-specific context retrieval service
* Document generation orchestration for resume/CV/SOP flows

### Database

* User-specific structured tables
* Modular section storage
* Long-lived personalized knowledge base per user

### Integrations

* LaTeX compiler (local/cloud)
* External ATS tools (initial phase)
* PageIndex or vectorless RAG retrieval layer
* Template system for Jake's template and future templates

---

## 6. End-to-End Workflow

1. User inputs Job Description
2. System extracts key requirements
3. Matches against the user's personalized context space
4. Rewrites and prioritizes content using JD + company context
5. Generates LaTeX resume/CV/SOP
6. Compiles to PDF and renders preview
7. Provides downloadable output
8. Scores ATS compatibility and suggests improvements

---

## 7. Future Scope

* Cover letter generation
* LinkedIn/GitHub integration
* AI career insights
* Recruiter simulation feedback
* Multi-language support
* Company-aware drafting improvements based on employer knowledge

---

## 8. Tech Stack (Suggested)

* Frontend: React / Next.js
* Backend: Node.js / FastAPI
* Database: PostgreSQL / MongoDB
* NLP: LLM APIs
* LaTeX: pdflatex / Overleaf
* Retrieval: PageIndex or vectorless RAG
* Preview: in-browser PDF viewer / embedded LaTeX preview

---

## 9. Why ResuMess?

Because job applications are already stressful.

Your resume shouldn’t be.

---

## 10. Taglines

* "Turn your resume mess into a masterpiece."
* "Fix your resume chaos instantly."
* "One click. Job-ready resume."
