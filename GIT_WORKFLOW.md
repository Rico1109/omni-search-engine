# Git Branch Structure for omni-search-engine Refactoring

**Last Updated**: 2026-02-15
**Current Branch**: `feature/capture-pipeline`
**Current Phase**: Phase 1 - Foundation

---

## Repository Tree Structure

```
UPSTREAM REPOSITORY (Jaggerxtrm)
┌─────────────────────────────────────────────────────────────┐
│ github.com/Jaggerxtrm/omni-search-engine                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ main (upstream/main)                                    │ │
│ │ • Original repository baseline                          │ │
│ │ • Tracked for future upstream sync                      │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ (forked)
                           ▼
FORK REPOSITORY (Rico1109)
┌─────────────────────────────────────────────────────────────┐
│ github.com/Rico1109/omni-search-engine                      │
│                                                             │
│  main (origin/main) ✅                                      │
│  ├─ Commit: 44bbdc5                                        │
│  ├─ Status: Baseline with planning docs + Google API       │
│  ├─ Files: WORKFLOW_TRANSFORMATION_PLAN.md                 │
│  │         GIT_WORKFLOW.md                                 │
│  │         services/gemini_embedding_service.py            │
│  │                                                          │
│  │                                                          │
│  ├─► feature/capture-pipeline 🔵 ← ACTIVE                 │
│  │   ├─ Branch from: main (44bbdc5)                       │
│  │   ├─ Commit: 0be275d                                   │
│  │   ├─ Phase: 1 - Foundation                             │
│  │   ├─ Goal: Implement /capture command                  │
│  │   ├─ Status: IN PROGRESS                               │
│  │   └─ Merges to: main (when complete)                   │
│  │                                                          │
│  ├─► feature/activity-logging ⚪ (not created yet)        │
│  │   ├─ Phase: 2 - Refinement + Logging                   │
│  │   ├─ Goal: /refine + activity tracking                 │
│  │   └─ Merges to: main (after Phase 1)                   │
│  │                                                          │
│  ├─► feature/continuity-system ⚪ (not created yet)       │
│  │   ├─ Phase: 3 - Continuity System                      │
│  │   ├─ Goal: /good-morning, /harvest, weekly notes       │
│  │   └─ Merges to: main (after Phase 2)                   │
│  │                                                          │
│  ├─► feature/documentation ⚪ (not created yet)           │
│  │   ├─ Phase: 4 - Polish + Documentation                 │
│  │   ├─ Goal: Comprehensive docs + tests                  │
│  │   └─ Merges to: main (after Phase 3)                   │
│  │                                                          │
│  └─► fork-backup (backup)                                 │
│      ├─ Commit: 1f6cbc9                                   │
│      ├─ Purpose: Original fork history backup             │
│      └─ Contains: Credential rotation, Qwen integration   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Legend:
  ✅ = Completed and merged
  🔵 = Active development
  ⚪ = Planned (not started)
  🔴 = Blocked/Issues
```

---

## Phase Progress Tracker

### ✅ Phase 0: Planning & Setup (COMPLETE)
- [x] Create WORKFLOW_TRANSFORMATION_PLAN.md
- [x] Create GIT_WORKFLOW.md
- [x] Fork repository to Rico1109
- [x] Configure git remotes (origin/upstream)
- [x] Create baseline commit on main
- [x] Create `feature/capture-pipeline` branch

### 🔵 Phase 1: Foundation (IN PROGRESS)
**Branch**: `feature/capture-pipeline`
**Started**: 2026-02-15
**Target**: Week 1

**Tasks**:
- [ ] Create `/capture` skill structure
  - [ ] `~/.claude/skills/capture/SKILL.md`
  - [ ] `~/.claude/skills/capture/scripts/`
  - [ ] `~/.claude/skills/capture/references/`
- [ ] Implement core services
  - [ ] `services/classifier_service.py` - Content type detection
  - [ ] `services/enricher_service.py` - Frontmatter generation
  - [ ] `services/placement_service.py` - Folder suggestion
  - [ ] `services/workflow_service.py` - Orchestration
- [ ] Update MCP server
  - [ ] Add `capture_text()` tool to `server.py`
- [ ] Update dependencies
  - [ ] Register services in `dependencies.py`
- [ ] Validation
  - [ ] Test `/capture` end-to-end
  - [ ] Verify frontmatter generation
  - [ ] Verify folder placement
- [ ] Create PR: `feature/capture-pipeline` → `main`

**Deliverables**:
- Working `/capture` command
- Properly structured notes with frontmatter
- Auto-placement in correct folders

### ⚪ Phase 2: Refinement + Logging (PLANNED)
**Branch**: `feature/activity-logging` (to be created)
**Target**: Week 2

**Tasks**:
- [ ] Implement `/refine` skill
- [ ] Create activity logging system
- [ ] Add event decorators to existing tools
- [ ] Add activity timeline queries
- [ ] Create PR: `feature/activity-logging` → `main`

### ⚪ Phase 3: Continuity System (PLANNED)
**Branch**: `feature/continuity-system` (to be created)
**Target**: Week 3

**Tasks**:
- [ ] Implement periodic notes structure
- [ ] Implement `/good-morning` skill
- [ ] Implement `/harvest` skill
- [ ] Add task alignment metadata
- [ ] Implement `/status` skill
- [ ] Create PR: `feature/continuity-system` → `main`

### ⚪ Phase 4: Polish + Documentation (PLANNED)
**Branch**: `feature/documentation` (to be created)
**Target**: Week 4

**Tasks**:
- [ ] Write comprehensive SKILL.md files
- [ ] Create reference documentation
- [ ] Implement error handling
- [ ] Performance optimization
- [ ] Integration tests
- [ ] User onboarding docs
- [ ] Create PR: `feature/documentation` → `main`

---

## Git Workflow Commands

### Working on Current Phase (Phase 1)

```bash
# Ensure you're on the feature branch
git checkout feature/capture-pipeline

# Make changes
git add <files>
git commit -m "feat(capture): <description>"

# Push to remote
git push origin feature/capture-pipeline

# When ready for review
# Go to: https://github.com/Rico1109/omni-search-engine/pull/new/feature/capture-pipeline
```

### Completing Current Phase & Starting Next

```bash
# 1. Create PR on GitHub (feature/capture-pipeline → main)
# 2. Review and merge PR

# 3. Update local main
git checkout main
git pull origin main

# 4. Create next phase branch
git checkout -b feature/activity-logging
git push -u origin feature/activity-logging

# 5. Update this file (GIT_WORKFLOW.md) to mark Phase 1 complete
```

### Syncing with Upstream (if needed)

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream/main into your main
git checkout main
git merge upstream/main

# Push updated main to your fork
git push origin main
```

---

## Branch Naming Convention

- **Main**: `main` - Stable, production-ready
- **Feature**: `feature/<phase-name>` - Phase-specific work
- **Hotfix**: `hotfix/<issue-name>` - Emergency fixes
- **Backup**: `<name>-backup` - Saved histories

---

## PR Template

When creating PRs for phase merges, use this template:

**Title**: `feat: [Phase X] - <Phase Name>`

**Example**: `feat: [Phase 1] - Foundation (Capture Pipeline)`

**Body**:
```markdown
## Phase Summary
Phase 1: Foundation - Implement /capture transformation pipeline

## Changes
- ✅ Created classifier service for content type detection
- ✅ Created enricher service for frontmatter generation
- ✅ Created placement service for folder suggestions
- ✅ Created workflow service for orchestration
- ✅ Added capture_text() MCP tool
- ✅ Updated dependency injection

## New Files
- `services/classifier_service.py`
- `services/enricher_service.py`
- `services/placement_service.py`
- `services/workflow_service.py`
- `~/.claude/skills/capture/SKILL.md`

## Testing
- [x] `/capture "Meeting with John"` creates properly formatted note
- [x] Frontmatter includes: created, type, tags, status
- [x] Content has structure (## Attendees, ## Discussion, etc.)
- [x] Auto-placement in correct folder
- [x] No filename collisions

## Checklist
- [ ] Code follows project standards (type hints, logging, error handling)
- [ ] All tests pass
- [ ] Documentation updated (README.md, USAGE.md)
- [ ] No breaking changes
- [ ] Ready for merge to main

## Next Steps
After merge:
- Create `feature/activity-logging` branch
- Begin Phase 2 implementation
```

---

## Repository Information

**Fork (Work Here)**:
- URL: `https://github.com/Rico1109/omni-search-engine`
- Remote: `origin`
- Purpose: Active development

**Upstream (Original)**:
- URL: `https://github.com/Jaggerxtrm/omni-search-engine`
- Remote: `upstream`
- Purpose: Track original repo, potential future contributions

**Local Configuration**:
```bash
# View remotes
git remote -v

# View branches
git branch -a

# View current status
git status
```

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `git checkout feature/capture-pipeline` | Switch to Phase 1 branch |
| `git status` | Check current changes |
| `git log --oneline --graph --all -10` | View git history tree |
| `git push origin feature/capture-pipeline` | Push current work |
| `git pull origin main` | Sync with main branch |
| `git fetch upstream` | Get upstream changes |

---

## Notes

- **Always work on feature branches**, never directly on main
- **Create PRs** for all phase merges for review/documentation
- **Update this file** after completing each phase
- **Backup important work** before major git operations
- **Test thoroughly** before creating phase completion PRs

---

**Last Commit on Current Branch**: `0be275d` - "docs: update git workflow with current repository state"
**Next Milestone**: Complete Phase 1 implementation → Create PR → Merge to main
