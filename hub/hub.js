// Set to the Community invite link once Task 4 creates it; shown in the fallback.
const COMMUNITY_URL = "";

function communityLink(url) {
  return typeof url === "string" && /^https?:\/\//.test(url) ? url : null;
}

// Pure helper: keep only groups with a join link, grouped by town then sport.
function groupByTown(groups) {
  const towns = {};
  for (const g of groups || []) {
    if (!g || !g.join_url || !/^https?:\/\//.test(g.join_url)) continue;
    (towns[g.town] = towns[g.town] || []).push(g);
  }
  return towns;
}

function el(tag, props, children) {
  const e = document.createElement(tag);
  Object.assign(e, props || {});
  for (const c of children || []) e.append(c);
  return e;
}

async function main() {
  const root = document.getElementById("towns");
  let groups = [];
  try {
    const res = await fetch("groups.json", { cache: "no-store" });
    groups = await res.json();
  } catch (_) { /* fall through to the fallback text */ }
  const towns = groupByTown(groups);
  const names = Object.keys(towns).sort();
  if (!names.length) {
    document.getElementById("fallback").hidden = false;
    const link = communityLink(COMMUNITY_URL);
    if (link) {
      const a = document.getElementById("community");
      a.href = link;
      a.hidden = false;
    }
    return;
  }
  for (const town of names) {
    const d = el("details", {}, [el("summary", { textContent: town })]);
    for (const g of towns[town]) {
      d.append(el("a", {
        className: "join", href: g.join_url, rel: "noopener",
        textContent: `${g.sport} · ${g.name} — Join on WhatsApp`,
      }));
    }
    root.append(d);
  }
}

if (typeof module !== "undefined") module.exports = { groupByTown, communityLink };
else main();
