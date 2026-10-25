import { validatePortrait } from './portrait.js';

// The eight families are mandatory in 5.2. One order owns table, review and export.
export const ORDER = ['OR','CV','D','F','V','L','P','N'];
export const CORE = ORDER;
export const FAMILY_LABELS = {OR:'Origem',CV:'Convicção',D:'Desejo',F:'Forma de agir',V:'Expressão',L:'Vínculo',P:'Pressão',N:'Conflito interno'};
export const MODULES = {nucleo:'Núcleo',expansao:'Expansão 4.0',expansao_5:'Expansão 5.0',expansao_5_2:'Expansão 5.2'};
export const JOURNEY_LABELS = {call:'Chamado',response:'Resposta',fact:'Fato',belief:'Crença',choice:'Margem de escolha'};
export const emptyJourney = () => ({call:'',response:'',fact:'',belief:'',choice:''});
export const blank = () => ({id:null,name:'',role:'',context:'',cards:{},fields:{},locks:[],enabled:[...ORDER],notes:'',portrait:'',finalized:false,journey:emptyJourney()});
const record = value => Boolean(value && typeof value==='object' && !Array.isArray(value));

/** Structural validity accepts historical partial characters; completion does not. */
export function validateCharacter(c,lookup) {
  if(!record(c))return false;
  if(!validatePortrait(c.portrait) || c.finalized!==undefined && typeof c.finalized!=='boolean')return false;
  if(['name','role','context','notes'].some(key=>typeof c[key]!=='string'||c[key].length>20000))return false;
  if(!record(c.cards)||!record(c.fields))return false;
  if(!Array.isArray(c.enabled)||!Array.isArray(c.locks)||['D','F','V'].some(family=>!c.enabled.includes(family)))return false;
  if(c.enabled.some(f=>!ORDER.includes(f))||c.locks.some(f=>!ORDER.includes(f))||new Set(c.enabled).size!==c.enabled.length||new Set(c.locks).size!==c.locks.length)return false;
  if(Object.entries(c.cards).some(([family,code])=>!ORDER.includes(family)||typeof code!=='string'||!new RegExp(`^${family}\\d{2}$`).test(code)||(lookup&&lookup[code]?.familia!==family)))return false;
  if(Object.entries(c.fields).some(([family,value])=>!ORDER.includes(family)||typeof value!=='string'||value.length>20000))return false;
  if(c.journey!==undefined && (!record(c.journey)||Object.keys(JOURNEY_LABELS).some(key=>c.journey[key]!==undefined&&(typeof c.journey[key]!=='string'||c.journey[key].length>20000))))return false;
  return c.id===null||typeof c.id==='string';
}

/** Add empty required slots without inventing biography or discarding legacy text. */
export function normalizeCharacter(c,lookup) {
  const next={...c,portrait:c.portrait===undefined?'':c.portrait,enabled:[...ORDER],journey:{...emptyJourney(),...(record(c.journey)?c.journey:{})},finalized:c.finalized===true};
  if(completionIssues(next,lookup).length)next.finalized=false;
  return next;
}
export function applyCards(draft,changes) {
  const fields={...draft.fields},cards={...draft.cards};
  for(const card of changes){cards[card.familia]=card.codigo;if(!Object.hasOwn(fields,card.familia))fields[card.familia]=Object.values(card.campos)[0]||'';}
  return {...draft,cards,fields,enabled:[...ORDER],finalized:false};
}
export function parseImport(text,lookup) {
  const data=JSON.parse(text);
  if(data?.app!=='Persona Cards'||!['5.0','5.1','5.2'].includes(data?.version)||!validateCharacter(data.character,lookup))throw Error('Estrutura ou códigos incompatíveis. Use uma exportação Persona Cards 5.0, 5.1 ou 5.2.');
  return normalizeCharacter(data.character,lookup);
}
export function completionIssues(c,lookup) {
  if(!validateCharacter(c,lookup))return [{field:'character',message:'A ficha contém dados incompatíveis. Revise as cartas, o guia e a foto.'}];
  const issues=[];
  if(!c.name.trim())issues.push({field:'name',message:'Dê um nome ao personagem.'});
  else if(c.name.length>120)issues.push({field:'name',message:'Use até 120 caracteres no nome.'});
  for(const family of ORDER){
    const code=c.cards[family];
    const card=lookup?.[code];
    if(!code || lookup && (!card||card.familia!==family)){
      issues.push({field:'cards',family,message:`Escolha uma carta de ${FAMILY_LABELS[family]}.`});
      continue;
    }
    const value=c.fields[family]?.trim()||'';
    const prompt=card?(Object.values(card.campos)[0]||'').trim():null;
    if(!value || prompt!==null && value===prompt)issues.push({field:'fields',family,message:`Interprete a carta de ${FAMILY_LABELS[family]} com detalhes do personagem.`});
  }
  for(const [key,label] of Object.entries(JOURNEY_LABELS)){
    if(!c.journey?.[key]?.trim())issues.push({field:'journey',journeyField:key,message:`Complete ${label.toLowerCase()} no guia Chamado/Destino.`});
  }
  return issues;
}
export function finalizeCharacter(c,lookup) {
  const issues=completionIssues(c,lookup);
  if(issues.length){const error=Error('Complete as oito cartas e o guia Chamado/Destino antes de finalizar.');error.issues=issues;throw error;}
  return {...normalizeCharacter(c,lookup),finalized:true};
}
export function journeyOptions(guide,key) {
  const label=key==='call'?'Chamado':'Resposta';
  return String(guide?.campos?.[label]||'').split('\n').map(line=>line.replace(/^\s*\d+\s*[.)—–-]\s*/,'').trim()).filter(Boolean);
}
export function characterMarkdown(c,lookup) {
  const lines=[`# ${c.name||'Personagem sem nome'}`,'',c.role,c.context];
  for(const family of ORDER){
    const card=lookup[c.cards[family]];
    lines.push('',`## ${FAMILY_LABELS[family]}${card?' — '+card.codigo+' · '+card.titulo:''}`,card?'':'Carta ainda não escolhida.',c.fields[family]||'Interpretação pendente.');
  }
  lines.push('','## Chamado/Destino — G07');
  for(const [key,label] of Object.entries(JOURNEY_LABELS))lines.push('',`**${label}:** ${c.journey?.[key]||'Pendente.'}`);
  if(c.notes)lines.push('','## Notas de interpretação',c.notes);
  return lines.filter(value=>value!==undefined&&value!==null).join('\n')+'\n';
}
