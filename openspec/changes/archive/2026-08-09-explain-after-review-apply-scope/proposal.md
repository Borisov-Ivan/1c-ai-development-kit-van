## Why

После `/review`, `/release-review` и `/opsx:apply` нет перехода в `/opsx:explain` с уже известным списком обработанного кода: бриф explain приходится заполнять вручную, хотя охват уже лежит в отчёте ревью или `code-map`. Нужен handoff и автозаполнение Охвата в entry-брифе для подтверждения.

## What Changes

- Финалы review/release-review и apply (acceptance/final с BSL) могут предлагать `/opsx:explain` (ниже приоритета fix/extend).
- В `review-*.md`, `code-map.md` / handoff-acceptance появляется секция `## Explain scope` (files ± procedures).
- `/opsx:explain` при входе из review/apply строит B-explain с Охватом обработанного кода (для огромного release — Варианты рамки); пути — в Контекст.
- HALT брифа уточняется: запрещён сырой dump модулей как замена сценарию; разрешён компактный охват post-review/apply.
- Эталон брифа и примеры команды для `@review-*.md` / `@code-map.md`.

## Capabilities

### New Capabilities

- `explain-post-implementation-scope`: handoff охвата из review/apply в `/opsx:explain` и подтверждение рамки в B-explain.

### Modified Capabilities

- (нет существующих specs в `openspec/specs/`)

## Impact

- Kit: `openspec-explain`, `review/SKILL`, `openspec-apply-change`, `opsx-output-style`, `review-guide`, команды explain/review/release-review.
- Продуктовый BSL не меняется.
- Вне scope: disposition as-designed/queue-fix (ЗНИ `independent-review-disposition`).

## Metadata (comment markers)

developer: N/A
comment_suffix:
marker_style: minimal

<!-- Kit meta-change: BSL comment markers не применяются. -->

## Forms mode

form_mode: n/a

## Scope

- In scope: skills/commands/docs kit для explain + propose из review/apply + секция Explain scope.
- Out of scope: критическое disposition ревью; отдельный `temp/explain-handoff-*.md`; автостарт explain без подтверждения брифа.
