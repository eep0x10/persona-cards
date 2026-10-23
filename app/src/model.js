export const CORE = ["D", "F", "V"];
export const ORDER = ["D", "F", "V", "L", "P", "N"];
export const MODULES = { nucleo: "Núcleo", expansao: "Expansão 4.0", expansao_5: "Expansão 5.0" };
export const blank = () => ({ id: null, name: "", role: "", context: "", cards: {}, fields: {}, locks: [], enabled: [...CORE], notes: "", portrait: "", finalized: false });
export function normalizeCharacter(c) {
  return { ...c, portrait: c.portrait === undefined ? "" : c.portrait, finalized: c.finalized === undefined ? false : c.finalized };
}
export function validateCharacter(c, lookup) {
  if (!c || typeof c !== "object" || Array.isArray(c)) return false;
  if (!validatePortrait(c.portrait) || c.finalized !== undefined && typeof c.finalized !== "boolean") return false;
  if (["name", "role", "context", "notes"].some((k) => typeof c[k] !== "string" || c[k].length > 2e4)) return false;
  if (!c.cards || typeof c.cards !== "object" || Array.isArray(c.cards) || !c.fields || typeof c.fields !== "object" || Array.isArray(c.fields)) return false;
  if (!Array.isArray(c.enabled) || !Array.isArray(c.locks) || CORE.some((f) => !c.enabled.includes(f))) return false;
  if (c.enabled.some((f) => !ORDER.includes(f)) || c.locks.some((f) => !ORDER.includes(f)) || new Set(c.enabled).size !== c.enabled.length || new Set(c.locks).size !== c.locks.length) return false;
  if (Object.entries(c.cards).some(([f, code]) => !ORDER.includes(f) || typeof code !== "string" || !new RegExp(`^${f}\\d{2}$`).test(code) || lookup && lookup[code]?.familia !== f)) return false;
  if (Object.entries(c.fields).some(([f, value]) => !ORDER.includes(f) || typeof value !== "string" || value.length > 2e4)) return false;
  return c.id === null || typeof c.id === "string";
}
export function applyCards(draft, changes) {
  const fields = { ...draft.fields }, cards = { ...draft.cards };
  for (const card of changes) {
    cards[card.familia] = card.codigo;
    if (!Object.hasOwn(fields, card.familia)) fields[card.familia] = Object.values(card.campos)[0] || "";
  }
  return { ...draft, cards, fields, enabled: [.../* @__PURE__ */ new Set([...draft.enabled, ...changes.map((c) => c.familia)])] };
}
export function parseImport(text, lookup) {
  const data = JSON.parse(text);
  if (data?.app !== "Persona Cards" || !["5.0", "5.1"].includes(data?.version) || !validateCharacter(data.character, lookup)) throw Error("Estrutura ou códigos incompatíveis. Use uma exportação Persona Cards 5.0 ou 5.1.");
  return normalizeCharacter(data.character);
}
export function completionIssues(c, lookup) {
  const issues = [];
  if (!validateCharacter(c, lookup)) return [{ field: "character", message: "A ficha contém dados incompatíveis. Revise as cartas e a foto." }];
  if (!c.name.trim()) issues.push({ field: "name", message: "Dê um nome ao personagem." });
  else if (c.name.length > 120) issues.push({ field: "name", message: "Use até 120 caracteres no nome." });
  for (const family of c.enabled) {
    const card = lookup?.[c.cards[family]];
    if (!card || card.familia !== family) {
      issues.push({ field: "cards", family, message: `Escolha uma carta para ${family}.` });
      continue;
    }
    const value = c.fields[family]?.trim() || "";
    const prompt = (Object.values(card.campos)[0] || "").trim();
    if (!value || value === prompt) issues.push({ field: "fields", family, message: `Interprete a carta ${family} com detalhes do personagem.` });
  }
  return issues;
}
export function finalizeCharacter(c, lookup) {
  const issues = completionIssues(c, lookup);
  if (issues.length) {
    const error = new Error("Preencha as pendências antes de finalizar.");
    error.issues = issues;
    throw error;
  }
  return { ...normalizeCharacter(c), finalized: true };
}
export function characterMarkdown(c, lookup) {
  const labels = { D: "Objetivo", F: "Forma de agir", V: "Expressão", L: "Vínculo", P: "Pressão", N: "Conflito interno" };
  const lines = [`# ${c.name || "Combinação sem nome"}`, "", c.role, c.context];
  for (const f of ORDER) if (c.enabled.includes(f) && c.fields[f]) lines.push("", `## ${labels[f]}`, c.fields[f]);
  if (c.notes) lines.push("", "## Notas de interpretação", c.notes);
  lines.push("", "## Cartas", "", ...ORDER.filter((f) => c.enabled.includes(f) && lookup[c.cards[f]]).map((f) => `- ${c.cards[f]}: ${lookup[c.cards[f]].titulo}`));
  const hidden = ORDER.filter((f) => !c.enabled.includes(f) && (c.fields[f] || c.cards[f]));
  if (hidden.length) {
    lines.push("", "## Camadas guardadas, fora da combinação atual");
    for (const f of hidden) lines.push("", `### ${labels[f]}`, c.cards[f] || "", c.fields[f] || "");
  }
  return lines.filter((v) => v !== void 0 && v !== null).join("\n") + "\n";
}
import { validatePortrait } from "./portrait.js";
