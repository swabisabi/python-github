# How Tyre Degradation Decides a Grand Prix

- **Niche:** F1
- **Format:** Long (about 8-9 min, roughly 1,250 spoken words)
- **Status:** Draft 1
- **Notes:** Follow-up to the undercut video (01). Example numbers are illustrative. Use a real race from FastF1 where possible.

---

## 0:00 | Hook (20 sec)
**VO:** "Two drivers. Same car speed, same start. One finishes 20 seconds ahead, and nothing dramatic happened. No crash, no safety car. The only difference was how long each of them made a handful of rubber last. This is tyre degradation, and it quietly decides most Grand Prix results."

**[VISUAL]** Two lap-time lines drifting apart over a race. Freeze on the final gap, then cut to the title.

## 0:20 | The idea in one line (40 sec)
**VO:** "Every lap, a tyre gets a little slower. Not because the driver is tired, but because the rubber itself is wearing out. Strategy in F1 is the art of deciding how much of that slowdown you can afford, and when to pay for fresh tyres with a pit stop."

**[VISUAL]** Single stint chart: lap time on the y-axis, lap number on the x-axis, a line that climbs. Caption: "The tyre is a fuel gauge for speed."

## 1:00 | The three compounds (60 sec)
**VO:** "Pirelli makes a range of tyre compounds, and for each race weekend they bring three: soft, medium and hard. Softer means more grip and faster laps, but it wears quickly. Harder means slower laps, but it lasts. Think of it as speed versus lifespan, and no compound gives you both."

**[VISUAL]** Three tyre icons (red, yellow, white) on a slider from "fast, short-lived" to "slow, durable". Add a note: "Dry races require at least two different compounds."

## 2:00 | Why tyres wear out (90 sec)
**VO:** "Tyres lose performance in two main ways.

The first is mechanical wear. Rubber is physically scraped off as the car turns, brakes and accelerates. Abrasive tracks and high-load corners do this faster.

The second is thermal. Tyres work best in a temperature window. Push them too hard, or race in the heat, and they overheat. The surface can slide, tear into little rolls called graining, or even bubble. Run them too cold and they don't grip at all.

A driver sliding the car, or following closely in someone's dirty air, makes both problems worse. That's why a lot of tyre management is about driving smoothly, not driving slowly."

**[VISUAL]** Two animated panels: rubber shavings coming off a tyre (mechanical), and a temperature gauge sliding into the red (thermal). Show a labelled close-up of graining using a stock or licensed image.

## 3:30 | The fuel effect (60 sec)
**VO:** "There's a trick when you read the data. Cars start the race with around 100 kilos of fuel, and burn it off lap by lap. A lighter car is faster, by roughly a few tenths of a second a lap at the start, less near the end. So if lap times are flat, the tyres may actually be getting worse, and the fuel burn is hiding it. Analysts correct for this, and so should anyone reading a lap-time chart."

**[VISUAL]** Overlay two lines on one chart: raw lap times (flat) and fuel-corrected lap times (rising). Label them clearly.

## 4:30 | The cliff (60 sec)
**VO:** "Degradation isn't always a gentle slope. Many tyres lose time slowly, and then suddenly fall off a cliff. One lap you're fine, the next you're a second slower, and then two. That moment is why teams stop 'just in case' and why a driver who stays out a lap too long can lose a place, or a race."

**[VISUAL]** A lap-time graph with a long gentle slope and a sharp upward kink. Mark the kink "the cliff".

## 5:30 | Building a strategy (2 min)
**VO:** "Now we put it together. Suppose the soft tyre is two-thirds of a second a lap faster than the hard when fresh, but it degrades much faster. Over a long race, one stop on mediums and hards might be slower per lap, but you only lose the pit-lane time once. Two stops on softer tyres means more time lost in the pits, but you're faster between them.

Which wins? It depends on three numbers: how fast each tyre is when fresh, how quickly it degrades, and how much a pit stop costs at this track. Teams run thousands of simulations to find the crossover. But you can follow the logic yourself:

Total race time equals your lap times added up, plus pit-stop time. A fast tyre that wears out costs more stops. A slow tyre that lasts costs fewer. The winning strategy is the combination that adds up to the smallest total."

**[VISUAL]** Side-by-side animated bars showing total race time for a one-stop and a two-stop strategy, built up from lap time + pit loss. End with the lower total highlighted.

## 7:30 | How it ties back to the undercut (30 sec)
**VO:** "And this is why the undercut works. If your tyres have degraded and a rival's have too, fresh rubber is a big gain. The more a track punishes tyres, the more powerful the undercut. Where tyres barely wear, it barely works. Degradation is the engine behind the whole pit-stop game."

**[VISUAL]** Quick clip of your undercut animation, with an arrow labelled "tyre delta".

## 8:00 | What to watch for in a race (40 sec)
**VO:** "Next race, watch the lap times in the timing screen. When a driver's laps start creeping up by a few tenths, their tyres are fading. When a team calls them in, you'll know why. And when someone stays out and their pace holds, you're watching tyre management at work."

**[VISUAL]** A mock timing screen you build yourself. Highlight one driver's lap times rising.

## 8:40 | Outro (15 sec)
**VO:** "That's tyre degradation. If you missed the undercut video, it's linked here. And subscribe, because next time we look at how teams use this to decide who actually wins."

---

## Pulling real data with FastF1
```python
import fastf1
fastf1.Cache.enable_cache("cache")
session = fastf1.get_session(2024, "Bahrain", "R")   # pick a real race
session.load()
laps = session.laps.pick_drivers("VER")              # check your FastF1 version's method name
stint = laps[laps["Stint"] == 2]
print(stint[["LapNumber", "LapTime", "Compound", "TyreLife"]])
```
- Plot lap time against `TyreLife` to show the degradation trend.
- Exclude in-laps, out-laps and laps under safety cars or yellow flags, or the chart will look messy.
- To show the fuel effect, add a simple correction: subtract a small fixed amount per lap, based on laps completed. Say on screen that it's an estimate.

## Footage and copyright
Use your own charts and animation, and licensed or public-domain images for tyre close-ups. Keep any broadcast clips short and add your own commentary.

## Shorts cut (30 sec)
**VO:** "Why do F1 drivers pit when their car is still working fine? Because every lap, the tyre gets slower. Softer tyres are fast but die quickly. Harder ones last but cost you pace. Every race is a maths problem: how many stops, on which tyres, adds up to the smallest total time? That's tyre degradation."

**[VISUAL]** A rising lap-time line with captions timed to each sentence.
