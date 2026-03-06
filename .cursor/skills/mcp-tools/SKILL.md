# MCP Tools Usage Guide

## PRINCIPLE

**Choose the right tool based on task context, not tool name similarity**

```yaml
Strategy:
 1. Identify task type (search, validate, analyze, etc)
 2. Identify domain (1C docs, project code, metadata, etc)
 3. Use decision tree to select tool
 4. Call tool with correct parameters
 5. If unclear, load skill for detailed guidance

Token savings:
 - Clear decision trees: -30% exploratory calls
 - Parameter documentation: -20% trial-and-error
 - Context-aware selection: +50% first-try success
```

---

## TOOL CATEGORIES

### 1. Documentation & Reference Tools
**Purpose:** Find information about 1C platform, БСП, templates

**Tools:**
- `search_1c_docs`: Platform documentation (methods, syntax)
- `search_bsp_functions`: БСП (SSL) library functions
- `search_1c_templates`: Code templates and patterns

### 2. Code Validation Tools
**Purpose:** Check syntax and logic errors

**Tools:**
- `check_bsl_syntax`: BSL syntax validation
- `check_1c_logic`: Business logic validation via 1С:Напарник

### 3. Forms Tools
**Purpose:** Work with 1C managed forms

**Tools:**
- `get_form_xsd_schema`: XSD schema for forms
- `get_form_json_schema`: JSON schema for forms
- `get_form_instructions`: Integration instructions

### 4. Project-Specific Tools
**Purpose:** Search code, metadata, documentation in project MCP

**Tool patterns (если MCP подключён):**
- `user-PROJECT-codemetadata-metadatasearch`: Поиск объектов метаданных
- `user-PROJECT-codemetadata-codesearch`: Поиск по BSL-коду
- `user-PROJECT-graph-search_metadata`: Neo4j-поиск по метаданным

### 5. LSP Tools (BSL LSP Bridge)
**Status: NOT_CONNECTED** — инструменты недоступны, пока не подключён BSL LSP Bridge.

Когда будет подключён:
- `get_diagnostics`: Ошибки и предупреждения
- `get_definition`: Место определения символа
- `get_call_graph`: Граф вызовов
- `rename_symbol`: Безопасное переименование

---

## DECISION TREES

### Tree 1: Documentation Search

```yaml
User asks about 1C method/function:
 → "Как использовать СтрРазделить?"
 → "What does ПолучитьДанные do?"
 
Decision:
 1. Is it platform method? → search_1c_docs
 2. Is it БСП function? → search_bsp_functions
 3. Need code example? → search_1c_templates

Examples:
 - "Как разделить строку?" → search_1c_docs(query="СтрРазделить")
 - "Функции работы с файлами БСП" → search_bsp_functions(query="файлы")
 - "Шаблон обработки" → search_1c_templates(query="обработка")
```

### Tree 2: Code Validation

```yaml
User wants to validate code:
 → "Проверь код на ошибки"
 → "Есть ли синтаксические ошибки?"
 
Decision:
 1. Syntax errors? → check_bsl_syntax
 2. Logic errors? → check_1c_logic
 3. Both? → check_bsl_syntax first, then check_1c_logic

Examples:
 - "Проверь синтаксис модуля" → check_bsl_syntax(code="...")
 - "Правильная ли логика?" → check_1c_logic(code="...")
 - "Полная проверка" → check_bsl_syntax + check_1c_logic
```

### Tree 3: Project Code Search

```yaml
User asks about project code:
 → "Где реализована функция X?"
 → "Какие поля у справочника Y?"

Decision:
 1. Метаданные (объекты, поля) → user-PROJECT-codemetadata-metadatasearch
 2. Код (функции, процедуры) → user-PROJECT-codemetadata-codesearch
 3. Neo4j граф → user-PROJECT-graph-search_metadata

Examples:
 - "Поля справочника Клиенты"
 → user-PROJECT-codemetadata-metadatasearch(query="Справочники.Клиенты.Реквизиты")
 
 - "Где функция ПолучитьДанные"
 → user-PROJECT-codemetadata-codesearch(query="ПолучитьДанные")
```

---

## USAGE PATTERNS

### Pattern 1: Documentation Lookup

```yaml
User asks "how to do X":
 1. Identify domain (platform, БСП, templates)
 2. Search appropriate documentation
 3. If not found, try alternative source
 4. Return answer with examples

Example:
 User: "Как работать с файлами?"
 
 Step 1: search_1c_docs(query="работа с файлами")
 Step 2: If not enough, search_bsp_functions(query="файлы")
 Step 3: If need example, search_1c_templates(query="работа с файлами")
```

### Pattern 2: Code Search in Project

```yaml
User asks about project code:
 1. Identify what to find (metadata, code)
 2. Use appropriate project MCP tool
 3. If not found, try alternative (code → metadata)

Example:
 User: "Где функция ПолучитьКлиента?"
 
 Step 1: user-PROJECT-codemetadata-codesearch(query="ПолучитьКлиента")
 Step 2: If not found, user-PROJECT-codemetadata-metadatasearch(query="ПолучитьКлиента")
```

### Pattern 3: Code Validation Workflow

```yaml
Before committing code:
 1. Check syntax: check_bsl_syntax
 2. If syntax OK, check logic: check_1c_logic
 3. If errors, fix and re-check
 4. If OK, proceed with commit

Example:
 User: "Проверь код перед коммитом"
 
 Step 1: check_bsl_syntax(code="...")
 Step 2: If errors, report and stop
 Step 3: If OK, check_1c_logic(code="...")
 Step 4: If errors, report and stop
 Step 5: If OK, approve commit
```

---

## TOOL NAME MAPPING

**IMPORTANT:** MCP servers use original names. This mapping is for AI reasoning clarity.

```yaml
Conceptual Name → Actual MCP Tool Name

1C Documentation:
 search_1c_docs → user-1c-help-docsearch
 search_bsp_functions → user-1c-ssl-ssl_search
 search_1c_templates → user-1c-templates-templatesearch

Code Validation:
 check_bsl_syntax → user-1c-syntax-checker-syntaxcheck
 check_1c_logic → user-1c-code-checker-check_1c_code

Forms:
 get_form_xsd_schema → user-1c-forms-get_xsd_schema
 get_form_json_schema → user-1c-forms-get_json_schema
 get_form_instructions → user-1c-forms-get_instructions
```

---

## TOOL REFERENCE

### 1C Documentation Tools

#### search_1c_docs
```yaml
Purpose: Search 1C platform documentation
When: User asks about platform method/function
Actual tool: user-1c-help-docsearch
Parameters:
 - query (string, required): Method name or description in Russian
Returns: Top search results with documentation
Example: user-1c-help-docsearch(query="СтрРазделить")
Skill: .cursor/skills/1c-help-mcp/SKILL.md
```

#### search_bsp_functions
```yaml
Purpose: Search БСП (SSL) library functions
When: User asks about standard subsystems
Parameters:
 - query (string, required): Function name or description
Returns: БСП functions with usage examples
Example: search_bsp_functions(query="работа с файлами")
Skill: .cursor/skills/1c-bsp/SKILL.md
```

#### search_1c_templates
```yaml
Purpose: Search 1C code templates
When: User needs code example or boilerplate
Parameters:
 - query (string, required): Template description
Returns: Code templates with examples
Example: search_1c_templates(query="обработка с формой")
```

### Code Validation Tools

#### check_bsl_syntax
```yaml
Purpose: Check BSL syntax errors
When: Before commit, after code generation
Parameters:
 - code (string, required): BSL code to check
Returns: Syntax errors with line numbers
Example: check_bsl_syntax(code="Процедура Test() КонецПроцедуры")
```

#### check_1c_logic
```yaml
Purpose: Check 1C business logic via 1С:Напарник
When: Deep code analysis, logic validation
Parameters:
 - code (string, required): BSL code to check
 - check_type (string, optional): "syntax", "logic", "performance"
Returns: Logic errors and recommendations
Example: check_1c_logic(code="...", check_type="logic")
```

### Forms Tools

#### get_form_xsd_schema
```yaml
Purpose: Get XSD schema for 1C forms
When: Generating forms, need schema reference
Parameters: None
Returns: Complete XSD schema definition
Example: get_form_xsd_schema()
Skill: .cursor/skills/1c-forms/SKILL.md
```

#### get_form_json_schema
```yaml
Purpose: Get JSON schema for 1C forms
When: Generating forms, prefer JSON format
Parameters: None
Returns: JSON schema with metadata
Example: get_form_json_schema()
Skill: .cursor/skills/1c-forms/SKILL.md
```

#### get_form_instructions
```yaml
Purpose: Get form integration instructions
When: Need to integrate generated form into metadata
Parameters: None
Returns: Step-by-step integration guide
Example: get_form_instructions()
Skill: .cursor/skills/1c-forms/SKILL.md
```

---

## CRITICAL RULES

1. **Use decision trees** — Don't guess, follow the tree
2. **Load skills when needed** — Reference skill files for detailed guidance
3. **Validate before commit** — Always check syntax and logic
4. **Search in order** — Try specific → general → alternative

---

## INTEGRATION WITH OTHER RULES

This skill works with:
- `model-selection.mdc` — When to use Opus vs Sonnet
- `1c-agent-delegation.mdc` — Agent delegation patterns

---

**Last updated:** 2026-03-06
**Version:** 2.0
**Status:** Converted from rule to skill
