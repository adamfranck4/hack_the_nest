# hack_the_nest

Project for the Hack the Nest hackathon.

> Status: repo scaffold only. The idea, stack and setup steps get filled in once the build starts.

## What it does

_To be written: the problem and the one-sentence pitch._

## Getting started

_To be written: install and run commands._

Copy `.env.example` to `.env` and fill in the values. Never commit `.env`.

## Tech stack

_To be decided._

## Working with the agent team

This repo ships a Claude Code agent team in [.claude/agents](.claude/agents). Opening a Claude Code session in this folder starts the `manager` agent, which splits a goal into tasks and hands them to five workers:

| Agent | Owns |
|---|---|
| `manager` | Planning, delegation, checking results |
| `frontend` | UI, pages, components, styling |
| `backend` | Server, API routes, business logic, auth |
| `data-integrations` | Database schema, seed data, third-party APIs |
| `qa-tester` | Tests, running the app, bug reports |
| `docs-demo` | README, demo script, pitch material |

Give the manager a goal, for example: "build the MVP for <idea> with login and a dashboard".

## Team

_Add names here._
