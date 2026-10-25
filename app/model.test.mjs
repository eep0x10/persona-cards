import test from "node:test";
import assert from "node:assert/strict";
import { blank, normalizeCharacter, validateCharacter, parseImport, completionIssues, finalizeCharacter, applyCards, ORDER, emptyJourney, journeyOptions, characterMarkdown } from "./src/model.js";
import { loadPersistence } from "./src/persistence.js";
import { validatePortrait, preparePortrait, MAX_PORTRAIT_DATA_URL_LENGTH } from "./src/portrait.js";

const lookup = Object.fromEntries(ORDER.map((familia) => [`${familia}01`, {
  familia, codigo: `${familia}01`, campos: { Convite: `Interprete ${familia}` }, titulo: familia,
}]));
const complete = () => ({...blank(),name:"Lina",cards:Object.fromEntries(ORDER.map(family=>[family,`${family}01`])),fields:Object.fromEntries(ORDER.map(family=>[family,`Uma interpretação específica de ${family}, com pessoas e decisões.`])),journey:{call:"Um convite inesperado",response:"Renegocio as condições",fact:"O barco voltou vazio.",belief:"A capitã acredita que foi um aviso.",choice:"Pode investigar antes de aceitar a missão."}});
const legacy = () => ({id:"old",name:"Lina",role:"Mercadora",context:"Porto",notes:"Anotações antigas",cards:{D:"D01",F:"F01",V:"V01"},fields:{D:"Objetivo anterior",F:"Método anterior",V:"Voz anterior",N:"Texto guardado"},locks:["F"],enabled:["D","F","V"],finalized:true});
const png = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a9uoAAAAASUVORK5CYII=";

test("legacy imports preserve all authored data and add eight empty required slots without biography",()=>{
  for(const version of ["5.0","5.1"]){
    const old=legacy();old.fields.D="x".repeat(20000);old.role="r".repeat(20000);old.portrait=png;
    const before=JSON.stringify(old);
    const imported=parseImport(JSON.stringify({app:"Persona Cards",version,character:old}),lookup);
    assert.deepEqual(imported.cards,old.cards);assert.deepEqual(imported.fields,old.fields);assert.deepEqual(imported.locks,old.locks);
    for(const key of ["name","role","context","notes","portrait"])assert.equal(imported[key],old[key]);
    assert.deepEqual(imported.enabled,ORDER);assert.deepEqual(imported.journey,emptyJourney());assert.equal(imported.finalized,false);
    assert.equal(Object.hasOwn(imported.cards,"OR"),false);assert.equal(Object.hasOwn(imported.fields,"CV"),false);
    assert.equal(JSON.stringify(old),before);
  }
});

test("5.2 finalization requires all eight interpreted cards and the entire five-part journey",()=>{
  assert.deepEqual(completionIssues(complete(),lookup),[]);
  for(const family of ORDER){
    const c=complete();c.enabled=["D","F","V"];delete c.cards[family];
    assert.ok(completionIssues(c,lookup).some(issue=>issue.field==="cards"&&issue.family===family));
    assert.throws(()=>finalizeCharacter(c,lookup));
    for(const value of [""," ",`Interprete ${family}`]){
      const draft=complete();draft.fields[family]=value;
      assert.ok(completionIssues(draft,lookup).some(issue=>issue.field==="fields"&&issue.family===family));
    }
  }
  for(const key of Object.keys(emptyJourney())){
    const c=complete();c.journey[key]=" ";
    assert.ok(completionIssues(c,lookup).some(issue=>issue.journeyField===key));assert.throws(()=>finalizeCharacter(c,lookup));
  }
  const noJourney=complete();delete noJourney.journey;assert.equal(completionIssues(noJourney,lookup).filter(issue=>issue.field==="journey").length,5);
  assert.ok(completionIssues({...complete(),name:" "},lookup).some(issue=>issue.field==="name"));
  assert.ok(completionIssues({...complete(),name:"n".repeat(121)},lookup).some(issue=>issue.field==="name"));
});

test("finalized 5.2 roundtrip preserves portrait, journey and long legacy notes",()=>{
  const c={...complete(),portrait:png,notes:"Nota antiga"};const final=finalizeCharacter(c,lookup);
  assert.equal(final.finalized,true);assert.equal(c.finalized,false);
  assert.deepEqual(parseImport(JSON.stringify({app:"Persona Cards",version:"5.2",character:final}),lookup),final);
  assert.deepEqual(normalizeCharacter(final,lookup),final);
  const changed=applyCards(final,[lookup.CV01]);assert.equal(changed.finalized,false);assert.deepEqual(changed.journey,c.journey);assert.deepEqual(changed.enabled,ORDER);
});

test("OR/CV codes are validated as multi-character families without accepting mismatches",()=>{
  for(const code of ["OR99","OR001","CV01","D01"]){const c=complete();c.cards.OR=code;assert.equal(validateCharacter(c,lookup),false,code);}
  assert.equal(validateCharacter(complete(),lookup),true);
  for(const journey of [[],null,{...emptyJourney(),fact:null}])assert.equal(validateCharacter({...complete(),journey},lookup),false);
});

test("guide offers six exact choices and text export includes all eight layers and five journey answers",()=>{
  const guide={campos:{Chamado:"1. Um convite\n2. Um encontro\n3. Uma ordem\n4. Uma ameaça\n5. Um desejo\n6. Um sinal",Resposta:"1. Aceito\n2. Recuso\n3. Adio\n4. Renegocio\n5. Redireciono\n6. Rompo"}};
  assert.deepEqual(journeyOptions(guide,"call"),["Um convite","Um encontro","Uma ordem","Uma ameaça","Um desejo","Um sinal"]);
  assert.equal(journeyOptions(guide,"response").length,6);
  const c=complete(),text=characterMarkdown(c,lookup);
  for(const family of ORDER)assert.ok(text.includes(`${family}01`)&&text.includes(c.fields[family]));
  for(const value of Object.values(c.journey))assert.ok(text.includes(value));
  assert.ok(text.includes("Chamado/Destino — G07"));
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


test("local saved legacy drafts normalize without losing cards, locks, photo or authored text",()=>{
  const old={...legacy(),portrait:png};
  const raw=JSON.stringify({draft:old,saved:[old],modules:["nucleo"],customMetadata:"preserved"});
  const map=new Map([["fixture",raw]]);
  const storage={getItem:key=>map.get(key)??null,setItem:(key,value)=>map.set(key,value)};
  const loaded=loadPersistence(storage,"fixture",lookup);
  assert.equal(loaded.recovery,null);assert.equal(map.get("fixture"),raw);
  for(const c of [loaded.data.draft,...loaded.data.saved]){
    assert.deepEqual(c.cards,old.cards);assert.deepEqual(c.fields,old.fields);assert.deepEqual(c.locks,old.locks);assert.equal(c.portrait,png);assert.equal(c.notes,old.notes);
    assert.deepEqual(c.enabled,ORDER);assert.deepEqual(c.journey,emptyJourney());assert.equal(c.finalized,false);
  }
  assert.equal(loaded.data.customMetadata,"preserved");
});
