---
name: openspec-composer
model: inherit
description: "(DEPRECATED) Legacy composer for openspec/sessions/analysis.md — read-only if session exists"
---

# (DEPRECATED) OpenSpec Composer

**Не вызывать в активном workflow Ultra-Lite explore.**

Исторически: сборка `openspec/sessions/<slug>/analysis.md` из `step-*.md`. Новые исследования — [`.cursor/skills/openspec-explore/SKILL.md`](../skills/openspec-explore/SKILL.md); финал в чате (`## Для /opsx:ff`) + `temp/reports/`.

Если в репозитории уже есть legacy-сессия с `analysis.md` — ff/extend могут прочитать файл read-only. Новые sessions не создавать.
