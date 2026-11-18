# The Undercut Explained: Why Pitting First Wins Races

- **Niche:** F1
- **Format:** Long (about 8-9 min, roughly 1,250 spoken words)
- **Status:** Draft 1
- **Notes:** Example numbers are made up for clarity. Replace with a real race from FastF1 where possible.

---

## 0:00 | Hook (20 sec)
**VO:** "Two cars are a second and a half apart. Neither is faster. Neither can overtake. And yet one of them is about to pass the other, on pit lane, while going slower than the car in front. This is the undercut, and it decides more races than any overtake."

**[VISUAL]** Animated track map, two dots. The rear dot dives into the pits, and the front dot continues. Freeze, then cut to the title.

## 0:20 | The problem (45 sec)
**VO:** "Modern F1 cars are very hard to follow. Get within a second of someone and your front tyres overheat in their turbulent air. So if you're stuck behind a car with the same pace, overtaking on track is close to impossible. Teams need another way to pass, and the pit stop is it."

**[VISUAL]** Diagram of dirty air behind a car (turbulence cone). Text on screen: "Same pace = stuck."

## 1:05 | What an undercut is (60 sec)
**VO:** "An undercut is simple. The car behind pits first, before the car in front. It comes out on fresh tyres. Fresh tyres are faster, often by a full second a lap or more, compared to old, worn ones. So while the car in front stays out on tired rubber, the car behind starts lapping quicker. Then the car in front pits, and when it rejoins, it finds the other car has already passed it."

**[VISUAL]** Two lap-time lines on a graph. One drops sharply after the stop. A "tyre delta" bracket marks the gap between them.

## 2:05 | Why tyres matter: degradation (75 sec)
**VO:** "Why is a fresh tyre so much faster? Tyre degradation. As a tyre wears, it loses grip, and the car gets slower every lap. The softer the compound, the faster it falls off. Pirelli brings soft, medium and hard tyres, and the strategy is about picking when to swap them."

**[VISUAL]** FastF1 chart: lap time vs lap number for one stint, with a clear upward trend as the tyres wear. Label: "Lap time rises as the tyre wears."

**VO:** "So there's a trade-off. Stay out longer and you hold track position, but your lap times are getting worse. Pit earlier and you're faster, but you lose time in the pit lane."

## 3:20 | The maths with an example (2 min)
**VO:** "Let's use made-up numbers. Car A is 1.8 seconds behind Car B. Both stops cost about 22 seconds in the pit lane. That cost is the same for both cars, so it cancels out. What matters is what happens on track in between.

On lap 20, Car A pits. Car B stays out. Over the next two laps, Car A's fresh tyres are about a second a lap quicker than Car B's worn ones. That's roughly two seconds gained. The gap was 1.8. So when Car B pits on lap 22, Car A comes out ahead.

That's the undercut. It's not about being faster overall. It's about swapping slow tyre time for fast tyre time, and doing it first."

**[VISUAL]** Step-by-step animation. Show the gap as a number: 1.8s → 0.8s → −0.2s (A ahead). Highlight the crossover.

**VO:** "Notice the key idea. It works when the gain per lap, times the number of laps before the other car responds, is bigger than the gap."

**[VISUAL]** Equation card: `gap < tyre gain per lap × laps before they respond`

## 5:20 | When it fails (90 sec)
**VO:** "It doesn't always work. Here's what breaks it.

One. Traffic. If you pit and rejoin behind slower cars, your fresh tyres are wasted. You're stuck behind them, and the advantage disappears.

Two. Cold tyres. A new tyre needs a lap or two to get to temperature. If it doesn't warm up quickly, you lose the gain you were counting on.

Three. The other team responds. If the car in front pits the very next lap, you've only had one lap of benefit. That's why you'll see teams react to each other so quickly on the radio.

Four. Low-degradation circuits. If old tyres barely lose pace, the delta is small, and there's nothing to undercut with."

**[VISUAL]** Four quick icons or cards, one per failure point. Animate a car rejoining into a pack of cars for the traffic example.

## 6:50 | The overcut (60 sec)
**VO:** "Sometimes the smarter move is the opposite. The overcut. You stay out and let the other car pit first. If your tyres are still holding up, and the track is clear, you can lap quickly in clean air while they're stuck on a cold out-lap. When you finally pit, you rejoin ahead.

Undercut when your tyres are dying. Overcut when they're still alive."

**[VISUAL]** Mirror the earlier animation, with the front car staying out and the rear car pitting first, but ending with the front car still ahead.

## 7:50 | How to spot it yourself (45 sec)
**VO:** "Next time you watch a race, look for three things. The gap between two cars, usually within two to three seconds. How old each car's tyres are. And whether the team behind pits first. When all three line up, an undercut is coming. And now you'll see it before the commentators say it."

**[VISUAL]** Broadcast-style graphic you make yourself: a gap, a tyre age and a pit-window indicator.

## 8:35 | Outro (15 sec)
**VO:** "That's the undercut. Next, we look at how tyre degradation decides an entire Grand Prix. Subscribe so you don't miss it."

---

## Pulling real data with FastF1
```python
import fastf1
fastf1.Cache.enable_cache("cache")
session = fastf1.get_session(2024, "Bahrain", "R")   # pick a real race
session.load()
laps = session.laps.pick_drivers("VER")              # check your FastF1 version's method name
print(laps[["LapNumber", "LapTime", "Compound", "TyreLife", "PitInTime", "PitOutTime"]])
```
Look for two drivers within about 2 seconds of each other where one pitted first, then compare their lap times over the next three laps. That's your real-world example.

## Footage and copyright
Use your own graphics and animation. If you show any broadcast clips, keep them very short and add your own commentary. Don't build the video around them.

## Shorts cut (30 sec)
**VO:** "Two F1 cars, same speed, 1.5 seconds apart. Neither can pass on track. So the car behind pits first. Fresh tyres, a second a lap quicker. The car in front pits two laps later... and comes out behind. That's the undercut."

**[VISUAL]** Just the track-map animation, with big captions timed to each sentence.
