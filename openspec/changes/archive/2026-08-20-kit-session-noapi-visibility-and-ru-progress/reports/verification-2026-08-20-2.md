---
verify_mode: pre-apply
change: kit-session-noapi-visibility-and-ru-progress
date: 2026-08-20
verdict: GO
scope: slices-S2-S3
layer_status:
  layer_1_hygiene: PASS
  layer_2_internal_coherence: PASS
  layer_2_5_loop_detection: PASS
  layer_3_problem_solution: PASS
  layer_4_independent_challenge: SKIPPED-incremental
  layer_5_implementation_readiness: PASS
snapshot:
  accepted_tasks:
    - S2.1
    - S2.2
    - S2.3
    - S2.4
    - S2.5
    - S2.6
    - S2.7
    - S2.8
    - S2.9
    - S2.10
    - S3.1
    - S3.2
    - S3.6
    - S3.3
    - S3.4
    - S3.7
    - S3.5
  open_decision_id: null
  verify_depth: incremental
---

# Verify S2–S3 (статическая сверка правил kit)

Кода 1С нет. Проверка по тексту правил и скиллов.

## S2 — русский progress

- Stub §6 и полное тело §6 требуют русский progress `/opsx:*`; английские каркасы — примеры провала, не новые пункты HALT.
- Stub §1b пункт 10 и полное тело §1b пункт 10 — «язык»; заголовок полного тела: 10 пунктов. Счёт совпадает.
- В `/opsx:verify` нет каркаса «I'll rerun»; допустимы канон лимита, «Модель архитектора: Opus 5», «Дописываю постановку…».
- Профиль Grok: MAY прямой речи не меняет язык `/opsx:*`. Стиль §2 отсылает runtime-норму в бюджет чата.

## S3 — маркер только при BSL

- `/opsx:new`: вопрос маркера при `.bsl` / `src/`; деловой язык без литерала — спросить; пропуск только при доказанном kit-only (`developer: n/a` закрывает гейт без WARNING).
- Mode Gate формы не в том же сообщении, что вопрос маркера.
- `/opsx:apply`: `n/a` не пишется в маркер; при непустом `marker_scope` — defaultDeveloper или один вопрос ФИО.

## Вердикт

Блокеров постановки нет. Приёмка S1.accept / S2.accept / S3.accept — чтение правил, без ИБ.
