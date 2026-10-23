import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { completionIssues, validateCharacter, parseImport } from "./src/model.js";

const read = (name) => JSON.parse(readFileSync(new URL(name, import.meta.url), "utf8"));
const catalog = read("./public/inspirations.json");
const deck = read("./public/deck.json");
const lookup = Object.fromEntries(deck.cartas.map((c) => [c.codigo, c]));
const allowedMedia = ["Anime", "Cinema", "Animação", "Quadrinhos", "Séries", "Jogos"];
const allowedArchetypes = ["Herói", "Vilão", "Ambíguo", "Coadjuvante"];

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

test("all templates finalize, roundtrip as 5.1 and retain specific valid interpretations", () => {
  const interpretations = new Set();
  for (const entry of catalog.characters) {
    const c = entry.character;
    assert.equal(c.id, null, entry.id);
    assert.equal(c.name, entry.name);
    assert.equal(c.portrait, "");
    assert.equal(c.finalized, true);
    assert.equal(validateCharacter(c, lookup), true, entry.id);
    assert.deepEqual(completionIssues(c, lookup), [], entry.id);
    assert.deepEqual(parseImport(JSON.stringify({ app: "Persona Cards", version: "5.1", character: c }), lookup), c);
    assert.match(c.context, /Cena proposta/);
    assert.match(c.notes, /não eventos canônicos/);
    assert.deepEqual(Object.keys(c.cards), c.enabled);
    for (const family of c.enabled) {
      assert.equal(lookup[c.cards[family]].familia, family, entry.id);
      assert.ok(c.fields[family].length >= 50, entry.id + family);
      assert.ok(!interpretations.has(c.fields[family]), `Repeated field: ${entry.id} ${family}`);
      interpretations.add(c.fields[family]);
    }
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

test("sampling includes six media, four roles and selective optional layers", () => {
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
