# Anthropic Agent Skills API: Complete implementation guide for native skill migration

**The Agent Skills API uses a filesystem-based architecture with SKILL.md files that achieve 98% token reduction through progressive disclosure**—only loading full instructions when Claude determines a skill is relevant. For your alcanzai research paper processing system with 15 skills across three tiers (register, core, output), migration from bundled Python prompts to native .skill files will dramatically improve token efficiency while maintaining your compositional structure. This guide provides the complete technical specification and migration patterns.

## The SKILL.md file format requires only two fields but supports sophisticated composition

Every skill is a directory containing a required `SKILL.md` file with YAML frontmatter and Markdown body. The format is deceptively simple yet powerful:

```markdown
---
name: extract-arguments
description: Extract logical arguments and claims from academic papers. Use when analyzing scholarly texts for thesis statements, supporting evidence, counterarguments, and reasoning chains.
---

# Argument Extraction

## Quick workflow
1. Identify thesis statements (main claim)
2. Map supporting evidence chains
3. Flag counterarguments and rebuttals

## Extraction patterns
[Instructions Claude will follow]
```

**Required YAML fields:**
- `name`: 1-64 characters, lowercase alphanumeric + hyphens only, must exactly match directory name, cannot contain "anthropic" or "claude"
- `description`: 1-1024 characters, must specify both what the skill does AND when to use it (critical for Claude's skill selection)

**Optional YAML fields:** `license`, `compatibility`, `metadata` (key-value map), `allowed-tools`, `dependencies`

The directory structure supports arbitrary depth for resource organization:

```
skill-name/
├── SKILL.md              # Required entry point
├── references/           # Documentation loaded on-demand
│   └── detailed-rules.md
├── scripts/              # Executable code (zero-context execution)
│   └── analyze.py
└── assets/               # Templates, schemas, configuration
    └── output-template.json
```

## Skills are discovered at startup but loaded only when activated

The API implements a **three-stage progressive disclosure architecture** that fundamentally changes token economics:

| Stage | Content loaded | Token cost | When loaded |
|-------|----------------|------------|-------------|
| **Discovery** | `name` + `description` only | ~100 tokens/skill | Always at startup |
| **Activation** | Full SKILL.md body | ~5,000 tokens max | When Claude determines relevance |
| **Execution** | Reference files, scripts | As needed | On explicit request during task |

**For your 15 skills:** At startup, Claude loads ~1,500 tokens (15 × ~100). When processing a paper, perhaps 3-4 skills activate (~15,000 tokens loaded). Without progressive disclosure, all 15 skills would cost ~75,000 tokens upfront.

To upload skills via the API, use the `/v1/skills` endpoint with required beta headers:

```python
import anthropic
from anthropic.lib import files_from_dir

client = anthropic.Anthropic()

skill = client.beta.skills.create(
    display_title="Extract Arguments",
    files=files_from_dir("./skills/extract-arguments"),
    betas=["skills-2025-10-02"]
)
# Returns skill_id like "skill_01AbCdEfGhIjKlMnOpQrStUv"
```

**Upload options:** ZIP file, directory path helper (`files_from_dir`), or individual file tuples. Maximum upload size is **8MB** per skill. The `name` field in SKILL.md frontmatter must exactly match the top-level directory name.

## Skills are self-contained but compose through the Messages API container

**Native cross-skill dependencies do not exist** in the Agent Skills format. Each skill is designed to be complete and independent. However, composition happens at runtime through the `container` parameter:

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "custom", "skill_id": "skill_extract_args", "version": "latest"},
            {"type": "custom", "skill_id": "skill_identify_terms", "version": "latest"},
            {"type": "custom", "skill_id": "skill_quick_summary", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Analyze this academic paper..."}]
)
```

**For your alcanzai architecture**, the compositional structure maps to runtime skill selection. Your Python code currently bundling skills as prompts should instead:

1. Upload each skill separately to `/v1/skills`
2. Select which skills to include in `container.skills` based on the task
3. Let Claude dynamically activate only the skills it needs

Within a single skill, you can achieve internal composition through file references:

```markdown
# In SKILL.md:
## Register variations

**High jargon + long sentences + detailed explanations**: 
See [registers/academic-dense.md](registers/academic-dense.md)

**Low jargon + short sentences + minimal explanations**:
See [registers/public-accessible.md](registers/public-accessible.md)
```

## Token optimization requires strategic file splitting and lazy reference patterns

The progressive disclosure system enables powerful optimization strategies. Here's how to structure your 9 register skills efficiently:

**Strategy 1: Consolidate registers into a single skill with conditional references**

Instead of 9 separate register skills, create one `register-controller` skill:

```
register-controller/
├── SKILL.md
└── registers/
    ├── academic-dense.md       # high jargon × long × detailed
    ├── academic-moderate.md    # high jargon × long × minimal
    ├── expert-accessible.md    # medium jargon × mixed × detailed
    ├── public-summary.md       # low jargon × short × minimal
    └── [5 more combinations]
```

**SKILL.md for register-controller:**
```markdown
---
name: register-controller
description: Adapt academic paper explanations for different audiences. Use when summarizing research for specific reader types (researchers, practitioners, general public).
---

# Register Selection

## Available registers
| Jargon | Sentence | Depth | Reference |
|--------|----------|-------|-----------|
| High | Long | Detailed | [academic-dense.md](registers/academic-dense.md) |
| High | Long | Minimal | [academic-moderate.md](registers/academic-moderate.md) |
| [continue table]

## Selection logic
Based on target audience, load ONE register file only.
```

**Token impact:** ~100 tokens at startup (vs 900 for 9 skills). Only the selected register file loads (~500 tokens), not all 9.

**Strategy 2: Zero-context script execution**

Bundle scripts that execute without loading into context:

```markdown
## In SKILL.md:
For terminology extraction, RUN (don't read):
`python3 scripts/extract_terms.py input.pdf --format json`

The script handles: NLP processing, domain classification, frequency analysis
```

Scripts execute in the code execution container—only their **output** consumes tokens, not their source code.

**Strategy 3: Explicit conditional loading triggers**

```markdown
## When to load references

- **For argument mapping**: Read [references/argument-patterns.md](references/argument-patterns.md)
- **For basic extraction**: No additional files needed
- **For citation analysis**: Read [references/citation-rules.md](references/citation-rules.md)

Claude should load references ONLY when the task requires that specific capability.
```

## Anthropic recommends evaluation-first development and concise instructions

**Key best practices from official documentation:**

The "Start with evaluation" approach means building test cases before writing extensive skill content:

1. Run Claude on representative academic paper tasks without skills
2. Document where Claude fails or needs repeated guidance
3. Create 3+ evaluation scenarios testing those specific gaps
4. Write **minimal** instructions addressing only the gaps
5. Iterate based on evaluation results

**The "Think from Claude's perspective" principle** emphasizes conciseness:

```markdown
# ❌ Bad (unnecessary explanation):
"Academic papers typically contain arguments that support a thesis. 
An argument consists of premises leading to a conclusion. To extract 
arguments, you need to identify the logical structure..."

# ✅ Good (Claude already knows this):
"## Extraction workflow
1. Identify thesis (usually abstract/intro)
2. Map evidence chains per section  
3. Flag counterarguments in discussion
4. Output: JSON with claim hierarchy"
```

**Structure for scale** means splitting when SKILL.md exceeds **500 lines** or **5,000 tokens**:

```
understand-academic-text/
├── SKILL.md (lean: 150 lines)
├── ABSTRACTS.md (abstract parsing rules)
├── METHODS.md (methods section patterns)
├── RESULTS.md (results interpretation)
└── DISCUSSION.md (discussion analysis)
```

## Recent updates: open standard adoption and API maturation

**Key developments as of January 2026:**

The Agent Skills format was released as an **open standard** at [agentskills.io](https://agentskills.io) in December 2025, with adoption by GitHub Copilot, VS Code, and other platforms beyond Claude. The specification is version 1.0.

**API status:** The Skills API remains in beta, requiring these headers:
- `skills-2025-10-02` (skills functionality)
- `code-execution-2025-08-25` (container execution)
- `files-api-2025-04-14` (file upload/download)

**Prompt caching consideration:** Changing the skills list in your `container` parameter breaks the cache. For optimal caching, keep your skill list consistent across related requests.

**Limits:**
- Maximum **8 skills** per request
- Maximum **8MB** upload size per skill
- Skills execute in an isolated container with **no network access**
- Only pre-installed packages available (no runtime installation)

## Migration path for alcanzai: from bundled prompts to native skills

**Recommended architecture for your 15-skill system:**

```
skills/
├── understand-academic-text/
│   ├── SKILL.md
│   └── references/
│       ├── section-parsing.md
│       └── citation-handling.md
├── extract-arguments/
│   ├── SKILL.md
│   └── scripts/
│       └── argument_mapper.py
├── identify-terminology/
│   ├── SKILL.md
│   └── domain_glossaries/
│       └── [domain-specific term lists]
├── register-controller/          # Consolidates your 9 register variants
│   ├── SKILL.md
│   └── registers/
│       └── [9 register definition files]
├── quick-summary/
│   └── SKILL.md
├── detailed-summary/
│   ├── SKILL.md
│   └── templates/
│       └── summary-structure.json
└── glossary-extraction/
    ├── SKILL.md
    └── scripts/
        └── term_processor.py
```

**Migration steps:**

1. **Extract skill definitions** from Python prompt bundling code into SKILL.md files
2. **Consolidate 9 register skills** into single `register-controller` with reference files
3. **Upload skills** via API, storing returned `skill_id` values
4. **Replace prompt bundling** with `container.skills` selection at runtime
5. **Test with evaluations** comparing token usage and output quality

**Example request after migration:**
```python
# Instead of bundling all prompts:
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=8192,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "custom", "skill_id": alcanzai_skills["understand-academic-text"]},
            {"type": "custom", "skill_id": alcanzai_skills["extract-arguments"]},
            {"type": "custom", "skill_id": alcanzai_skills["register-controller"]},
            {"type": "custom", "skill_id": alcanzai_skills["detailed-summary"]}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": f"Analyze this paper for expert audience: {paper_text}"}]
)
```

## Conclusion: key implementation decisions for alcanzai

The Agent Skills API provides a production-ready path from your bundled-prompt architecture. **Consolidate registers into one skill with reference files** for maximum token efficiency. **Bundle analytical scripts** (terminology extraction, argument mapping) for zero-context execution. **Use explicit conditional loading** in SKILL.md to ensure Claude only reads what's needed.

The progressive disclosure architecture transforms your token economics: instead of ~75,000 tokens loading all 15 skills upfront, you'll pay ~1,500 tokens at startup plus ~5,000-15,000 tokens for activated skills. For iterative research paper analysis, this represents **70-80% token savings** while gaining version control, modular updates, and cross-platform portability through the open standard.