# Shot list: The Undercut Explained (no broadcast footage)

Companion to `01-undercut-explained.md`. Uses only own gameplay, FastF1 animations and drawn graphics.

**Tools:** OBS Studio (record the game), Python with FastF1 and matplotlib (charts and animations), Canva or Kdenlive titles (diagrams and cards), Kdenlive (editing).

| Time | Script section | Shot | Source | How to make it |
|---|---|---|---|---|
| 0:00 | Hook | Two dots on a track map; the rear one dives into the pits | FastF1 animation | Plot a circuit outline from lap position data and animate two cars with `FuncAnimation`, exported to MP4 |
| 0:20 | The problem | Turbulence cone behind a car, caption "Same pace = stuck" | Drawn graphic | Canva or Kdenlive titles |
| 0:20 | The problem (optional) | Following closely and watching tyre temperature climb | Game gameplay | Follow an AI car closely for a lap with the tyre-temperature HUD showing |
| 1:05 | What an undercut is | Pit first, rejoin on fresh tyres, rival's lap times worse | Game gameplay + chart | Set up a custom race, pit a lap before the car ahead, record the stop and out-lap. Overlay a two-line lap-time chart |
| 2:05 | Why tyres matter | Lap time rising across a stint | FastF1 chart | Plot `LapTime` vs `TyreLife`, excluding in-laps, out-laps and safety-car laps |
| 3:20 | The maths | Gap counter going 1.8s → 0.8s → -0.2s | Animated graphic | Animate the numbers on a simple timeline, then the equation card |
| 5:20 | When it fails: traffic | Rejoining into a pack of cars | Game gameplay | Pit on a lap when the pit exit will drop you behind traffic |
| 5:20 | When it fails: cold tyres | Tyre temperature shown blue and low | Game gameplay | Capture the tyre HUD on the out-lap |
| 5:20 | Other two failures | Icon cards (rival responds, low-degradation track) | Drawn graphic | Canva or Kdenlive titles |
| 6:50 | The overcut | Mirror of the undercut animation, front car stays ahead | FastF1 animation | Reuse the 0:00 animation with the roles swapped |
| 7:50 | Spot it yourself | Mock timing screen showing gap, tyre age, pit window | Drawn graphic | Build it yourself, don't copy the broadcast layout |
| 8:35 | Outro | End card with next video | Drawn graphic | Title card |

## Game recording checklist
1. Record in OBS at 1080p, 60 fps.
2. Pick a track and tyre setting where wear is noticeable, so the undercut visibly works.
3. Shorten the race and make a save point right before the pit window, so you can retry.
4. Capture several takes of each moment (pit entry, out-lap, rejoin) and pick the cleanest.
5. Show the tyre-wear and gap displays on screen so the viewer can follow the numbers.
6. Check EA's content-creator policy before monetizing gameplay.

## FastF1 animation tips
- Use position data from one real race for the map. Check that your FastF1 version supports the method you call.
- Export with ffmpeg through matplotlib's animation writer, then drop the MP4 into Kdenlive.
- Keep the same colors for the two cars throughout the video so viewers track them easily.

## Time estimate
About 6-8 hours: 2 hours recording the game, 2-3 hours building the FastF1 animations and charts, 1-2 hours on graphics, then editing.
