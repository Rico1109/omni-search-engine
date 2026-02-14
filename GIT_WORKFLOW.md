# Git Branch Structure for omni-search-engine Refactoring

## Current State
- Repository: https://github.com/Jaggerxtrm/omni-search-engine
- Current branch: main
- Status: Modified from OpenAI to Google APIs

## Branch Strategy

### Main Branch
- **Purpose**: Stable, production-ready code
- **Updates**: Only via PR merges from feature branches

### Feature Branches (4 phases)

#### Phase 1: Foundation
**Branch**: `feature/capture-pipeline`
**Goal**: Implement /capture command end-to-end
**Merges to**: main (after Phase 1 complete)

#### Phase 2: Refinement + Logging
**Branch**: `feature/activity-logging`
**Goal**: /refine skill + activity tracking
**Merges to**: main (after Phase 2 complete)

#### Phase 3: Continuity System
**Branch**: `feature/continuity-system`
**Goal**: /good-morning, /harvest, weekly notes
**Merges to**: main (after Phase 3 complete)

#### Phase 4: Polish
**Branch**: `feature/documentation`
**Goal**: Comprehensive docs + testing
**Merges to**: main (after Phase 4 complete)

## Workflow Commands

### Starting Phase 1
```bash
git checkout main
git pull origin main
git checkout -b feature/capture-pipeline
git push -u origin feature/capture-pipeline
```

### Completing Phase 1
```bash
git checkout feature/capture-pipeline
git add <files>
git commit -m "feat: implement /capture transformation pipeline"
git push origin feature/capture-pipeline
# Create PR on GitHub: feature/capture-pipeline → main
# Merge PR after review
```

### Starting Phase 2
```bash
git checkout main
git pull origin main
git checkout -b feature/activity-logging
git push -u origin feature/activity-logging
```

*Repeat pattern for Phase 3 and Phase 4*

## PR Template (for each phase merge)

**Title**: `feat: [Phase X] - [Description]`

**Body**:
```
## Changes
- List key changes

## Testing
- How was it tested

## Checklist
- [ ] Code follows project standards
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Ready for merge to main
```

## Current Phase Status

- [x] Planning complete (WORKFLOW_TRANSFORMATION_PLAN.md created)
- [ ] Phase 1: Foundation (feature/capture-pipeline)
- [ ] Phase 2: Refinement + Logging (feature/activity-logging)
- [ ] Phase 3: Continuity System (feature/continuity-system)
- [ ] Phase 4: Polish (feature/documentation)
