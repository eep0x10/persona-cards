import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { completionIssues, validateCharacter, parseImport, ORDER, emptyJourney } from "./src/model.js";

const read = (name) => JSON.parse(readFileSync(new URL(name, import.meta.url), "utf8"));
const catalog = read("./public/inspirations.json");
const deck = read("./public/deck.json");
const lookup = Object.fromEntries(deck.cartas.map((c) => [c.codigo, c]));
const allowedMedia = ["Anime", "Cinema", "Animação", "Quadrinhos", "Séries", "Jogos"];
const allowedArchetypes = ["Herói", "Vilão", "Ambíguo", "Coadjuvante"];

test("353 explanations cover every selected layer and preserve the original character templates", () => {
  const explanations = [];
  for (const entry of catalog.characters) {
    assert.deepEqual(Object.keys(entry.rationale), entry.character.enabled, entry.id);
    assert.equal(Object.hasOwn(entry.character, "rationale"), false, entry.id);
    for (const family of entry.character.enabled) {
      const text = entry.rationale[family];
      assert.equal(typeof text, "string", entry.id + family);
      assert.ok(text.length >= 35 && text.length <= 200, entry.id + family);
      assert.equal(text, text.trim());
      assert.notEqual(text, entry.character.fields[family], entry.id + family);
      assert.notEqual(text, lookup[entry.character.cards[family]].leitura, entry.id + family);
      explanations.push(text);
    }
  }
  assert.equal(explanations.length, 353);
  assert.equal(new Set(explanations).size, 353);
  // Recorded before adding explanatory metadata: all 100 character objects stay exact.
  const hash = createHash("sha256").update(JSON.stringify(catalog.characters.map((e) => e.character))).digest("hex");
  assert.equal(hash, "489995a3d3f4e27a25ff02c23754b23169ae2203f40442d92b44a543303a5cf3");
});

test("exactly 100 distinct inspirations use the complete published schema", () => {
  assert.equal(catalog.version, "5.1");
  assert.match(catalog.disclaimer, /não são eventos canônicos/);
  assert.equal(catalog.characters.length, 100);
  assert.equal(new Set(catalog.characters.map((c) => c.id)).size, 100);
  assert.equal(new Set(catalog.characters.map((c) => c.name)).size, 100);
  for (const entry of catalog.characters) {
    assert.match(entry.id, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
    for (const key of ["name", "franchise", "excerpt"]) assert.ok(entry[key].trim().length > 2, entry.id + key);
    assert.ok(allowedMedia.includes(entry.medium), entry.id);
    assert.ok(allowedArchetypes.includes(entry.archetype), entry.id);
    assert.ok(["direto", "adaptado"].includes(entry.audit.fit), entry.id);
    assert.ok(entry.audit.note.length > 50, entry.id);
    assert.ok(Array.isArray(entry.audit.gapTags));
    if (entry.audit.fit === "adaptado") assert.ok(entry.audit.gapTags.length > 0, entry.id);
  }
});

test("the 100 historical 5.1 readings remain partial and import as unfinished 5.2 drafts",()=>{
  for(const entry of catalog.characters){
    const c=entry.character,before=JSON.stringify(c);
    assert.equal(c.id,null);assert.equal(c.name,entry.name);assert.equal(validateCharacter(c,lookup),true,entry.id);
    const issues=completionIssues(c,lookup);
    for(const family of ["OR","CV"])assert.ok(issues.some(issue=>issue.family===family&&issue.field==="cards"),entry.id+family);
    assert.equal(issues.filter(issue=>issue.field==="journey").length,5,entry.id);
    const imported=parseImport(JSON.stringify({app:"Persona Cards",version:"5.1",character:c}),lookup);
    assert.deepEqual(imported.enabled,ORDER);assert.deepEqual(imported.cards,c.cards);assert.deepEqual(imported.fields,c.fields);assert.deepEqual(imported.locks,c.locks);
    assert.deepEqual(imported.journey,emptyJourney());assert.equal(imported.finalized,false);
    assert.equal(Object.hasOwn(imported.cards,"OR"),false);assert.equal(Object.hasOwn(imported.cards,"CV"),false);
    for(const key of ["name","role","context","notes","portrait"])assert.equal(imported[key],c[key]);
    if(!c.cards.N)assert.equal(Object.hasOwn(imported.cards,"N"),false,"Do not invent internal conflict: "+entry.id);
    assert.equal(JSON.stringify(c),before);
    for(const family of c.enabled){assert.equal(lookup[c.cards[family]].familia,family);assert.ok(c.fields[family].length>=50);}
  }
});

test("sources identify official franchises via HTTPS without embedding remote portraits", () => {
  const official = ["one-piece.com", "naruto-official.com", "en.dragon-ball-official.com", "demonslayer-anime.com", "jujutsukaisen.jp", "www.starwars.com", "www.youtube.com", "www.harrypotter.com", "www.lionsgate.com", "amblin.com", "movies.disney.com", "www.paramountplus.com", "www.dc.com", "www.marvel.com", "www.netflix.com", "www.doctorwho.tv", "www.pbs.org", "www.amc.com", "www.nintendo.com", "mario.nintendo.com", "www.pokemon.com", "www.square-enix.com", "store.steampowered.com"];
  for (const entry of catalog.characters) {
    assert.ok(entry.sources.length > 0, entry.id);
    for (const source of entry.sources) {
      const url = new URL(source.url);
      assert.equal(url.protocol, "https:");
      assert.ok(official.includes(url.hostname), entry.id + source.url);
      assert.equal(url.username + url.password, "");
      assert.ok(source.label.length > 5);
    }
    assert.equal(entry.character.portrait, "");
  }
});

test("sampling includes six media, four roles and historically selective layers, without pretending 5.2 completion", () => {
  const entries = catalog.characters;
  for (const medium of allowedMedia) assert.ok(entries.filter((e) => e.medium === medium).length >= 10, medium);
  for (const archetype of allowedArchetypes) assert.ok(entries.filter((e) => e.archetype === archetype).length >= 10, archetype);
  for (const family of ["L", "P", "N"]) {
    const count = entries.filter((e) => e.character.enabled.includes(family)).length;
    assert.ok(count > 0 && count < 100, family);
  }
  const codes = new Set(entries.flatMap((e) => Object.values(e.character.cards)));
  const noN = entries.filter((e) => !e.character.enabled.includes("N")).length;
  console.log(JSON.stringify({ characters: entries.length, distinctCodes: codes.size, noN,
    media: Object.fromEntries(allowedMedia.map((m) => [m, entries.filter((e) => e.medium === m).length])),
    fit: Object.fromEntries(["direto", "adaptado"].map((f) => [f, entries.filter((e) => e.audit.fit === f).length])) }));
});
