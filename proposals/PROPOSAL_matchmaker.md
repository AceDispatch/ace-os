# SKILL PROPOSAL — The Matchmaker (v0.1 outline, future organ)

**Status:** PARKED 2026-06-13 — a completely separate system for later, when
there are more carriers to match. Not stressed this phase. The Refiner's CRM
output is already shaped to feed it whenever it's built. Hold as written.
**Derived from:** the verified-door inventory from both passes + the
relationship-brokering model the operator confirmed.

## What this hat is

The Matchmaker crosses verified/reachable shippers against the carrier book and
surfaces the move: which carrier (by lane) should be connected to which shipper
(by location + freight + door). It is where GEOGRAPHY finally enters — the thing
deliberately excluded from every upstream stage.

### Proposed doctrine (what the passes taught us it will need)

**1. Geography enters HERE, and only here.**
Every upstream stage ran geographically agnostic on purpose. The Matchmaker is
where a shipper's location is crossed against a carrier's actual running lanes.
This is the payoff of holding geography to the end: the same shipper pool serves
ANY carrier's geography.

**2. Match on three dimensions, not just distance:**
- **Lane:** does the shipper's location sit on/near a carrier's existing or
  desired lane?
- **Equipment:** flatbed shipper -> flatbed carrier. AND — the dump-vertical
  pool the Refiner tagged means the Matchmaker can ALSO match dump shippers to
  dump carriers when that vertical opens. (The "wrong trailer" results become
  matchable inventory for a future equipment type.)
- **Effort tier:** match a hungry/new carrier to a Tier-1 self-onboard door
  (fast win); reserve the Tier-2/3 "takes a call" doors for when there's a
  relationship worth the dispatcher's effort.

**3. The verified-door inventory is the seed.**
The 14 verified doors (12 flatbed + 2 dump) from the two passes are the first
matchable inventory. The dump pool specifically is a STANDING ASSET that lets a
dump-dispatch vertical launch warm instead of cold — a recursive-value win
(this vertical's rejects = next vertical's seed).

**4. The Matchmaker proposes the connection; the dispatcher makes the call.**
Consistent with the relationship-brokering model and Earned Authority: the
Matchmaker surfaces "carrier X fits shipper Y's door" as a proposal. The human
makes the outreach that establishes the lane. No autonomous outreach.

### What the Matchmaker would output
A ranked set of carrier<->shipper match proposals: which carrier, which shipper,
why (lane + equipment + effort tier), and the door/contact to use. Acted on by
the dispatcher.

### Dependencies before this can be built
- A structured carrier book (carriers + their lanes + equipment) — the right
  side of the equation. Does this exist yet in usable form?
- Enough verified shippers in the registry to make matching worthwhile (the two
  passes seeded it; more Refiner runs grow it).

### Open question for operator
- This is Phase 3 and depends on a structured carrier-lane book. Does that book
  exist, or is building it a prerequisite task we should scope separately?
