# Obsidian Workflow Transformation: From Plain Text to State-of-the-Art

## Context

**Current State:**
- 23-file vault with excellent trading notes (frontmatter, structure) but plain text dumps elsewhere
- PARA folder structure (1.Projects, 2.Areas, 3.Resources, Templates)
- omni-search-engine fully functional with Gemini embeddings + FlashRank reranking

**Problem:**
1. **Format friction**: Plain text instead of rich Markdown → avoidance
2. **No organization system**: Information loss, binge work/study cycles
3. **Missing continuity**: No log/path to track progress across sessions
4. **Never finishing projects**: Disconnected work sessions without context

**User's Vision:**
- "Get obsessed with Obsidian" through frictionless note-taking
- Transform plain text brainstorms → state-of-art Markdown automatically
- Auto-placement in correct folders
- Complete omni-search-engine refactoring on forked repo with feature branches

**User Preferences** (from questioning):
- Mix of quick captures + daily notes
- Auto-detect folder placement with AskUserQuestion when ambiguous
- Auto-transformation with clarification dialogs for edge cases
- Open to continuity solutions

**Inspiration from Claude Life OS:**
- **Periodic Cascade**: Daily ← Weekly ← Quarterly alignment prevents binge work
- **Harvest Routine**: End-of-day closure for psychological completeness
- **Task Alignment**: Every task links to a project/goal (no orphan work)
- **Chief of Staff Pattern**: Proactive agent vs passive chatbot

**Inspiration from Zettelkasten/Obsidian Best Practices:**
- **Atomic Notes**: One note = one idea (enforced by classifier service)
- **Links over Folders**: Semantic search finds connections, auto-generates wikilinks
- **MOCs (Maps of Content)**: Auto-generate project MOCs from note clusters
- **Properties/Dataview**: Rich frontmatter enables queryable vault
- **Templates**: Content-type specific templates reduce friction

---

## Solution Architecture

### High-Level Design

```
User Input (/capture, /refine)
    ↓
Workflow Orchestration Layer
    ↓
Classification → Enrichment → Placement → Logging
    ↓
Write Note + Auto-Index + Activity Log
```

**Core Components:**
1. **Classification Service**: Detect content type (meeting, research, idea, daily, etc.)
2. **Enrichment Service**: Generate frontmatter + structure content + find related notes
3. **Placement Service**: Auto-detect folder with confidence scoring
4. **Activity Service**: Log events + maintain timeline + project breadcrumbs
5. **Workflow Service**: Orchestrate multi-step processes with state management
6. **Periodic Notes System**: Weekly/Daily cascade for goal alignment (Life OS)
7. **Harvest Routine**: End-of-day closure and reflection (Life OS)

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

**Goal**: Get `/capture` command working end-to-end

**Tasks:**
1. Create `/capture` skill structure:
   - `~/.claude/skills/capture/SKILL.md`
   - `~/.claude/skills/capture/scripts/`
   - `~/.claude/skills/capture/references/`

2. Implement core services:
   - `services/classifier_service.py` - Rule-based content type detection
   - `services/enricher_service.py` - Frontmatter generation + content structuring
   - `services/placement_service.py` - Folder suggestion with confidence scoring
   - `services/workflow_service.py` - Orchestration layer

3. Add MCP tool to `server.py`:
   ```python
   @mcp.tool()
   async def capture_text(content: str, source: str = "manual") -> dict:
       workflow = get_workflow_service()
       return await workflow.capture(content, source)
   ```

4. Update dependency injection in `dependencies.py`:
   ```python
   @lru_cache
   def get_workflow_service() -> WorkflowService:
       return WorkflowService(
           classifier=get_classifier(),
           enricher=get_enricher(),
           placement=get_placement()
       )
   ```

**Validation:**
- `/capture "Met with John about trading bot"` → creates properly formatted note in correct folder
- Frontmatter includes: created, type, tags, status
- Content has structure: ## Attendees, ## Discussion, ## Action Items
- Filename is descriptive and collision-free

**Critical Files:**
- `services/classifier_service.py` (new)
- `services/enricher_service.py` (new)
- `services/placement_service.py` (new)
- `services/workflow_service.py` (new)
- `server.py` (modify - add capture_text tool)
- `dependencies.py` (modify - register new services)

---

### Phase 2: Refinement + Activity Logging (Week 2)

**Goal**: Enable post-hoc enrichment + track all vault activity

**Tasks:**
1. Implement `/refine` skill:
   - Analyze existing notes for gaps (missing frontmatter, no links, insufficient tags)
   - Generate diff preview
   - Apply improvements with user confirmation

2. Create activity logging system:
   - `services/activity_service.py` - Event tracking + timeline queries
   - `data/activity.sqlite` schema:
     ```sql
     CREATE TABLE activity_log (
         timestamp TEXT, event_type TEXT, resource TEXT,
         context TEXT, duration INTEGER
     );
     CREATE TABLE sessions (
         start_time TEXT, notes_created INTEGER, searches_performed INTEGER
     );
     ```

3. Add event decorators to existing tools:
   ```python
   @emit_event("note_created")
   @mcp.tool()
   async def write_note(...):
       # existing implementation

   @emit_event("search_performed")
   @mcp.tool()
   async def semantic_search(...):
       # existing implementation
   ```

4. Add MCP tool for activity queries:
   ```python
   @mcp.tool()
   async def get_activity_timeline(hours: int = 24) -> list[dict]:
       activity = get_activity_service()
       return activity.get_timeline(hours)
   ```

**Validation:**
- `/refine 1.Projects/UnitaiPR/NewFeatures.md` → preview shows suggested improvements
- Activity events logged to `activity.sqlite` with correct timestamps
- `get_activity_timeline(24)` returns last 24h of note creations, searches, etc.

**Critical Files:**
- `services/activity_service.py` (new)
- `data/activity.sqlite` (new database)
- `server.py` (modify - add refine_note, get_activity_timeline tools + decorators)
- `dependencies.py` (modify - register activity_service)
- `settings.py` (modify - add ActivitySettings)

---

### Phase 3: Continuity System (Week 3) - **Enhanced with Life OS Concepts**

**Goal**: Solve "no log, no path, information loss" problem using Periodic Notes Cascade

**Tasks:**

1. **Implement Periodic Notes Structure** (Life OS-inspired):
   - Weekly notes template: `Templates/weekly-note.md`
     - Section: ## This Week's Focus (3 max goals)
     - Section: ## Projects Active This Week
     - Section: ## Daily Summaries (auto-populated)
   - Daily notes enhancement to existing `tp_daily_hub.md`:
     - Add: [[This Week's Focus]] link at top
     - Add: ## Alignment Check (shows weekly goals)
     - Keep existing trading-specific sections

2. **Implement `/good-morning` skill** (Life OS-inspired):
   - Phase 1: Read yesterday's daily note for open loops
   - Phase 2: Read this week's focus goals
   - Phase 3: Suggest top 3 tasks aligned with weekly goals
   - Phase 4: Auto-create today's daily note with:
     - Weekly goals reminder
     - Yesterday's incomplete tasks
     - Suggested priorities

3. **Implement `/harvest` skill** (NEW - Life OS-inspired):
   - Run at end of day
   - Scan today's unstructured logs/captures
   - Categorize: ✅ Completed, ⏭️ Migrate to tomorrow, 💡 Extract as insight
   - Update weekly note with daily summary
   - Mark incomplete tasks for tomorrow's `/good-morning`
   - **Purpose**: Psychological closure + prevent information loss

4. **Add Task Alignment Metadata** (Life OS-inspired):
   - When capturing tasks, classify as:
     - Project-linked: `project: TradingSystem`
     - Area-linked: `area: Learning`
     - Orphan: triggers AskUserQuestion ("Which goal does this serve?")
   - Prevent "no orphan work" rule enforcement

5. **Implement `/status` skill** (enhanced):
   - Query activity log grouped by project
   - Read weekly note for incomplete goals
   - Suggest next action based on weekly focus + last activity
   - Return quick actions: process inbox, review yesterday's notes, check weekly progress

6. Add MCP tools:
   ```python
   @mcp.tool()
   async def good_morning() -> dict:
       # Initialize the day with context from yesterday + this week

   @mcp.tool()
   async def harvest() -> dict:
       # End-of-day closure: categorize logs, migrate tasks, update weekly

   @mcp.tool()
   async def get_weekly_focus(week: str = "current") -> dict:
       # Return this week's goals and alignment status
   ```

**Validation:**
- `/good-morning` creates today's daily note with weekly goals + yesterday's carryover
- `/harvest` categorizes day's work and updates weekly summary
- `/status` shows projects + weekly goal alignment
- User experiences "closure" at end of each day
- User knows what to work on each morning without decision paralysis

**Critical Files:**
- `services/workflow_service.py` (modify - add good_morning, harvest, get_weekly_focus methods)
- `server.py` (modify - add good_morning, harvest, get_weekly_focus tools)
- `utils.py` (new functions - extract_incomplete_tasks, update_markdown_section, parse_weekly_goals)
- `Templates/weekly-note.md` (new template)
- `Templates/tp_daily_hub.md` (modify - add weekly alignment section)

---

### Phase 4: Polish + Documentation (Week 4)

**Goal**: Production-ready with comprehensive docs

**Tasks:**
1. Write SKILL.md files:
   - `~/.claude/skills/capture/SKILL.md` - Usage examples, workflow, troubleshooting
   - `~/.claude/skills/refine/SKILL.md` - Batch mode, gap analysis
   - `~/.claude/skills/status/SKILL.md` - Session resume patterns

2. Create reference documentation:
   - `content-types.md` - All supported content types + detection rules
   - `frontmatter-spec.md` - YAML schema for each content type
   - `placement-rules.md` - Folder suggestion decision tree

3. Error handling:
   - Graceful degradation when classification confidence <0.5
   - Fallback to AskUserQuestion for ambiguous content
   - Validate file paths (security)
   - Handle collisions (duplicate filenames)

4. Performance optimization:
   - Cache embedding results for placement suggestions
   - Batch process multiple captures
   - Debounce activity logging (max 1 event/sec per type)

5. Integration tests:
   - Test full `/capture` → classify → enrich → place → log pipeline
   - Test `/refine` on existing plain text notes
   - Test `/status` with real activity data
   - Test edge cases (long text, no clear type, multiple projects)

6. User onboarding:
   - Setup guide: fork repo, install deps, configure .env
   - Quickstart: first 5 captures
   - FAQ: common issues and solutions

**Validation:**
- All skills have comprehensive documentation
- Error messages are helpful (not just stack traces)
- Performance benchmarks: `/capture` <2s, `/refine` <1s
- Integration tests pass on sample vault

**Critical Files:**
- `~/.claude/skills/capture/SKILL.md` (new)
- `~/.claude/skills/capture/references/*.md` (new)
- `README.md` (modify - add new features)
- `USAGE.md` (new - comprehensive usage guide)

---

## Git Workflow Strategy

### Repository Setup

1. **Fork omni-search-engine**:
   ```bash
   cd ~/Projects/CodeBase
   git clone https://github.com/yourusername/omni-search-engine.git omni-search-engine-fork
   cd omni-search-engine-fork
   git remote add upstream https://github.com/original/omni-search-engine.git
   ```

2. **Create main branch**:
   ```bash
   git checkout -b main
   git push -u origin main
   ```

3. **Branch strategy**:
   - `main` - stable, production-ready
   - `feature/capture-pipeline` - Phase 1 work
   - `feature/activity-logging` - Phase 2 work
   - `feature/continuity-system` - Phase 3 work
   - `feature/documentation` - Phase 4 work

### Merge Strategy

**Phase 1 → main**:
```bash
git checkout feature/capture-pipeline
# Complete all Phase 1 tasks
git add services/classifier_service.py services/enricher_service.py ...
git commit -m "feat: implement /capture transformation pipeline"
git checkout main
git merge --no-ff feature/capture-pipeline
git push origin main
```

**Phase 2 → main** (after Phase 1 merged):
```bash
git checkout -b feature/activity-logging main
# Complete Phase 2 tasks
git commit -m "feat: add activity logging and /refine skill"
git checkout main
git merge --no-ff feature/activity-logging
git push origin main
```

*Repeat for Phase 3 and Phase 4.*

**Pull from upstream** (if needed):
```bash
git fetch upstream
git rebase upstream/main
```

---

## Feature Prioritization Matrix

| Feature | Impact on Adoption | Implementation Effort | Priority |
|---------|-------------------|---------------------|----------|
| `/capture` basic transformation | ★★★★★ (solves main pain) | Medium | **P0** |
| Frontmatter generation | ★★★★★ (enables automation) | Low | **P0** |
| Auto folder placement | ★★★★☆ (reduces friction) | Medium | **P0** |
| Activity logging | ★★★☆☆ (nice to have) | Low | **P1** |
| `/refine` for existing notes | ★★★★☆ (cleanup backlog) | Medium | **P1** |
| **`/good-morning` routine** | **★★★★★ (prevents binge cycles)** | **Medium** | **P1** |
| **`/harvest` end-of-day closure** | **★★★★★ (psychological closure)** | **Medium** | **P1** |
| **Weekly notes cascade** | **★★★★★ (goal alignment)** | **Low** | **P1** |
| `/status` session resume | ★★★★☆ (continuity) | Low | **P2** |
| Task alignment metadata | ★★★★☆ (no orphan work) | Low | **P2** |
| Daily note auto-generation | ★★★☆☆ (tracking) | Low | **P2** |
| Batch `/refine` | ★★☆☆☆ (vault-wide cleanup) | Medium | **P3** |
| Auto-linking (Zettelkasten) | ★★★☆☆ (graph density) | Medium | **P4 (Future)** |
| Auto-generate MOCs (Zettelkasten) | ★★★☆☆ (navigation) | Medium | **P4 (Future)** |
| Ghost link tracking (Zettelkasten) | ★★☆☆☆ (prompts for content) | Low | **P4 (Future)** |

**Phase 1 = P0 features, Phase 2 = P1 features, Phase 3 = P1+P2 features (with Life OS concepts), Phase 4 = polish**

**Life OS Integration Rationale:**
- **Weekly Notes Cascade**: Directly solves "binge work/study" → forces alignment check every morning
- **`/good-morning` routine**: Eliminates decision paralysis → clear priorities every day
- **`/harvest` closure**: Prevents information loss → ensures nothing falls through cracks
- **Task alignment**: Enforces "no orphan work" → every action serves a goal

**NOT Adopting from Life OS:**
- ❌ Quarterly/Monthly OKR system (too heavy for starting, can add later)
- ❌ Shadow Observer (we have activity logging already)
- ❌ Complex "Iron Laws" (start simple, add governance later)

**Zettelkasten Principles (Phase 5 / Future Enhancement - "Side Quest"):**
- ⏭️ **Atomic Notes**: Can be enforced more strictly later (not core MVP)
- ⏭️ **Auto-Linking**: Semantic search → auto wikilinks (powerful but complex)
- ✅ **Properties/Templates**: Content-type specific frontmatter (already in Phase 1)
- ⏭️ **MOCs**: Auto-generated from note clusters (nice-to-have, not critical)
- ⏭️ **Dataview queries**: User can add manually (outside automation scope)

---

## Success Metrics & Tracking

### Adoption Metrics (via activity.sqlite)

**Week 1 Target**:
- 3+ `/capture` invocations
- 1+ manually refined note

**Month 1 Target**:
- 20+ notes created via `/capture`
- 10+ refined notes
- 50+ activity events logged

**Month 3 Target**:
- 100+ total notes in vault
- 70%+ have frontmatter
- User reports "obsessed with Obsidian"

### Quality Metrics

**Frontmatter Coverage**:
```sql
SELECT
    COUNT(*) AS total_notes,
    SUM(CASE WHEN has_frontmatter THEN 1 ELSE 0 END) AS with_frontmatter,
    ROUND(100.0 * SUM(CASE WHEN has_frontmatter THEN 1 ELSE 0 END) / COUNT(*), 1) AS coverage_pct
FROM notes;
```
Target: >80%

**Tag Consistency**:
- % of tags reused (vs. new tags created)
- Target: >60% reused (indicates convergence to canonical tags)

**Link Density**:
- Average wikilinks per note
- Target: >3 (indicates connected thinking)

### Behavioral Metrics

**Session Frequency**:
```sql
SELECT
    DATE(timestamp) AS date,
    COUNT(DISTINCT session_id) AS sessions
FROM activity_log
GROUP BY DATE(timestamp)
ORDER BY date DESC
LIMIT 7;
```
Target: 5+ days/week with activity

**Project Continuity**:
- % of projects with activity in last 7 days
- Target: >50% (prevents project abandonment)

**Inbox Clearance**:
- % of notes moved from 0.Inbox within 7 days
- Target: >80% (good organization habits)

---

## Critical Files Summary

### New Files to Create (16 total)

**Services** (8 files):
1. `services/classifier_service.py` - Content type detection
2. `services/enricher_service.py` - Frontmatter + structure generation
3. `services/placement_service.py` - Folder suggestion engine
4. `services/activity_service.py` - Event logging + timeline
5. `services/workflow_service.py` - Multi-step orchestration
6. `services/gemini_embedding_service.py` - *(already exists)*
7. `utils.py` - *(modify)* Add markdown section parsing

**Skills** (3 directories):
8. `~/.claude/skills/capture/SKILL.md`
9. `~/.claude/skills/refine/SKILL.md`
10. `~/.claude/skills/status/SKILL.md`

**References** (3 files):
11. `~/.claude/skills/capture/references/content-types.md`
12. `~/.claude/skills/capture/references/frontmatter-spec.md`
13. `~/.claude/skills/capture/references/placement-rules.md`

**Database**:
14. `data/activity.sqlite` - Activity tracking database

**Documentation**:
15. `USAGE.md` - Comprehensive usage guide
16. `QUICKSTART.md` - 5-minute onboarding

### Files to Modify (5 total)

1. `server.py` - Add 5 new MCP tools + event decorators
2. `dependencies.py` - Register 5 new services
3. `settings.py` - Add ActivitySettings + ClassificationSettings
4. `README.md` - Update with new features
5. `requirements.txt` - Add dependencies (if any)

---

## Verification Steps

### End-to-End Test: /capture Flow

1. **Invoke skill**:
   ```
   /capture "Discussed AI embeddings with Marco. Should try Gemini API for cost savings. Action: Research Gemini pricing and limits."
   ```

2. **Expected classification**:
   - Type: `meeting`
   - Entities: {people: ["Marco"], tools: ["Gemini API"]}
   - Confidence: 0.85

3. **Expected enrichment**:
   ```yaml
   ---
   created: 2026-02-14T15:30:00+00:00
   type: meeting
   status: draft
   tags: [type/meeting, project/omni-search-engine, tool/gemini-api]
   participants: [Marco]
   source: capture
   ---

   # Meeting with Marco - AI Embeddings

   ## Attendees
   - Marco

   ## Discussion
   Discussed AI embeddings cost optimization. Gemini API could provide savings compared to OpenAI.

   ## Action Items
   - [ ] Research Gemini pricing and rate limits
   - [ ] Compare embedding quality vs OpenAI
   ```

4. **Expected placement**:
   - Folder: `1.Projects/omni-search-engine/meetings/` (confidence: 0.85)
   - Filename: `2026-02-14-marco-embeddings.md`

5. **Expected activity log**:
   ```json
   {
     "timestamp": "2026-02-14T15:30:00",
     "event_type": "note_created",
     "resource": "1.Projects/omni-search-engine/meetings/2026-02-14-marco-embeddings.md",
     "context": {
       "folder": "1.Projects/omni-search-engine/meetings",
       "tags": ["type/meeting", "project/omni-search-engine"]
     },
     "duration": 1850
   }
   ```

6. **Validation checks**:
   - File exists at correct path
   - Frontmatter is valid YAML
   - Content has proper structure
   - Note is indexed in ChromaDB
   - Activity event logged

### End-to-End Test: /status Flow

1. **Invoke skill**: `/status`

2. **Expected output**:
   ```json
   {
     "summary": "12 events in last 24h",
     "projects": [
       {
         "project": "omni-search-engine",
         "last_note": "meetings/2026-02-14-marco-embeddings.md",
         "hours_since_activity": 0.5,
         "incomplete_tasks": 2,
         "suggested_next": "Complete task: Research Gemini pricing"
       },
       {
         "project": "TradingSystem",
         "last_note": "1.Daily/2026-02-14.md",
         "hours_since_activity": 12.3,
         "incomplete_tasks": 0,
         "suggested_next": "Review yesterday's trading notes"
       }
     ],
     "quick_actions": [
       "Process 3 items in 0.Inbox",
       "Continue working on omni-search-engine"
     ]
   }
   ```

3. **Validation**:
   - Activity timeline accurate
   - Incomplete tasks extracted from project READMEs
   - Suggested next actions are contextually relevant

---

## Phase 5: Zettelkasten Enhancements (Future / "Side Quest")

**After Phases 1-4 are stable and user is "obsessed with Obsidian"**, consider:

### Zettelkasten Automation (Optional)

**Auto-Linking System:**
- `services/linking_service.py` - Use semantic search to find related notes
- Auto-insert wikilinks inline where concepts match
- Add "Related Notes" section in frontmatter

**MOC Generation:**
- `/generate-moc [project]` skill
- Cluster notes by topic using embeddings
- Create project index notes with auto-generated sections

**Atomic Note Enforcement:**
- Detect when a note has multiple topics
- Suggest splitting into separate notes
- Auto-extract distinct concepts

**Ghost Link Tracking:**
- Identify unresolved `[[wikilinks]]`
- Suggest content to fill ghost links
- Prioritize by link frequency

---

## Extension Points (Even Later)

**After Zettelkasten automation**, consider:

1. **ML-Based Classification**:
   - Train small classifier on user's vault
   - Learn project-specific patterns
   - Improve accuracy over time

2. **Smart Templates**:
   - User-defined templates per content type
   - Template variables ({{project}}, {{date}}, etc.)
   - Template suggestions based on content

3. **Batch Operations**:
   - `/refine-vault` - process entire vault
   - `/reorg-vault` - reorganize based on learned patterns
   - `/dedupe-vault` - merge duplicate content

4. **Integrations**:
   - Capture from browser (bookmarklet)
   - Capture from mobile (Shortcuts integration)
   - Export to Obsidian Publish

5. **Analytics Dashboard**:
   - Vault health score
   - Weekly activity report
   - Project progress tracking

---

## Risk Mitigation

### Technical Risks

1. **Risk**: Classification accuracy too low
   - **Mitigation**: Start with rule-based + manual override via AskUserQuestion
   - **Fallback**: User selects content type manually

2. **Risk**: Folder placement wrong
   - **Mitigation**: Confidence threshold + AskUserQuestion for <0.8
   - **Fallback**: Default to 0.Inbox, user moves manually

3. **Risk**: Performance degradation (large vaults)
   - **Mitigation**: Cache embeddings, batch operations
   - **Fallback**: Progressive enhancement, disable features if slow

### Behavioral Risks

1. **Risk**: User abandons tool after 1 week
   - **Mitigation**: Quick wins in Phase 1, immediate value
   - **Metric**: Track weekly usage, intervene if drops

2. **Risk**: Tool adds friction instead of removing it
   - **Mitigation**: Minimize required inputs, smart defaults
   - **UX**: 1-command workflow, no multi-step dialogs

3. **Risk**: User overwhelmed by features
   - **Mitigation**: Incremental rollout, Phase 1 → 2 → 3
   - **Onboarding**: Start with /capture only, introduce /refine later

---

## Next Steps

1. **User approval**: Review plan, adjust priorities
2. **Fork repository**: Create clean fork with main branch
3. **Phase 1 kickoff**: Implement capture pipeline (1 week)
4. **Weekly check-ins**: Review metrics, adjust course
5. **Iterate**: Add Phase 2 features based on adoption

**Ready to transform your Obsidian workflow from plain text to state-of-the-art!** 🚀
