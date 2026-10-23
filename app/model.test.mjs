import test from "node:test";
import assert from "node:assert/strict";
import { blank, normalizeCharacter, validateCharacter, parseImport, completionIssues, finalizeCharacter, applyCards } from "./src/model.js";
import { validatePortrait, preparePortrait, MAX_PORTRAIT_DATA_URL_LENGTH } from "./src/portrait.js";

const lookup = Object.fromEntries(["D", "F", "V", "L", "P", "N"].map((familia) => [`${familia}01`, {
  familia, codigo: `${familia}01`, campos: { Convite: `Interprete ${familia}` }, titulo: familia,
}]));
const complete = () => ({ ...blank(), name: "Lina", cards: { D: "D01", F: "F01", V: "V01" }, fields: { D: "Abrir a travessia", F: "Reunir os moradores", V: "Explicar o plano" } });
const png = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a9uoAAAAASUVORK5CYII=";

test("legacy 5.0 and 5.1 imports preserve all text and normalize optional defaults", () => {
  const legacy = complete();
  delete legacy.portrait; delete legacy.finalized;
  legacy.fields.D = "x".repeat(20000);
  legacy.role = "r".repeat(20000);
  legacy.context = "Contexto"; legacy.notes = "Notas";
  for (const version of ["5.0", "5.1"]) {
    const imported = parseImport(JSON.stringify({ app: "Persona Cards", version, character: legacy }), lookup);
    assert.deepEqual(imported, { ...legacy, portrait: "", finalized: false });
  }
  assert.equal(normalizeCharacter(legacy).fields.D.length, 20000);
});

test("finalization preserves portrait and text through JSON export/import", () => {
  const c = { ...complete(), portrait: png, role: "", context: "", notes: "Nota" };
  assert.deepEqual(completionIssues(c, lookup), []);
  const final = finalizeCharacter(c, lookup);
  assert.equal(final.finalized, true);
  assert.equal(c.finalized, false);
  assert.deepEqual(parseImport(JSON.stringify({ app: "Persona Cards", version: "5.1", character: final }), lookup), final);
});

test("finalization requires a name, selected valid cards and interpreted enabled layers", () => {
  assert.ok(completionIssues({ ...complete(), name: " " }, lookup).some((i) => i.field === "name"));
  assert.ok(completionIssues({ ...complete(), name: "n".repeat(121) }, lookup).some((i) => i.field === "name"));
  for (const family of ["D", "F", "V", "L"]) {
    const c = complete();
    if (family === "L") c.enabled.push("L");
    delete c.cards[family];
    assert.ok(completionIssues(c, lookup).some((i) => i.family === family && i.field === "cards"));
    assert.throws(() => finalizeCharacter(c, lookup), (error) => error.issues.length > 0);
  }
  for (const value of ["", " ", "Interprete D"]) {
    const c = complete(); c.fields.D = value;
    assert.ok(completionIssues(c, lookup).some((i) => i.family === "D" && i.field === "fields"));
  }
  const bad = complete(); bad.cards.D = "F01";
  assert.equal(validateCharacter(bad, lookup), false);
  assert.ok(completionIssues(bad, lookup).length);
});

test("enabled layers retain addition order and hidden fields remain intact", () => {
  const c = complete(); c.fields.N = "Texto guardado";
  const changed = applyCards(c, [lookup.P01, lookup.N01, lookup.L01]);
  assert.deepEqual(changed.enabled, ["D", "F", "V", "P", "N", "L"]);
  assert.equal(changed.fields.N, "Texto guardado");
  assert.equal(validateCharacter(changed, lookup), true);
});

test("portrait rejects active URLs, SVG, spoofed MIME, malformed and oversized data", () => {
  assert.equal(validatePortrait(png), true);
  for (const value of [null, {}, "javascript:alert(1)", "file:///portrait.png", "https://example.com/photo.jpg",
    "data:image/svg+xml;base64,PHN2Zy8+", "data:image/png;base64,PHN2Zy8+", png.replace("image/png", "image/jpeg"),
    png + " ", "data:image/jpeg;base64,!!!!", "x".repeat(MAX_PORTRAIT_DATA_URL_LENGTH + 1)]) {
    assert.equal(validatePortrait(value), false);
    assert.equal(validateCharacter({ ...complete(), portrait: value }, lookup), false);
  }
  assert.equal(validateCharacter({ ...complete(), finalized: "true" }, lookup), false);
  const large = "data:image/png;base64," + "iVBORw0KGgoA" + "A".repeat(300000);
  assert.equal(validatePortrait(large), true);
});

test("portrait upload handles cancellation and rejects invalid input before decoding", async () => {
  assert.equal(await preparePortrait(null), null);
  await assert.rejects(preparePortrait({ type: "image/svg+xml", size: 100 }), /JPEG, PNG ou WebP/);
  await assert.rejects(preparePortrait({ type: "image/png", size: 11 * 1024 * 1024 }), /10 MB/);
  await assert.rejects(preparePortrait({ type: "image/png", size: 10, slice: () => ({ arrayBuffer: async () => new Uint8Array([1, 2, 3]).buffer }) }), /conteúdo/);
});
