# AGENTS.md

## Purpose

This repository hosts public-ready material for workshops, live coding sessions, talks, experiments, demos, tools, and shared assets around AI systems, software architecture, and system thinking.

Contributions should keep the repository clear, minimal, and easy to navigate. Prefer practical structure over cleverness.

## Repository Structure

- `workshops/`: structured workshop packages intended for guided learning
- `live-coding/`: session-oriented examples that can be followed in real time
- `talks/`: presentation material, notes, and supporting assets for talks
- `experiments/`: bounded explorations, prototypes, and technical investigations
- `demos/`: concise demonstrations of ideas, workflows, or system behavior
- `tools/`: lightweight helper utilities that support learning or repository workflows
- `shared/`: reusable assets, diagrams, and templates used across multiple areas

## Content Guidelines

- Keep artifacts focused and educational.
- Prefer small, understandable examples over broad sample applications.
- Add only the files needed to explain or run the artifact.
- Avoid placeholder implementation code beyond minimal README guidance.
- Do not add unrelated setup, generated files, or private working notes.

## Documentation Expectations

- All public-facing documentation must be written in English.
- Each substantial artifact should include a local `README.md`.
- A local README should explain purpose, scope, prerequisites, and how to use or review the artifact.
- If an artifact is incomplete, document its current state clearly and neutrally.

## Naming Conventions

- Use lowercase kebab-case for directories and files unless a language or tool requires another format.
- Keep names short, specific, and descriptive.
- Workshops may use optional numeric prefixes such as `001-building-ai-chat-agents`.
- Avoid vague names such as `test`, `misc`, `new`, or `final`.

## Public-Friendly Standards

- Assume the repository can be viewed by anyone at any time.
- Remove internal-only context, secrets, credentials, and private links.
- Use professional, neutral wording.
- Prefer clear explanations over marketing language.
- Keep examples and documentation safe to share publicly.

## Avoid Overengineering

- Do not introduce frameworks, build tooling, package managers, or CI unless explicitly required by the artifact.
- Prefer plain Markdown and simple folder structures.
- Keep examples self-contained where possible.
- Workshops and live sessions should be runnable or reviewable with minimal setup.
- Choose the smallest structure that keeps the content understandable and maintainable.

## Working Style for Agents

- Respect the existing structure and extend it only when needed.
- Keep changes minimal and scoped to the task.
- When adding a substantial new folder, include a local `README.md`.
- When adding workshops or sessions, make them self-contained where possible.
- Reuse material from `shared/` only when it genuinely serves multiple artifacts.
