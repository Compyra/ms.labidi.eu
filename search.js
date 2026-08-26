/* Search index + ranking per docs/12 §5. Exposes MSHUB.buildIndex/search/resolveGo. */
(function () {
  "use strict";
  var HUB = window.MSHUB = window.MSHUB || {};
  var byId = Object.create(null);
  var byAlias = Object.create(null);
  var synByTerm = Object.create(null);
  var docs = [];
  var licProfile = [];

  HUB.setLicenseProfile = function (arr) { licProfile = arr || []; };

  HUB.coveredByProfile = function (lic) {
    if (!lic || !licProfile.length) { return false; }
    if (licProfile.indexOf(lic) >= 0) { return true; }
    var reg = (HUB.registry && HUB.registry.licenses) || {};
    for (var i = 0; i < licProfile.length; i++) {
      var e = reg[licProfile[i]];
      if (e && e.inc && e.inc.indexOf(lic) >= 0) { return true; }
    }
    return false;
  };

  HUB.buildIndex = function () {
    docs = [];
    byId = Object.create(null);
    byAlias = Object.create(null);
    synByTerm = Object.create(null);
    (HUB.commands || []).forEach(function (rec) {
      byId[rec.id] = rec;
      (rec.aliases || []).forEach(function (a) { byAlias[a] = rec; });
      var text = [rec.id].concat(rec.aliases || [])
        .concat([rec.name || "", rec.category || "", rec.group || "",
                 rec.desc || "", rec.path || ""])
        .concat(rec.keywords || [])
        .join(" ").toLowerCase();
      docs.push({ rec: rec, text: text, name: (rec.name || "").toLowerCase() });
    });
    (HUB.kql || []).concat(HUB.ps || []).forEach(function (entry) {
      entry.name = entry.title;
      entry.category = entry.subject;
      byId[entry.id] = entry;
      var text = [entry.id, entry.title || "", entry.subject || "", entry.kind || "",
                  entry.table || "", entry.module || "", entry.code || ""]
        .concat(entry.tags || [])
        .join(" ").toLowerCase();
      docs.push({ rec: entry, text: text, name: (entry.title || "").toLowerCase() });
    });
    (HUB.runbooks || []).forEach(function (entry) {
      entry.name = entry.title;
      entry.category = entry.subject;
      byId[entry.id] = entry;
      var text = [entry.id, entry.title || "", entry.subject || "", "runbook",
                  entry.level || ""]
        .concat(entry.tags || []).concat(entry.steps || [])
        .join(" ").toLowerCase();
      docs.push({ rec: entry, text: text, name: (entry.title || "").toLowerCase() });
    });
    (HUB.synonyms || []).forEach(function (s) { synByTerm[s.term] = s; });
  };

  HUB.libraryFor = function (recordId) {
    return (HUB.kql || []).concat(HUB.ps || []).filter(function (entry) {
      return (entry.related || []).indexOf(recordId) >= 0;
    });
  };

  HUB.runbooksFor = function (recordId) {
    return (HUB.runbooks || []).filter(function (entry) {
      return (entry.related || []).indexOf(recordId) >= 0;
    });
  };

  HUB.resolveGo = function (token) {
    token = (token || "").trim().toLowerCase();
    if (!token) { return null; }
    var rec = byId[token] || byAlias[token];
    if (!rec || !rec.url) { return null; }
    var url = rec.url;
    var cloud = rec.aliasClouds && rec.aliasClouds[token];
    if (cloud && rec.clouds && rec.clouds[cloud]) { url = rec.clouds[cloud]; }
    return { url: url, rec: rec };
  };

  HUB.getById = function (id) { return byId[id] || null; };

  function tokenMatches(token, doc) {
    if (doc.text.indexOf(token) >= 0) { return true; }
    var syn = synByTerm[token];
    if (!syn) { return false; }
    var words = syn.expandsTo.split(/\s+/).filter(function (w) {
      return w.length > 3;
    });
    return words.length > 0 && words.every(function (w) {
      return doc.text.indexOf(w) >= 0;
    });
  }

  function isSubsequence(needle, hay) {
    var i = 0;
    for (var j = 0; j < hay.length && i < needle.length; j++) {
      if (hay[j] === needle[i]) { i++; }
    }
    return i === needle.length;
  }

  HUB.search = function (query) {
    query = (query || "").trim().toLowerCase();
    if (!query) { return []; }
    var filters = {};
    var tokens = [];
    query.split(/\s+/).forEach(function (t) {
      var m = /^(cat|kind|role):([a-z0-9-]+)$/.exec(t);
      if (m) { filters[m[1]] = m[2]; } else if (t) { tokens.push(t); }
    });
    var joined = tokens.join(" ");
    var tokenBoost = tokens.map(function (t) {
      var syn = synByTerm[t];
      if (!syn || !syn.boostIds || !syn.boostIds.length) { return null; }
      var set = Object.create(null);
      syn.boostIds.forEach(function (id) { set[id] = true; });
      return set;
    });
    var out = [];
    docs.forEach(function (d) {
      var rec = d.rec;
      if (filters.cat && rec.category !== filters.cat) { return; }
      if (filters.kind && rec.kind !== filters.kind) { return; }
      if (filters.role && (!rec.roles || rec.roles.indexOf(filters.role) < 0)) { return; }
      var score = 0;
      if (joined && rec.id === joined) {
        score = 1000;
      } else if (joined && (rec.aliases || []).indexOf(joined) >= 0) {
        score = 900;
      } else if (joined && rec.id.indexOf(joined) === 0) {
        score = 700;
      } else if (joined && (rec.aliases || []).some(function (a) {
        return a.indexOf(joined) === 0;
      })) {
        score = 650;
      } else if (joined && d.name.indexOf(joined) === 0) {
        score = 620;
      } else if (tokens.length && tokens.every(function (t, i) {
        return tokenMatches(t, d) || (tokenBoost[i] && tokenBoost[i][rec.id]);
      })) {
        score = tokens.some(function (t, i) {
          return tokenBoost[i] && tokenBoost[i][rec.id];
        }) ? 850 : 400;
      }
      if (rec.deprecated && score > 10) { score -= 5; }
      if (score && HUB.coveredByProfile(rec.license)) { score += 5; }
      if (!score && !tokens.length &&
          (filters.cat || filters.kind || filters.role)) { score = 10; }
      if (score) { out.push({ rec: rec, score: score }); }
    });
    if (!out.length && tokens.length === 1 && tokens[0].length >= 3) {
      docs.forEach(function (d) {
        if (filters.cat && d.rec.category !== filters.cat) { return; }
        if (filters.kind && d.rec.kind !== filters.kind) { return; }
        if (filters.role && (!d.rec.roles || d.rec.roles.indexOf(filters.role) < 0)) { return; }
        if (isSubsequence(tokens[0], d.rec.id) ||
            isSubsequence(tokens[0], d.name)) {
          out.push({ rec: d.rec, score: 100 });
        }
      });
    }
    out.sort(function (a, b) {
      if (b.score !== a.score) { return b.score - a.score; }
      if (a.rec.name.length !== b.rec.name.length) {
        return a.rec.name.length - b.rec.name.length;
      }
      return a.rec.id < b.rec.id ? -1 : 1;
    });
    return out.slice(0, tokens.length ? 100 : 1000);
  };
})();
