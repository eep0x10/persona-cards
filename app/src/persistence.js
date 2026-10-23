import { MODULES, validateCharacter } from './model.js';
const record = v => Boolean(v && typeof v === 'object' && !Array.isArray(v));
export function loadPersistence(storage, key, lookup) {
  let raw;
  try { storage = typeof storage === "function" ? storage() : storage; raw = storage.getItem(key); } catch {
    return { data:{}, recovery:{raw:null,unreadable:true}, warning:'Armazenamento indisponível. Gravações bloqueadas; mantenha esta aba aberta e exporte suas novas combinações.' };
  }
  if(raw===null) return {data:{},recovery:null,warning:''};
  let original;
  try { original=JSON.parse(raw); } catch { original=null; }
  const data=record(original)?{...original}:{};
  let invalid=!record(original);
  if(data.draft!==undefined&&!validateCharacter(data.draft,lookup)){delete data.draft;invalid=true;}
  if(data.saved!==undefined){
    if(!Array.isArray(data.saved)){data.saved=[];invalid=true;}
    else {const valid=data.saved.filter(c=>validateCharacter(c,lookup));invalid ||= valid.length!==data.saved.length;data.saved=valid;}
  }
  if(data.modules!==undefined){
    if(!Array.isArray(data.modules)){delete data.modules;invalid=true;}
    else {const valid=[...new Set(data.modules.filter(m=>Object.hasOwn(MODULES,m)))];invalid ||= valid.length!==data.modules.length;data.modules=valid;}
  }
  if(!invalid)return {data,recovery:null,warning:''};
  const recovery={raw,backupKey:null};
  const backedUp=ensureRecoveryBackup(storage,key,recovery);
  return {data,recovery,warning:backedUp
    ? 'Dados válidos recuperados. O original completo foi protegido em backup local; baixe-o em Ajuda ou Importar · exportar.'
    : 'Dados válidos recuperados em memória. Gravações bloqueadas porque o backup falhou; baixe o original em Ajuda ou Importar · exportar.'};
}
export function ensureRecoveryBackup(storage,key,recovery){
  if(!recovery)return true;
  if(recovery.unreadable||typeof recovery.raw!=='string')return false;
  try {
    if(recovery.backupKey&&storage.getItem(recovery.backupKey)===recovery.raw)return true;
    let candidate;
    do {candidate=`${key}-recovery-${Date.now()}-${globalThis.crypto.randomUUID()}`;} while(storage.getItem(candidate)!==null);
    storage.setItem(candidate,recovery.raw);
    if(storage.getItem(candidate)!==recovery.raw)return false;
    recovery.backupKey=candidate;
    return true;
  }catch{return false;}
}
export function persistProtected(storage,key,payload,recovery){
  try { storage = typeof storage === "function" ? storage() : storage; }
  catch { return {ok:false,error:'O navegador bloqueou o armazenamento. Mudanças mantidas só nesta sessão; exporte a combinação antes de fechar.'}; }
  if(!ensureRecoveryBackup(storage,key,recovery))return {ok:false,error:'O backup local falhou. O original continua intacto; baixe-o antes de fechar. As mudanças atuais permanecem só nesta sessão.'};
  try{
    const next={...payload};
    if(recovery?.backupKey){const previous=Array.isArray(payload.recoveryBackupKeys)?payload.recoveryBackupKeys.filter(v=>typeof v==='string'):[];next.recoveryBackupKeys=[...new Set([...previous,recovery.backupKey])];}
    storage.setItem(key,JSON.stringify(next));
    return {ok:true};
  }catch{return {ok:false,error:'O navegador não conseguiu salvar. Exporte a combinação atual antes de fechar.'};}
}
