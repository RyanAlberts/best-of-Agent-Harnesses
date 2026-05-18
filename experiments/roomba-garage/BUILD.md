# Roomba Garage — Build Plan & Shopping List

Source reel: <https://www.instagram.com/reel/DMs716wy9Zm/> — titled
"Genius Roomba Garage Storage Ideas". The web session that received this task
sat behind a network policy that blocks `instagram.com`, so the video itself
could not be fetched and inspected frame-by-frame from inside the agent
harness. The plan below is the **planter-topped end-table variant** of the
build, which is the most common and most photogenic version of "Roomba garage"
that matches a "genius" / single-shot reel format. See
[`tools/reel_processor.py`](tools/reel_processor.py) for a script that will
pull the reel + transcribe it once you're on a network that can reach
Instagram; if the actual video shows a different variant (full buffet cabinet,
under-stairs cubby, or IKEA SEKTION hack), adjust dimensions but the shopping
list stays ~80% the same.

## What you're building

A freestanding side-table-sized wood box, ~20" wide × 20" deep × 22" tall:

```
            ┌────────────────────┐  ← live planter box (top, recessed)
            │      🌿 🌱 🌿     │
            ├────────────────────┤  ← removable lid (access water/mop tank)
            │                    │
            │   (Roomba bay)     │  ← interior: 18" × 18" × 8"
            │                    │
            │   ┌──────────┐     │  ← drive-through door, hinged at top
            └───┘          └─────┘     OR cut-out opening with magnetic flap
                ↑
            Roomba enters here
```

Functional requirements the design has to hit:

1. **Roomba clearance.** iRobot Roomba j7/j9/Combo/i7 are all roughly 13.4"
   diameter × 3.5" tall. Allow ≥1.5" of slack on every side so the dock-seek
   doesn't bonk the carcass. Interior floor target: **18" × 18", 8" headroom**.
2. **Dock cable.** The home base needs a power cable run; drill a 1/2" grommet
   hole in the **back panel**, low and to one side, so the Roomba can still
   approach the dock head-on.
3. **IR line-of-sight.** Roomba uses an IR beam from the base to find home.
   Either (a) leave the front opening permanently open with a 2" lip, or
   (b) use a top-hinged flap the Roomba can nose open. **Magnets, not latches.**
4. **Planter ≠ leak.** The top planter box gets a separate plastic liner
   (cheap rectangular planter insert or a plastic storage tote cut to fit).
   No water ever touches structural wood.
5. **Top access for mop/water tank.** If you have a Combo j7/j9, leave the
   planter as a **removable tray** so you can lift it off and pop the
   Roomba's tank without dragging the whole unit out.

## Tools

You don't need everything — anything with a `(opt)` next to it has a manual
workaround.

- Tape measure, speed square, pencil
- Circular saw + straight-edge guide  *(or a table saw)*
- Jigsaw — for the front door cutout
- Drill / driver, 1/8" pilot bit, countersink bit
- Pocket-hole jig (Kreg K4 or similar) — easiest carcass joinery
- Brad nailer + 1¼" brads  *(opt; can hand-nail or just rely on pocket screws + glue)*
- Random-orbit sander, 80 / 120 / 220 grit pads
- 4 × 6" bar clamps
- Level
- Stud finder *(only if you're going to anchor it to a wall — usually not needed)*

## Shopping list

Prices are rough US retail at a big-box hardware store; round up.

### Lumber & sheet goods
| Qty | Item | Notes | $ |
|----:|---|---|---:|
| 1 | 4'×4' sheet ¾" birch plywood | Carcass: top, bottom, two sides, back. Have the store rip it for you. | 55 |
| 1 | 2'×4' sheet ¼" birch plywood | Planter tray bottom + door panel | 18 |
| 1 | 1"×2"×8' poplar | Face-frame trim around the door | 6 |
| 1 | 1"×3"×8' poplar | Top edge banding for the planter rim | 8 |
| 4 | 4" tapered wood furniture legs (or hairpin legs) | Lifts the base off the floor, hides the cable | 25 |

### Hardware
| Qty | Item | $ |
|----:|---|---:|
| 1 box | Kreg #8 × 1¼" pocket screws | 8 |
| 1 pack | 1¼" 18-ga brads | 5 |
| 2 | Small magnetic catches (if doing a hinged flap door) | 6 |
| 2 | Soss-style hidden mini hinges *or* a piano hinge | 10 |
| 4 | Felt furniture pads (so it doesn't scratch the floor) | 3 |
| 1 | ½" rubber grommet (for cable pass-through) | 2 |

### Finish
| Qty | Item | $ |
|----:|---|---:|
| 1 | 8 oz wood glue (Titebond II) | 6 |
| 1 | Small tub stainable wood filler | 5 |
| 1 | Pint of stain *or* paint in your accent color | 15 |
| 1 | Pint of water-based poly (satin) | 18 |
| 1 pack | Tack cloths | 4 |

### Planter
| Qty | Item | $ |
|----:|---|---:|
| 1 | Rectangular plastic planter insert ~16" × 16" × 5" | 12 |
| 1 bag | Indoor potting mix (small) | 8 |
| 1–2 | Plants — pothos, snake plant, or faux greenery if you don't trust yourself | 20 |

**Rough total: ~$235** with real plants; ~$200 with faux.

### Skip the build entirely?
If the reel turns out to be a "buy this, don't build this" recommendation,
the equivalent ready-made products are:
- mDesign Robot Vacuum Garage Cabinet — ~$90 on Amazon, no planter top
- Etsy "Roomba garage cabinet plans" PDF — ~$15 (plans only)
- IKEA hack: a single BESTÅ base cabinet (~$60) + 4 legs + a top cutout — see
  the IKEA Hackers article linked in the references below.

## Build order (one weekend)

1. **Confirm dock footprint.** Plug the dock in, push the Roomba onto it, and
   measure the bounding box. Add 1.5" of slack on every side. That's your
   interior floor. Adjust the cut list below if your robot is bigger than a
   standard Roomba (Roborock S8 Pro Ultra, for instance, is ~14" diameter +
   a much taller auto-empty base — you may need a 24"-tall carcass).
2. **Cut the carcass.** From the ¾" plywood:
   - Bottom: 20" × 20"
   - Two sides: 20" × 14"
   - Back: 18½" × 14"
   - Top (planter floor): 20" × 20"
3. **Drill pocket holes** on the underside edges of the bottom and the
   underside of the top — three per joint.
4. **Cut the front door opening** in what will become the front face. Use a
   jigsaw. Opening: ~14" wide × 5" tall, centered, 1" up from the bottom edge.
   Save the cutout — that's the door panel itself.
5. **Drill the cable grommet** — 1/2" hole in the back panel, ~2" up from the
   bottom, offset 4" from one side.
6. **Dry-fit** the whole carcass with clamps. The Roomba should drive in and
   out cleanly; the dock should sit flush against the back wall with its
   cable routed through the grommet.
7. **Glue and screw** the carcass together. Pocket screws + Titebond on every
   joint. Wipe squeeze-out immediately.
8. **Trim the door opening** with the 1"×2" poplar so the cut edge of the
   plywood doesn't show. Hang the cutout panel back as a door using the
   piano hinge (top-hinged so the Roomba noses it open) and magnetic catches.
9. **Build the planter tray** as a separate piece: 19½" × 19½" frame of
   1"×3" poplar with a ¼" plywood floor, sized to drop neatly into the top
   of the carcass. Don't glue it in — it has to lift off.
10. **Attach legs** to the bottom with the hanger bolts that came with them.
11. **Sand** 80 → 120 → 220. Fill nail holes. Sand again.
12. **Finish.** Stain or paint, then 2 coats of poly with a light 220 sand
    between coats.
13. **Drop the plastic liner into the planter tray, pot your plants, set the
    tray on top.**
14. **Move it into position.** Plug in the dock, route the cable through the
    grommet, run a Roomba job, and confirm it docks cleanly. If it bumps the
    door, widen the opening by ½" and re-trim.

## What to verify against the actual reel

When you run `python tools/reel_processor.py` and read `report.md`, double-check:

- [ ] Planter on top, or solid lid?
- [ ] Drive-through door (hinged) vs. open archway?
- [ ] Freestanding furniture, or wall-mounted / built-in?
- [ ] Single piece, or a stack of multiple "garages" (some reels show a row of
      three matching units for Roomba + dog bowl + shoe storage)?
- [ ] Any built-in lighting? (Some viral versions add a strip of warm LEDs
      inside the bay — add 1 × 3' USB LED strip ~$8 if so.)

If any of those answers disagree with this plan, the structural carcass and
shopping list still hold — only the top treatment / door style changes.

## References

- [How To Hide Robot Vacuum? — ECOVACS](https://www.ecovacs.com/au/blog/how-to-hide-robot-vacuum)
- [Robot Vacuum Cabinet & Storage Ideas — Dreame](https://www.dreametech.com/blogs/blog/robot-vacuum-docking-ideas)
- [Places You Should (and Shouldn't) Store Your Roomba — Reader's Digest](https://www.rd.com/article/should-store-roomba/)
- [This clever storage trick hides your robot vacuum — Ideal Home](https://www.idealhome.co.uk/house-manual/floorcare/robot-garage-to-hide-a-robot-vacuum-cleaner)
- [Creating a Garage for my Roomba — billyjacoby](https://www.billyjaco.by/blog/creating-a-garage-for-my-roomba)
- [DIY Robot Vacuum Garage: An IKEA Hack — IKEAHackers](https://ikeahackers.net/2025/09/robot-vacuum-garage-laundry-station.html)
- [Roomba Garage Cabinet Plans (paid PDF) — Etsy](https://www.etsy.com/listing/1850294341/roomba-garage-cabinet-plans)
- [Adorable Garage for a Roomba — Dengarden](https://dengarden.com/news/roomba-storage)
