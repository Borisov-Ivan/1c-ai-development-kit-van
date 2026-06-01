### 1. Standards Compliance
```yaml
Check against:
  - Р‘РЎРџ (Р‘РёР±Р»РёРѕС‚РµРєР° СЃС‚Р°РЅРґР°СЂС‚РЅС‹С… РїРѕРґСЃРёСЃС‚РµРј)
  - 1C coding conventions
  - Naming conventions (Russian/English)
  - Code structure and organization
  - Documentation requirements
```

For deep vendor-standards compliance (transactions, event handlers, queries, locking): Read `.cursor/skills/1c-vendor-standards/SKILL.md`, check all domains touched by reviewed code. For details: Read the relevant domain file from `.cursor/docs/standard/` (see `1c-standards-navigator.md`). Do NOT read platform documentation routinely вЂ” only if the reviewed code uses an unfamiliar platform mechanism.

Integration exchange trigger: if reviewed code prepares JSON/HTTP/RMQ messages or data exchange (`Р—Р°РїРёСЃР°С‚СЊJSON`, `Р—Р°РїРёСЃСЊJSON`, `РџСЂРѕС‡РёС‚Р°С‚СЊJSON`, `РЎС‚СЂСѓРєС‚СѓСЂР°РЎРѕРѕР±С‰РµРЅРёСЏ`, `Р’СЃС‚Р°РІРёС‚СЊ("GUID"`, `HTTP`, `RMQ`, `РћР±РјРµРЅ`, `Р’С‹РіСЂСѓР·`, `Р—Р°РіСЂСѓР·`), read `.cursor/docs/standard/std-12-integration-exchange.md` and apply AP-048..AP-050 via the anti-pattern registry. Do not treat AP-050 as a mass lint for all user strings: only flag blocking messages that stop a scenario and do not explain actual/expected state.

### 2. Performance Analysis
```yaml
Identify:
  - N+1 query problems
  - Missing indexes
  - Inefficient loops
  - Unnecessary database calls
  - Memory leaks
  - Slow algorithms
```

### 3. Security Review
```yaml
Detect:
  - SQL injection vulnerabilities
  - XSS in forms
  - Insufficient access control
  - Hardcoded credentials
  - Unsafe data handling
  - RLS bypass attempts
```

### 4. Code Quality
```yaml
Evaluate:
  - Cyclomatic complexity
  - Code duplication
  - Function length
  - Parameter count
  - Error handling
  - Testability
  - Stub/placeholder code returning empty or dummy values (empty Thumbprint, hardcoded "TODO", always-false conditions) вЂ” HIGH вЂ” AP-024. See anti-pattern registry
  - AP-007: Parameter overwrite / collection mutation вЂ” HIGH/MEDIUM. See anti-pattern registry
  - Duplicated magic constant: same numeric literal (not 0/1/-1) or same string literal appears 2+ times in module вЂ” MEDIUM. Exception: query text, structure keys, metadata names, 0/1/-1/РСЃС‚РёРЅР°/Р›РѕР¶СЊ. See 1c-coding-standards.mdc rule 22
  - Mixed responsibilities: procedure >40 lines combining 3+ distinct concerns (rights check, transaction management, business logic, persistence/write, logging, UI feedback) вЂ” MEDIUM. Sign: procedure could be split into independent functions without passing internal state
```

### 5. Extension Annotations (1C Extensions)
```yaml
Check:
  - &РџРµСЂРµРґ/&РџРѕСЃР»Рµ applied to a function (not procedure) вЂ” CRITICAL вЂ” AP-022. See anti-pattern registry
  - &Р’РјРµСЃС‚Рѕ used where &РџРµСЂРµРґ/&РџРѕСЃР»Рµ would suffice вЂ” HIGH
  - &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ used by default without justification вЂ” HIGH. This annotation is brittle and should be avoided if the task can be solved via &РџРѕСЃР»Рµ, &РџРµСЂРµРґ, or &Р’РјРµСЃС‚Рѕ. Reviewer MUST demand justification for its use.
  - &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ: code outside #Р’СЃС‚Р°РІРєР°/#РЈРґР°Р»РµРЅРёРµ blocks differs from base вЂ” HIGH (prerelease: CRITICAL). Signs: variable renaming, formatting/indent changes, refactoring outside blocks, adding/removing #РћР±Р»Р°СЃС‚СЊ/#РљРѕРЅРµС†РћР±Р»Р°СЃС‚Рё in base (typed) code, NEW CODE added outside directive blocks. Any of these breaks extension applicability.
  - Business logic placed directly inside #Р’СЃС‚Р°РІРєР° block instead of delegating to a separate procedure вЂ” MEDIUM
  - AP-046: Hook-scope early return вЂ” feature-flag or business guard suppresses entire body of intercepted procedure (&РџРµСЂРµРґ/&РџРѕСЃР»Рµ/&Р’РјРµСЃС‚Рѕ/&РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ) вЂ” HIGH; for &Р’РјРµСЃС‚Рѕ without РџСЂРѕРґРѕР»Р¶РёС‚СЊР’С‹Р·РѕРІ вЂ” CRITICAL. See anti-pattern registry
  - &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ VERIFICATION PROCEDURE (mandatory when such methods exist):
    1. Identify all methods with &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ in the reviewed file.
    2. For each: load the base method from cf/ (path: replace cfe/<ExtName>/ with cf/ in file path).
    3. Extract code OUTSIDE #Р’СЃС‚Р°РІРєР°/#РљРѕРЅРµС†Р’СЃС‚Р°РІРєРё and #РЈРґР°Р»РµРЅРёРµ/#РљРѕРЅРµС†РЈРґР°Р»РµРЅРёСЏ blocks from the extension method.
    4. Diff against base: any divergence (added lines, deleted lines, modified lines) вЂ” CRITICAL (prerelease) / HIGH (normal).
    5. If base file not found вЂ” mark NEEDS_MANUAL_REVIEW.
```

### 6. Module Structure
```yaml
Check:
  - Missing #РћР±Р»Р°СЃС‚СЊ markup entirely вЂ” MEDIUM (only if module > 100 lines; for modules в‰¤ 100 lines вЂ” LOW)
  - Wrong order: РџСЂРѕРіСЂР°РјРјРЅС‹Р№РРЅС‚РµСЂС„РµР№СЃ в†’ РЎР»СѓР¶РµР±РЅС‹Р№РџСЂРѕРіСЂР°РјРјРЅС‹Р№РРЅС‚РµСЂС„РµР№СЃ в†’ РЎР»СѓР¶РµР±РЅС‹РµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё вЂ” MEDIUM
  - Duplicate #РћР±Р»Р°СЃС‚СЊ or #РљРѕРЅРµС†РћР±Р»Р°СЃС‚Рё directives вЂ” HIGH
  - Export method placed in #РћР±Р»Р°СЃС‚СЊ РЎР»СѓР¶РµР±РЅС‹РµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё (private region) вЂ” MEDIUM
  - Export procedure/function in form module (Forms/*/Module.bsl) вЂ” HIGH вЂ” AP-033. Exception: РџРѕРґРєР»СЋС‡Р°РµРјС‹Р№_* (BSP attachable commands), callbacks via РћРїРёСЃР°РЅРёРµРћРїРѕРІРµС‰РµРЅРёСЏ(..., Р­С‚РѕС‚РћР±СЉРµРєС‚). See anti-pattern registry
  - Module header comment name does not match actual module name вЂ” LOW
  - No module header comment (module purpose) вЂ” LOW
```

### 7. Method Documentation
```yaml
Check:
  - Export method without header comment (purpose, parameters, return value) вЂ” MEDIUM
  - Event handler without description вЂ” LOW
  - Header format does not match BSP template (РџР°СЂР°РјРµС‚СЂС‹/Р’РѕР·РІСЂР°С‰Р°РµРјРѕРµ Р·РЅР°С‡РµРЅРёРµ/РџСЂРёРјРµСЂ) вЂ” LOW
```

### 8. Extension Naming
```yaml
Check:
  - Intercepted method (&Р’РјРµСЃС‚Рѕ/&РџРµСЂРµРґ/&РџРѕСЃР»Рµ) without extension prefix вЂ” HIGH
  - Own new method (not intercept) with extension prefix вЂ” MEDIUM
  - Export own method without unique readable name вЂ” MEDIUM
  - Inconsistent prefix usage: export method without extension prefix in module that contains other exports WITH prefix вЂ” MEDIUM. Exception: intercept methods (&Р’РјРµСЃС‚Рѕ/&РџРµСЂРµРґ/&РџРѕСЃР»Рµ of base method) naturally lack prefix
```

### 9. Code Cleanliness
```yaml
Check:
  Principle: comments describe code intent, not change history.
  Do NOT treat as release-hygiene or remove: directives #Р’СЃС‚Р°РІРєР°, #РљРѕРЅРµС†Р’СЃС‚Р°РІРєРё, #РЈРґР°Р»РµРЅРёРµ, #РљРѕРЅРµС†РЈРґР°Р»РµРЅРёСЏ вЂ” they are 1C extension override syntax, required for correct merge.

  Project-level whitelist: if openspec/project.md contains section В«Р¤РѕСЂРјР°С‚С‹ Рё СЃРѕРіР»Р°С€РµРЅРёСЏ РїРѕ РєРѕРјРјРµРЅС‚Р°СЂРёСЏРј BSLВ»
  with subsection В«Whitelist РїСЂРµРґСЂРµР»РёР·Р°В» (table: prefix after //, optional regex on full // line, scope glob per row),
  comments in files matching that scope that match the whitelist are NOT release-hygiene findings.
  Read project.md before flagging changelog-style markers (e.g. +++/---) in whitelisted lines.

  Whitelisted marker normalization (AP-051):
    - When changelog markers fall under project whitelist (openspec/project.md в†’ Whitelist РїСЂРµРґСЂРµР»РёР·Р°),
      they are NOT removed (AP-040 does not apply), but they MUST be compact:
      adjacent +++/--- blocks for the same [ID#NNN] and the same semantic change
      are merged into one outer block.
    - When merged opening markers carry different dates, keep the latest.
    - Do NOT propose marker merging where AP-040 applies (markers not in whitelist) вЂ”
      correct finding there is removal, not merging.

  Release hygiene (process metadata in comments only):
    - Whitelisted Р—РќР-РїР°СЂС‹ // +++ / // --- (openspec/project.md) вЂ” РЅРµ СЃС‡РёС‚Р°С‚СЊ findings AP-040 (СЃРј. AP-040 whitelist РІ bsl-antipatterns.mdc).
    - РЈСЃС‚Р°СЂРµРІС€РёРµ / РІРЅРµ-whitelist РјР°СЂРєРµСЂС‹: // РќРђР§РђР›Рћ/РљРћРќР•Р¦ РР·РјРµРЅРµРЅРёСЏ, // Р Р“РРўРЎ ..., Р—Р°СЏРІРєР° в„–, РџРѕРґСЂСЏРґС‡РёРє:, date-author Р±РµР· С€Р°Р±Р»РѕРЅР° whitelist вЂ” MEDIUM
    - JSDoc РЅР°Рґ РџСЂРѕС†РµРґСѓСЂР°/Р¤СѓРЅРєС†РёСЏ: СЃРЅРѕСЃРєРё (СЃРј. <kebab-change> ...), РїСѓС‚Рё reports/openspec/temp/reports, СѓРїРѕРјРёРЅР°РЅРёРµ *.md РєР°Рє РґРѕРєР°Р·Р°С‚РµР»СЊСЃС‚РІР° СЂРµС€РµРЅРёСЏ вЂ” MEDIUM (AP-040)
    - Commented-out old code with replacement markers
      ("РћСЂРёРіРёРЅР°Р»СЊРЅС‹Р№ РєРѕРґ:", "РќРѕРІС‹Р№ РєРѕРґ:", "РЎС‚Р°СЂС‹Р№ РІР°СЂРёР°РЅС‚:") вЂ” MEDIUM
    - Work instructions in code
      ("Р”РѕР±Р°РІРёС‚СЊ РІ xml...", "РџРµСЂРµРЅРµСЃС‚Рё РІ...", "TODO РїРµСЂРµРЅРµСЃС‚Рё") вЂ” MEDIUM
    - Design/process artifact references in comments вЂ” MEDIUM:
        Short-form refs: // Design В§3, // D11, // F5
        Natural-language refs: // РџРѕ design Decision 6 (fix-signing-result): ...
        Change names (kebab-case in comments): fix-signing-result, add-feature-X
        Process terms in comments: design, decision, proposal, architecture,
          exploration, root cause, trace-analysis, Р—РќР, ADR
        Task number refs: Рї. 3.1, Р·Р°РґР°С‡Р° 2.2, Decision N
      Detection: look for English process nouns in Russian comment lines,
        kebab-case identifiers, and numbered decision/task references.

  Code waste:
    - Dead code вЂ” see category 15 (Obsolete and Unused Code)
    - Logic duplication between modules вЂ” MEDIUM
    - Commented-out code without explanation вЂ” MEDIUM
```

### 10. Specific 1C Patterns
```yaml
Check via Anti-pattern Registry (see category 16):
  AP-001: Server scope by default in form modules (РџРµСЂРµРј/РўРёРї without &РќР°РљР»РёРµРЅС‚Рµ) вЂ” HIGH
  AP-002: Client-only methods in server context вЂ” HIGH
  AP-003: Р­С‚Р°Р¤РѕСЂРјР° instead of Р­С‚РѕС‚РћР±СЉРµРєС‚ in callbacks вЂ” HIGH
  AP-004: Defensive check on fixed-contract source вЂ” HIGH
  AP-005: РЎРІРѕР№СЃС‚РІРѕ() on non-Structure type вЂ” HIGH
  AP-006: Defensive cake (stacked redundant checks) вЂ” HIGH
  AP-008: РџРѕРїС‹С‚РєР° wrapping deterministic operation вЂ” CRITICAL
  AP-009: Silent degradation in РСЃРєР»СЋС‡РµРЅРёРµ вЂ” HIGH
  AP-010: Traceless exception suppression вЂ” HIGH
  AP-011: РўРµРєСѓС‰Р°СЏР”Р°С‚Р°() instead of РўРµРєСѓС‰Р°СЏР”Р°С‚Р°РЎРµР°РЅСЃР°() вЂ” CRITICAL
  AP-012: РЎРѕРѕР±С‰РёС‚СЊ() instead of BSP methods вЂ” HIGH
  AP-013: Query in loop (N+1) вЂ” HIGH
  AP-014: Attribute via reference dot notation вЂ” HIGH
  AP-017: Inverted early exit (condition tied to exit instead of action) вЂ” MEDIUM
  AP-018: РўРµРєСѓС‰Р°СЏРЎС‚СЂРѕРєР°() on form TableValue attribute (use Р­Р»РµРјРµРЅС‚С‹.<Name>.РўРµРєСѓС‰РёРµР”Р°РЅРЅС‹Рµ) вЂ” HIGH
  AP-019: РќРѕРІС‹Р№ РўРёРї(...) instead of РўРёРї(...) for type descriptor вЂ” HIGH
  AP-020: Missing explicit directive on procedure/function in form module вЂ” HIGH
  AP-021: Fail-fast violation (silent skip on structural precondition) вЂ” HIGH
  AP-025: User-facing string without РќРЎС‚СЂ() вЂ” MEDIUM
  AP-027: Guard-then-catch (РџРѕРїС‹С‚РєР° after guard validating same value) вЂ” HIGH
  AP-028: Check-after-establish (property/attribute check after type established) вЂ” HIGH
  AP-029: Defense stack (РџРѕРїС‹С‚РєР° + РЎРІРѕР№СЃС‚РІРѕ as contract uncertainty compensation) вЂ” HIGH/CRITICAL
  AP-030: Hidden partial result (РџРѕРїС‹С‚РєР°+РџСЂРѕРґРѕР»Р¶РёС‚СЊ/Р’РѕР·РІСЂР°С‚ without user feedback) вЂ” HIGH
  AP-032: Inconsistent persistent state (РџРѕРїС‹С‚РєР° + persistent write + no re-raise + downstream dependency) вЂ” CRITICAL
  AP-047: Substituted Authority вЂ” local implementation replaces delegation to the owner of behavior (base/BSP/platform/common module) вЂ” HIGH
  AP-048: Manual reference/GUID serialization in exchange code вЂ” HIGH
  AP-049: Numeric string via РЎС‚СЂРѕРєР°() + whitespace cleanup вЂ” MEDIUM
  AP-050: Uninformative blocking user message вЂ” MEDIUM (REFACTOR by default; MUST_FIX when user cannot recover)

Remain inline (not in registry):
  - Ternary operator ?() вЂ” MEDIUM
  - Excessive info logging inside loop or 3+ info-level calls вЂ” LOW
```

### 11. Band-Aid Detection
```yaml
Check via Anti-pattern Registry:
  AP-016: Band-aid fix вЂ” HIGH (see .cursor/rules/verified-cause-gate.mdc)

Remain inline:
  - Design-prescribed anti-pattern: guard in code matches design.md recommendation,
    but violates rule 14 вЂ” HIGH (tag: design-prescribed)
```

### 12. Release Readiness (checked only in mode=prerelease)
```yaml
Check:
  - Typos and encoding errors in user-facing strings: mixed Cyrillic/Latin chars (РЎ vs C, Р° vs a, Рѕ vs o, Рµ vs e), spelling errors in РќРЎС‚СЂ/РџРѕРєР°Р·Р°С‚СЊРџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ arguments вЂ” HIGH
  - Stub/placeholder code вЂ” see category 4 Code Quality (always checked, not prerelease-only)
  - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ without logging вЂ” moved to category 10 (always-checked, HIGH). See category 10 for detection; do NOT duplicate finding here
```

### 13. Transactions and Locking
```yaml
Check:
  AP-015: Transaction without safety pattern (РќР°С‡Р°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ without РџРѕРїС‹С‚РєР°+Р—Р°С„РёРєСЃРёСЂРѕРІР°С‚СЊ+РћС‚РјРµРЅРёС‚СЊ) вЂ” CRITICAL. See anti-pattern registry
  AP-023: User interaction (РџРѕРєР°Р·Р°С‚СЊР’РѕРїСЂРѕСЃ, РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ, РЎРѕРѕР±С‰РёС‚СЊ) inside transaction вЂ” HIGH. See anti-pattern registry
  Remain inline:
  - Read-then-write without Р‘Р»РѕРєРёСЂРѕРІРєР°Р”Р°РЅРЅС‹С… in concurrent scenario вЂ” HIGH
  - Nested РќР°С‡Р°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ() without justification вЂ” MEDIUM
```

### 14. Resource Leaks
```yaml
Check:
  - COMРћР±СЉРµРєС‚ (РќРѕРІС‹Р№ COMРћР±СЉРµРєС‚()) created without РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ ensuring release вЂ” HIGH
  - HTTPРЎРѕРµРґРёРЅРµРЅРёРµ/FTPРЎРѕРµРґРёРЅРµРЅРёРµ created but not wrapped in РџРѕРїС‹С‚РєР° for timeout/error handling вЂ” MEDIUM
  - File reader/writer (Р§С‚РµРЅРёРµXML, РќР°С‡Р°С‚СЊР—Р°РїРёСЃСЊXML, Р§С‚РµРЅРёРµJSON, Р—Р°РїРёСЃСЊJSON, РўРµРєСЃС‚РѕРІС‹Р№Р”РѕРєСѓРјРµРЅС‚.РћС‚РєСЂС‹С‚СЊ) opened without close in error path вЂ” MEDIUM
  - Temporary file created (РџРѕР»СѓС‡РёС‚СЊРРјСЏР’СЂРµРјРµРЅРЅРѕРіРѕР¤Р°Р№Р»Р°) without cleanup in error path вЂ” LOW
```

### 15. Obsolete and Unused Code
```yaml
Check:
  Unused procedures/functions (std-06 Рї.2, std-01 Рї.2.2):
    - For each РџСЂРѕС†РµРґСѓСЂР°/Р¤СѓРЅРєС†РёСЏ in reviewed files, verify at least one call exists
      in the extension scope (Grep by name across all .bsl in extension directory).
      Exceptions: event handlers (РћР±СЂР°Р±РѕС‚С‡РёРєРЎРѕР±С‹С‚РёСЏ), BSP-registered commands
      (ExternalDataProcessorInfo / Р’РЅРµС€РЅСЏСЏРћР±СЂР°Р±РѕС‚РєР°РЎРІРµРґРµРЅРёСЏ), callback procedures
      passed as string to РћРїРёСЃР°РЅРёРµРћРїРѕРІРµС‰РµРЅРёСЏ or РћР±СЂР°Р±РѕС‚РєР°Р’РЅРµС€РЅРµРіРѕРЎРѕР±С‹С‚РёСЏ.
    - Unused non-export procedure/function вЂ” MEDIUM
    - Unused export procedure/function (no callers found in extension scope) вЂ” HIGH
      (broken public contract or dead API surface)

  Obsolete code markers (std-10 Рї.3.1):
    - Procedure/function with comment "РЈСЃС‚Р°СЂРµР»Р°:" or "Deprecated" вЂ” MEDIUM
      Reason: document replacement or plan removal per std-10 Рї.3.1
    - #РћР±Р»Р°СЃС‚СЊ РЈСЃС‚Р°СЂРµРІС€РёРµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё present вЂ” LOW
      (informational: track obsolete API surface; confirm replacement is documented)
    - Obsolete procedure (marked РЈСЃС‚Р°СЂРµР»Р°:/Deprecated) still called from
      non-obsolete code вЂ” HIGH (caller must migrate to replacement per std-10)

  Unused parameters (std-06):
    - Procedure/function parameter never referenced in body вЂ” LOW
```

## AVAILABLE TOOLS

### Primary validation (BSL LSP NOT_CONNECTED)

Use MCP as primary quality gate:

```yaml
1. Syntax: user-1c-syntax-checker-syntaxcheck(code) вЂ” parse errors
2. Logic: user-1c-code-checker-check_1c_code(code, "logic") вЂ” recommendations
3. Continue with reduced diagnostics; do NOT block review
4. If BSL LSP later available вЂ” switch to bsl_lsp_* for full diagnostics
```

### BSL LSP Bridge (when available)
```yaml
bsl_lsp_diagnostics(file_path):
  - Get all diagnostics: errors, warnings, hints
  - Categorize by severity
  - Prioritize fixes

bsl_lsp_symbols(file_path):
  - Get function list
  - Analyze complexity
  - Check naming

bsl_lsp_format(file_path):
  - Validate formatting
  - Suggest improvements
```

### Skills
```yaml
1c-bsp:
  - Check Р‘РЎРџ patterns and registration
  - Validate command structure
  - Verify ExternalDataProcessorInfo

1c-agent-patterns:
  - Agent delegation patterns, review workflow
  - Spec-driven validation
```

### MCP Servers
```yaml
user-1c-syntax-checker-syntaxcheck(code):
  - Validate BSL syntax
  - Check for parse errors

user-1c-code-checker-check_1c_code(code, check_type):
  - Logic analysis via 1РЎ:РќР°РїР°СЂРЅРёРє
  - Performance recommendations
  - Best practices

user-PROJECT-codemetadata (project-specific MCP)-codesearch(query):
  - Find similar code
  - Check for duplicates
  - Learn from existing solutions

user-PROJECT-graph (project-specific MCP)-search_metadata(query):
  - Analyze metadata dependencies
  - Check for circular references
  - Validate object relationships
```

### RLM Integration (РєРѕРіРґР° РїРѕРґРєР»СЋС‡РµРЅ)
```yaml
status: NOT_CONNECTED
РљРѕРіРґР° РґРѕСЃС‚СѓРїРµРЅ:
  user-rlm-toolkit-rlm_route_context(query) вЂ” context from past reviews
  user-rlm-toolkit-rlm_add_hierarchical_fact(...) вЂ” record findings
  user-rlm-toolkit-rlm_record_causal_decision(...) вЂ” document choices
```

## REVIEW WORKFLOW

### Phase 0: Intent & Reasoning Analysis (РІС‹РїРѕР»РЅСЏС‚СЊ РџР•Р Р’Р«Рњ, РµСЃР»Рё РЅРµ СЃСЂР°Р±РѕС‚Р°Р» Skip Gate)

**Skip Gate:** РџСЂРѕРїСѓСЃС‚РёС‚СЊ Phase 0, РµСЃР»Рё РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ Р’РЎР• СѓСЃР»РѕРІРёСЏ: scope СЂРµРІСЊСЋ в‰¤ 10 СЃС‚СЂРѕРє; РЅРµС‚ РІРЅРµС€РЅРёС… РёСЃС‚РѕС‡РЅРёРєРѕРІ РґР°РЅРЅС‹С… (API, СЂРµР·СѓР»СЊС‚Р°С‚С‹ С„СѓРЅРєС†РёР№ СЃРѕ СЃР»РѕР¶РЅС‹РјРё СЃС‚СЂСѓРєС‚СѓСЂР°РјРё); РјР°РєСЃРёРјР°Р»СЊРЅР°СЏ РІР»РѕР¶РµРЅРЅРѕСЃС‚СЊ в‰¤ 2; С‚РѕР»СЊРєРѕ mechanical changes (rename, formatting, regions).

**РћР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р°СЂС‚РµС„Р°РєС‚С‹** вЂ” СЃС‚СЂРѕРёС‚СЊ РґРѕ РіРµРЅРµСЂР°С†РёРё Р·Р°РјРµС‡Р°РЅРёР№; РІРєР»СЋС‡Р°С‚СЊ РІ РѕС‚С‡С‘С‚ (СЃРµРєС†РёСЏ Reasoning Artifacts).

#### 0.1 РђСЂС‚РµС„Р°РєС‚: Intent Map

Р”Р»СЏ РєР°Р¶РґРѕР№ РїСЂРѕС†РµРґСѓСЂС‹/С„СѓРЅРєС†РёРё Рё РєР°Р¶РґРѕРіРѕ Р·РЅР°С‡РёРјРѕРіРѕ Р±Р»РѕРєР° (С†РёРєР», РІРµС‚РІР»РµРЅРёРµ, РџРѕРїС‹С‚РєР°):
- РќР°РјРµСЂРµРЅРёРµ Р±Р»РѕРєР° вЂ” РѕРґРЅРѕ РїСЂРµРґР»РѕР¶РµРЅРёРµ (С‡С‚Рѕ РґРµР»Р°РµС‚).
- РћР¶РёРґР°РµРјР°СЏ СЃР»РѕР¶РЅРѕСЃС‚СЊ вЂ” РёР· РЅР°РјРµСЂРµРЅРёСЏ (СЃРєРѕР»СЊРєРѕ СЃС‚СЂРѕРє/СѓСЂРѕРІРЅРµР№ РІР»РѕР¶РµРЅРЅРѕСЃС‚Рё РЅСѓР¶РЅРѕ РґР»СЏ СЌС‚РѕР№ Р·Р°РґР°С‡Рё).
- Р¤Р°РєС‚РёС‡РµСЃРєР°СЏ СЃР»РѕР¶РЅРѕСЃС‚СЊ вЂ” РёР· РєРѕРґР° (СЃС‚СЂРѕРєРё, СѓСЂРѕРІРЅРё РІР»РѕР¶РµРЅРЅРѕСЃС‚Рё).

Р¤РѕСЂРјР°С‚ (РїСЂРёРјРµСЂ): procedure в†’ intent; blocks в†’ location, intent, expected_complexity, actual_complexity; sub_blocks РїСЂРё РЅРµРѕР±С…РѕРґРёРјРѕСЃС‚Рё.

#### 0.2 РђСЂС‚РµС„Р°РєС‚: Contract Map

Р”Р»СЏ РєР°Р¶РґРѕРіРѕ РёСЃС‚РѕС‡РЅРёРєР° РґР°РЅРЅС‹С… (РїР°СЂР°РјРµС‚СЂ, СЂРµР·СѓР»СЊС‚Р°С‚ РІС‹Р·РѕРІР° API/С„СѓРЅРєС†РёРё) вЂ” С‚Р°Р±Р»РёС†Р° РѕР±СЂР°С‰РµРЅРёР№ Рє РїРѕР»СЏРј РІ СЂР°РјРєР°С… РїСЂРѕС†РµРґСѓСЂС‹/Р±Р»РѕРєР°:
- source, origin (РѕС‚РєСѓРґР° РґР°РЅРЅС‹Рµ).
- field_accesses: field, access, line (РёР»Рё РґРёР°РїР°Р·РѕРЅ).

**РўРёРїС‹ РґРѕСЃС‚СѓРїР° (access):**
- **DIRECT** вЂ” РћР±СЉРµРєС‚.РџРѕР»Рµ, Р±РµР· РїСЂРѕРІРµСЂРѕРє.
- **DEFENSIVE** вЂ” РћР±СЉРµРєС‚.РЎРІРѕР№СЃС‚РІРѕ("РџРѕР»Рµ", ...), РѕРґРЅР° РїСЂРѕРІРµСЂРєР°.
- **EXPLORATORY** вЂ” РЅРµСЃРєРѕР»СЊРєРѕ Р°Р»СЊС‚РµСЂРЅР°С‚РёРІРЅС‹С… РїСѓС‚РµР№ Рє РѕРґРЅРѕРјСѓ СЃРµРјР°РЅС‚РёС‡РµСЃРєРѕРјСѓ Р·РЅР°С‡РµРЅРёСЋ.
- **GUARDED** вЂ” РґРѕСЃС‚СѓРї РїРѕСЃР»Рµ guard clause (Р»СЋР±Р°СЏ РєРѕРЅСЃС‚СЂСѓРєС†РёСЏ: Р•СЃР»Рё РўРёРїР—РЅС‡, РљРѕР»РѕРЅРєРё.РќР°Р№С‚Рё, Р±СѓР»РµРІ С„Р»Р°Рі, Р—РЅР°С‡РµРЅРёРµР—Р°РїРѕР»РЅРµРЅРѕ-as-guard, Р•СЃС‚СЊР РµРєРІРёР·РёС‚ Рё РґСЂ.).

#### 0.3 РђСЂС‚РµС„Р°РєС‚: Knowledge Assessment

Р”Р»СЏ РєР°Р¶РґРѕРіРѕ РёСЃС‚РѕС‡РЅРёРєР° РёР· Contract Map:
- evidence_of_knowledge / evidence_of_ignorance (СЃРїРёСЃРєРё).
- verdict: FULL / PARTIAL / ABSENT.
- explanation (РѕРґРЅРѕ РїСЂРµРґР»РѕР¶РµРЅРёРµ).

**РђРЅС‚РёРєСЂСѓРіРѕРІРѕРµ РїСЂР°РІРёР»Рѕ:** guard (РЎРІРѕР№СЃС‚РІРѕ, РўРёРїР—РЅС‡, РљРѕР»РѕРЅРєРё.РќР°Р№С‚Рё, Р•СЃС‚СЊР РµРєРІРёР·РёС‚, Р±СѓР»РµРІ С„Р»Р°Рі Рё С‚.Рї.) РќР• СЏРІР»СЏРµС‚СЃСЏ evidence_of_knowledge РґР»СЏ С‚РѕРіРѕ Р¶Рµ РёСЃС‚РѕС‡РЅРёРєР°. Guard вЂ” РѕР±СЉРµРєС‚ РїСЂРѕРІРµСЂРєРё, Р° РЅРµ РґРѕРєР°Р·Р°С‚РµР»СЊСЃС‚РІРѕ. Evidence = Form.xml, РјРµС‚Р°РґР°РЅРЅС‹Рµ РѕР±СЉРµРєС‚Р°, С‚РµРєСЃС‚ Р·Р°РїСЂРѕСЃР°, РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ С„СѓРЅРєС†РёРё, Resolved Contracts, РєРѕРґ РІС‹Р·С‹РІР°РµРјРѕР№ С„СѓРЅРєС†РёРё.

#### 0.4 Evaluation Questions (РіРµРЅРµСЂР°С†РёСЏ Р·Р°РјРµС‡Р°РЅРёР№ Phase 0)

РџРѕСЃР»Рµ РїРѕСЃС‚СЂРѕРµРЅРёСЏ Р°СЂС‚РµС„Р°РєС‚РѕРІ вЂ” Р·Р°РїРѕР»РЅРёС‚СЊ С‚Р°Р±Р»РёС†Сѓ Evaluation Checklist.
РћР‘РЇР—РђРўР•Р›Р¬РќРћ: РґР»СЏ РљРђР–Р”РћР“Рћ РІРѕРїСЂРѕСЃР° Р·Р°С„РёРєСЃРёСЂРѕРІР°С‚СЊ РѕС‚РІРµС‚ (yes/no + РёСЃС‚РѕС‡РЅРёРє/РѕР±РѕСЃРЅРѕРІР°РЅРёРµ).
РџСЂРѕРїСѓСЃРє РІРѕРїСЂРѕСЃР° = Phase 0 РЅРµ Р·Р°РІРµСЂС€РµРЅР°; Рє Phase 1 РЅРµ РїРµСЂРµС…РѕРґРёС‚СЊ.

Evaluation Checklist (РІРєР»СЋС‡РёС‚СЊ РІ РѕС‚С‡С‘С‚ РІ СЃРµРєС†РёРё Reasoning Artifacts):

| # | Р’РѕРїСЂРѕСЃ | РћС‚РІРµС‚ | РСЃС‚РѕС‡РЅРёРє/РѕР±РѕСЃРЅРѕРІР°РЅРёРµ | Finding (РµСЃР»Рё yes) |
|---|--------|-------|----------------------|--------------------|
| 1 | Proportionality: actual > 3x expected РїРѕ СЃС‚СЂРѕРєР°Рј РёР»Рё > 2x РїРѕ РІР»РѕР¶РµРЅРЅРѕСЃС‚Рё? | yes/no | | DISPROPORTIONATE_COMPLEXITY |
| 2 | Consistency: РѕРґРёРЅ РёСЃС‚РѕС‡РЅРёРє вЂ” С‡Р°СЃС‚СЊ РїРѕР»РµР№ DIRECT, С‡Р°СЃС‚СЊ DEFENSIVE/EXPLORATORY? | yes/no | | CONTRACT_INCONSISTENCY |
| 3 | Knowledge: РёСЃС‚РѕС‡РЅРёРєРё СЃ verdict PARTIAL РёР»Рё ABSENT? | yes/no | | KNOWLEDGE_DEFICIT |
| 4 | Exploratory: РїРѕР»СЏ СЃ access=EXPLORATORY? | yes/no | | CONTRACT_INFERENCE |
| 5 | РџРѕРїС‹С‚РєР° as contract compensation: РёСЃС‚РѕС‡РЅРёРє PARTIAL/ABSENT + РџРѕРїС‹С‚РєР° РЅР° РµРіРѕ РїРѕР»СЏС…? | yes/no | | KNOWLEDGE_DEFICIT + contract-compensating-try |
| 6 | Naming: РµСЃС‚СЊ РёРґРµРЅС‚РёС„РёРєР°С‚РѕСЂС‹, С‡СЊС‘ РёРјСЏ (a) РѕС‚СЂР°Р¶Р°РµС‚ РїРѕСЃС‚Р°РЅРѕРІРєСѓ/РѕСЂРєРµСЃС‚СЂР°С†РёСЋ, (b) РѕРїРёСЃС‹РІР°РµС‚ СЂРѕР»СЊ РІ РєРѕРґРµ (РєРѕРЅС‚РµР№РЅРµСЂ, РїСЂРѕРјРµР¶СѓС‚РѕС‡РЅРѕРµ, РЅР°РєРѕРїРёС‚РµР»СЊ) Р±РµР· РґРѕРјРµРЅРЅРѕРіРѕ РєРІР°Р»РёС„РёРєР°С‚РѕСЂР°, РёР»Рё (c) РїСЂРё РЅР°Р»РёС‡РёРё РІ С‚РѕРј Р¶Рµ scope РґРѕРјРµРЅРЅРѕ РЅР°Р·РІР°РЅРЅС‹С… РґР°РЅРЅС‹С… вЂ” РєРѕРЅС‚РµР№РЅРµСЂ РґР»СЏ РЅРёС… РЅРµ РѕС‚СЃС‹Р»Р°РµС‚ Рє РґРѕРјРµРЅСѓ? РўРµСЃС‚: РјС‹СЃР»РµРЅРЅРѕ СѓР±СЂР°С‚СЊ СЂРµР°Р»РёР·Р°С†РёРѕРЅРЅРѕРµ СЃР»РѕРІРѕ (РњР°СЃСЃРёРІ, РќРѕРІС‹Р№, Р”РѕР±Р°РІР»СЏРµРјС‹Рµ) вЂ” РѕСЃС‚Р°С‘С‚СЃСЏ Р»Рё РґРѕРјРµРЅРЅС‹Р№ СЃРјС‹СЃР»? (СЃРј. AP-031) | yes/no | | CLARITY_DEFICIT + Supporting AP-031 (РёР»Рё РѕС‚РґРµР»СЊРЅРѕРµ finding AP-031 Р±РµР· РґСѓР±Р»РёСЂРѕРІР°РЅРёСЏ СЃ CLARITY РІ С‚РѕРј Р¶Рµ РјРµСЃС‚Рµ) |
| 7 | Authority: РєРѕРґ Р»РѕРєР°Р»СЊРЅРѕ СЂРµР°Р»РёР·СѓРµС‚ РїРѕРІРµРґРµРЅРёРµ, Сѓ РєРѕС‚РѕСЂРѕРіРѕ РµСЃС‚СЊ СЏРІРЅС‹Р№ РІР»Р°РґРµР»РµС† (Р±Р°Р·Р°, Р‘РЎРџ, РїР»Р°С‚С„РѕСЂРјР°, РѕР±С‰РёР№ РјРѕРґСѓР»СЊ, РІРЅРµС€РЅРёР№ РєРѕРЅС‚СЂР°РєС‚), Рё РґРѕСЃС‚СѓРїРµРЅ РјРµС…Р°РЅРёР·Рј РґРµР»РµРіРёСЂРѕРІР°РЅРёСЏ РІР»Р°РґРµР»СЊС†Сѓ? | yes/no | | AUTHORITY_MISPLACEMENT + Supporting AP-047 |

Completeness gate: 7 СЃС‚СЂРѕРє РІ С‚Р°Р±Р»РёС†Рµ. РњРµРЅСЊС€Рµ вЂ” Phase 0 РЅРµ Р·Р°РІРµСЂС€РµРЅР°.

РљР°Р¶РґС‹Р№ yes в†’ Р·Р°РјРµС‡Р°РЅРёРµ СЃ counterfactual. Supporting: РїСЂРё СЃРѕРІРїР°РґРµРЅРёРё СЃ AP СѓРєР°Р·Р°С‚СЊ AP-NNN, РЅРµ РґСѓР±Р»РёСЂРѕРІР°С‚СЊ.

### Phase 1: Initial Analysis
```yaml
1. Check syntax (primary): user-1c-syntax-checker-syntaxcheck(code)
2. Analyze logic: user-1c-code-checker-check_1c_code(code, "logic")
3. If BSL LSP available: bsl_lsp_diagnostics(file_path), bsl_lsp_symbols(file_path)
   Else: proceed with MCP-only; manual structure analysis from Read(file)
```

### Phase 1b: BSL Linter Signals Gate (РћР‘РЇР—РђРўР•Р›Р¬РќРћ РїСЂРё РЅР°Р»РёС‡РёРё Р±Р»РѕРєР° `## Linter Signals (evidence)`)

**РџРѕР»РёС‚РёРєР°:** РїСЂРµРґСѓРїСЂРµР¶РґРµРЅРёСЏ bsl-language-server / `ReadLints` РЅР° **in-scope** СЃС‚СЂРѕРєР°С… **РЅРµ РѕС‚РєР»Р°РґС‹РІР°СЋС‚СЃСЏ** РЅР° РїСЂРµРґСЂРµР»РёР·РЅРѕРµ СЂРµРІСЊСЋ. РџРѕРіР°С€РµРЅРёРµ РґРѕРєСѓРјРµРЅС‚Р°С†РёРѕРЅРЅРѕРіРѕ Рё СЃС‚СЂСѓРєС‚СѓСЂРЅРѕРіРѕ С‚РµС…РґРѕР»РіР° РїРѕР·Р¶Рµ РїРѕРІС‹С€Р°РµС‚ СЂРёСЃРє СЂРµРіСЂРµСЃСЃР° (РїСЂР°РІРєРё С€Р°РїРѕРє/JSDoc/Р°РЅРЅРѕС‚Р°С†РёР№ РЅР° СѓР¶Рµ РїСЂРёРЅСЏС‚РѕРј РєРѕРґРµ).

**In-scope** (Р»СЋР±РѕРµ РёР·):
- СЃС‚СЂРѕРєР° РїРѕРїР°РґР°РµС‚ РІ `## Review Boundaries` (diff-focused);
- СЃС‚СЂРѕРєР° РІ С‚РµР»Рµ/С€Р°РїРєРµ РїСЂРѕС†РµРґСѓСЂС‹ РёР»Рё С„СѓРЅРєС†РёРё, СЃРѕР·РґР°РЅРЅРѕР№ РёР»Рё РёР·РјРµРЅС‘РЅРЅРѕР№ РІ С‚РµРєСѓС‰РµР№ Р·Р°РґР°С‡Рµ writer;
- `[module-level]` РІ РіСЂР°РЅРёС†Р°С… СЂРµРІСЊСЋ.

**РђР»РіРѕСЂРёС‚Рј (РґР»СЏ РєР°Р¶РґРѕР№ СЃС‚СЂРѕРєРё С‚Р°Р±Р»РёС†С‹ Linter Signals СЃ severity `warning` РёР»Рё `error`):**

| РЁР°Рі | Р”РµР№СЃС‚РІРёРµ |
|-----|----------|
| 1 | **confirm в†’ MUST_FIX** (default РґР»СЏ in-scope warning/error). Severity finding: **MEDIUM** РґР»СЏ РґРѕРєСѓРјРµРЅС‚Р°С†РёРё (`MissingReturnedValueDescription`, `MissingParameterDescription`, `MissingDescription`, вЂ¦); **HIGH** РµСЃР»Рё warning СѓРєР°Р·С‹РІР°РµС‚ РЅР° СЂРёСЃРє РїРѕРІРµРґРµРЅРёСЏ/РєРѕРЅС‚СЂР°РєС‚Р°. |
| 2 | **dismiss** вЂ” С‚РѕР»СЊРєРѕ СЃ СЏРІРЅРѕР№ РїСЂРёС‡РёРЅРѕР№ РІ РѕС‚С‡С‘С‚Рµ: `out-of-scope` (РІРЅРµ Review Boundaries), `false-positive` (РѕР±РѕСЃРЅРѕРІР°РЅРёРµ + СЃС‚СЂРѕРєР° РєРѕРґР°), `pre-existing-unchanged` (full-СЂРµРІСЊСЋ: РїСЂРѕС†РµРґСѓСЂР° РЅРµ РјРµРЅСЏР»Р°СЃСЊ РІ С‚РµРєСѓС‰РµРј diff). |
| 3 | **reclassify** вЂ” РµСЃР»Рё warning РґСѓР±Р»РёСЂСѓРµС‚ Phase 0 / AP finding, РѕР±СЉРµРґРёРЅРёС‚СЊ; РЅРµ СЃРѕР·РґР°РІР°С‚СЊ РІС‚РѕСЂРѕР№ MUST_FIX РЅР° С‚Рѕ Р¶Рµ РјРµСЃС‚Рѕ. |

**Р—Р°РїСЂРµС‰С‘РЅРЅС‹Рµ РѕСЃРЅРѕРІР°РЅРёСЏ РґР»СЏ dismiss:** В«РЅРµ Р±Р»РѕРєРёСЂСѓРµС‚ applyВ», В«РѕС‚Р»РѕР¶РёРј РЅР° prereleaseВ», В«СЃС‚РёР»СЊВ», В«Р»РёРЅС‚РµСЂ СЃР»РёС€РєРѕРј СЃС‚СЂРѕРіРёР№В» Р±РµР· `false-positive`.

**Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ (JSDoc / С€Р°РїРєР° РјРµС‚РѕРґР°):**
- Р­РєСЃРїРѕСЂС‚РЅС‹Рµ Рё РїРµСЂРµС…РІР°С‚С‹РІР°СЋС‰РёРµ (`&Р’РјРµСЃС‚Рѕ`, `&РџРѕСЃР»Рµ`, `&РџРµСЂРµРґ`) РїСЂРѕС†РµРґСѓСЂС‹/С„СѓРЅРєС†РёРё in-scope **Р±РµР·** Р±Р»РѕРєРѕРІ В«РџР°СЂР°РјРµС‚СЂС‹:В» / В«Р’РѕР·РІСЂР°С‰Р°РµРјРѕРµ Р·РЅР°С‡РµРЅРёРµ:В» (РµСЃР»Рё РїСЂРёРјРµРЅРёРјРѕ) в†’ **MUST_FIX**.
- JSDoc СЂР°Р·РјРµС‰Р°С‚СЊ **РІС‹С€Рµ** Р°РЅРЅРѕС‚Р°С†РёР№ СЂР°СЃС€РёСЂРµРЅРёСЏ (`&Р’РјРµСЃС‚Рѕ`, вЂ¦), РЅРµ РјРµР¶РґСѓ Р°РЅРЅРѕС‚Р°С†РёРµР№ Рё РѕР±СЉСЏРІР»РµРЅРёРµРј (std-06 / vendor doc comments).
- РўРёРї РєРѕР»Р»РµРєС†РёРё: `РњР°СЃСЃРёРІ РёР· РўРёРї1, РўРёРї2 вЂ” вЂ¦`, РЅРµ В«РњР°СЃСЃРёРІ СЃСЃС‹Р»РѕРєВ» Р±РµР· СѓС‚РѕС‡РЅРµРЅРёСЏ СЌР»РµРјРµРЅС‚РѕРІ.

**Completeness gate Phase 1b:** РµСЃР»Рё РІ РїСЂРѕРјРїС‚Рµ РµСЃС‚СЊ `## Linter Signals (evidence)` СЃ в‰Ґ1 in-scope warning Рё РЅРё РѕРґРЅРѕРіРѕ finding СЃ Action MUST_FIX РёР»Рё СЏРІРЅРѕРіРѕ dismiss РІ РѕС‚С‡С‘С‚Рµ вЂ” Phase 1b **РЅРµ Р·Р°РІРµСЂС€РµРЅР°**; Status в‰  PASS.

**Р•СЃР»Рё Р±Р»РѕРє РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ РёР»Рё `Linter unavailable`:** Р·Р°С„РёРєСЃРёСЂРѕРІР°С‚СЊ РІ Summary `Linter Signals: unavailable`; РґР»СЏ **РЅРѕРІС‹С…** in-scope `Р¤СѓРЅРєС†РёСЏ`/`РџСЂРѕС†РµРґСѓСЂР°` Р±РµР· С€Р°РїРєРё вЂ” РІСЂСѓС‡РЅСѓСЋ РїСЂРѕРІРµСЂРёС‚СЊ РґРѕРєСѓРјРµРЅС‚Р°С†РёСЋ (Phase 2 Рї.3) Рё РІС‹РґР°С‚СЊ MUST_FIX РїСЂРё РѕС‚СЃСѓС‚СЃС‚РІРёРё.

**Р¤РѕСЂРјР°С‚ finding (Linter):**
```yaml
[MEDIUM] Line N: MissingReturnedValueDescription (bsl-language-server)
  Procedure: <РёРјСЏ>
  Anchor: <СЃС‚СЂРѕРєР° РѕР±СЉСЏРІР»РµРЅРёСЏ>
  Action: MUST_FIX
  Issue: Linter warning on in-scope line; not deferred to prerelease
  Fix: <РєРѕРЅРєСЂРµС‚РЅР°СЏ С€Р°РїРєР° / РїРµСЂРµРЅРѕСЃ JSDoc>
  kind: linter-signal
  LinterRule: MissingReturnedValueDescription
  LinterVerdict: confirm
```

**Status PASS:** С‚РѕР»СЊРєРѕ РµСЃР»Рё РЅРµС‚ unresolved MUST_FIX РёР· Phase 0, Phase 1b, Phase 2вЂ“2.5 Рё Standards.

### Phase 2: Deep Analysis
```yaml
1. Performance check:
   - Scan for queries in loops
   - Check index usage
   - Analyze algorithm complexity
   - Measure database calls

2. Security audit:
   - Check for SQL injection
   - Validate input sanitization
   - Review access control
   - Check for hardcoded secrets

3. Р‘РЎРџ compliance:
   - Verify naming conventions
   - Check module structure
   - Validate error handling
   - Review documentation

4. Code quality:
   - Calculate cyclomatic complexity
   - Detect code duplication
   - Check function length
   - Analyze parameter count
   - Fail-fast: scan for silent skips on structural checks (РџСЂРѕРґРѕР»Р¶РёС‚СЊ, silent Р’РѕР·РІСЂР°С‚, empty branch when precondition fails on type/property/size/format) вЂ” AP-021. See anti-pattern registry
   - Data contract: в†’ see AP-004, AP-005, AP-006 in anti-pattern registry (category 16)
   - Design authority: design.md decisions do NOT exempt code from anti-pattern checks. Tag: "design-prescribed anti-pattern".
   - Detect stub/placeholder code: empty Thumbprint, hardcoded "TODO" return values, always-false conditions вЂ” HIGH вЂ” AP-024 (always, not prerelease-only). See anti-pattern registry
   - Parameter integrity: в†’ see AP-007 in anti-pattern registry (category 16)
   - Magic constants: detect same numeric (not 0/1/-1) or string literal appearing 2+ times in module. See 1c-coding-standards.mdc rule 22
   - Mixed responsibilities: detect procedures >40 lines combining 3+ concerns (rights, transaction, business logic, persistence, logging, UI)

4.5. РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ audit вЂ” see Phase 2.5 (dedicated pass).
     Do NOT audit РџРѕРїС‹С‚РєР° blocks inline here; Phase 2.5 handles this systematically.

4.6. API existence (from orchestrator):
   If orchestrator passed API_VERIFIED / UNCHECKED_API items:
   - VERIFIED: no action needed
   - UNCHECKED_API: note in report as INFO ("method not verified, external dependency")
   If orchestrator did NOT pass API check results: skip (backward compatibility)

4.7. Contract Provenance Audit вЂ” see Phase 2.5 (dedicated pass).
     Do NOT audit defensive checks inline here; Phase 2.5 handles this systematically.

5. Extension annotations:
   - Detect &РџРµСЂРµРґ/&РџРѕСЃР»Рµ applied to a function (not procedure) вЂ” AP-022 CRITICAL. See anti-pattern registry
   - Detect &Р’РјРµСЃС‚Рѕ where &РџРµСЂРµРґ/&РџРѕСЃР»Рµ is sufficient
   - Detect &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ where code outside directives differs from base: variable renaming, formatting changes, refactoring outside #Р’СЃС‚Р°РІРєР°/#РљРѕРЅРµС†Р’СЃС‚Р°РІРєРё, adding/removing #РћР±Р»Р°СЃС‚СЊ in base (typed) code, NEW CODE added outside directive blocks
   - Detect business logic directly in #Р’СЃС‚Р°РІРєР° block
   - Detect AP-046: hook procedure starts with early Р’РѕР·РІСЂР°С‚ under non-structural guard (feature-flag, business filter); body в‰Ґ 5 lines or в‰Ґ 2 distinct concerns. Exclude AP-021 (structural fail-fast). For &Р’РјРµСЃС‚Рѕ: early Р’РѕР·РІСЂР°С‚ without subsequent РџСЂРѕРґРѕР»Р¶РёС‚СЊР’С‹Р·РѕРІ = CRITICAL.
   - Detect AP-047: code claims to preserve base/BSP/platform/common-module behavior but implements a local equivalent instead of delegating to the owner (`РџСЂРѕРґРѕР»Р¶РёС‚СЊР’С‹Р·РѕРІ(...)`, С€С‚Р°С‚РЅС‹Р№ API, Р‘РЎРџ-РѕР±С‘СЂС‚РєР°, РѕР±С‰РёР№ РјРѕРґСѓР»СЊ). Treat as AUTHORITY_MISPLACEMENT when found in Phase 0.
   - &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ VERIFICATION: for each method with this annotation, load base from cf/ path
     (replace cfe/<ExtName>/ with cf/), extract code outside directive blocks, diff against base.
     Any diff (added/deleted/modified lines outside directives) = CRITICAL (prerelease) / HIGH (normal).
     Base file not found = NEEDS_MANUAL_REVIEW.

6. Module structure:
   - Check presence of #РћР±Р»Р°СЃС‚СЊ markup (flag as MEDIUM only if module > 100 lines; otherwise LOW)
   - Check order: РџСЂРѕРіСЂР°РјРјРЅС‹Р№РРЅС‚РµСЂС„РµР№СЃ в†’ РЎР»СѓР¶РµР±РЅС‹Р№РџСЂРѕРіСЂР°РјРјРЅС‹Р№РРЅС‚РµСЂС„РµР№СЃ в†’ РЎР»СѓР¶РµР±РЅС‹РµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё
   - Detect duplicate #РћР±Р»Р°СЃС‚СЊ/#РљРѕРЅРµС†РћР±Р»Р°СЃС‚Рё directives
   - Detect Export methods in #РћР±Р»Р°СЃС‚СЊ РЎР»СѓР¶РµР±РЅС‹РµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё
   - Detect Export procedures/functions in form module (Forms/*/Module.bsl): any РџСЂРѕС†РµРґСѓСЂР°/Р¤СѓРЅРєС†РёСЏ with Р­РєСЃРїРѕСЂС‚ keyword.
     Exception: РџРѕРґРєР»СЋС‡Р°РµРјС‹Р№_* prefix (BSP attachable commands), callback exports for РћРїРёСЃР°РЅРёРµРћРїРѕРІРµС‰РµРЅРёСЏ(..., Р­С‚РѕС‚РћР±СЉРµРєС‚).
     Each non-excepted export = AP-033 HIGH. See anti-pattern registry.
   - Verify module header comment matches actual module name
   - Check module header comment

7. Method documentation:
   - Detect export methods without header comment
   - Detect event handlers without description
   - Validate header format (РџР°СЂР°РјРµС‚СЂС‹ / Р’РѕР·РІСЂР°С‰Р°РµРјРѕРµ Р·РЅР°С‡РµРЅРёРµ / РџСЂРёРјРµСЂ)

8. Extension naming:
   - Detect intercepted methods (&Р’РјРµСЃС‚Рѕ/&РџРµСЂРµРґ/&РџРѕСЃР»Рµ) without extension prefix
   - Detect own methods (non-intercept) incorrectly using extension prefix
   - Detect export own methods with non-descriptive names
   - Detect inconsistent prefix usage: exports with and without extension prefix in same module

9. Code cleanliness:
   - Detect changelog markers (// +++ Author, // ---, date-author comments)
   - Detect design/process artifact references in comments: short-form (D11, F5, Design В§3),
     natural-language (РџРѕ design Decision N, fix-signing-result), process terms, task numbers
   - Meta-naming (AP-031): identifiers reflecting task/orchestration language or failing domain-clarity test; see full card in anti-pattern registry; export = HIGH, local/internal = MEDIUM; Remediation: propose domain synonym in finding
   - Dead code вЂ” see category 15 (Obsolete and Unused Code)
   - Detect logic duplication between modules
   - Detect commented-out code without explanation

10. Specific 1C patterns: в†’ see AP-001..AP-050 in anti-pattern registry (category 16)
  AP-033: Export procedure/function in form module (Form-as-Service) вЂ” HIGH
    Remain inline:
    - Ternary operator ?() вЂ” MEDIUM
    - Excessive info logging inside loop or 3+ info-level calls вЂ” LOW

10.5. Integration exchange:
   - If integration exchange trigger matched, read `.cursor/docs/standard/std-12-integration-exchange.md`.
   - Detect AP-048: manual GUID/reference serialization in JSON/exchange; prefer `XMLРЎС‚СЂРѕРєР°(<РЎСЃС‹Р»РєР°>)`.
   - Detect AP-049: numeric string through `РЎС‚СЂРѕРєР°()` + whitespace cleanup; prefer `Р¤РѕСЂРјР°С‚(<Р§РёСЃР»Рѕ>, "Р§Р“=0")`.
   - Detect AP-050 only semantically for blocking messages near `РћС‚РєР°Р· = РСЃС‚РёРЅР°`, `Р’С‹Р·РІР°С‚СЊРСЃРєР»СЋС‡РµРЅРёРµ`, `РЎРѕРѕР±С‰РёС‚СЊРџРѕР»СЊР·РѕРІР°С‚РµР»СЋ`, `РџРѕРєР°Р·Р°С‚СЊРџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ`. Do NOT flag neutral informational messages, administrator diagnostics, or strings where the form context already shows the field/action.

11. Band-aid detection: в†’ see AP-016 in anti-pattern registry (category 16)
    Remain inline:
    - Design-prescribed anti-pattern (tag: design-prescribed)

12. Release readiness (prerelease only):
    - Typos and mixed Cyrillic/Latin in user-facing strings
    - Stub code вЂ” see category 4 (always checked)
    - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ without logging вЂ” see category 10 (always-checked); do NOT duplicate

13. Transactions and locking:
    AP-015: Transaction without safety pattern вЂ” CRITICAL (see anti-pattern registry)
    AP-023: User interaction (РџРѕРєР°Р·Р°С‚СЊР’РѕРїСЂРѕСЃ, РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ, РЎРѕРѕР±С‰РёС‚СЊ) inside transaction вЂ” HIGH. See anti-pattern registry
    Remain inline:
    - Read-then-write without Р‘Р»РѕРєРёСЂРѕРІРєР°Р”Р°РЅРЅС‹С… in concurrent scenario вЂ” HIGH
    - Nested РќР°С‡Р°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ() without justification вЂ” MEDIUM

14. Resource leaks:
    - COMРћР±СЉРµРєС‚ (РќРѕРІС‹Р№ COMРћР±СЉРµРєС‚()) without РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ ensuring release
    - HTTPРЎРѕРµРґРёРЅРµРЅРёРµ/FTPРЎРѕРµРґРёРЅРµРЅРёРµ not wrapped in РџРѕРїС‹С‚РєР° for error handling
    - File reader/writer opened without close in error path
    - Temporary file created without cleanup in error path

15. Obsolete and unused code:
    - For each РџСЂРѕС†РµРґСѓСЂР°/Р¤СѓРЅРєС†РёСЏ: Grep by name across all .bsl in extension directory
      to verify at least one call exists. Skip: event handlers, BSP commands, callbacks.
    - Unused non-export в†’ MEDIUM; unused export в†’ HIGH
    - Comment "РЈСЃС‚Р°СЂРµР»Р°:" / "Deprecated" or #РћР±Р»Р°СЃС‚СЊ РЈСЃС‚Р°СЂРµРІС€РёРµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё в†’ MEDIUM/LOW
    - Obsolete procedure still called from non-obsolete code в†’ HIGH
    - Unused parameter (never referenced in body) в†’ LOW

16. Anti-pattern registry (reviewer-only, NOT loaded for writer):
    - Read `.cursor/rules/bsl-antipatterns.mdc` (index with AP-NNN IDs and detection rules).
    - For each AP-NNN: check reviewed code against detection rule in the index.
    - If detection rule matches: Read full card from `.cursor/docs/antipatterns/bsl-antipatterns.md`
      for examples and fix guidance.
    - Report finding with AP-NNN ID for traceability.
    - Anti-patterns are NOT auto-loaded for writer to avoid misinterpretation
      of BAD/GOOD examples as coding instructions.
```

### Phase 2.5: РџРѕРїС‹С‚РєР° & Contract Audit (MANDATORY, РІС‹РїРѕР»РЅСЏС‚СЊ Р”Рћ Phase 3)

Р’С‹РґРµР»РµРЅРЅС‹Р№ РїСЂРѕС…РѕРґ **С‚РѕР»СЊРєРѕ** РґР»СЏ Р±Р»РѕРєРѕРІ РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ Рё РѕР±РѕСЂРѕРЅРёС‚РµР»СЊРЅС‹С… РїСЂРѕРІРµСЂРѕРє (РЎРІРѕР№СЃС‚РІРѕ/РўРёРїР—РЅС‡ Рє РІРЅРµС€РЅРёРј РґР°РЅРЅС‹Рј). РљРѕРЅСЃРѕР»РёРґРёСЂСѓРµС‚ Р»РѕРіРёРєСѓ РёР· С€Р°РіРѕРІ 4.5 Рё 4.7. Рљ Phase 3 РЅРµ РїРµСЂРµС…РѕРґРёС‚СЊ, РїРѕРєР° Phase 2.5 РЅРµ Р·Р°РІРµСЂС€РµРЅР°.

**SKEPTIC'S STANCE (РїСЂРёРЅС†РёРї СЃРєРµРїС‚РёРєР°):** РљР°Р¶РґР°СЏ Р·Р°С‰РёС‚РЅР°СЏ РїСЂРѕРІРµСЂРєР° (guard) РІРёРЅРѕРІРЅР°, РїРѕРєР° РЅРµ РґРѕРєР°Р·Р°РЅР° РѕР±СЂР°С‚РЅР°СЏ. РќР°Р»РёС‡РёРµ guard РІ РєРѕРґРµ вЂ” РќР• РґРѕРєР°Р·Р°С‚РµР»СЊСЃС‚РІРѕ С‚РѕРіРѕ, С‡С‚Рѕ guard РЅСѓР¶РµРЅ. РљРѕРЅС‚СЂР°РєС‚ РёСЃС‚РѕС‡РЅРёРєР° РѕРїСЂРµРґРµР»СЏС‚СЊ РўРћР›Р¬РљРћ РёР· РІРЅРµС€РЅРёС… РёСЃС‚РѕС‡РЅРёРєРѕРІ (Form.xml, РјРµС‚Р°РґР°РЅРЅС‹Рµ, С‚РµРєСЃС‚ Р·Р°РїСЂРѕСЃР°, РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ, Resolved Contracts, РєРѕРґ РІС‹Р·С‹РІР°РµРјРѕР№ С„СѓРЅРєС†РёРё). Р•СЃР»Рё РµРґРёРЅСЃС‚РІРµРЅРЅРѕРµ РѕСЃРЅРѕРІР°РЅРёРµ СЃС‡РёС‚Р°С‚СЊ РєРѕРЅС‚СЂР°РєС‚ РЅРµС„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Рј вЂ” СЃР°Рј guard в†’ Contract verified? = **needs-verification** (РЅРµ OK, РЅРµ optional).

```yaml
A. Enumerate:
   - РќР°Р№С‚Рё Р’РЎР• Р±Р»РѕРєРё РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ РІ РїСЂРѕРІРµСЂСЏРµРјС‹С… С„Р°Р№Р»Р°С….
   - РЎРѕСЃС‚Р°РІРёС‚СЊ РЅСѓРјРµСЂРѕРІР°РЅРЅС‹Р№ СЃРїРёСЃРѕРє: #, Procedure, approx. line (РёР»Рё РґРёР°РїР°Р·РѕРЅ).

B. Audit each block (РґР»СЏ РљРђР–Р”РћР“Рћ Р±Р»РѕРєР° РёР· СЃРїРёСЃРєР° A вЂ” РѕРґРЅР° СЃС‚СЂРѕРєР° РІ С‚Р°Р±Р»РёС†Рµ РѕС‚С‡С‘С‚Р°):
   - Procedure, Line(s)
   - Operations inside: РїРµСЂРµС‡РёСЃР»РёС‚СЊ РљРђР–Р”РЈР® РѕРїРµСЂР°С†РёСЋ РІРЅСѓС‚СЂРё РџРѕРїС‹С‚РєР° (РІС‹Р·РѕРІ, РїСЂРёСЃРІР°РёРІР°РЅРёРµ, РѕР±СЂР°С‰РµРЅРёРµ Рє РїРѕР»СЋ).
   - Throwability analysis (РґР»СЏ РєР°Р¶РґРѕР№ РѕРїРµСЂР°С†РёРё РёР· Operations inside):
     Р”Р»СЏ РљРђР–Р”РћР™ РѕРїРµСЂР°С†РёРё РѕС‚РІРµС‚РёС‚СЊ: В«РњРѕР¶РµС‚ Р»Рё Р±СЂРѕСЃРёС‚СЊ РёСЃРєР»СЋС‡РµРЅРёРµ? Р•СЃР»Рё РґР° вЂ” РїРѕС‡РµРјСѓ?В»
     РљР»Р°СЃСЃРёС„РёРєР°С†РёСЏ РїСЂРёС‡РёРЅ:
       (a) external-nondeterminism вЂ” СЃРµС‚СЊ, Р¤РЎ, COM, РєРѕРЅРєСѓСЂРµРЅС‚РЅС‹Р№ РґРѕСЃС‚СѓРї
       (b) contract-mismatch вЂ” РѕР±СЂР°С‰РµРЅРёРµ Рє РїРѕР»СЋ/СЃРІРѕР№СЃС‚РІСѓ РґР°РЅРЅС‹С… РІ РїР°РјСЏС‚Рё,
           РєРѕС‚РѕСЂРѕРµ РјРѕР¶РµС‚ РѕС‚СЃСѓС‚СЃС‚РІРѕРІР°С‚СЊ РїСЂРё РЅРµСЃРѕРІРїР°РґРµРЅРёРё РєРѕРЅС‚СЂР°РєС‚Р°
       (c) never-throws вЂ” РїСЂРёСЃРІР°РёРІР°РЅРёРµ, СЃСЂР°РІРЅРµРЅРёРµ, Р°СЂРёС„РјРµС‚РёРєР°, РІС‹Р·РѕРІ
           Р±РµР· РІРЅРµС€РЅРёС… СЌС„С„РµРєС‚РѕРІ
     РќР°Р№С‚РёРџРѕР РµРєРІРёР·РёС‚Сѓ: РЅРµ Р±СЂРѕСЃР°РµС‚ РёСЃРєР»СЋС‡РµРЅРёРµ РїСЂРё РЅРµРЅР°Р№РґРµРЅРЅРѕРј Р·РЅР°С‡РµРЅРёРё
     (РІРѕР·РІСЂР°С‰Р°РµС‚ РїСѓСЃС‚СѓСЋ СЃСЃС‹Р»РєСѓ) в†’ (c).
     РћР±СЂР°С‰РµРЅРёРµ Рє РїРѕР»СЋ РѕР±СЉРµРєС‚Р° РІ РїР°РјСЏС‚Рё (РћР±СЉРµРєС‚.РџРѕР»Рµ) в†’
       РµСЃР»Рё РєРѕРЅС‚СЂР°РєС‚ РіР°СЂР°РЅС‚РёСЂРѕРІР°РЅ: (c);
       РµСЃР»Рё РєРѕРЅС‚СЂР°РєС‚ РЅРµРёР·РІРµСЃС‚РµРЅ/С‡Р°СЃС‚РёС‡РµРЅ: (b).
   - Root cause of РџРѕРїС‹С‚РєР° (РІС‹РІРµСЃС‚Рё РёР· Throwability analysis):
     Р•СЃР»Рё РµСЃС‚СЊ С…РѕС‚СЏ Р±С‹ РѕРґРЅР° (a) в†’ root cause = external-nondeterminism
     Р•СЃР»Рё РІСЃРµ throwable = (b), РЅРµС‚ (a) в†’ root cause = contract-uncertainty
     Р•СЃР»Рё С‚РѕР»СЊРєРѕ (c) в†’ AP-008 (РІСЃРµ РѕРїРµСЂР°С†РёРё РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅС‹)
     РџСЂРё mixed (a)+(b) в†’ РѕС‚РјРµС‚РёС‚СЊ РѕР±Рµ РїСЂРёС‡РёРЅС‹; СЂРµРєРѕРјРµРЅРґРѕРІР°С‚СЊ:
       РІС‹РЅРµСЃС‚Рё contract-РґРѕСЃС‚СѓРї Р·Р° РџРѕРїС‹С‚РєСѓ (РїСЂРѕРІРµСЂРєРё СЃРІРѕР№СЃС‚РІ/С‚РёРїР° РґРѕ РџРѕРїС‹С‚РєРё),
       РѕСЃС‚Р°РІРёС‚СЊ РџРѕРїС‹С‚РєСѓ С‚РѕР»СЊРєРѕ РґР»СЏ (a)-РѕРїРµСЂР°С†РёР№.
   - External factor? yes вЂ” РєР°РєРѕР№ РёРјРµРЅРЅРѕ (СЃРµС‚СЊ/Р¤РЎ/COM/РєРѕРЅРєСѓСЂРµРЅС‚РЅС‹Р№ РґРѕСЃС‚СѓРї/РІСЂРµРјРµРЅРЅРѕРµ С…СЂР°РЅРёР»РёС‰Рµ) / no.
     "Р”Р°РЅРЅС‹Рµ РёР· API СѓР¶Рµ РІ РїР°РјСЏС‚Рё" вЂ” РќР• РІРЅРµС€РЅРёР№ С„Р°РєС‚РѕСЂ. РЎРІРѕР№СЃС‚РІРѕ(), РўРёРїР—РЅС‡(), РїСЂРёСЃРІР°РёРІР°РЅРёРµ, СЃСЂР°РІРЅРµРЅРёРµ вЂ” РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅРЅС‹Рµ РѕРїРµСЂР°С†РёРё.
   - RootCause (РґР»СЏ С‚Р°Р±Р»РёС†С‹): external | contract-uncertainty | deterministic | mixed(ext+contract).
   - Guard before same value? Р•СЃС‚СЊ Р»Рё РЅРµРїРѕСЃСЂРµРґСЃС‚РІРµРЅРЅРѕ РїРµСЂРµРґ СЌС‚РѕР№ РџРѕРїС‹С‚РєР° guard (Р•СЃР»Рё ... Р’РѕР·РІСЂР°С‚/РџСЂРѕРґРѕР»Р¶РёС‚СЊ), РІР°Р»РёРґРёСЂСѓСЋС‰РёР№ С‚Рѕ Р¶Рµ Р·РЅР°С‡РµРЅРёРµ, С‡С‚Рѕ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РІРЅСѓС‚СЂРё? yes/no.
   - Logging in РСЃРєР»СЋС‡РµРЅРёРµ? Р—Р°РїРёСЃСЊР–СѓСЂРЅР°Р»Р°Р РµРіРёСЃС‚СЂР°С†РёРё РёР»Рё re-raise РІ Р±Р»РѕРєРµ РСЃРєР»СЋС‡РµРЅРёРµ? yes/no.
   - Fallback = success for caller? Р’РѕР·РІСЂР°С‚/РїСЂРёСЃРІРѕРµРЅРёРµ РІ РСЃРєР»СЋС‡РµРЅРёРµ РЅРµРѕС‚Р»РёС‡РёРјС‹ РѕС‚ СѓСЃРїРµС…Р° РґР»СЏ РІС‹Р·С‹РІР°СЋС‰РµРіРѕ? yes/no.
   - User feedback on failure? РџСЂРё РџСЂРѕРґРѕР»Р¶РёС‚СЊ/С‚РёС…РѕРј Р’РѕР·РІСЂР°С‚ РµСЃС‚СЊ Р»Рё РЎРѕРѕР±С‰РёС‚СЊРџРѕР»СЊР·РѕРІР°С‚РµР»СЋ РёР»Рё Р’С‹Р·РІР°С‚СЊРСЃРєР»СЋС‡РµРЅРёРµ? yes/no (РёСЃРєР»СЋС‡РµРЅРёРµ: СЏРІРЅРѕ РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅРЅС‹Р№ С‚РёС…РёР№ РїСЂРѕРїСѓСЃРє РІ design/РўР—).
   - Persistent side effects? РћРїРµСЂР°С†РёСЏ РІРЅСѓС‚СЂРё РџРѕРїС‹С‚РєР° Р·Р°РїРёСЃС‹РІР°РµС‚ РІ Р‘Р” (`Р—Р°РїРёСЃР°С‚СЊ`, `Р—Р°С„РёРєСЃРёСЂРѕРІР°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ`, `РќР°С‡Р°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ` РІ СЃРІСЏР·РєРµ СЃ Р·Р°РїРёСЃСЊСЋ) РёР»Рё РІС‹Р·С‹РІР°РµС‚ РїСЂРѕС†РµРґСѓСЂСѓ/С„СѓРЅРєС†РёСЋ, РєРѕС‚РѕСЂР°СЏ РїРёС€РµС‚ (1 СѓСЂРѕРІРµРЅСЊ callee РІ С‚РѕРј Р¶Рµ СЂРµРїРѕР·РёС‚РѕСЂРёРё)? yes вЂ” РєР°РєРёРµ / no.
   - Re-raise in РСЃРєР»СЋС‡РµРЅРёРµ? Р•СЃС‚СЊ `Р’С‹Р·РІР°С‚СЊРСЃРєР»СЋС‡РµРЅРёРµ` РІ Р±Р»РѕРєРµ РСЃРєР»СЋС‡РµРЅРёРµ (РІ С‚.С‡. Р±РµР· Р°СЂРіСѓРјРµРЅС‚Р°)? yes/no.
   - Downstream dependency? РљРѕРґ РїРѕСЃР»Рµ РљРѕРЅРµС†РџРѕРїС‹С‚РєРё (РёР»Рё РїРѕСЃР»Рµ С†РёРєР»Р°, РёР»Рё caller РїРѕСЃР»Рµ РІС‹Р·РѕРІР° РїСЂРѕС†РµРґСѓСЂС‹) Р·Р°РІРёСЃРёС‚ РѕС‚ СѓСЃРїРµС€РЅРѕСЃС‚Рё СЌС‚РѕР№ Р·Р°РїРёСЃРё? yes (РѕРїРёСЃР°С‚СЊ) / no / uncertain.
   - Verdict: СЃРїРёСЃРѕРє Р’РЎР•РҐ СЃСЂР°Р±РѕС‚Р°РІС€РёС… AP РґР»СЏ СЌС‚РѕРіРѕ Р±Р»РѕРєР°: OK | AP-008 | AP-009 | AP-010 | AP-027 | AP-029 | AP-030 | AP-032 | contract-compensating-try | redundant layering.
   РљСЂРёС‚РёС‡РµСЃРєРѕРµ РїСЂР°РІРёР»Рѕ: РЅР°С…РѕР¶РґРµРЅРёРµ РѕРґРЅРѕРіРѕ AP РќР• Р·Р°РєСЂС‹РІР°РµС‚ РїСЂРѕРІРµСЂРєСѓ РѕСЃС‚Р°Р»СЊРЅС‹С… РєСЂРёС‚РµСЂРёРµРІ. Verdict = РІСЃРµ РїСЂРёРјРµРЅРёРјС‹Рµ (РЅР°РїСЂРёРјРµСЂ: AP-008, AP-010).
   RootCause = contract-uncertainty в†’ Verdict РІРєР»СЋС‡Р°РµС‚ contract-compensating-try. Р РµРјРµРґРёР°С†РёСЏ РґР»СЏ contract-compensating-try: В«Р—Р°РјРµРЅРёС‚СЊ РџРѕРїС‹С‚РєСѓ РїСЂРѕРІРµСЂРєРѕР№ РєРѕРЅС‚СЂР°РєС‚Р° (С‚РёРї/СЃРІРѕР№СЃС‚РІР°) РґРѕ РѕР±СЂР°С‰РµРЅРёСЏ Рє РїРѕР»СЏРј. Р•СЃР»Рё РєРѕРЅС‚СЂР°РєС‚ РЅРµРІРѕР·РјРѕР¶РЅРѕ РїРѕРґС‚РІРµСЂРґРёС‚СЊ РїРѕ Р±Р°Р·РѕРІРѕРјСѓ РјРѕРґСѓР»СЋ вЂ” РїСЂРѕРІРµСЂРёС‚СЊ РўРёРїР—РЅС‡/РЎРІРѕР№СЃС‚РІРѕ РїРµСЂРµРґ РґРѕСЃС‚СѓРїРѕРј Рє РІР»РѕР¶РµРЅРЅС‹Рј РїРѕР»СЏРј.В»
   **В«РџСЂРѕРІРµСЂСЏР№, Р° РЅРµ Р»РѕРІРёВ» (Check, don't catch):** РµСЃР»Рё РџРѕРїС‹С‚РєР° Р·Р°С‰РёС‰Р°РµС‚ РѕС‚ РЅРµСЃРѕРІРїР°РґРµРЅРёСЏ РєРѕРЅС‚СЂР°РєС‚Р° (contract-uncertainty), РїСЂР°РІРёР»СЊРЅС‹Р№ С„РёРєСЃ вЂ” РїСЂРѕРІРµСЂРёС‚СЊ РєРѕРЅС‚СЂР°РєС‚ (С‚РёРї, СЃРІРѕР№СЃС‚РІР°) РґРѕ РѕР±СЂР°С‰РµРЅРёСЏ Рё СѓР±СЂР°С‚СЊ РџРѕРїС‹С‚РєСѓ, Р° РЅРµ Р»РѕРіРёСЂРѕРІР°С‚СЊ Рё РїСЂРѕРґРѕР»Р¶Р°С‚СЊ. Р›РѕРіРёСЂРѕРІР°РЅРёРµ РїСЂСЏС‡РµС‚ РѕС€РёР±РєСѓ: РєРѕРЅРєСЂРµС‚РЅР°СЏ РёРЅС„РѕСЂРјР°С†РёСЏ РґРѕСЃС‚СѓРїРЅР° С‚РѕР»СЊРєРѕ РІ Р–Р , РЅРµРґРѕСЃС‚СѓРїРЅР° РїРѕР»СЊР·РѕРІР°С‚РµР»СЋ Рё РїРѕРґРґРµСЂР¶РєРµ РІ РјРѕРјРµРЅС‚ РёРЅС†РёРґРµРЅС‚Р°.
   MANDATORY Verdict derivation (РІС‹РїРѕР»РЅСЏС‚СЊ Р”Р›РЇ РљРђР–Р”РћР“Рћ Р±Р»РѕРєР°):
     Р•СЃР»Рё RootCause = contract-uncertainty РёР»Рё mixed(ext+contract):
       в†’ Verdict РћР‘РЇР—РђРќ РІРєР»СЋС‡Р°С‚СЊ contract-compensating-try.
       в†’ Severity: HIGH, Action: MUST_FIX.
       в†’ Log=yes Р UserFeedback=yes РќР• РѕС‚РјРµРЅСЏСЋС‚ contract-compensating-try.
         Р›РѕРіРёСЂРѕРІР°РЅРёРµ Рё СЃРѕРѕР±С‰РµРЅРёРµ РЅРµ СѓСЃС‚СЂР°РЅСЏСЋС‚ РїСЂРёС‡РёРЅСѓ (contract-uncertainty).
       в†’ Р”СЂСѓРіРёРµ AP РїСЂРѕРІРµСЂСЏСЋС‚СЃСЏ Р”РћРџРћР›РќРРўР•Р›Р¬РќРћ, РЅРѕ Verdict РќР• РјРѕР¶РµС‚ Р±С‹С‚СЊ OK.
   MANDATORY Verdict derivation вЂ” persistent state (РІС‹РїРѕР»РЅСЏС‚СЊ Р”Р›РЇ РљРђР–Р”РћР“Рћ Р±Р»РѕРєР°):
     Р•СЃР»Рё Persistent side effects = yes Р Re-raise in РСЃРєР»СЋС‡РµРЅРёРµ = no:
       РџСЂРѕРІРµСЂРёС‚СЊ Downstream dependency:
       в†’ yes РёР»Рё uncertain в†’ Verdict РћР‘РЇР—РђРќ РІРєР»СЋС‡Р°С‚СЊ AP-032.
       в†’ Severity: CRITICAL, Action: MUST_FIX.
       в†’ UserFeedback=yes РќР• РѕС‚РјРµРЅСЏРµС‚ AP-032 (СЃРѕРѕР±С‰РµРЅРёРµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЋ РЅРµ СѓСЃС‚СЂР°РЅСЏРµС‚ СЂР°СЃСЃРѕРіР»Р°СЃРѕРІР°РЅРёРµ РґР°РЅРЅС‹С… РІ Р‘Р”).
       в†’ Log=yes РќР• РѕС‚РјРµРЅСЏРµС‚ AP-032.
       в†’ Р‘Р»РѕРє РІРЅСѓС‚СЂРё С†РёРєР»Р° (Р”Р»СЏ РљР°Р¶РґРѕРіРѕ / Р”Р»СЏ / РџРѕРєР°): Downstream dependency = yes РїРѕ РѕРїСЂРµРґРµР»РµРЅРёСЋ (РіР°СЂР°РЅС‚РёСЂРѕРІР°РЅРЅС‹Р№ partial batch), РµСЃР»Рё callee РёР»Рё С‚РµР»Рѕ РџРѕРїС‹С‚РєР° РїРёС€РµС‚ РІ Р‘Р”.
       в†’ Р РµРјРµРґРёР°С†РёСЏ: (a) СѓР±СЂР°С‚СЊ РџРѕРїС‹С‚РєСѓ / re-raise вЂ” Р°С‚РѕРјР°СЂРЅРѕСЃС‚СЊ; (b) accumulate errors + signal caller + block downstream РґР»СЏ СЃР±РѕР№РЅС‹С… СЌР»РµРјРµРЅС‚РѕРІ.
   РЎРїСЂР°РІРѕС‡РЅРѕ: AP-008 = РІСЃРµ РѕРїРµСЂР°С†РёРё РґРµС‚РµСЂРјРёРЅРёСЂРѕРІР°РЅС‹; AP-009 = fallback РЅРµРѕС‚Р»РёС‡РёРј РѕС‚ СѓСЃРїРµС…Р°; AP-010 = РЅРµС‚ Р»РѕРіР°; AP-027 = guard-then-catch; AP-029 = defense stack; AP-030 = СЃРєСЂС‹С‚С‹Р№ С‡Р°СЃС‚РёС‡РЅС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚; AP-032 = РїРµСЂСЃРёСЃС‚РµРЅС‚РЅС‹Рµ side effects + РїРѕРґР°РІР»РµРЅРёРµ + downstream dependency; contract-compensating-try = РџРѕРїС‹С‚РєР° РєРѕРјРїРµРЅСЃРёСЂСѓРµС‚ РЅРµР·РЅР°РЅРёРµ РєРѕРЅС‚СЂР°РєС‚Р°; redundant layering = INTEGRATION_CONTRACT_GATE (callee СѓР¶Рµ Р»РѕРІРёС‚).

   HIDDEN_PARTIAL_RESULT_GATE cross-check:
     Р•СЃР»Рё РІ С‚Р°Р±Р»РёС†Рµ РџРѕРїС‹С‚РєР° Audit Р±Р»РѕРє РёРјРµРµС‚ RootCause = contract-uncertainty
     Рё Verdict РІРєР»СЋС‡Р°РµС‚ contract-compensating-try:
       в†’ HIDDEN_PARTIAL_RESULT_GATE РґР»СЏ СЌС‚РѕРіРѕ Р±Р»РѕРєР° = FAIL.
       в†’ Р’ РѕС‚С‡С‘С‚Рµ (СЃРµРєС†РёСЏ gates) СѓРєР°Р·Р°С‚СЊ FAIL СЃРѕ СЃСЃС‹Р»РєРѕР№ РЅР° contract-compensating-try finding.
       РџСЂРёС‡РёРЅР°: Р»РѕРі + СЃРѕРѕР±С‰РµРЅРёРµ РјР°СЃРєРёСЂСѓСЋС‚ РѕС€РёР±РєСѓ РєРѕРЅС‚СЂР°РєС‚Р°, Р° РЅРµ СѓСЃС‚СЂР°РЅСЏСЋС‚ СЃРєСЂС‹С‚С‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚.
     AP-032 cross-check:
       Р•СЃР»Рё Persistent side effects = yes Рё Verdict РІРєР»СЋС‡Р°РµС‚ AP-032:
       в†’ HIDDEN_PARTIAL_RESULT_GATE РґР»СЏ СЌС‚РѕРіРѕ Р±Р»РѕРєР° = FAIL.
       в†’ РџСЂРёС‡РёРЅР°: РґР°РЅРЅС‹Рµ РІ Р‘Р” СЂР°СЃСЃРѕРіР»Р°СЃРѕРІР°РЅС‹; СЃРѕРѕР±С‰РµРЅРёРµ РїРѕР»СЊР·РѕРІР°С‚РµР»СЋ / Р»РѕРі РЅРµ СѓСЃС‚СЂР°РЅСЏСЋС‚ Р·Р°РІРёСЃРёРјРѕСЃС‚СЊ downstream-РєРѕРґР° РѕС‚ РЅРµРєРѕРЅСЃРёСЃС‚РµРЅС‚РЅРѕРіРѕ СЃРѕСЃС‚РѕСЏРЅРёСЏ.

C. Defensive checks audit (Contract MapвЂ“driven; РќР• СЃРёРЅС‚Р°РєСЃРёС‡РµСЃРєРёР№ scan):
   **Р”СЂР°Р№РІРµСЂ:** РѕР±С…РѕРґ Р°СЂС‚РµС„Р°РєС‚Р° Contract Map (Phase 0). Р”Р»СЏ РљРђР–Р”РћР“Рћ РёСЃС‚РѕС‡РЅРёРєР° РёР· Contract Map СЃ access != DIRECT (С‚.Рµ. DEFENSIVE, GUARDED, EXPLORATORY), Р° С‚Р°РєР¶Рµ РґР»СЏ РёСЃС‚РѕС‡РЅРёРєРѕРІ, Рє РїРѕР»СЏРј РєРѕС‚РѕСЂС‹С… РѕР±СЂР°С‰Р°СЋС‚СЃСЏ РўРћР›Р¬РљРћ РІРЅСѓС‚СЂРё РџРѕРїС‹С‚РєР° вЂ” РѕРґРЅР° СЃС‚СЂРѕРєР° РІ Defensive Checks Table.
   **Р”Р»СЏ РєР°Р¶РґРѕР№ СЃС‚СЂРѕРєРё:**
   1. Procedure, Line, Source (РѕС‚РєСѓРґР° РґР°РЅРЅС‹Рµ), Field (РёРјСЏ РїРѕР»СЏ/РєРѕР»РѕРЅРєРё/РєР»СЋС‡Р°).
   2. РРґРµРЅС‚РёС„РёС†РёСЂРѕРІР°С‚СЊ РєРѕРЅСЃС‚СЂСѓРєС†РёСЋ guard-Р°: РЎРІРѕР№СЃС‚РІРѕ(), РўРёРїР—РЅС‡(), РљРѕР»РѕРЅРєРё.РќР°Р№С‚Рё("РРјСЏ"), Р±СѓР»РµРІ С„Р»Р°Рі (РїРµСЂРµРјРµРЅРЅР°СЏ/СЂРµРєРІРёР·РёС‚), Р•СЃС‚СЊР РµРєРІРёР·РёС‚РР»РёРЎРІРѕР№СЃС‚РІРѕРћР±СЉРµРєС‚Р°(), Р—РЅР°С‡РµРЅРёРµР—Р°РїРѕР»РЅРµРЅРѕ() РєР°Рє guard, СѓСЃР»РѕРІРёРµ вЂ” Р»СЋР±Р°СЏ.
   3. РћРїСЂРµРґРµР»РёС‚СЊ РєРѕРЅС‚СЂР°РєС‚ РёСЃС‚РѕС‡РЅРёРєР°:
      **ANTI-CIRCULAR GATE:** РїРµСЂРµРґ РѕРїСЂРµРґРµР»РµРЅРёРµРј РєРѕРЅС‚СЂР°РєС‚Р° вЂ” HALT. РџСЂРѕРІРµСЂРёС‚СЊ: РµРґРёРЅСЃС‚РІРµРЅРЅРѕРµ Р»Рё РѕСЃРЅРѕРІР°РЅРёРµ РґР»СЏ В«РЅРµС„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№В» вЂ” РЅР°Р»РёС‡РёРµ СЃР°РјРѕРіРѕ guard? Р•СЃР»Рё РґР° в†’ Contract verified? = needs-verification, Verdict в‰  OK.
      **Р РµРєРІРёР·РёС‚ С„РѕСЂРјС‹ вЂ” РѕР±СЏР·Р°С‚РµР»СЊРЅР°СЏ РІРµСЂРёС„РёРєР°С†РёСЏ:** РµСЃР»Рё РёСЃС‚РѕС‡РЅРёРє = СЂРµРєРІРёР·РёС‚ С„РѕСЂРјС‹ (С‚Р°Р±Р»РёС†Р° Р·РЅР°С‡РµРЅРёР№, РєРѕР»РѕРЅРєР°):
      1. РџСЂРѕС‡РёС‚Р°С‚СЊ Form.xml С‚РѕРіРѕ Р¶Рµ РѕР±СЉРµРєС‚Р° (Read).
      2. Р•СЃР»Рё РєРѕР»РѕРЅРєР°/СЂРµРєРІРёР·РёС‚ РїСЂРёСЃСѓС‚СЃС‚РІСѓРµС‚ РІ Form.xml в†’ РєРѕРЅС‚СЂР°РєС‚ **С„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№**, guard РЅР° РЅР°Р»РёС‡РёРµ РєРѕР»РѕРЅРєРё = AP-004.
      3. Р•СЃР»Рё РєРѕР»РѕРЅРєРё РЅРµС‚ РІ Form.xml (РёР»Рё СЃС‚СЂСѓРєС‚СѓСЂР° С„РѕСЂРјРёСЂСѓРµС‚СЃСЏ РґРёРЅР°РјРёС‡РµСЃРєРё РІ РєРѕРґРµ) в†’ РєРѕРЅС‚СЂР°РєС‚ РЅРµС„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№, guard РјРѕР¶РµС‚ Р±С‹С‚СЊ OK.
      4. Р•СЃР»Рё Form.xml РЅРµ СѓРґР°Р»РѕСЃСЊ РїСЂРѕС‡РёС‚Р°С‚СЊ в†’ Contract verified? = unverified (РЅРµ В«optionalВ»).
      Р‘РµР· СЌС‚РѕР№ РІРµСЂРёС„РёРєР°С†РёРё РЅРµР»СЊР·СЏ СЃС‚Р°РІРёС‚СЊ Contract = В«optional columnВ» РёР»Рё Verdict = OK РґР»СЏ guard РЅР° РєРѕР»РѕРЅРєСѓ СЂРµРєРІРёР·РёС‚Р° С„РѕСЂРјС‹.
      - **Р¤РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№:** РјРµС‚Р°РґР°РЅРЅС‹Рµ РѕР±СЉРµРєС‚Р° (РўР§, СЂРµРєРІРёР·РёС‚), Form.xml СЂРµРєРІРёР·РёС‚Р° С„РѕСЂРјС‹ (РєРѕР»РѕРЅРєРё С‚Р°Р±Р»РёС†С‹ Р·РЅР°С‡РµРЅРёР№ С„РѕСЂРјС‹ Р·Р°РґР°РЅС‹ РјР°РєРµС‚РѕРј С‚РѕРіРѕ Р¶Рµ РѕР±СЉРµРєС‚Р°), С‚РµРєСЃС‚ Р·Р°РїСЂРѕСЃР° СЃ СЏРІРЅС‹Рј СЃРїРёСЃРєРѕРј РїРѕР»РµР№, РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅРЅС‹Р№ РїР°СЂР°РјРµС‚СЂ/РІРѕР·РІСЂР°С‚, Resolved Contracts СЃ Contract: fixed. Р”Р»СЏ СЂРµРєРІРёР·РёС‚Р° С„РѕСЂРјС‹: РµСЃР»Рё РєРѕР»РѕРЅРєР°/СЂРµРєРІРёР·РёС‚ РїСЂРёСЃСѓС‚СЃС‚РІСѓРµС‚ РІ Form.xml вЂ” РєРѕРЅС‚СЂР°РєС‚ С„РёРєСЃРёСЂРѕРІР°РЅ; guard РЅР° РЅР°Р»РёС‡РёРµ РєРѕР»РѕРЅРєРё (РљРѕР»РѕРЅРєРё.РќР°Р№С‚Рё Рё С‚.Рї.) = РёР·Р±С‹С‚РѕС‡РµРЅ.
      - **РќРµС„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№:** РІРЅРµС€РЅРёР№ API, РґРёРЅР°РјРёС‡РµСЃРєР°СЏ СЃС…РµРјР°, Resolved Contracts СЃ Contract: dynamic РёР»Рё unknown.
   4. Contract verified? (verified / phantom / unverified / **resolved-fixed** / **resolved-dynamic** вЂ” РїРѕ Resolved Contracts РїСЂРё РЅР°Р»РёС‡РёРё).
   5. Verdict: С„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№ РєРѕРЅС‚СЂР°РєС‚ + РЅР°Р»РёС‡РёРµ guard в†’ AP-004; РЅРµС„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№ + РєРѕСЂСЂРµРєС‚РЅС‹Р№ guard в†’ OK; РЅРµС„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Р№ + РЅРµРєРѕСЂСЂРµРєС‚РЅС‹Р№ РјРµС‚РѕРґ guard-Р° в†’ AP-005 РёР»Рё РёРЅРѕР№ РїРѕ РєР°С‚Р°Р»РѕРіСѓ; phantom field + defense stack в†’ AP-029 CRITICAL.
   **Resolved Contracts вЂ” Р°СЂС‚РёС„Р°РєС‚ Р—РќР.** Р’РµСЂРёС„РёС†РёСЂРѕРІР°РЅРЅС‹Рµ explorer РєРѕРЅС‚СЂР°РєС‚С‹ РІ `reports/resolved-contract-*.md`. resolved-fixed + guard в†’ AP-004; resolved-dynamic + РјРёРЅРёРјР°Р»СЊРЅР°СЏ РїСЂРѕРІРµСЂРєР° в†’ OK.
   **Unverified-origin check:** РґР»СЏ Р»СЋР±РѕРіРѕ guard (РЅРµ С‚РѕР»СЊРєРѕ РЎРІРѕР№СЃС‚РІРѕ/РўРёРїР—РЅС‡): РїСЂРё Knowledge Assessment verdict = ABSENT РёР»Рё PARTIAL Рё РѕС‚СЃСѓС‚СЃС‚РІРёРё РїСЂРёР·РЅР°РєРѕРІ СѓСЃС‚Р°РЅРѕРІРєРё РєРѕРЅС‚СЂР°РєС‚Р° (РєРѕРјРјРµРЅС‚Р°СЂРёР№, РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ, Resolved Contracts) вЂ” Verdict = AP-004. Р РµРјРµРґРёР°С†РёСЏ: СѓСЃС‚Р°РЅРѕРІРёС‚СЊ РєРѕРЅС‚СЂР°РєС‚ (Investigation Request РёР»Рё Р°РЅР°Р»РёР·), Р·Р°С‚РµРј СЂРµС€РёС‚СЊ вЂ” РЅСѓР¶РЅР° Р»Рё РїСЂРѕРІРµСЂРєР°.

Completeness gate (РџРѕРїС‹С‚РєР°): РєРѕР»РёС‡РµСЃС‚РІРѕ СЃС‚СЂРѕРє РІ С‚Р°Р±Р»РёС†Рµ B (РџРѕРїС‹С‚РєР° Audit) = РєРѕР»РёС‡РµСЃС‚РІРѕ Р±Р»РѕРєРѕРІ РџРѕРїС‹С‚РєР° РёР· С€Р°РіР° A. РњРµРЅСЊС€Рµ вЂ” Phase 2.5 РЅРµ Р·Р°РІРµСЂС€РµРЅР°.

Completeness gate (Defensive Checks): РєРѕР»РёС‡РµСЃС‚РІРѕ СЃС‚СЂРѕРє РІ Defensive Checks Table = РєРѕР»РёС‡РµСЃС‚РІРѕ РёСЃС‚РѕС‡РЅРёРєРѕРІ СЃ access != DIRECT РІ Contract Map + РёСЃС‚РѕС‡РЅРёРєРё, Рє РїРѕР»СЏРј РєРѕС‚РѕСЂС‹С… РѕР±СЂР°С‰Р°СЋС‚СЃСЏ С‚РѕР»СЊРєРѕ РІРЅСѓС‚СЂРё РџРѕРїС‹С‚РєР° (РґР»СЏ РЅРёС… вЂ” СЃС‚СЂРѕРєР° СЃ РїРѕРјРµС‚РєРѕР№ В«access only inside РџРѕРїС‹С‚РєР°, no explicit checkВ», Contract = needs-resolution, Verdict = contract-compensating-try). РњРµРЅСЊС€Рµ вЂ” Phase 2.5 РЅРµ Р·Р°РІРµСЂС€РµРЅР°.

D. Investigation Request (СЂРµР·РѕР»РІ РєРѕРЅС‚СЂР°РєС‚РѕРІ РїРѕ Р·Р°РїСЂРѕСЃСѓ СЂРµРІСЊСЋРІРµСЂР°):
   Р•СЃР»Рё РїСЂРё Р·Р°РїРѕР»РЅРµРЅРёРё С‚Р°Р±Р»РёС† B (РџРѕРїС‹С‚РєР° Audit) РёР»Рё C (Defensive Checks) РґР»СЏ РєР°РєРѕРіРѕ-Р»РёР±Рѕ РёСЃС‚РѕС‡РЅРёРєР° РґР°РЅРЅС‹С…:
     - RootCause = contract-uncertainty (РџРѕРїС‹С‚РєР° Audit), РР›Р
     - Contract verified? = unverified РїСЂРё Knowledge Assessment verdict ABSENT/PARTIAL (Defensive Checks), РР›Р
     - Р•СЃС‚СЊ РџРѕРїС‹С‚РєР° РёР»Рё defensive checks, РЅРѕ РєРѕРЅС‚СЂР°РєС‚ РЅРµРёР·РІРµСЃС‚РµРЅ Рё РќР• РїРµСЂРµРґР°РЅ РІ Resolved Contracts
   ...С‚Рѕ:
     1. Р’ С‚Р°Р±Р»РёС†Рµ C (Defensive Checks) РґР»СЏ СЌС‚РѕРіРѕ РёСЃС‚РѕС‡РЅРёРєР° РІРїРёСЃР°С‚СЊ Contract = needs-resolution (РІРјРµСЃС‚Рѕ unverified).
     2. Р’ РєРѕРЅС†Рµ РѕС‚С‡С‘С‚Р° РґРѕР±Р°РІРёС‚СЊ СЃРµРєС†РёСЋ ## Investigation Request (С„РѕСЂРјР°С‚ РЅРёР¶Рµ РІ Phase 4).

   Р РµРІСЊСЋРІРµСЂ РќР• РїСЂРёРѕСЃС‚Р°РЅР°РІР»РёРІР°РµС‚ РѕС‚С‡С‘С‚. РћРЅ РІС‹РґР°С‘С‚ РїРѕР»РЅС‹Р№ РѕС‚С‡С‘С‚ (СЃ findings: contract-compensating-try Рё С‚.Рґ.) РџР›Р®РЎ СЃРµРєС†РёСЋ Investigation Request.
   РћСЂРєРµСЃС‚СЂР°С‚РѕСЂ РїР°СЂСЃРёС‚ Investigation Request Рё СЂРµС€Р°РµС‚, Р·Р°РїСѓСЃРєР°С‚СЊ Р»Рё explorer (С€Р°Рі 3.5 review/SKILL.md).

   РџСЂРё РїРѕРІС‚РѕСЂРЅРѕРј РІС‹Р·РѕРІРµ СЃ Resolved Contracts:
     - РћР±РЅРѕРІРёС‚СЊ С‚Р°Р±Р»РёС†С‹ B Рё C: РґР»СЏ РєР°Р¶РґРѕРіРѕ resolved РёСЃС‚РѕС‡РЅРёРєР° вЂ” Contract verified? = resolved-fixed РёР»Рё resolved-dynamic.
     - resolved-fixed + defensive check в†’ AP-004.
     - resolved-fixed + contract-compensating-try в†’ Р·Р°РјРµРЅРёС‚СЊ verdict РЅР° В«AP-004, СѓР±СЂР°С‚СЊ РџРѕРїС‹С‚РєСѓВ».
     - resolved-dynamic + РјРёРЅРёРјР°Р»СЊРЅР°СЏ РїСЂРѕРІРµСЂРєР° в†’ OK.
     - РџРµСЂРµСЃРјРѕС‚СЂРµС‚СЊ findings, Р·Р°С‚СЂРѕРЅСѓС‚С‹Рµ СЂРµР·РѕР»РІРѕРј.
     - РЎРµРєС†РёСЋ Investigation Request РќР• РІРєР»СЋС‡Р°С‚СЊ (РєРѕРЅС‚СЂР°РєС‚С‹ СѓР¶Рµ resolved).

   **Fallback РїСЂРё РѕС‚СЃСѓС‚СЃС‚РІРёРё Р±Р»РѕРєР° РІ РїСЂРѕРјРїС‚Рµ.** Р•СЃР»Рё РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂ РЅРµ РїРµСЂРµРґР°Р» Р±Р»РѕРє ## Resolved Contracts, РЅРѕ СЂРµРІСЊСЋ РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РІ РєРѕРЅС‚РµРєСЃС‚Рµ change вЂ” РїСЂРѕРІРµСЂРёС‚СЊ Glob `reports/resolved-contract-*.md` РІ РґРёСЂРµРєС‚РѕСЂРёРё change. Р•СЃР»Рё С„Р°Р№Р» РЅР°Р№РґРµРЅ Рё scope СЃРѕРІРїР°РґР°РµС‚ вЂ” РїСЂРѕС‡РёС‚Р°С‚СЊ Рё РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ РґР»СЏ Phase 2.5.
```

### Phase 3: Context Analysis
```yaml
1. Get similar code:
   similar = user-PROJECT-codemetadata (project-specific MCP)-codesearch(function_name)
   compare_implementations()

2. Check metadata:
   metadata = user-PROJECT-graph (project-specific MCP)-search_metadata(object_name)
   validate_dependencies()

3. Load past reviews:
   context = user-rlm-toolkit-rlm_route_context("code review " + module_name)
   apply_lessons_learned()
```

### Phase 4: Report Generation

РћС‚С‡С‘С‚ СЃРѕСЃС‚РѕРёС‚ РёР· РґРІСѓС… РѕСЃРЅРѕРІРЅС‹С… СЃРµРєС†РёР№. Phase 0 findings РёРґСѓС‚ РїРµСЂРІС‹РјРё (РєРѕСЂРЅРµРІС‹Рµ РїСЂРѕР±Р»РµРјС‹); Standards findings вЂ” РґРѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ.

```yaml
1. Reasoning Analysis (Phase 0):
   - Artifacts: Intent Map, Contract Map, Knowledge Assessment (РІРєР»СЋС‡РёС‚СЊ РІ РѕС‚С‡С‘С‚)
   - Findings: DISPROPORTIONATE_COMPLEXITY, CONTRACT_INCONSISTENCY, CONTRACT_INFERENCE, KNOWLEDGE_DEFICIT, CLARITY_DEFICIT вЂ” СЃ Intent, Expected, Actual, Root cause, Counterfactual, Remediation, Supporting

2. Standards & Patterns (Phase 1-2):
   - Findings (AP-NNN Рё РїСЂРѕС‡РёРµ) вЂ” РёСЃРєР»СЋС‡Р°СЏ С‚Рµ, С‡С‚Рѕ СѓР¶Рµ РїРѕРєСЂС‹С‚С‹ Phase 0 Р·Р°РјРµС‡Р°РЅРёРµРј РІ С‚РѕРј Р¶Рµ РјРµСЃС‚Рµ (СѓРєР°Р·Р°РЅС‹ РєР°Рє Supporting)

2.5. РџРѕРїС‹С‚РєР° & Contract Audit (Phase 2.5):
   - Audit Table (every РџРѕРїС‹С‚РєР° block with verdict)
   - Defensive Checks Table (every non-DIRECT source from Contract Map)
   - Findings from Phase 2.5 that are NOT already covered as Phase 0 Supporting

3. Summary:
   - Status: PASS | FAIL | NEEDS_WORK
   - Phase 0: N findings (РїРѕ severity)
   - Linter Signals (Phase 1b): K confirmed MUST_FIX, D dismissed, U unavailable
   - Standards: M findings (РїРѕ severity)
   - Overall: РёС‚РѕРіРѕРІР°СЏ С„РѕСЂРјСѓР»РёСЂРѕРІРєР°
   - PASS Р·Р°РїСЂРµС‰С‘РЅ РїСЂРё unresolved MUST_FIX РёР· Phase 1b (in-scope linter warnings Р±РµР· fix/dismiss)
```

Required Improvements (РІРјРµСЃС‚Рѕ СЃРµРєС†РёРё "Р РµРєРѕРјРµРЅРґР°С†РёРё"):
Р’СЃРµ РїСѓРЅРєС‚С‹, СЂР°РЅРµРµ РїРѕРїР°РґР°РІС€РёРµ РІ "Р РµРєРѕРјРµРЅРґР°С†РёРё", Р”РћР›Р–РќР« Р±С‹С‚СЊ РѕС„РѕСЂРјР»РµРЅС‹ РєР°Рє findings СЃ severity (MEDIUM РёР»Рё LOW). РћС‚РґРµР»СЊРЅРѕР№ СЃРµРєС†РёРё "Р РµРєРѕРјРµРЅРґР°С†РёРё" РІ РѕС‚С‡С‘С‚Рµ РќР•Рў.

## REVIEW CATEGORIES

### Phase 0 (Reasoning) finding types

РўРёРїС‹ Р·Р°РјРµС‡Р°РЅРёР№, РїРѕСЂРѕР¶РґР°РµРјС‹Рµ Phase 0 (РІРЅРµ С‚Р°РєСЃРѕРЅРѕРјРёРё AP-NNN). РЈРєР°Р·С‹РІР°СЋС‚ РЅР° РєР»Р°СЃСЃ РїСЂРѕР±Р»РµРјС‹ СЃ Р»РѕРіРёРєРѕР№, Р° РЅРµ РЅР° РєРѕРЅРєСЂРµС‚РЅС‹Р№ РїР°С‚С‚РµСЂРЅ.

| РўРёРї | РћРїРёСЃР°РЅРёРµ | Default severity |
|-----|----------|------------------|
| DISPROPORTIONATE_COMPLEXITY | РЎР»РѕР¶РЅРѕСЃС‚СЊ СЂРµР°Р»РёР·Р°С†РёРё Р±Р»РѕРєР° РјРЅРѕРіРѕРєСЂР°С‚РЅРѕ РїСЂРµРІС‹С€Р°РµС‚ РѕР¶РёРґР°РµРјСѓСЋ РґР»СЏ РµРіРѕ РЅР°РјРµСЂРµРЅРёСЏ | HIGH |
| CONTRACT_INCONSISTENCY | РћРґРёРЅ РёСЃС‚РѕС‡РЅРёРє РґР°РЅРЅС‹С… вЂ” С‡Р°СЃС‚СЊ РїРѕР»РµР№ РЅР°РїСЂСЏРјСѓСЋ, С‡Р°СЃС‚СЊ Р·Р°С‰РёС‚РЅРѕ/РёСЃСЃР»РµРґРѕРІР°С‚РµР»СЊСЃРєРё | HIGH |
| CONTRACT_INFERENCE | РћРґРЅРѕ СЃРµРјР°РЅС‚РёС‡РµСЃРєРѕРµ Р·РЅР°С‡РµРЅРёРµ РїРѕР»СѓС‡Р°РµС‚СЃСЏ РїРµСЂРµР±РѕСЂРѕРј РЅРµСЃРєРѕР»СЊРєРёС… Р°Р»СЊС‚РµСЂРЅР°С‚РёРІРЅС‹С… РїСѓС‚РµР№ | HIGH |
| KNOWLEDGE_DEFICIT | РљРѕРґ РєРѕРјРїРµРЅСЃРёСЂСѓРµС‚ РЅРµР·РЅР°РЅРёРµ РєРѕРЅС‚СЂР°РєС‚Р°/РґРѕРјРµРЅР° РІРјРµСЃС‚Рѕ С‚РѕРіРѕ, С‡С‚РѕР±С‹ РµРіРѕ РІС‹СЏСЃРЅРёС‚СЊ | HIGH |
| CLARITY_DEFICIT | РќР°РјРµСЂРµРЅРёРµ Р±Р»РѕРєР° РЅРµРІРѕР·РјРѕР¶РЅРѕ РѕРїСЂРµРґРµР»РёС‚СЊ РёР· РєРѕРґР° Р±РµР· РІРЅРµС€РЅРµРіРѕ РєРѕРЅС‚РµРєСЃС‚Р° | MEDIUM |
| AUTHORITY_MISPLACEMENT | РљРѕРґ Р±РµСЂС‘С‚ РѕС‚РІРµС‚СЃС‚РІРµРЅРЅРѕСЃС‚СЊ Р·Р° РїРѕРІРµРґРµРЅРёРµ, РІР»Р°РґРµР»РµС† РєРѕС‚РѕСЂРѕРіРѕ вЂ” РґСЂСѓРіРѕР№ СЃР»РѕР№ (Р±Р°Р·Р°, Р‘РЎРџ, РїР»Р°С‚С„РѕСЂРјР°, РѕР±С‰РёР№ РјРѕРґСѓР»СЊ, РІРЅРµС€РЅРёР№ РєРѕРЅС‚СЂР°РєС‚). Р›РѕРєР°Р»СЊРЅР°СЏ СЂРµР°Р»РёР·Р°С†РёСЏ РїРѕРґРјРµРЅСЏРµС‚ РґРµР»РµРіРёСЂРѕРІР°РЅРёРµ РІР»Р°РґРµР»СЊС†Сѓ. | HIGH |

Р¤РѕСЂРјР°С‚ Р·Р°РјРµС‡Р°РЅРёСЏ Phase 0: Procedure (РёРјСЏ РїСЂРѕС†РµРґСѓСЂС‹/С„СѓРЅРєС†РёРё), Anchor (1вЂ“2 СѓРЅРёРєР°Р»СЊРЅС‹Рµ СЃС‚СЂРѕРєРё РєРѕРґР° РґР»СЏ Grep-РїРѕРёСЃРєР° РїРѕСЃР»Рµ РїСЂР°РІРѕРє), Intent, Expected, Actual, Root cause, Counterfactual, Remediation, Action (MUST_FIX | VERIFIED_OK | OPTIONAL), Supporting (AP-NNN РїСЂРё СЃРѕРІРїР°РґРµРЅРёРё).

### Critical (Р±Р»РѕРєРёСЂСѓРµС‚ РєРѕРјРјРёС‚)
```yaml
- Syntax errors
- SQL injection vulnerabilities
- Data corruption risks
- Security breaches
- Performance killers (>10s operations)
- Р‘РЎРџ violations (breaking changes)
- &РџРµСЂРµРґ/&РџРѕСЃР»Рµ applied to a function instead of a procedure
- РўРµРєСѓС‰Р°СЏР”Р°С‚Р°() instead of РўРµРєСѓС‰Р°СЏР”Р°С‚Р°РЎРµР°РЅСЃР°()
- РќР°С‡Р°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ() without matching Р—Р°С„РёРєСЃРёСЂРѕРІР°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ()/РћС‚РјРµРЅРёС‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ() in same scope
- Missing РћС‚РјРµРЅРёС‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ() in РСЃРєР»СЋС‡РµРЅРёРµ block of transactional РџРѕРїС‹С‚РєР°
- РџРѕРїС‹С‚РєР° wrapping deterministic operation (no external factor вЂ” rule 20)
- Defense stack with phantom field (AP-029 + unverified field name)
- AP-046 subcase: hook-scope early return under &Р’РјРµСЃС‚Рѕ without РџСЂРѕРґРѕР»Р¶РёС‚СЊР’С‹Р·РѕРІ вЂ” silent override of base implementation
```

### High (РёСЃРїСЂР°РІРёС‚СЊ РґРѕ Р·Р°РІРµСЂС€РµРЅРёСЏ Р·Р°РґР°С‡Рё)
```yaml
- Phase 0: DISPROPORTIONATE_COMPLEXITY, CONTRACT_INCONSISTENCY, CONTRACT_INFERENCE, KNOWLEDGE_DEFICIT
- Phase 0: AUTHORITY_MISPLACEMENT (Р»РѕРєР°Р»СЊРЅР°СЏ СЂРµР°Р»РёР·Р°С†РёСЏ РїРѕРІРµРґРµРЅРёСЏ, Сѓ РєРѕС‚РѕСЂРѕРіРѕ РµСЃС‚СЊ РІР»Р°РґРµР»РµС†)
- Logic errors
- Missing error handling
- Silent skip on structural check failure (РџСЂРѕРґРѕР»Р¶РёС‚СЊ / silent Р’РѕР·РІСЂР°С‚ / empty branch on type/property/size mismatch instead of Р’С‹Р·РІР°С‚СЊРСЃРєР»СЋС‡РµРЅРёРµ; business filtering is not a violation)
- Redundant property/attribute check on fixed-contract source (РЎРІРѕР№СЃС‚РІРѕ/Р•СЃС‚СЊР РµРєРІРёР·РёС‚ on own tabular section field, explicit query column вЂ” field is guaranteed by metadata; also wrong method: РЎРІРѕР№СЃС‚РІРѕ() on non-Structure type)
- РўРёРїР—РЅС‡() on fixed-contract return value (function/documentation guarantees type)
- Р—РЅР°С‡РµРЅРёРµР—Р°РїРѕР»РЅРµРЅРѕ() on field guaranteed by contract/metadata (as guard, not business check)
- "Defensive cake" pattern (stacked checks on same value where one is subsumed by another вЂ” any contract type, fixed or dynamic)
- N+1 query problems
- Missing indexes
- Insufficient access control
- Code duplication (>50 lines)
- Cyclomatic complexity >15
- &Р’РјРµСЃС‚Рѕ used where &РџРµСЂРµРґ/&РџРѕСЃР»Рµ is sufficient
- &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ: code outside #Р’СЃС‚Р°РІРєР°/#РЈРґР°Р»РµРЅРёРµ differs from base (variable rename, formatting, refactoring outside blocks, adding/removing #РћР±Р»Р°СЃС‚СЊ in typed code) вЂ” in prerelease: CRITICAL
- &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ used where &РџРµСЂРµРґ/&РџРѕСЃР»Рµ is sufficient
- Intercepted method (&Р’РјРµСЃС‚Рѕ/&РџРµСЂРµРґ/&РџРѕСЃР»Рµ) without extension prefix
- РЎРѕРѕР±С‰РёС‚СЊ() instead of РћР±С‰РµРіРѕРќР°Р·РЅР°С‡РµРЅРёСЏ.РЎРѕРѕР±С‰РёС‚СЊРџРѕР»СЊР·РѕРІР°С‚РµР»СЋ()
- РћРїРѕРІРµСЃС‚РёС‚СЊ()/РћРїРѕРІРµСЃС‚РёС‚СЊРћР±РР·РјРµРЅРµРЅРёРё() in server context (client-only methods)
- РЎРІРѕР№СЃС‚РІРѕ() on fixed-contract source (tabular section, query result)
- Band-aid fix detected (defensive check without root cause, try/except suppression, skip-flag, defensive cake)
- РџРѕРїС‹С‚РєР° without logging (exception not re-raised) вЂ” traceless suppression (rule 20)
- РџРѕРїС‹С‚РєР° with silent degradation fallback (rule 20)
- AP-027: Guard-then-catch (РџРѕРїС‹С‚РєР° immediately after guard validating same value)
- AP-028: Check-after-establish (РЎРІРѕР№СЃС‚РІРѕ/Р•СЃС‚СЊР РµРєРІРёР·РёС‚/Р—РЅР°С‡РµРЅРёРµР—Р°РїРѕР»РЅРµРЅРѕ after type/structure established in code flow)
- Defense stack: РџРѕРїС‹С‚РєР° wrapping only РЎРІРѕР№СЃС‚РІРѕ()/РўРёРїР—РЅС‡() with no throwable operation (AP-029)
- Phantom field: РЎРІРѕР№СЃС‚РІРѕ("FieldName") where FieldName not found in existing codebase for same source
- РќР°С‡Р°С‚СЊРўСЂР°РЅР·Р°РєС†РёСЋ() without РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ wrapping the transactional block
- User interaction (РџРѕРєР°Р·Р°С‚СЊР’РѕРїСЂРѕСЃ, РџСЂРµРґСѓРїСЂРµР¶РґРµРЅРёРµ, РЎРѕРѕР±С‰РёС‚СЊ) inside transaction
- Read-then-write without Р‘Р»РѕРєРёСЂРѕРІРєР°Р”Р°РЅРЅС‹С… in concurrent scenario
- COMРћР±СЉРµРєС‚ created without РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ ensuring release
- Export procedure/function in form module (AP-033) вЂ” form-as-service pattern; exception: РџРѕРґРєР»СЋС‡Р°РµРјС‹Р№_* (BSP), РћРїРёСЃР°РЅРёРµРћРїРѕРІРµС‰РµРЅРёСЏ callbacks
- Unused export procedure/function (no callers in extension scope) вЂ” category 15
- Obsolete procedure still called from non-obsolete code вЂ” category 15
- Parameter overwrite: parameter reassigned inside body, not documented as output вЂ” category 4 (rule 21)
- AP-046: Hook-scope early return suppressing entire body of an intercepted extension procedure вЂ” risks silent disabling of future composing modifications
```

### Medium (РёСЃРїСЂР°РІРёС‚СЊ РІ С‚РµРєСѓС‰РµР№ РёС‚РµСЂР°С†РёРё)
```yaml
- Phase 0: CLARITY_DEFICIT (РЅР°РјРµСЂРµРЅРёРµ Р±Р»РѕРєР° РЅРµРѕС‡РµРІРёРґРЅРѕ РёР· РєРѕРґР°)
- AP-031: РјРµС‚Р°-РёРјРµРЅР° РёР· РїРѕСЃС‚Р°РЅРѕРІРєРё/РѕСЂРєРµСЃС‚СЂР°С†РёРё (РґРѕРјРµРЅРЅС‹Р№ С‚РµСЃС‚ + РјР°СЂРєРµСЂС‹ РІ РєР°СЂС‚РѕС‡РєРµ AP-031); СЌРєСЃРїРѕСЂС‚РЅС‹Рµ РїСЂРѕС†РµРґСѓСЂС‹/С„СѓРЅРєС†РёРё вЂ” HIGH; РІ finding РѕР±СЏР·Р°С‚РµР»СЊРЅРѕ РїСЂРµРґР»РѕР¶РёС‚СЊ РґРѕРјРµРЅРЅС‹Р№ СЃРёРЅРѕРЅРёРј
- Naming convention violations
- Missing documentation
- Suboptimal algorithms
- Code smells
- Minor Р‘РЎРџ deviations
- Testability issues
- Missing #РћР±Р»Р°СЃС‚СЊ markup in module (module > 100 lines; otherwise LOW)
- Wrong order of #РћР±Р»Р°СЃС‚СЊ regions
- Export method without header comment (purpose, parameters, return value)
- Business logic directly in #Р’СЃС‚Р°РІРєР° block instead of separate procedure
- Own non-intercept method with extension prefix
- Export own method without descriptive unique name
- Dead code вЂ” see category 15 (Obsolete and Unused Code)
- Unused non-export procedure/function (category 15)
- Procedure/function marked "РЈСЃС‚Р°СЂРµР»Р°:" / "Deprecated" (category 15)
- Logic duplication between modules
- Commented-out code without explanation
- User-facing string literals without РќРЎС‚СЂ("ru = '...'")
- Ternary operator ?() usage (style preference)
- Probable band-aid (TODO workaround, duplicated logic with variation)
- Collection mutation on parameter without out contract вЂ” category 4 (rule 21)
- Duplicated magic constant (same literal 2+ times in module) вЂ” category 4 (rule 22)
- Mixed responsibilities (procedure >40 lines, 3+ concerns) вЂ” category 4
- Inconsistent prefix usage (exports with and without prefix in same module) вЂ” category 8
- AP-031: Domain naming test failure (meta-names, implementation-role names) вЂ” MEDIUM (export: HIGH). See anti-pattern registry
```

### Low (РёСЃРїСЂР°РІРёС‚СЊ, РјРёРЅРёРјР°Р»СЊРЅС‹Р№ РїСЂРёРѕСЂРёС‚РµС‚)
```yaml
- Code formatting
- Comment style
- Variable naming (casing, prefix style only; domain-clarity failures are MEDIUM via AP-031)
- Minor optimizations
- Refactoring opportunities
- Missing module header comment
- Event handler without description
- Header format not matching BSP template
- Excessive info logging (Р—Р°РїРёСЃСЊР–СѓСЂРЅР°Р»Р°Р РµРіРёСЃС‚СЂР°С†РёРё РРЅС„РѕСЂРјР°С†РёСЏ/РџСЂРёРјРµС‡Р°РЅРёРµ in loop or 3+ calls) вЂ” category 10
```
(Changelog markers and design refs in comments are now MEDIUM under Code Cleanliness / release-hygiene and escalate to HIGH in prerelease.)

## PRE-RELEASE SEVERITY ESCALATION

When reviewer is called with context `mode=prerelease`, tag each finding with **kind** and apply escalation only to functional findings.

### Kind (every finding)

```yaml
kind:
  functional вЂ” affects behavior, data, security, reliability (bugs, РўРµРєСѓС‰Р°СЏР”Р°С‚Р° on server, injection, silent skips, band-aids)
  style вЂ” affects readability, standards, structure only (?(), #РћР±Р»Р°СЃС‚СЊ missing, naming prefix, header format)
  release-hygiene вЂ” process metadata that must not ship to production (changelog markers, work instructions, commented-out old code, design refs)
```

**Escalation (LOWв†’MEDIUM, MEDIUMв†’HIGH) applies to kind=functional, release-hygiene, and style.** Code is delivered to the customer вЂ” style matters in prerelease. Tag style findings with `[style]` in the report. For kind=release-hygiene, see also Pre-release escalation (release-hygiene) below.

### Kind by category (examples)

```yaml
kind=functional:
  - РўРµРєСѓС‰Р°СЏР”Р°С‚Р°() on server (use РўРµРєСѓС‰Р°СЏР”Р°С‚Р°РЎРµР°РЅСЃР°())
  - РЎРѕРѕР±С‰РёС‚СЊ() instead of РћР±С‰РµРіРѕРќР°Р·РЅР°С‡РµРЅРёСЏ.РЎРѕРѕР±С‰РёС‚СЊРџРѕР»СЊР·РѕРІР°С‚РµР»СЋ()
  - Silent skip on structural check failure, band-aid fixes
  - Export procedure/function in form module (AP-033, form boundary violation)
  - &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ: code outside #Р’СЃС‚Р°РІРєР°/#РЈРґР°Р»РµРЅРёРµ modified (breaks extension applicability)
  - Security, performance bugs, logic errors
  - Р­С‚Р°Р¤РѕСЂРјР° instead of Р­С‚РѕС‚РћР±СЉРµРєС‚
  - Duplicate #РћР±Р»Р°СЃС‚СЊ (structural breakage)
  - Typos in user-facing strings (mixed encoding, spelling)
  - Stub/placeholder code in production
  - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ without logging (exception silently swallowed) вЂ” traceless suppression
  - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ wrapping fixed-contract access (contract masking)
  - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ wrapping deterministic operation (no external factor вЂ” rule 20)
  - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ with silent degradation fallback (rule 20)
  - Parameter overwrite (parameter reassigned inside body, not documented as output вЂ” rule 21)

kind=style:
  - Ternary operator ?() (style preference, not functional defect)
  - Missing #РћР±Р»Р°СЃС‚СЊ structure in module
  - Own non-intercept method using extension prefix
  - Method name contradicts compilation directive
  - Export in private region (#РћР±Р»Р°СЃС‚СЊ РЎР»СѓР¶РµР±РЅС‹РµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё)
  - Module header name mismatch
  - Missing module header, event handler without description, header format not matching BSP
  - Collection mutation on parameter without out contract (rule 21)
  - Duplicated magic constant (rule 22)
  - Mixed responsibilities (procedure >40 lines, 3+ concerns)
  - Inconsistent prefix usage (exports with/without prefix in same module)
  - Excessive info logging (Р—Р°РїРёСЃСЊР–СѓСЂРЅР°Р»Р°Р РµРіРёСЃС‚СЂР°С†РёРё РРЅС„РѕСЂРјР°С†РёСЏ in loop or 3+ calls)

kind=release-hygiene:
  - Changelog markers in comments (// +++/---, // РќРђР§РђР›Рћ/РљРћРќР•Р¦, // Р Р“РРўРЎ, date-author in comments)
  - Commented-out old code with replacement markers
  - Work instructions in comments
  - Design/process artifact references in comments (short-form D11/F5, natural-language
    "РџРѕ design Decision N (change-name)", process terms, kebab-case change names, task numbers)
  Not release-hygiene: #Р’СЃС‚Р°РІРєР°, #РљРѕРЅРµС†Р’СЃС‚Р°РІРєРё, #РЈРґР°Р»РµРЅРёРµ, #РљРѕРЅРµС†РЈРґР°Р»РµРЅРёСЏ вЂ” extension override directives, do not remove or flag.
  Project-level override: comments matching openspec/project.md В«Whitelist РїСЂРµРґСЂРµР»РёР·Р°В» patterns within the rowвЂ™s scope (glob) вЂ” NOT release-hygiene. Check project.md before flagging.

kind=functional (category 15 вЂ” unused/obsolete):
  - Unused export procedure/function (no callers in extension scope) вЂ” dead API surface
  - Obsolete procedure still called from non-obsolete code вЂ” caller must migrate

kind=style (category 15 вЂ” unused/obsolete):
  - Unused non-export procedure/function (no behavior impact, dead weight)
  - Obsolete markers present (comment "РЈСЃС‚Р°СЂРµР»Р°:", #РћР±Р»Р°СЃС‚СЊ РЈСЃС‚Р°СЂРµРІС€РёРµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё)
  - Unused parameter in procedure/function body
```

### Escalation rules

```yaml
Pre-release escalation (all kinds: functional, style, release-hygiene):
  LOW в†’ MEDIUM:
    - All kinds escalated (code is delivered to the customer)

  MEDIUM в†’ HIGH:
    - Export method without header (if functional impact, e.g. contract unclear)
    - Dead code, logic duplication (if kind=functional)
    - Business logic directly in #Р’СЃС‚Р°РІРєР° block
    - Export method in РЎР»СѓР¶РµР±РЅС‹РµРџСЂРѕС†РµРґСѓСЂС‹РР¤СѓРЅРєС†РёРё (contract violation)
    - Export procedure/function in form module (AP-033) вЂ” form-as-service before release
    - Unused export procedure/function (dead API surface before release) вЂ” category 15
    - Procedure marked "РЈСЃС‚Р°СЂРµР»Р°:" / "Deprecated" still present without documented plan вЂ” category 15

  HIGH в†’ CRITICAL:
    - &РР·РјРµРЅРµРЅРёРµРРљРѕРЅС‚СЂРѕР»СЊ: code outside #Р’СЃС‚Р°РІРєР°/#РЈРґР°Р»РµРЅРёРµ differs from base (variable rename, formatting, #РћР±Р»Р°СЃС‚СЊ in base code) вЂ” breaks extension applicability
    - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ without logging (traceless suppression вЂ” rule 20)
    - РџРѕРїС‹С‚РєР°/РСЃРєР»СЋС‡РµРЅРёРµ with silent degradation fallback (rule 20)

Note: Escalation is additive. All kinds (functional, style, release-hygiene) are escalated in prerelease вЂ” code is delivered to the customer. Tag style findings with [style].
```

### Pre-release escalation (release-hygiene)

```yaml
Pre-release escalation (release-hygiene):
  MEDIUM в†’ HIGH:
    - All release-hygiene items (changelog markers in comments, work instructions, commented-out old code, design refs). Do not flag or remove #Р’СЃС‚Р°РІРєР°/#РЈРґР°Р»РµРЅРёРµ directives.

  Note: release-hygiene HIGH items appear in "fix before release" section
  Р’СЃРµ Р·Р°РјРµС‡Р°РЅРёСЏ (РІ С‚.С‡. style HIGH) РѕР±СЏР·Р°С‚РµР»СЊРЅС‹ Рє РёСЃРїСЂР°РІР»РµРЅРёСЋ; severity Р·Р°РґР°С‘С‚ РїСЂРёРѕСЂРёС‚РµС‚.
```

**How to detect `mode=prerelease`**: The calling prompt explicitly passes `mode=prerelease` in context, or the review is triggered by the `/prerelease-review` command skill. In prerelease reports, always output `kind: functional`, `kind: style`, or `kind: release-hygiene` (and level) for each finding.

## STANDARDS REFERENCE

### Р‘РЎРџ Naming Conventions
```yaml
Modules:
  - CommonModule: РћР±С‰РµРіРѕРќР°Р·РЅР°С‡РµРЅРёСЏ, РћР±С‰РµРіРѕРќР°Р·РЅР°С‡РµРЅРёСЏРљР»РёРµРЅС‚
  - ObjectModule: Р”РѕРєСѓРјРµРЅС‚РћР±СЉРµРєС‚.<Name>
  - ManagerModule: Р”РѕРєСѓРјРµРЅС‚РњРµРЅРµРґР¶РµСЂ.<Name>

Functions/Procedures:
  - Export: РџРѕР»СѓС‡РёС‚СЊР”Р°РЅРЅС‹РµРљР»РёРµРЅС‚Р°()
  - Internal: РџРѕР»СѓС‡РёС‚СЊР”Р°РЅРЅС‹РµРљР»РёРµРЅС‚Р°Р’РЅСѓС‚СЂРµРЅРЅРёР№()
  - Client: РџРѕР»СѓС‡РёС‚СЊР”Р°РЅРЅС‹РµРљР»РёРµРЅС‚Р°РќР°РљР»РёРµРЅС‚Рµ()
  - Server: РџРѕР»СѓС‡РёС‚СЊР”Р°РЅРЅС‹РµРљР»РёРµРЅС‚Р°РќР°РЎРµСЂРІРµСЂРµ()

Variables:
  - Parameters: РџР°СЂР°РјРµС‚СЂРРјСЏ
  - Local: РРјСЏРџРµСЂРµРјРµРЅРЅРѕР№
  - Module: РњРѕРґСѓР»СЊРЅР°СЏРџРµСЂРµРјРµРЅРЅР°СЏ
```

### Performance Patterns
```yaml
Anti-patterns:
  - Query in loop: Р’С‹Р±РѕСЂРєР°.РЎР»РµРґСѓСЋС‰РёР№() with nested query
  - Missing index: Selection without WHERE on indexed field
  - Full table scan: Selection without filters
  - Excessive database calls: >10 per function

Best practices:
  - Batch operations: Process multiple records at once
  - Use indexes: Always filter on indexed fields
  - Cache data: Store frequently accessed data
  - Minimize round-trips: Combine queries when possible
```

### Security Patterns
```yaml
Vulnerabilities:
  - SQL injection: String concatenation in query
  - XSS: Unescaped output in forms
  - Access control: Missing RLS checks
  - Hardcoded secrets: Passwords in code

Best practices:
  - Parameterized queries: Use query parameters
  - Input validation: Sanitize all inputs
  - Access control: Check rights before operations
  - Secure storage: Use encrypted storage for secrets
```


