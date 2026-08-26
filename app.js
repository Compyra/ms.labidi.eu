/* App shell: palette wiring, routing (?go=, ?q=, #q=, #/s/), result rendering. */
(function () {
  "use strict";
  var HUB = window.MSHUB;
  var input, host, listbox, countEl, statusEl;
  var results = [];
  var active = -1;
  var SUBJECTS = [
    ["entra", "Entra ID"], ["intune", "Intune"], ["defender", "Defender XDR"],
    ["sentinel", "Sentinel"], ["azure", "Azure"], ["m365", "Microsoft 365"],
    ["purview", "Purview"], ["power", "Power Platform"], ["windows", "Windows Cloud"],
    ["automation", "Automation"], ["licensing", "Licensing"], ["msp", "MSP"],
    ["toolbox", "Toolbox"], ["mypages", "My Pages"]
  ];
  var SUBJ_NAME = {};
  SUBJECTS.forEach(function (s) { SUBJ_NAME[s[0]] = s[1]; });
  var KIND_LABEL = { portal: "Portals", setting: "Settings", tool: "Tools",
    docs: "Docs", enduser: "End-user", concept: "Concepts" };
  var GKEYS = { e: "entra", i: "intune", d: "defender", s: "sentinel", a: "azure",
    m: "m365", p: "purview", o: "power", w: "windows", u: "automation",
    l: "licensing", x: "msp", t: "toolbox", y: "mypages" };
  var gPending = false;

  function pref(key, val) {
    try {
      if (val === undefined) { return localStorage.getItem(key); }
      if (val === null) { localStorage.removeItem(key); }
      else { localStorage.setItem(key, val); }
    } catch (e) { return null; }
    return val;
  }

  function urlFor(rec) {
    var cloud = pref("mshub-cloud");
    if (cloud && cloud !== "com" && rec.clouds && rec.clouds[cloud]) {
      return rec.clouds[cloud];
    }
    return rec.url || "";
  }

  function getRecents() {
    try { return JSON.parse(pref("mshub-recents") || "[]"); }
    catch (e) { return []; }
  }

  function addRecent(id) {
    var r = getRecents().filter(function (x) { return x !== id; });
    r.unshift(id);
    pref("mshub-recents", JSON.stringify(r.slice(0, 8)));
  }

  function getLic() {
    try { return JSON.parse(pref("mshub-lic") || "[]"); }
    catch (e) { return []; }
  }

  function setLic(arr) {
    pref("mshub-lic", JSON.stringify(arr));
    HUB.setLicenseProfile(arr);
  }

  function roleName(id) {
    var reg = (HUB.registry && HUB.registry.roles) || {};
    return reg[id] || id;
  }

  function licName(id) {
    var reg = (HUB.registry && HUB.registry.licenses) || {};
    return (reg[id] && reg[id].n) || id;
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function safeDecode(s) {
    try { return decodeURIComponent(s); } catch (e) { return s; }
  }

  function openUrl(url) {
    window.open(url, "_blank", "noopener,noreferrer");
  }

  function copyText(text, node) {
    navigator.clipboard.writeText(text).then(function () {
      node.classList.add("copied");
      setTimeout(function () { node.classList.remove("copied"); }, 1200);
    }).catch(function () {
      window.prompt("Copy manually:", text);
    });
  }

  function clearAria() {
    input.setAttribute("aria-expanded", "false");
    input.removeAttribute("aria-activedescendant");
    input.removeAttribute("aria-controls");
  }

  function renderHome() {
    host.innerHTML = "";
    listbox = null;
    results = [];
    clearAria();
    document.title = "ms.labidi.eu - the Microsoft admin command line";
    var counts = (HUB.meta && HUB.meta.counts) || {};
    var grid = document.createElement("div");
    grid.className = "tiles";
    SUBJECTS.forEach(function (s) {
      var a = document.createElement("a");
      a.className = "tile";
      a.href = "#/s/" + s[0];
      a.innerHTML = "<span class=\"tile-name\">" + esc(s[1]) + "</span>" +
        "<span class=\"tile-count\">" + (counts[s[0]] || 0) + "</span>";
      grid.appendChild(a);
    });
    host.appendChild(grid);
    var libs = [["#/kql", "KQL library", (HUB.kql || []).length],
                ["#/ps", "PowerShell library", (HUB.ps || []).length],
                ["#/runbooks", "Runbooks", (HUB.runbooks || []).length],
                ["#/licensing", "License matrix", (HUB.licensing || []).length],
                ["#/tables", "KQL tables",
                 ((HUB.registry && HUB.registry.tables) || []).length]];
    var libGrid = document.createElement("div");
    libGrid.className = "tiles libtiles";
    libs.forEach(function (l) {
      if (!l[2]) { return; }
      var a = document.createElement("a");
      a.className = "tile";
      a.href = l[0];
      a.innerHTML = "<span class=\"tile-name\">" + esc(l[1]) + "</span>" +
        "<span class=\"tile-count\">" + l[2] + "</span>";
      libGrid.appendChild(a);
    });
    if (libGrid.children.length) { host.appendChild(libGrid); }
    var recents = getRecents().map(HUB.getById).filter(Boolean);
    if (recents.length) {
      var head = document.createElement("div");
      head.className = "sechead";
      head.innerHTML = "<h2>Recently used</h2>" +
        "<button class=\"chip\" id=\"clear-recents\">clear</button>";
      host.appendChild(head);
      var ul = document.createElement("ul");
      ul.className = "rlist";
      recents.forEach(function (rec) { ul.appendChild(makeRow(rec)); });
      host.appendChild(ul);
      head.querySelector("#clear-recents").addEventListener("click", function () {
        pref("mshub-recents", null);
        renderHome();
      });
    }
    statusEl.textContent = "Type to search " + ((HUB.meta && HUB.meta.records) || 0) +
      " commands. Press / to focus, ? for help.";
  }

  function badgeHtml(rec) {
    var out = "";
    if (rec.kind && rec.kind !== "portal") {
      out += "<span class=\"badge kind\">" + esc(rec.kind) + "</span>";
    }
    if (rec.deprecated) { out += "<span class=\"badge dep\">deprecated</span>"; }
    if (rec.level) { out += "<span class=\"badge lvl\">" + esc(rec.level) + "</span>"; }
    if (rec.blastRadius === "high") {
      out += "<span class=\"badge blast-high\" title=\"High blast radius: not on a Friday\">high blast</span>";
    }
    if (HUB.coveredByProfile && HUB.coveredByProfile(rec.license) ||
        (rec.kind === "lic" && HUB.licCovered && HUB.licCovered(rec))) {
      out += "<span class=\"badge inc\" title=\"Included in your license profile\">included</span>";
    }
    if (rec.source === "cmdms") { out += "<span class=\"badge src\">cmd.ms</span>"; }
    return out;
  }

  function cloudChips(rec) {
    if (!rec.clouds) { return ""; }
    return Object.keys(rec.clouds).map(function (c) {
      return "<button class=\"chip cloud\" data-cloud=\"" + esc(c) + "\" " +
        "title=\"Open " + esc(c.toUpperCase()) + " variant\">" +
        esc(c) + "</button>";
    }).join("");
  }

  function makeRow(rec, asOption) {
    var li = document.createElement("li");
    li.className = "row";
    if (asOption) {
      li.setAttribute("role", "option");
      li.setAttribute("aria-selected", "false");
    }
    var isLib = !!rec.code;
    var crumb = rec.category + (rec.group ? " > " + rec.group : "") +
      (isLib ? " > " + (rec.table || rec.module || "") : "");
    li.innerHTML =
      "<span class=\"rid\">" + esc(rec.id) + "</span>" +
      "<span class=\"rname\">" + esc(rec.name) +
      (rec.desc ? " <span class=\"rdesc\">" + esc(rec.desc) + "</span>" : "") +
      "</span>" +
      "<span class=\"rcrumb\">" + esc(crumb) + "</span>" +
      "<span class=\"rbadges\">" + badgeHtml(rec) + cloudChips(rec) +
      "<button class=\"chip copy\" title=\"" +
      (isLib ? "Copy code" : "Copy URL") + "\">copy</button>" +
      (rec.url ? "<a class=\"chip open\" target=\"_blank\" rel=\"noopener noreferrer\" href=\"" +
        esc(urlFor(rec)) + "\">open</a>" : "") +
      "</span>";
    li.addEventListener("click", function (ev) {
      var t = ev.target;
      if (t.classList.contains("copy")) {
        copyText(isLib ? rec.code :
          (urlFor(rec) || "https://ms.labidi.eu/?go=" + rec.id), t);
      } else if (t.classList.contains("cloud")) {
        openUrl(rec.clouds[t.getAttribute("data-cloud")]);
      } else if (!t.classList.contains("open")) {
        location.hash = "#/c/" + rec.id;
      }
    });
    return li;
  }

  function renderResults(query) {
    results = HUB.search(query);
    active = -1;
    host.innerHTML = "";
    listbox = document.createElement("ul");
    listbox.className = "rlist";
    listbox.id = "listbox";
    listbox.setAttribute("role", "listbox");
    input.setAttribute("aria-expanded", "true");
    input.setAttribute("aria-controls", "listbox");
    input.removeAttribute("aria-activedescendant");
    statusEl.textContent = results.length + " hit" + (results.length === 1 ? "" : "s") +
      (results.length ? ". Enter opens the card, Ctrl+Enter the portal." : "");
    var frag = document.createDocumentFragment();
    results.forEach(function (r, i) {
      var li = makeRow(r.rec, true);
      li.id = "opt-" + i;
      frag.appendChild(li);
    });
    listbox.appendChild(frag);
    host.appendChild(listbox);
  }

  function renderHub(slug) {
    var name = SUBJ_NAME[slug];
    if (!name) { renderHome(); return; }
    results = [];
    listbox = null;
    input.value = "";
    clearAria();
    host.innerHTML = "";
    document.title = name + " | ms.labidi.eu";
    var recs = HUB.commands.filter(function (r) { return r.category === slug; });
    statusEl.textContent = name + ": " + recs.length +
      " record" + (recs.length === 1 ? "" : "s");
    if (!recs.length) {
      var p = document.createElement("p");
      p.className = "note";
      p.textContent = "No records here yet: this hub fills with the enrichment pass " +
        "(roadmap phase 3).";
      host.appendChild(p);
      return;
    }
    var groups = {};
    recs.forEach(function (r) {
      var g = r.group || KIND_LABEL[r.kind] || "Other";
      (groups[g] = groups[g] || []).push(r);
    });
    Object.keys(groups).sort().forEach(function (g) {
      var h2 = document.createElement("h2");
      h2.className = "gname";
      h2.textContent = g;
      host.appendChild(h2);
      var ul = document.createElement("ul");
      ul.className = "rlist";
      groups[g].sort(function (a, b) { return a.name.localeCompare(b.name); })
        .forEach(function (rec) { ul.appendChild(makeRow(rec)); });
      host.appendChild(ul);
    });
  }

  function renderCard(id) {
    var rec = HUB.getById((id || "").toLowerCase());
    if (!rec) { input.value = id; onInput(); return; }
    if (rec.kind === "runbook") { renderRunbookCard(rec); return; }
    if (rec.kind === "lic") { renderLicCard(rec); return; }
    if (rec.code) { renderLibraryCard(rec); return; }
    results = [];
    listbox = null;
    clearAria();
    host.innerHTML = "";
    addRecent(rec.id);
    document.title = rec.id + " - " + rec.name + " | ms.labidi.eu";
    statusEl.textContent = "";
    var card = document.createElement("article");
    card.className = "card";
    var subj = SUBJ_NAME[rec.category] || rec.category;
    var h = "<header class=\"card-head\"><span class=\"rid\">" + esc(rec.id) +
      "</span><h1>" + esc(rec.name) + "</h1>" + badgeHtml(rec) + "</header>";
    if (rec.deprecated) {
      var succ = rec.related && rec.related[0];
      h += "<p class=\"warnline\">Deprecated." + (succ ? " Use <a href=\"#/c/" +
        esc(succ) + "\">" + esc(succ) + "</a> instead." : "") + "</p>";
    }
    h += "<dl class=\"meta\">";
    h += "<dt>Subject</dt><dd><a href=\"#/s/" + esc(rec.category) + "\">" + esc(subj) +
      "</a>" + (rec.group ? " &gt; " + esc(rec.group) : "") + "</dd>";
    if (rec.aliases && rec.aliases.length) {
      h += "<dt>Aliases</dt><dd>" + rec.aliases.map(esc).join(", ") + "</dd>";
    }
    if (rec.path) { h += "<dt>Path</dt><dd>" + esc(rec.path) + "</dd>"; }
    if (rec.desc) { h += "<dt>About</dt><dd>" + esc(rec.desc) + "</dd>"; }
    if (rec.blastRadius) {
      h += "<dt>Blast radius</dt><dd><span class=\"badge blast-" + esc(rec.blastRadius) +
        "\">" + esc(rec.blastRadius) + "</span>" +
        (rec.blastRadius === "high" ? " change windows only; test tenant first" : "") +
        "</dd>";
    }
    if (rec.standards) {
      h += "<dt>Standards</dt><dd>" + rec.standards.map(esc).join(", ") + "</dd>";
    }
    if (rec.roles) {
      h += "<dt>Role</dt><dd>" + rec.roles.map(function (r) {
        return esc(roleName(r));
      }).join(", ") + "</dd>";
    }
    if (rec.license) {
      h += "<dt>License</dt><dd>" + esc(licName(rec.license)) +
        (HUB.coveredByProfile(rec.license) ? " <span class=\"badge inc\">in your profile</span>" : "") +
        "</dd>";
    }
    if (rec.shareText) { h += "<dt>Share</dt><dd>" + esc(rec.shareText) + "</dd>"; }
    if (rec.ps) {
      var psVal = /^(ps|kql)-[a-z0-9-]+$/.test(rec.ps)
        ? "<a href=\"#/c/" + esc(rec.ps) + "\"><code>" + esc(rec.ps) + "</code></a>"
        : "<code>" + esc(rec.ps) + "</code>";
      h += "<dt>PowerShell</dt><dd>" + psVal + "</dd>";
    }
    if (rec.docs) {
      h += "<dt>Docs</dt><dd><a href=\"" + esc(rec.docs) +
        "\" target=\"_blank\" rel=\"noopener noreferrer\">" + esc(rec.docs) + "</a></dd>";
    }
    if (rec.verified) { h += "<dt>Verified</dt><dd>" + esc(rec.verified) + "</dd>"; }
    h += "<dt>Source</dt><dd>" +
      (rec.source === "cmdms" ? "cmd.ms (MIT)" : "ms.labidi.eu") + "</dd></dl>";
    card.innerHTML = h;
    var actions = document.createElement("div");
    actions.className = "actions";
    if (rec.url) {
      var openA = document.createElement("a");
      openA.className = "btn";
      openA.target = "_blank";
      openA.rel = "noopener noreferrer";
      openA.href = urlFor(rec);
      openA.textContent = "Open portal";
      actions.appendChild(openA);
    }
    Object.keys(rec.clouds || {}).forEach(function (c) {
      var a = document.createElement("a");
      a.className = "btn ghost";
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      a.href = rec.clouds[c];
      a.textContent = "Open " + c.toUpperCase();
      actions.appendChild(a);
    });
    [["Copy URL", function () { return urlFor(rec); }],
     ["Copy id", function () { return rec.id; }],
     ["Copy go-link", function () { return "https://ms.labidi.eu/?go=" + rec.id; }]]
      .forEach(function (pair) {
        if (pair[0] === "Copy URL" && !rec.url) { return; }
        var b = document.createElement("button");
        b.className = "btn ghost";
        b.textContent = pair[0];
        b.addEventListener("click", function () { copyText(pair[1](), b); });
        actions.appendChild(b);
      });
    card.appendChild(actions);
    if (rec.related && rec.related.length) {
      var rel = document.createElement("p");
      rel.className = "related";
      rel.innerHTML = "Related: " + rec.related.map(function (r) {
        return "<a href=\"#/c/" + esc(r) + "\">" + esc(r) + "</a>";
      }).join(", ");
      card.appendChild(rel);
    }
    var snippets = HUB.libraryFor ? HUB.libraryFor(rec.id) : [];
    if (snippets.length) {
      var lib = document.createElement("div");
      lib.className = "cardlib";
      lib.innerHTML = "<h2 class=\"gname\">Queries &amp; snippets</h2>";
      var ul = document.createElement("ul");
      ul.className = "rlist";
      snippets.forEach(function (entry) { ul.appendChild(makeRow(entry)); });
      lib.appendChild(ul);
      card.appendChild(lib);
    }
    var books = HUB.runbooksFor ? HUB.runbooksFor(rec.id) : [];
    if (books.length) {
      var rbl = document.createElement("div");
      rbl.className = "cardlib cardrbs";
      rbl.innerHTML = "<h2 class=\"gname\">Runbooks</h2>";
      var rul = document.createElement("ul");
      rul.className = "rlist";
      books.forEach(function (entry) { rul.appendChild(makeRow(entry)); });
      rbl.appendChild(rul);
      card.appendChild(rbl);
    }
    host.appendChild(card);
  }

  function renderLibraryCard(rec) {
    results = [];
    listbox = null;
    clearAria();
    host.innerHTML = "";
    addRecent(rec.id);
    document.title = rec.id + " - " + rec.name + " | ms.labidi.eu";
    statusEl.textContent = "";
    var card = document.createElement("article");
    card.className = "card";
    var langLabel = rec.kind === "kql" ? "KQL" : "PowerShell";
    var h = "<header class=\"card-head\"><span class=\"rid\">" + esc(rec.id) +
      "</span><h1>" + esc(rec.name) + "</h1>" +
      "<span class=\"badge kind\">" + esc(langLabel) + "</span></header>";
    h += "<dl class=\"meta\">";
    h += "<dt>Subject</dt><dd><a href=\"#/s/" + esc(rec.category) + "\">" +
      esc(SUBJ_NAME[rec.category] || rec.category) + "</a></dd>";
    if (rec.table) {
      h += "<dt>Table</dt><dd><a href=\"#/tables\">" + esc(rec.table) + "</a></dd>";
    }
    if (rec.module) { h += "<dt>Module</dt><dd>" + esc(rec.module) + "</dd>"; }
    if (rec.scopes) { h += "<dt>Needs</dt><dd>" + esc(rec.scopes) + "</dd>"; }
    if (rec.tags) { h += "<dt>Tags</dt><dd>" + rec.tags.map(esc).join(", ") + "</dd>"; }
    if (rec.docs) {
      h += "<dt>Docs</dt><dd><a href=\"" + esc(rec.docs) +
        "\" target=\"_blank\" rel=\"noopener noreferrer\">" + esc(rec.docs) + "</a></dd>";
    }
    if (rec.verified) { h += "<dt>Verified</dt><dd>" + esc(rec.verified) + "</dd>"; }
    h += "</dl><pre class=\"code\"><code>" + esc(rec.code) + "</code></pre>";
    card.innerHTML = h;
    var actions = document.createElement("div");
    actions.className = "actions";
    var copyBtn = document.createElement("button");
    copyBtn.className = "btn";
    copyBtn.textContent = "Copy " + langLabel;
    copyBtn.addEventListener("click", function () { copyText(rec.code, copyBtn); });
    actions.appendChild(copyBtn);
    var linkBtn = document.createElement("button");
    linkBtn.className = "btn ghost";
    linkBtn.textContent = "Copy go-link";
    linkBtn.addEventListener("click", function () {
      copyText("https://ms.labidi.eu/#/c/" + rec.id, linkBtn);
    });
    actions.appendChild(linkBtn);
    card.appendChild(actions);
    if (rec.related && rec.related.length) {
      var rel = document.createElement("p");
      rel.className = "related";
      rel.innerHTML = "Used with: " + rec.related.map(function (r) {
        return "<a href=\"#/c/" + esc(r) + "\">" + esc(r) + "</a>";
      }).join(", ");
      card.appendChild(rel);
    }
    host.appendChild(card);
  }

  var LEVEL_LABEL = { L1: "L1 (service desk)", L2: "L2 (escalation)", L3: "L3 (expert)" };

  function rbSection(label, items, ordered) {
    if (!items || !items.length) { return ""; }
    var tag = ordered ? "ol" : "ul";
    return "<h2 class=\"gname\">" + esc(label) + "</h2><" + tag + " class=\"rbsec\">" +
      items.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") +
      "</" + tag + ">";
  }

  function renderRunbookCard(rec) {
    results = [];
    listbox = null;
    clearAria();
    host.innerHTML = "";
    addRecent(rec.id);
    document.title = rec.id + " - " + rec.name + " | ms.labidi.eu";
    statusEl.textContent = "";
    var card = document.createElement("article");
    card.className = "card runbook";
    var h = "<header class=\"card-head\"><span class=\"rid\">" + esc(rec.id) +
      "</span><h1>" + esc(rec.name) + "</h1>" +
      "<span class=\"badge lvl\">" + esc(rec.level) + "</span>" +
      "<span class=\"badge kind\">runbook</span></header>";
    h += "<dl class=\"meta\">";
    h += "<dt>Subject</dt><dd><a href=\"#/s/" + esc(rec.category) + "\">" +
      esc(SUBJ_NAME[rec.category] || rec.category) + "</a></dd>";
    h += "<dt>Level</dt><dd>" + esc(LEVEL_LABEL[rec.level] || rec.level) + "</dd>";
    if (rec.tags) { h += "<dt>Tags</dt><dd>" + rec.tags.map(esc).join(", ") + "</dd>"; }
    if (rec.verified) { h += "<dt>Verified</dt><dd>" + esc(rec.verified) + "</dd>"; }
    h += "</dl>";
    h += rbSection("Preconditions", rec.pre, false);
    h += rbSection("Steps", rec.steps, true);
    h += rbSection("Verify", rec.verify, false);
    h += rbSection("Rollback", rec.rollback, false);
    h += rbSection("Escalate when", rec.escalate, false);
    card.innerHTML = h;
    var actions = document.createElement("div");
    actions.className = "actions";
    var copyBtn = document.createElement("button");
    copyBtn.className = "btn";
    copyBtn.textContent = "Copy steps";
    copyBtn.addEventListener("click", function () {
      var text = rec.name + "\n" + (rec.steps || []).map(function (s, i) {
        return (i + 1) + ". " + s;
      }).join("\n");
      copyText(text, copyBtn);
    });
    actions.appendChild(copyBtn);
    var linkBtn = document.createElement("button");
    linkBtn.className = "btn ghost";
    linkBtn.textContent = "Copy go-link";
    linkBtn.addEventListener("click", function () {
      copyText("https://ms.labidi.eu/#/c/" + rec.id, linkBtn);
    });
    actions.appendChild(linkBtn);
    card.appendChild(actions);
    if (rec.related && rec.related.length) {
      var rel = document.createElement("p");
      rel.className = "related";
      rel.innerHTML = "Works with: " + rec.related.map(function (r) {
        return "<a href=\"#/c/" + esc(r) + "\">" + esc(r) + "</a>";
      }).join(", ");
      card.appendChild(rel);
    }
    host.appendChild(card);
  }

  function renderLicCard(rec) {
    results = [];
    listbox = null;
    clearAria();
    host.innerHTML = "";
    addRecent(rec.id);
    document.title = rec.id + " - " + rec.name + " | ms.labidi.eu";
    statusEl.textContent = "";
    var card = document.createElement("article");
    card.className = "card";
    var h = "<header class=\"card-head\"><span class=\"rid\">" + esc(rec.id) +
      "</span><h1>" + esc(rec.name) + "</h1>" + badgeHtml(rec) + "</header>";
    h += "<dl class=\"meta\">";
    h += "<dt>Subject</dt><dd><a href=\"#/s/" + esc(rec.category) + "\">" +
      esc(SUBJ_NAME[rec.category] || rec.category) + "</a></dd>";
    h += "<dt>Minimum</dt><dd>" + esc(licName(rec.min)) +
      (HUB.coveredByProfile(rec.min) ? " <span class=\"badge inc\">in your profile</span>" : "") +
      "</dd>";
    if (rec.alsoIn && rec.alsoIn.length) {
      h += "<dt>Also in</dt><dd>" + rec.alsoIn.map(function (x) {
        return esc(licName(x)) +
          (HUB.coveredByProfile(x) ? " <span class=\"badge inc\">yours</span>" : "");
      }).join(", ") + "</dd>";
    }
    if (rec.notes) { h += "<dt>Notes</dt><dd>" + esc(rec.notes) + "</dd>"; }
    if (rec.docs) {
      h += "<dt>Docs</dt><dd><a href=\"" + esc(rec.docs) +
        "\" target=\"_blank\" rel=\"noopener noreferrer\">" + esc(rec.docs) + "</a></dd>";
    }
    if (rec.verified) { h += "<dt>Verified</dt><dd>" + esc(rec.verified) + "</dd>"; }
    h += "</dl>";
    card.innerHTML = h;
    var actions = document.createElement("div");
    actions.className = "actions";
    var matrixA = document.createElement("a");
    matrixA.className = "btn";
    matrixA.href = "#/licensing";
    matrixA.textContent = "Full matrix";
    actions.appendChild(matrixA);
    var linkBtn = document.createElement("button");
    linkBtn.className = "btn ghost";
    linkBtn.textContent = "Copy go-link";
    linkBtn.addEventListener("click", function () {
      copyText("https://ms.labidi.eu/?go=" + rec.id, linkBtn);
    });
    actions.appendChild(linkBtn);
    card.appendChild(actions);
    if (rec.related && rec.related.length) {
      var rel = document.createElement("p");
      rel.className = "related";
      rel.innerHTML = "Related: " + rec.related.map(function (r) {
        return "<a href=\"#/c/" + esc(r) + "\">" + esc(r) + "</a>";
      }).join(", ");
      card.appendChild(rel);
    }
    host.appendChild(card);
  }

  function renderLicensing() {
    var rows = HUB.licensing || [];
    results = [];
    listbox = null;
    input.value = "";
    clearAria();
    host.innerHTML = "";
    document.title = "License matrix | ms.labidi.eu";
    statusEl.textContent = "License matrix: " + rows.length + " features mapped to " +
      "their minimum license. Tick your SKUs under help (?) to highlight what you own.";
    var groups = {};
    rows.forEach(function (entry) {
      var g = SUBJ_NAME[entry.subject] || entry.subject || "Other";
      (groups[g] = groups[g] || []).push(entry);
    });
    Object.keys(groups).sort().forEach(function (g) {
      var h2 = document.createElement("h2");
      h2.className = "gname";
      h2.textContent = g;
      host.appendChild(h2);
      var body = groups[g].sort(function (a, b) {
        return a.name.localeCompare(b.name);
      }).map(function (r) {
        var owned = HUB.licCovered(r);
        return "<tr" + (owned ? " class=\"owned\"" : "") + ">" +
          "<td><a href=\"#/c/" + esc(r.id) + "\">" + esc(r.name) + "</a></td>" +
          "<td>" + esc(licName(r.min)) +
          (owned ? " <span class=\"badge inc\">yours</span>" : "") + "</td>" +
          "<td class=\"colnotes\">" + (r.alsoIn || []).map(function (x) {
            return esc(licName(x));
          }).join(", ") + "</td>" +
          "</tr>";
      }).join("");
      var wrap = document.createElement("div");
      wrap.className = "tblwrap";
      wrap.innerHTML = "<table class=\"tbl\"><thead><tr><th>Feature</th>" +
        "<th>Minimum</th><th class=\"colnotes\">Also in</th></tr></thead><tbody>" +
        body + "</tbody></table>";
      host.appendChild(wrap);
    });
  }

  function renderRunbooks() {
    var rows = HUB.runbooks || [];
    results = [];
    listbox = null;
    input.value = "";
    clearAria();
    host.innerHTML = "";
    document.title = "Runbooks | ms.labidi.eu";
    statusEl.textContent = "Runbooks: " + rows.length + " step-by-step procedures. " +
      "L1 service desk, L2 escalation, L3 expert.";
    var groups = {};
    rows.forEach(function (entry) {
      var g = SUBJ_NAME[entry.subject] || entry.subject || "Other";
      (groups[g] = groups[g] || []).push(entry);
    });
    Object.keys(groups).sort().forEach(function (g) {
      var h2 = document.createElement("h2");
      h2.className = "gname";
      h2.textContent = g;
      host.appendChild(h2);
      var ul = document.createElement("ul");
      ul.className = "rlist";
      groups[g].sort(function (a, b) { return a.name.localeCompare(b.name); })
        .forEach(function (entry) { ul.appendChild(makeRow(entry)); });
      host.appendChild(ul);
    });
  }

  function renderLibrary(kind) {
    var rows = (kind === "kql" ? HUB.kql : HUB.ps) || [];
    results = [];
    listbox = null;
    input.value = "";
    clearAria();
    host.innerHTML = "";
    var label = kind === "kql" ? "KQL library" : "PowerShell library";
    document.title = label + " | ms.labidi.eu";
    statusEl.textContent = label + ": " + rows.length + " entries. " +
      "Click a row for the full card, or copy straight from the list.";
    var groups = {};
    rows.forEach(function (entry) {
      var g = SUBJ_NAME[entry.subject] || entry.subject || "Other";
      (groups[g] = groups[g] || []).push(entry);
    });
    Object.keys(groups).sort().forEach(function (g) {
      var h2 = document.createElement("h2");
      h2.className = "gname";
      h2.textContent = g;
      host.appendChild(h2);
      var ul = document.createElement("ul");
      ul.className = "rlist";
      groups[g].sort(function (a, b) { return a.name.localeCompare(b.name); })
        .forEach(function (entry) { ul.appendChild(makeRow(entry)); });
      host.appendChild(ul);
    });
  }

  function renderTables() {
    var tables = (HUB.registry && HUB.registry.tables) || [];
    results = [];
    listbox = null;
    input.value = "";
    clearAria();
    host.innerHTML = "";
    document.title = "KQL tables | ms.labidi.eu";
    statusEl.textContent = "Table registry: " + tables.length + " tables.";
    var counts = {};
    (HUB.kql || []).forEach(function (q) {
      counts[q.table] = (counts[q.table] || 0) + 1;
    });
    var rowsHtml = tables.map(function (t) {
      var n = counts[t.name] || 0;
      return "<tr><td><code>" + esc(t.name) + "</code></td><td>" + esc(t.product) +
        "</td><td>" + esc(t.costTier) + "</td><td class=\"colnotes\">" + esc(t.notes) +
        "</td><td>" +
        (n ? "<a href=\"#q=" + encodeURIComponent(t.name) + "\">" + n + "</a>" : "") +
        "</td></tr>";
    }).join("");
    host.innerHTML = "<div class=\"tblwrap\"><table class=\"tbl\"><thead><tr>" +
      "<th>Table</th><th>Product</th><th>Cost tier</th>" +
      "<th class=\"colnotes\">Notes</th><th>Queries</th></tr></thead><tbody>" +
      rowsHtml + "</tbody></table></div>";
  }

  function renderAbout() {
    results = [];
    listbox = null;
    clearAria();
    host.innerHTML = "";
    document.title = "Help | ms.labidi.eu";
    statusEl.textContent = "";
    host.innerHTML =
      "<article class=\"card about\">" +
      "<h1>Help</h1>" +
      "<h2>Keyboard</h2>" +
      "<table class=\"kbdtab\"><tbody>" +
      "<tr><td><kbd>/</kbd> or <kbd>Ctrl</kbd>+<kbd>K</kbd></td><td>focus search</td></tr>" +
      "<tr><td><kbd>&uarr;</kbd> <kbd>&darr;</kbd></td><td>move through results</td></tr>" +
      "<tr><td><kbd>Enter</kbd></td><td>open the record card</td></tr>" +
      "<tr><td><kbd>Ctrl</kbd>+<kbd>Enter</kbd></td><td>open the portal directly</td></tr>" +
      "<tr><td><kbd>Shift</kbd>+<kbd>Enter</kbd></td><td>copy the URL, snippet code or share link</td></tr>" +
      "<tr><td><kbd>Esc</kbd></td><td>clear, then leave the search box</td></tr>" +
      "<tr><td><kbd>g</kbd> then a letter</td><td>jump to a hub " +
      "(e entra, i intune, d defender, s sentinel, a azure, m m365, p purview, " +
      "o power, w windows, u automation, l licensing, x msp, t toolbox, y my pages)</td></tr>" +
      "<tr><td><kbd>t</kbd></td><td>cycle theme auto/dark/light</td></tr>" +
      "<tr><td><kbd>?</kbd></td><td>this page</td></tr>" +
      "</tbody></table>" +
      "<h2>Address-bar keyword</h2>" +
      "<p>Add a custom search engine with URL " +
      "<code>https://ms.labidi.eu/?q=%s</code> (results) or " +
      "<code>https://ms.labidi.eu/?go=%s</code> (instant jump), keyword <code>ms</code>. " +
      "Chrome/Edge: Settings &gt; Search engine &gt; Manage. Firefox: bookmark with " +
      "keyword. This site also ships OpenSearch, so browsers can discover it.</p>" +
      "<h2>Filters</h2>" +
      "<p><code>cat:sentinel</code> limits to a subject, <code>kind:tool</code> to a " +
      "record kind, <code>role:caadmin</code> to a required role. Acronyms work: try " +
      "<code>air</code>, <code>gdap</code>, <code>prt</code>.</p>" +
      "<h2>Libraries</h2>" +
      "<p><a href=\"#/kql\">KQL library</a> and <a href=\"#/ps\">PowerShell library</a> " +
      "are searchable alongside portals (<code>kind:kql</code>, <code>kind:ps</code>); " +
      "every entry carries its table or module plus the role it needs. The " +
      "<a href=\"#/tables\">table registry</a> lists what each KQL table holds. " +
      "<a href=\"#/runbooks\">Runbooks</a> (<code>kind:runbook</code>) are step-by-step " +
      "procedures with verify, rollback and escalation guidance built in. The " +
      "<a href=\"#/licensing\">license matrix</a> (<code>kind:lic</code>) maps features " +
      "to their minimum license and highlights what your profile already covers.</p>" +
      "<h2>Cloud environments</h2>" +
      "<p>The cloud selector rewrites Open links to your environment (GCC, GCC High, " +
      "DoD) where a variant exists; commercial stays the fallback.</p>" +
      "<h2>Attribution</h2>" +
      "<p>Shortcut data includes <a href=\"https://cmd.ms/\" target=\"_blank\" " +
      "rel=\"noopener noreferrer\">cmd.ms</a> by Merill Fernando &amp; contributors " +
      "(MIT). This site is not affiliated with Microsoft.</p>" +
      "<h2>My licenses</h2>" +
      "<p>Tick what your tenant owns; records covered by those SKUs (directly or via " +
      "bundles) get an <span class=\"badge inc\">included</span> badge and a small " +
      "ranking nudge. Stored locally only.</p>" +
      "<div class=\"licgrid\" id=\"licgrid\"></div>" +
      "</article>";
    var reg = (HUB.registry && HUB.registry.licenses) || {};
    var prof = getLic();
    var grid = document.getElementById("licgrid");
    grid.innerHTML = Object.keys(reg).map(function (id) {
      return "<label class=\"licbox\"><input type=\"checkbox\" data-lic=\"" + esc(id) +
        "\"" + (prof.indexOf(id) >= 0 ? " checked" : "") + "> " +
        esc(reg[id].n) + "</label>";
    }).join("");
    grid.addEventListener("change", function (ev) {
      var cb = ev.target;
      if (!cb.getAttribute || !cb.getAttribute("data-lic")) { return; }
      var id = cb.getAttribute("data-lic");
      var p = getLic().filter(function (x) { return x !== id; });
      if (cb.checked) { p.push(id); }
      setLic(p);
    });
  }

  function setActive(i) {
    if (!listbox) { return; }
    var items = listbox.children;
    if (active >= 0 && items[active]) {
      items[active].classList.remove("active");
      items[active].setAttribute("aria-selected", "false");
    }
    active = i;
    if (active >= 0 && items[active]) {
      items[active].classList.add("active");
      items[active].setAttribute("aria-selected", "true");
      items[active].scrollIntoView({ block: "nearest" });
      input.setAttribute("aria-activedescendant", items[active].id);
    } else {
      input.removeAttribute("aria-activedescendant");
    }
  }

  function onInput() {
    var q = input.value.trim();
    if (q) {
      renderResults(q);
      history.replaceState(null, "", location.pathname + "#q=" + encodeURIComponent(q));
      document.title = "ms.labidi.eu - the Microsoft admin command line";
    } else {
      history.replaceState(null, "", location.pathname);
      renderHome();
    }
  }

  function onKeydown(ev) {
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      ev.preventDefault();
      if (!results.length) { return; }
      var n = results.length;
      setActive(ev.key === "ArrowDown" ? (active + 1) % n : (active - 1 + n) % n);
    } else if (ev.key === "Enter") {
      var idx = active >= 0 ? active : 0;
      var pick = results[idx];
      if (!pick) { return; }
      ev.preventDefault();
      if (ev.shiftKey) {
        var chip = listbox && listbox.children[idx] &&
          listbox.children[idx].querySelector(".copy");
        copyText(pick.rec.code || urlFor(pick.rec) ||
          "https://ms.labidi.eu/?go=" + pick.rec.id,
          chip || listbox.children[idx]);
      } else if (ev.ctrlKey || ev.metaKey) {
        if (pick.rec.url) { openUrl(urlFor(pick.rec)); }
      } else {
        location.hash = "#/c/" + pick.rec.id;
      }
    } else if (ev.key === "Escape") {
      if (input.value) {
        input.value = "";
        onInput();
      } else {
        input.blur();
      }
    }
  }

  function route() {
    var params = new URLSearchParams(location.search);
    var go = params.get("go");
    if (go) {
      var hit = HUB.resolveGo(go);
      if (hit) {
        var token = go.trim().toLowerCase();
        var url = (hit.rec.aliasClouds && hit.rec.aliasClouds[token]) ?
          hit.url : (urlFor(hit.rec) || hit.url);
        location.replace(url);
        return;
      }
      history.replaceState(null, "", location.pathname);
      var known = HUB.getById(go.trim().toLowerCase());
      if (known) {
        location.hash = "#/c/" + known.id;
        return;
      }
      input.value = go;
      onInput();
      return;
    }
    var q = params.get("q");
    var hash = safeDecode(location.hash || "");
    if (!q && hash.indexOf("#q=") === 0) { q = hash.slice(3); }
    if (q) {
      input.value = q;
      onInput();
      return;
    }
    if (hash.indexOf("#/s/") === 0) { renderHub(hash.slice(4)); return; }
    if (hash.indexOf("#/c/") === 0) { renderCard(hash.slice(4)); return; }
    if (hash === "#/kql") { renderLibrary("kql"); return; }
    if (hash === "#/ps") { renderLibrary("ps"); return; }
    if (hash === "#/runbooks") { renderRunbooks(); return; }
    if (hash === "#/licensing") { renderLicensing(); return; }
    if (hash === "#/tables") { renderTables(); return; }
    if (hash === "#/about") { renderAbout(); return; }
    input.value = "";
    renderHome();
  }

  function applyTheme() {
    var t = pref("mshub-theme") || "auto";
    if (t === "auto") { document.documentElement.removeAttribute("data-theme"); }
    else { document.documentElement.setAttribute("data-theme", t); }
    var btn = document.getElementById("theme-btn");
    if (btn) {
      btn.textContent = t === "auto" ? "\u25D0" : (t === "dark" ? "\u25CF" : "\u25CB");
      btn.setAttribute("aria-label", "Theme: " + t + " (press t to cycle)");
      btn.title = "Theme: " + t;
    }
  }

  function cycleTheme() {
    var order = ["auto", "dark", "light"];
    var cur = pref("mshub-theme") || "auto";
    pref("mshub-theme", order[(order.indexOf(cur) + 1) % 3]);
    applyTheme();
  }

  function init() {
    input = document.getElementById("q");
    host = document.getElementById("results");
    countEl = document.getElementById("count");
    statusEl = document.getElementById("status");
    HUB.buildIndex();
    HUB.setLicenseProfile(getLic());
    var meta = HUB.meta || {};
    countEl.textContent = (meta.records || 0) + " commands";
    var src = document.getElementById("src-note");
    if (src && meta.upstream) {
      src.textContent = "includes cmd.ms data (MIT, commit " +
        String(meta.upstream.commit).slice(0, 7) + ")";
    }
    var cloudSel = document.getElementById("cloud");
    if (cloudSel) {
      cloudSel.value = pref("mshub-cloud") || "com";
      cloudSel.addEventListener("change", function () {
        pref("mshub-cloud", cloudSel.value);
        route();
      });
    }
    var themeBtn = document.getElementById("theme-btn");
    if (themeBtn) { themeBtn.addEventListener("click", cycleTheme); }
    applyTheme();
    input.addEventListener("input", onInput);
    input.addEventListener("keydown", onKeydown);
    document.addEventListener("keydown", function (ev) {
      var el = document.activeElement;
      var typing = el === input ||
        (el && /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
      if ((ev.key === "/" && !typing) ||
          (ev.key.toLowerCase() === "k" && (ev.ctrlKey || ev.metaKey))) {
        ev.preventDefault();
        input.focus();
        input.select();
        gPending = false;
        return;
      }
      if (typing || ev.ctrlKey || ev.metaKey || ev.altKey) { return; }
      if (gPending) {
        gPending = false;
        var slug = GKEYS[ev.key.toLowerCase()];
        if (slug) {
          ev.preventDefault();
          location.hash = "#/s/" + slug;
        }
        return;
      }
      if (ev.key === "g") { gPending = true; return; }
      if (ev.key === "t") { cycleTheme(); return; }
      if (ev.key === "?") { location.hash = "#/about"; }
    });
    window.addEventListener("hashchange", route);
    route();
    input.focus();
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("sw.js", { updateViaCache: "none" })
        .catch(function () {});
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
