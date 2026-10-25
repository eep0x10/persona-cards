import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { completionIssues, validateCharacter, parseImport, ORDER, normalizeCharacter } from "./src/model.js";

const read = (name) => JSON.parse(readFileSync(new URL(name, import.meta.url), "utf8"));
const catalog = read("./public/inspirations.json");
const deck = read("./public/deck.json");
const lookup = Object.fromEntries(deck.cartas.map((c) => [c.codigo, c]));
const allowedMedia = ["Anime", "Cinema", "Animação", "Quadrinhos", "Séries", "Jogos"];
const allowedArchetypes = ["Herói", "Vilão", "Ambíguo", "Coadjuvante"];

test("800 explanations cover all eight families and include a separate journey rationale", () => {
  const explanations = [];
  for (const entry of catalog.characters) {
    assert.deepEqual(Object.keys(entry.rationale), ORDER, entry.id);
    assert.equal(Object.hasOwn(entry.character, "rationale"), false, entry.id);
    for (const family of entry.character.enabled) {
      const text = entry.rationale[family];
      assert.equal(typeof text, "string", entry.id + family);
      assert.ok(text.trim().length >= 25, entry.id + family);
      assert.equal(text, text.trim());
      assert.notEqual(text, entry.character.fields[family], entry.id + family);
      assert.notEqual(text, lookup[entry.character.cards[family]].leitura, entry.id + family);
      explanations.push(text);
    }
  }
  assert.equal(explanations.length, 800);
  for(const entry of catalog.characters)assert.ok(typeof entry.journeyRationale === "string" && entry.journeyRationale.trim().length >= 25,entry.id);
});

test("exactly 100 distinct inspirations use the complete published schema", () => {
  assert.equal(catalog.version, "5.2");
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

test("100 complete 5.2 readings import and clone as editable bases without losing eight cards or journey",()=>{
  for(const entry of catalog.characters){
    const c=entry.character,before=JSON.stringify(c);
    assert.equal(c.id,null);assert.equal(c.name,entry.name);assert.equal(validateCharacter(c,lookup),true,entry.id);
    assert.deepEqual(c.enabled,ORDER,entry.id);
    assert.deepEqual(Object.keys(c.cards),ORDER,entry.id);
    assert.deepEqual(Object.keys(c.fields),ORDER,entry.id);
    assert.equal(c.finalized,true,entry.id);
    assert.deepEqual(completionIssues(c,lookup),[],entry.id);
    const imported=parseImport(JSON.stringify({app:"Persona Cards",version:"5.2",character:c}),lookup);
    const base=normalizeCharacter({...structuredClone(c),id:null,finalized:false},lookup);
    for(const candidate of [imported,base]){
      assert.deepEqual(candidate.enabled,ORDER);assert.deepEqual(candidate.cards,c.cards);assert.deepEqual(candidate.fields,c.fields);
      assert.deepEqual(candidate.journey,c.journey);assert.deepEqual(candidate.locks,c.locks);
      for(const key of ["name","role","context","notes","portrait"])assert.equal(candidate[key],c[key]);
    }
    assert.equal(base.id,null);assert.equal(base.finalized,false);assert.equal(imported.finalized,true);
    base.fields.OR="Minha adaptação";base.journey.call="Outro chamado";
    assert.equal(JSON.stringify(c),before,"Adapting cannot mutate the catalogue: "+entry.id);
    for(const family of ORDER){assert.equal(lookup[c.cards[family]].familia,family);assert.ok(c.fields[family].trim().length>=25);}
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

test("sampling retains six media, four roles and usable name/franchise filters", () => {
  const entries = catalog.characters;
  for (const medium of allowedMedia) assert.ok(entries.filter((e) => e.medium === medium).length >= 10, medium);
  for (const archetype of allowedArchetypes) assert.ok(entries.filter((e) => e.archetype === archetype).length >= 10, archetype);
  const search=value=>value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  for(const entry of entries){
    assert.ok(entries.filter(candidate=>search(candidate.name+' '+candidate.franchise).includes(search(entry.name))).includes(entry),entry.id);
    assert.ok(entries.filter(candidate=>candidate.medium===entry.medium&&candidate.archetype===entry.archetype).includes(entry));
  }
  const codes = new Set(entries.flatMap((e) => Object.values(e.character.cards)));

  console.log(JSON.stringify({ characters: entries.length, distinctCodes: codes.size,
    media: Object.fromEntries(allowedMedia.map((m) => [m, entries.filter((e) => e.medium === m).length])),
    fit: Object.fromEntries(["direto", "adaptado"].map((f) => [f, entries.filter((e) => e.audit.fit === f).length])) }));
});
