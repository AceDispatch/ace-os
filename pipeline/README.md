# pipeline/ — the standardized region routine

One command runs a region through the canonical pipeline (Prospect → Classify → Research → Match)
and lands results in Supabase.

## Run
```
python pipeline/run_region.py --region <name> \
    --counties "ST:County,County;ST:County" \
    --vertical flatbed
```

Stages:
1. **Prospect** — slice the EPA roster(s) for the named counties → region roster.
2. **Classify** (`classify.py`) — sort EVERY company by equipment (flatbed/van/dump/tanker/heavy-haul)
   + FTL signal. Multi-vertical, mechanical, no web. **Sort, don't discard.**
3. **Worklist** — emit the target-vertical research worklist (+ chunked args for the research fan-out).
4. **Research** — the AI runs the research workflow on the worklist (verify FTL + door + lanes).
5. **Sync** — `python db/sync.py <results.csv>` upserts verified records into Supabase.

Per-region working files land in `outbox/<region>/`; the final dial sheet is the deliverable.

## Files
- `classify.py` — the multi-vertical **Classify** stage (supersedes the flatbed-only grader for the DB era).
- `run_region.py` — the orchestrator (Prospect + Classify + worklist; research + sync are the follow-on steps).
