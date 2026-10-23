import React, { useEffect, useMemo, useRef, useState } from 'react';
import { animate, createScope, stagger } from 'animejs';

const normalize = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const FAMILIES = {D:'Desejo',F:'Forma de agir',V:'Expressão',L:'Vínculo',P:'Pressão',N:'Conflito interno'};
const compare = (left,right) => left.localeCompare(right,'pt-BR');
const safeUrl = value => /^https?:\/\//i.test(value || '');

/** Keep the catalogue intact while giving the opening row a varied reading order. */
export function interleaveInspirations(characters) {
  const mediaOrder = ['Anime','Cinema','Animação','Quadrinhos','Séries','Jogos'];
  const extraMedia = [...new Set(characters.map(entry => entry.medium))]
    .filter(medium => !mediaOrder.includes(medium)).sort(compare);
  const groups = [...mediaOrder,...extraMedia]
    .map(medium => characters.filter(entry => entry.medium === medium));
  const result = [];
  const rounds = Math.max(0,...groups.map(group => group.length));
  for (let index=0; index<rounds; index+=1) {
    for (const group of groups) if (group[index]) result.push(group[index]);
  }
  return result;
}

function CardCombination({character,lookup}) {
  return <div className="inspiration-combination">{['D','F','V'].map(family => {
    const card=lookup[character.cards[family]];
    return <div key={family}><b>{card?.codigo || family}</b><span>{card?.titulo || 'Carta não disponível'}</span></div>;
  })}</div>;
}

/** Browsing is read-only. Only onUse asks the application to replace a draft. */
export default function InspirationGallery({dataset,lookup,Art,active,reduced,onUse,filters,onFiltersChange}) {
  const root = useRef(null);
  const dialog = useRef(null);
  const detailTrigger = useRef(null);
  const {query,medium,archetype}=filters;
  const setQuery=value=>onFiltersChange(previous=>({...previous,query:value}));
  const setMedium=value=>onFiltersChange(previous=>({...previous,medium:value}));
  const setArchetype=value=>onFiltersChange(previous=>({...previous,archetype:value}));
  const [detail,setDetail] = useState(null);
  const entries = useMemo(()=>interleaveInspirations(dataset.characters),[dataset.characters]);
  const media = useMemo(()=>[...new Set(entries.map(entry=>entry.medium))].sort(compare),[entries]);
  const roles = useMemo(()=>[...new Set(entries.map(entry=>entry.archetype))].sort(compare),[entries]);
  const filtered = useMemo(()=>entries.filter(entry =>
    (medium==='all'||entry.medium===medium) &&
    (archetype==='all'||entry.archetype===archetype) &&
    normalize(`${entry.name} ${entry.franchise}`).includes(normalize(query))
  ),[entries,query,medium,archetype]);
  const resultSignature = filtered.map(entry=>entry.id).join('|');
  const hasFilters = Boolean(query || medium!=='all' || archetype!=='all');

  useEffect(()=>{
    const scope=createScope({root}).add(()=>{
      if(!active||reduced)return;
      const visibleCards=[...root.current.querySelectorAll('.inspiration-card')].slice(0,18);
      if(visibleCards.length)animate(visibleCards,{translateY:[13,0],rotateZ:[-.5,0],opacity:[.65,1],duration:270,delay:stagger(16),ease:'out(3)'});
      animate('.inspiration-count',{scale:[.97,1],duration:190,ease:'out(3)'});
    });
    return()=>scope.revert();
  },[active,resultSignature,reduced]);
  useEffect(()=>{
    if(!detail||!dialog.current)return;
    const node=dialog.current;
    node.showModal();
    node.querySelector('.inspiration-close')?.focus();
    return()=>{node.close();detailTrigger.current?.focus({preventScroll:true});};
  },[detail]);
  useEffect(()=>{
    if(!detail)return;
    const scope=createScope({root}).add(()=>{
      if(!reduced)animate('.inspiration-detail-paper',{translateY:[22,0],rotateY:[-5,0],opacity:[.65,1],duration:320,ease:'out(3)'});
    });
    return()=>scope.revert();
  },[detail,reduced]);
  useEffect(()=>{if(!active)setDetail(null);},[active]);

  const inspect=(entry,event)=>{detailTrigger.current=event.currentTarget;setDetail(entry);};
  const reset=()=>{setQuery('');setMedium('all');setArchetype('all');};
  const useAsBase=event=>{
    const entry=detail;
    setDetail(null);
    onUse(entry,detailTrigger.current || event.currentTarget);
  };

  return <main ref={root} hidden={!active} className="inspiration-gallery">
    <div className="experience-heading inspiration-heading"><div><span className="experience-eyebrow">CEM MANEIRAS DE COMEÇAR</span><h1 data-screen-heading tabIndex={-1}>Inspiração para a sua mesa.</h1><p>Personagens conhecidos, lidos pelas cartas. Explore sem alterar sua criação.</p></div><span className="inspiration-total">{entries.length}<span>inspirações</span></span></div>
    <div className="inspiration-controls">
      <label className="inspiration-search">Nome ou universo<input type="search" value={query} onChange={event=>setQuery(event.target.value)} placeholder="Busque um personagem ou uma obra…" autoComplete="off"/></label>
      <label>Mídia<select value={medium} onChange={event=>setMedium(event.target.value)}><option value="all">Todas as mídias</option>{media.map(value=><option key={value} value={value}>{value}</option>)}</select></label>
      <label>Papel na história<select value={archetype} onChange={event=>setArchetype(event.target.value)}><option value="all">Todos os papéis</option>{roles.map(value=><option key={value} value={value}>{value}</option>)}</select></label>
    </div>
    <div className="inspiration-results-bar"><p className="inspiration-count" role="status" aria-live="polite">{filtered.length} {filtered.length===1?'personagem encontrado':'personagens encontrados'}{hasFilters?` · de ${entries.length}`:''}</p>{hasFilters&&<button onClick={reset}>Limpar filtros</button>}</div>
    {filtered.length ? <div className="inspiration-grid">{filtered.map(entry=><article className="inspiration-card" key={entry.id}>
      <button className="inspiration-inspect" onClick={event=>inspect(entry,event)} aria-label={`Conhecer a leitura de ${entry.name}, ${entry.franchise}`}>
        <div className="inspiration-card-top"><span className="inspiration-medium">{entry.medium}</span><span className="inspiration-role">{entry.archetype}</span></div>
        <div className="inspiration-identity"><div><span className="inspiration-franchise">{entry.franchise}</span><h2>{entry.name}</h2></div><Art code={entry.character.cards.D}/></div>
        <p className="inspiration-symbol-label">Arte do baralho · símbolo conceitual, não retrato</p>
        <p className="inspiration-excerpt">{entry.excerpt}</p>
        <CardCombination character={entry.character} lookup={lookup}/>
        <span className="inspiration-open">Conhecer esta leitura <span aria-hidden="true">↗</span></span>
      </button>
    </article>)}</div> : <div className="inspiration-empty"><h2>Nenhum personagem neste recorte.</h2><p>Tente outro nome ou universo, ou amplie os filtros.</p><button onClick={reset}>Ver todas as inspirações</button></div>}
    <p className="inspiration-disclaimer">{dataset.disclaimer}</p>
    {detail&&<dialog ref={dialog} className="inspiration-dialog" aria-labelledby="inspiration-detail-title" onCancel={()=>setDetail(null)}>
      <div className="inspiration-detail-paper">
        <div className="inspiration-detail-top"><span>{detail.medium} · {detail.archetype}</span><div className="inspiration-detail-top-actions"><button className="inspiration-detail-quick-use" onClick={useAsBase}>Usar como base</button><button className="inspiration-close" onClick={()=>setDetail(null)} aria-label="Fechar leitura do personagem">Fechar ×</button></div></div>
        <div className="inspiration-detail-identity"><div><span className="paper-eyebrow">{detail.franchise}</span><h2 id="inspiration-detail-title">{detail.name}</h2><p>{detail.excerpt}</p></div><div><Art code={detail.character.cards.D}/><span>Arte do baralho.<br/>Não é retrato do personagem.</span></div></div>
        <section className="inspiration-detail-section"><h3>O recorte desta leitura</h3><p>{detail.character.context}</p>{detail.character.role&&<p className="inspiration-detail-role">{detail.character.role}</p>}</section>
        <div className="inspiration-detail-layers">{detail.character.enabled.map(family=>{
          const card=lookup[detail.character.cards[family]];
          return <section key={family}><span className="paper-eyebrow">{FAMILIES[family]} · {card?.codigo}</span><h3>{card?.titulo}</h3><p>{detail.character.fields[family]}</p></section>;
        })}</div>
        {detail.character.notes&&<section className="inspiration-detail-section"><h3>Para levar à cena</h3><p>{detail.character.notes}</p></section>}
        <section className="inspiration-audit"><h3>Como ler esta interpretação</h3>{detail.audit?.fit!==undefined&&<span className="inspiration-fit">Aderência ao recorte: {String(detail.audit.fit)}</span>}<p>{detail.audit?.note}</p></section>
        <section className="inspiration-sources"><h3>Fontes e referências</h3><ul>{detail.sources.map((source,index)=><li key={`${source.url}-${index}`}>{safeUrl(source.url)?<a href={source.url} target="_blank" rel="noreferrer">{source.label} ↗</a>:<span>{source.label}</span>}</li>)}</ul></section>
        <p className="inspiration-detail-disclaimer">{dataset.disclaimer}</p>
        <div className="inspiration-use-bar"><p>Explorar não altera sua criação. Use como base para adaptar estas cartas.</p><button onClick={useAsBase}>Usar como base →</button></div>
      </div>
    </dialog>}
  </main>;
}
