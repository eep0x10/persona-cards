import React, { useEffect, useRef, useState } from 'react';
import { animate, createScope, stagger } from 'animejs';
import { completionIssues, ORDER, FAMILY_LABELS, JOURNEY_LABELS, journeyOptions } from './model.js';
import { preparePortrait } from './portrait.js';
import { downloadCharacterPng } from './exportPng.js';

const LABELS = FAMILY_LABELS;

function JourneyReview({journey,guide,onChange,issues,submitted,reduced}) {
  const root=useRef(null);
  useEffect(()=>{
    const scope=createScope({root}).add(()=>{
      if(reduced)return;
      const selected=root.current.querySelectorAll('.journey-choice[aria-pressed=true]');
      if(selected.length)animate(selected,{scale:[.97,1],duration:220,ease:'out(3)'});
    });
    return()=>scope.revert();
  },[journey.call,journey.response,reduced]);
  const update=(key,value)=>onChange({journey:{...journey,[key]:value}});
  const issueFor=key=>submitted?issues.find(issue=>issue.journeyField===key)?.message:null;
  return <section ref={root} className="journey-section" aria-labelledby="journey-heading">
    <span className="paper-eyebrow">03 · GUIA OBRIGATÓRIO · G07</span><h2 id="journey-heading">Chamado/Destino</h2>
    <p className="review-instruction">Escolha um chamado e uma resposta. Depois, separe o que aconteceu, o que o personagem acredita e a escolha que ainda pode fazer. Nenhum chamado determina a resposta.</p>
    {['call','response'].map(key=>{
      const options=journeyOptions(guide,key),error=issueFor(key);
      return <fieldset className="journey-choice-group" key={key} id={`review-journey-${key}`} tabIndex={-1} aria-describedby={error?`journey-error-${key}`:undefined}>
        <legend>{JOURNEY_LABELS[key]} <span>{key === "response" ? "obrigatória" : "obrigatório"}</span></legend>
        <div className="journey-choices">{options.map((option,index)=><button type="button" className="journey-choice" key={option} aria-pressed={journey[key]===option} onClick={()=>update(key,option)}><span>{index+1}</span><strong>{option}</strong>{journey[key]===option&&<b aria-hidden="true">✓</b>}</button>)}</div>
        {journey[key]&&!options.includes(journey[key])&&<p className="journey-retained">Resposta guardada: {journey[key]}</p>}
        {error&&<p id={`journey-error-${key}`} className="review-error">{error}</p>}
      </fieldset>;
    })}
    {['fact','belief','choice'].map(key=>{
      const promptKey={fact:'Fato',belief:'Crença',choice:'Escolha'}[key],error=issueFor(key);
      return <div className="journey-written" key={key}><label htmlFor={`review-journey-${key}`}>{JOURNEY_LABELS[key]} <span>{key === "fact" ? "obrigatório" : "obrigatória"}</span></label><p>{guide?.campos?.[promptKey]}</p><textarea id={`review-journey-${key}`} rows={3} maxLength={20000} value={journey[key]} onChange={event=>update(key,event.target.value)} aria-invalid={Boolean(error)} aria-describedby={error?`journey-error-${key}`:undefined}/>{error&&<p id={`journey-error-${key}`} className="review-error">{error}</p>}</div>;
    })}
  </section>;
}

export function CharacterReview({ draft, lookup, Art, onChange, onBack, onFinish, onChooseFamily, reduced, journeyGuide }) {
  const root = useRef(null);
  const photoInput = useRef(null);
  const photoRequest = useRef(0);
  const [photoBusy, setPhotoBusy] = useState(false);
  const [photoError, setPhotoError] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const issues = completionIssues(draft, lookup);
  const issueFor = (field, family) => submitted ? issues.find(issue => issue.field === field && (!family || issue.family === family))?.message : null;

  useEffect(() => {
    const scope = createScope({ root }).add(() => {
      if (!reduced) animate('.review-section', { translateY:[16,0], opacity:[0.6,1], duration:330, delay:stagger(45), ease:'out(3)' });
    });
    return () => scope.revert();
  }, [reduced]);

  useEffect(() => () => { photoRequest.current += 1; }, []);

  const loadPhoto = async event => {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file) return;
    const request = ++photoRequest.current;
    setPhotoBusy(true);
    setPhotoError('');
    try {
      const portrait = await preparePortrait(file);
      if (request === photoRequest.current && portrait) onChange({ portrait });
    } catch (error) {
      if (request === photoRequest.current) setPhotoError(error.message || 'Não foi possível abrir esta foto. A foto anterior foi mantida.');
    } finally {
      if (request === photoRequest.current) setPhotoBusy(false);
    }
  };
  const submit = event => {
    event.preventDefault();
    setSubmitted(true);
    if (issues.length) {
      const issue = issues[0];
      const id = issue.family ? `review-field-${issue.family}` : issue.field === "journey" ? `review-journey-${issue.journeyField}` : `review-${issue.field}`;
      document.getElementById(id)?.focus();
      return;
    }
    if (!photoBusy) onFinish();
  };

  return <main ref={root} className="character-review">
    <div className="experience-heading">
      <div><span className="experience-eyebrow">SUAS CARTAS, SUA HISTÓRIA</span><h1 data-screen-heading tabIndex={-1}>Dê vida ao personagem.</h1><p>Traga as cartas para o seu mundo. Seu rascunho acompanha você ao voltar à mesa.</p></div>
      <button className="outline-on-green" onClick={onBack}>← Voltar à mesa</button>
    </div>
    <form className="review-layout" onSubmit={submit} noValidate>
      <section className="review-section review-identity" aria-labelledby="identity-heading">
        <span className="paper-eyebrow">01 · IDENTIDADE</span><h2 id="identity-heading">Um nome. Uma presença.</h2>
        <div className="review-photo-row">
          <div className="review-photo"><Art code={draft.cards.D}/>{draft.portrait && <img key={draft.portrait} src={draft.portrait} alt="Retrato do personagem" onError={event => {event.currentTarget.style.display="none";setPhotoError("O retrato guardado não pôde ser aberto. A arte do baralho foi usada; você pode trocar ou remover a foto.");}}/>}</div>
          <div className="review-photo-controls"><p>Um retrato, se quiser.</p><span>JPG, PNG ou WebP · até 10 MB.<br/>A foto fica neste navegador.</span><button type="button" onClick={() => photoInput.current.click()} disabled={photoBusy}>{photoBusy?'Preparando foto…':draft.portrait?'Trocar foto':'Adicionar foto'}</button>{draft.portrait && <button type="button" className="review-text-button" onClick={() => { photoRequest.current += 1; setPhotoBusy(false); setPhotoError(''); onChange({portrait:''}); }}>Remover foto</button>}</div>
          <input ref={photoInput} hidden type="file" accept="image/jpeg,image/png,image/webp" onChange={loadPhoto}/>
        </div>
        {photoError && <p className="review-error" role="alert">{photoError}</p>}
        <label htmlFor="review-name">Nome <span>obrigatório</span></label>
        <input id="review-name" value={draft.name} maxLength={120} onChange={event => onChange({name:event.target.value})} autoComplete="off" aria-invalid={Boolean(issueFor('name'))} aria-describedby={issueFor('name')?'review-name-error':undefined}/>
        {issueFor('name') && <p id="review-name-error" className="review-error">{issueFor('name')}</p>}
        <label htmlFor="review-role">Papel na história <span>opcional</span></label>
        <input id="review-role" value={draft.role} maxLength={20000} onChange={event => onChange({role:event.target.value})} placeholder="Mercadora, rival, guardião…"/>
        <label htmlFor="review-context">Onde está a história? <span>opcional</span></label>
        <textarea id="review-context" rows={4} value={draft.context} maxLength={20000} onChange={event => onChange({context:event.target.value})} placeholder="Um lugar, uma situação, algo que está mudando…"/>
        <label htmlFor="review-notes">Notas de interpretação <span>opcional</span></label>
        <textarea id="review-notes" rows={4} value={draft.notes} maxLength={20000} onChange={event => onChange({notes:event.target.value})} placeholder="Uma competência, um prazer cotidiano, um limite…"/>
      </section>
      <section className="review-section review-interpretations" aria-labelledby="interpretation-heading">
        <span className="paper-eyebrow">02 · INTERPRETAÇÃO</span><h2 id="interpretation-heading">O que essas oito cartas dizem sobre ele?</h2>
        <p className="review-instruction">Transforme os convites em escolhas concretas. Substitua <b>[pessoas, lugares e objetivos]</b> pelo que existe na sua história. Os textos que você já escreveu continuam aqui.</p>
        <div className="interpretation-list">{ORDER.map((family, index) => {
          const card = lookup[draft.cards[family]];
          const issue = submitted ? issues.find(item => item.family === family)?.message : null;
          return <article className="interpretation-card" key={family}>
            <header><span className="interpretation-number">{index+1}</span><div><span>{LABELS[family]}{card?` · ${card.codigo}`:''}</span><h3>{card?.titulo || 'Escolha uma carta para esta camada'}</h3></div>{card && <Art code={card.codigo}/>}</header>
            {card ? <><p className="interpretation-reading">{card.leitura}</p><label htmlFor={`review-field-${family}`}>Na minha história…</label><textarea id={`review-field-${family}`} value={draft.fields[family] || ''} rows={3} maxLength={20000} onChange={event => onChange({fields:{...draft.fields,[family]:event.target.value}})} aria-invalid={Boolean(issue)} aria-describedby={issue?`review-error-${family}`:undefined}/></> : <button id={`review-field-${family}`} type="button" onClick={() => onChooseFamily(family)}>Escolher carta de {LABELS[family]}</button>}
            {issue && <p id={`review-error-${family}`} className="review-error">{issue}</p>}
          </article>;
        })}</div>
        <JourneyReview journey={draft.journey} guide={journeyGuide} onChange={onChange} issues={issues} submitted={submitted} reduced={reduced}/>
        <div className="review-finish"><p>Complete as oito interpretações e as cinco respostas do guia para guardar o personagem neste navegador e receber sua carta.</p><button className="review-finalize" type="submit" disabled={photoBusy}>Finalizar personagem →</button>{submitted && issues.length>0 && <p className="review-error" role="alert">Complete as {issues.length} {issues.length===1?'pendência indicada':'pendências indicadas'} acima.</p>}</div>
      </section>
    </form>
  </main>;
}

export function FinishedCharacter({ character, lookup, Art, onEdit, onNewVersion, onTable, onExport, reduced, edition }) {
  const root = useRef(null);
  const [exporting, setExporting] = useState(false);
  const [portraitFailed,setPortraitFailed]=useState(false);
  const [exportStatus, setExportStatus] = useState('');
  useEffect(() => {
    const scope = createScope({ root }).add(() => {
      if (!reduced) {
        animate('.finished-paper', { translateY:[34,0], rotateY:[-8,0], rotateZ:[-1,0], scale:[0.97,1], duration:540, ease:'out(3)' });
        animate('.finished-layer', { translateY:[12,0], opacity:[0.6,1], duration:300, delay:stagger(55,{start:130}), ease:'out(3)' });
      }
    });
    return () => scope.revert();
  }, [character.id,reduced]);
  const exportPng = async () => {
    if (exporting) return;
    setExporting(true); setExportStatus('Preparando sua carta…');
    try { await downloadCharacterPng(character, lookup, edition); setExportStatus('PNG preparado para download.'); }
    catch (error) { setExportStatus(error.message || 'Não foi possível gerar o PNG. Tente novamente.'); }
    finally { setExporting(false); }
  };
  return <main ref={root} className="finished-experience">
    <div className="experience-heading"><div><span className="experience-eyebrow">PRONTO PARA A PRÓXIMA CENA</span><h1 data-screen-heading tabIndex={-1}>Seu personagem ganhou forma.</h1></div><button className="outline-on-green" onClick={onTable}>← Voltar à mesa</button></div>
    <article className="finished-paper" aria-label={`Carta de personagem de ${character.name}`}>
      <div className="finished-hero"><div className="finished-portrait"><Art code={character.cards.D}/>{character.portrait && <img key={character.portrait} src={character.portrait} alt={`Retrato de ${character.name}`} onError={event => {event.currentTarget.style.display="none";setPortraitFailed(true);}}/>}<span className="portrait-caption">{portraitFailed?"ARTE DO BARALHO · RETRATO INDISPONÍVEL":`PERSONA CARDS · ${edition}`}</span></div><div className="finished-identity"><span className="paper-eyebrow">CARTA DO PERSONAGEM</span><h2>{character.name}</h2>{character.role && <p className="finished-role">{character.role}</p>}<div className="finished-codes">{ORDER.map(family => <span key={family}>{character.cards[family]}</span>)}</div>{character.context && <p className="finished-context">{character.context}</p>}</div></div>
      <div className="finished-layers">{ORDER.map((family,index) => { const card=lookup[character.cards[family]]; return <section className="finished-layer" key={family}><div className="finished-layer-art"><Art code={card.codigo}/></div><div><span className="paper-eyebrow">{String(index+1).padStart(2,'0')} · {LABELS[family]} · {card.codigo}</span><h3>{card.titulo}</h3><p>{character.fields[family]}</p></div></section>; })}</div>
      <section className="finished-journey"><div className="finished-journey-heading"><div><span className="paper-eyebrow">CHAMADO/DESTINO · G07</span><h3>Entre o que aconteceu e a próxima escolha.</h3></div><Art code="G07"/></div><dl>{Object.entries(JOURNEY_LABELS).map(([key,label])=><div key={key}><dt>{label}</dt><dd>{character.journey[key]}</dd></div>)}</dl></section>
      {character.notes && <section className="finished-notes"><span className="paper-eyebrow">PARA LEVAR À CENA</span><p>{character.notes}</p></section>}
      <footer className="finished-signature"><span>PERSONA CARDS</span><span>Personagens vivos. Escolhas reais.</span></footer>
    </article>
    <div className="finished-actions"><button className="download-png" onClick={exportPng} disabled={exporting}>{exporting?'Preparando…':'Baixar carta · PNG'}</button><button onClick={onEdit}>Editar personagem</button><button onClick={onNewVersion}>Criar nova versão</button><button onClick={() => onExport(character,'json')}>Guardar JSON</button></div>
    <p className="finished-export-status" role="status">{exportStatus || 'Salvo neste navegador. Guarde JSON para continuar em outro dispositivo.'}</p>
  </main>;
}
