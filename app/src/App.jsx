import React, { useEffect, useRef, useState } from "react";
import { animate, createScope, stagger } from "animejs";
import { useCardMotion } from "./motion.js";
import { loadPersistence, persistProtected } from "./persistence.js";
import deck from "../public/deck.json";
import atlas from "../../deck/illustration_sheets_5_1.json";
import { CORE, ORDER, MODULES, blank, validateCharacter, applyCards, parseImport, characterMarkdown } from "./model.js";
const KEY = "persona-cards-workbench-v1";
const FAMILIES = { D: "Desejo", F: "Forma de agir", V: "Expressão", L: "Vínculo", P: "Pressão", N: "Conflito interno", U: "Guias de uso", G: "Guias de contexto" };
const QUESTIONS = { D: "O que move seu personagem?", F: "Como ele tenta conseguir?", V: "Como sua presença aparece?", L: "Quem mais tem vontade própria nesta história?", P: "O que muda as condições da escolha?", N: "Quais dois valores vale a pena preservar?", U: "Um convite para usar as cartas.", G: "Um novo olhar para a sua história." };
const byCode = Object.fromEntries(deck.cartas.map((c) => [c.codigo, c]));
const artwork = Object.fromEntries(atlas.sheets.flatMap((s) => s.codes.map((code, i) => [code, { file: s.file, col: i % 3, row: Math.floor(i / 3) }])));
function readStorage() { return loadPersistence(() => localStorage, KEY, byCode); }
function Art({ code }) {
  const a = artwork[code];
  if (!a) return null;
  const crop = { N04: "inset(12% 0 0 0)", U02: "inset(11% 0 0 9%)", G02: "inset(13% 9% 0 9%)" }[code];
  return <span aria-hidden="true" className="card-art" style={{ backgroundImage: `url(${import.meta.env.BASE_URL}art/${a.file})`, backgroundPosition: `${a.col * 50}% ${a.row * 100}%`, clipPath: crop }} />;
}
function Face({ card, back = false }) {
  return <>
<div className="card-rule">
<span>{FAMILIES[card.familia]}</span>
<b>{card.codigo}</b>
</div>
<h2>{card.titulo}</h2>{back ? <dl className="operational" tabIndex={0} aria-label={`Como jogar com ${card.codigo}`}>{Object.entries(card.campos).map(([label, value]) => <div key={label}>
<dt>{label}</dt>
<dd>{value}</dd>
</div>)}</dl> : <>
<Art code={card.codigo} />
<p className="reading">{card.leitura}</p>

</>}</>;
}
function download(name, content, type) {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1e3);
}
function randomCard(pool) {
  if (!pool.length) return null;
  const value = new Uint32Array(1);
  crypto.getRandomValues(value);
  return pool[Math.floor(value[0] / 4294967296 * pool.length)];
}
export default function App() {
  const [initialStorage] = useState(readStorage);
  const stored = initialStorage.data;
  const [draft, setDraft] = useState(() => ({ ...blank(), ...stored.draft || {}, cards: { ...stored.draft?.cards || {} }, fields: { ...stored.draft?.fields || {} } }));
  const [saved, setSaved] = useState(() => stored.saved || []), [modules, setModules] = useState(() => stored.modules || Object.keys(MODULES));
  const [view, setView] = useState("table");
  const focusMesa = useRef(false);
  const [family, setFamily] = useState("D"), [positions, setPositions] = useState({}), [back, setBack] = useState(false);
  const [notice, setNotice] = useState(initialStorage.warning || ""), [panel, setPanel] = useState(null), [confirmation, setConfirmation] = useState(null), [pulse, setPulse] = useState(0), [changedFamilies, setChangedFamilies] = useState([]), [motionMode, setMotionMode] = useState(() => ["auto", "full", "reduced"].includes(stored.motionMode) ? stored.motionMode : stored.userReduced ? "reduced" : "auto");
  const [systemReduced, setSystemReduced] = useState(() => matchMedia("(prefers-reduced-motion: reduce)").matches), [storageReady, setStorageReady] = useState(true);
  const root = useRef(null), hand = useRef(null), dialog = useRef(null), trigger = useRef(null), touch = useRef(null), selectionSource = useRef(null), importInput = useRef(null), wheel = useRef({ amount: 0, last: 0 });
  const reduced = motionMode === "reduced" || motionMode === "auto" && systemReduced, guide = family === "U" || family === "G";
  const cards = deck.cartas.filter((c) => c.familia === family), index = (positions[family] || 0) % cards.length, active = cards[index], count = CORE.filter((f) => byCode[draft.cards[f]]).length;
  useEffect(() => {
    const media = matchMedia("(prefers-reduced-motion: reduce)");
    const change = () => setSystemReduced(media.matches);
    media.addEventListener("change", change);
    return () => media.removeEventListener("change", change);
  }, []);
  useEffect(() => {
    if (!storageReady) return;
    const result = persistProtected(() => localStorage, KEY,
      { ...stored, draft, saved, userReduced: motionMode === "reduced", motionMode, modules }, initialStorage.recovery);
    if (!result.ok) setNotice(result.error);
  }, [draft, saved, motionMode, modules, storageReady]);
  useCardMotion({ root, family, index, back, view, reduced, pulse, selectionSource });
  useEffect(() => {
    if (!panel) return;
    const node = dialog.current;
    node.showModal();
    return () => {
      node.close();
      trigger.current?.focus();
    };
  }, [Boolean(panel)]);
  useEffect(() => {
    if (!panel) return;
    dialog.current?.querySelector(".panel-body button")?.focus();
    const scope = createScope({ root }).add(() => {
      if (!reduced) animate(".panel-body", { opacity: [0.6, 1], translateY: [8, 0], duration: 180, ease: "out(3)" });
    });
    return () => scope.revert();
  }, [panel, reduced]);
  useEffect(() => {
    const scope = createScope({ root }).add(() => {
      if (!reduced && view === "grid") {
        animate(".grid-card", {
          opacity: [0.5, 1], translateY: [8, 0],
          duration: 210, delay: stagger(12), ease: "out(3)"
        });
      }
    });
    if (view === "table" && focusMesa.current) {
      focusMesa.current = false;
      hand.current?.querySelector(".flip-control")?.focus({ preventScroll: true });
      hand.current?.scrollIntoView({ block: "nearest", behavior: "instant" });
    }
    return () => scope.revert();
  }, [view, family, reduced]);
  const inspectGridCard = (card, cardIndex) => {
    setPositions(previous => ({ ...previous, [family]: cardIndex }));
    setBack(false);
    focusMesa.current = true;
    setView("table");
  };
  const open = (name, event) => {
    trigger.current = event.currentTarget;
    setPanel(name);
  };
  const navigate = (step) => {
    setPositions((p) => ({ ...p, [family]: ((p[family] || 0) + step + cards.length) % cards.length }));
    setBack(false);
  };
  const goFamily = (f) => {
    setFamily(f);
    setBack(false);
    wheel.current = { amount: 0, last: 0 };
  };
  useEffect(() => {
    const node = hand.current;
    const onWheel = (e) => {
      if (!(Math.abs(e.deltaX) > Math.abs(e.deltaY) || e.shiftKey)) return;
      const amount = e.deltaX || e.deltaY;
      if (!amount) return;
      e.preventDefault();
      const now = performance.now();
      if (now - wheel.current.last > 240) wheel.current.amount = 0;
      wheel.current.amount += amount;
      wheel.current.last = now;
      if (Math.abs(wheel.current.amount) > 65) {
        navigate(wheel.current.amount > 0 ? 1 : -1);
        wheel.current.amount = 0;
      }
    };
    node.addEventListener("wheel", onWheel, { passive: false });
    return () => node.removeEventListener("wheel", onWheel);
  }, [family, cards.length]);
  useEffect(() => {
    if (!notice || initialStorage.warning === notice) return;
    const timeout = setTimeout(() => setNotice(""), 6500);
    return () => clearTimeout(timeout);
  }, [notice]);
  const announceChanges = (changes, message) => {
    const paper = hand.current?.querySelector(".active-card");
    if (!reduced && view === "table" && !panel && changes.length === 1 && paper) {
      selectionSource.current = { node: paper.cloneNode(true), rect: paper.getBoundingClientRect() };
    }
    setStorageReady(true);
    setDraft((d) => applyCards(d, changes));
    setChangedFamilies(changes.map((c) => c.familia));
    setPulse((v) => v + 1);
    setNotice(message);
  };
  const choose = () => {
    if (guide) return;
    announceChanges([active], `${active.codigo} na sua combinação.${Object.hasOwn(draft.fields, family) ? " Seu texto anterior foi preservado." : ""}`);
    const next = CORE.find((f) => f !== family && !draft.cards[f]);
    if (next) goFamily(next);
  };
  const draw = (only) => {
    const families = only ? [only] : draft.enabled;
    const changes = [];
    let missing = false;
    for (const f of families) {
      if (draft.locks.includes(f)) continue;
      const card = randomCard(deck.cartas.filter((c) => c.familia === f && modules.includes(c.modulo) && c.codigo !== draft.cards[f]));
      if (card) changes.push(card);
      else missing = true;
    }
    if (changes.length) announceChanges(changes, `Novas cartas na mesa. Textos anteriores preservados.${missing ? " Uma família não tem outra carta nos módulos ativos." : ""}`);
    else setNotice(missing ? "Nenhuma outra carta disponível. Ative mais módulos." : "Todas as cartas estão mantidas. Libere uma para sortear.");
  };
  const save = () => {
    const character = { ...draft, id: draft.id || crypto.randomUUID(), name: draft.name || `Combinação ${ORDER.filter((f) => draft.enabled.includes(f) && draft.cards[f]).map((f) => draft.cards[f]).join(" · ")}`, updatedAt: (/* @__PURE__ */ new Date()).toISOString() };
    setStorageReady(true);
    setDraft(character);
    setSaved((s) => [character, ...s.filter((c) => c.id !== character.id)]);
    setNotice("Combinação salva neste navegador.");
  };
  const hasRecovery = Boolean(initialStorage.recovery?.raw || stored.recoveryBackupKeys?.length);
  const downloadRecovery = () => {
    try {
      const backupKey = stored.recoveryBackupKeys?.at(-1);
      const raw = initialStorage.recovery?.raw ?? (backupKey ? localStorage.getItem(backupKey) : null);
      if (typeof raw !== "string") throw Error();
      download("persona-cards-recuperacao-original.json", raw, "application/json");
      setNotice("Cópia original preparada para download, sem alterar os dados locais.");
    } catch { setNotice("Não foi possível ler a cópia original para download."); }
  };
  const exportCharacter = (character, type) => {
    try {
      const filename = (character.name || "persona").replace(/[<>:"/\\|?*]/g, "-");
      download(`${filename}.${type === "json" ? "json" : "md"}`, type === "json" ? JSON.stringify({ app: "Persona Cards", version: "5.1", character }, null, 2) : characterMarkdown(character, byCode), type === "json" ? "application/json" : "text/markdown");
      setNotice("Exportação preparada. Guarde o arquivo para transferir esta combinação.");
    } catch {
      setNotice("Não foi possível exportar. Tente novamente.");
    }
  };
  const hasWork = Boolean(draft.name || draft.role || draft.context || draft.notes || Object.keys(draft.cards).length || Object.keys(draft.fields).length);
  const requestAction = (action, event) => {
    if (event) trigger.current = event.currentTarget;
    if (hasWork && (action.type === "new" || action.type === "open")) {
      setConfirmation(action);
      setPanel("confirm");
    } else perform(action);
  };
  const perform = (action) => {
    if (action.type === "new") {
      setDraft(blank());
      setStorageReady(true);
      goFamily("D");
      setNotice("Mesa nova. Seus personagens salvos continuam na biblioteca.");
    } else if (action.type === "open") {
      setDraft({ ...blank(), ...action.character });
      setStorageReady(true);
      goFamily("D");
      setNotice("Combinação aberta. Todos os seus textos foram preservados.");
    } else if (action.type === "delete") {
      setSaved((s) => s.filter((c) => c.id !== action.id));
      if (draft.id === action.id) setDraft((d) => ({ ...d, id: null }));
      setNotice("Personagem excluído. O rascunho aberto foi preservado.");
    }
    setConfirmation(null);
    setPanel(action.type === "delete" ? "library" : null);
  };
  const duplicate = (character) => {
    setSaved((s) => [{ ...character, id: crypto.randomUUID(), name: (character.name || "Combinação") + " (cópia)", updatedAt: (/* @__PURE__ */ new Date()).toISOString() }, ...s]);
    setStorageReady(true);
    setNotice("Cópia criada na biblioteca.");
  };
  const importFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      if (file.size > 1e6) throw Error("Arquivo muito grande. Limite: 1 MB.");
      const character = parseImport(await file.text(), byCode);
      const imported = { ...character, id: crypto.randomUUID() };
      setSaved((s) => [imported, ...s]);
      setStorageReady(true);
      setPanel("library");
      setNotice("Ficha importada como novo personagem. Seu rascunho foi preservado.");
    } catch (error) {
      setNotice(`Não foi possível importar: ${error.message}`);
    }
    e.target.value = "";
  };
  const toggleLock = (f) => {
    setStorageReady(true);
    setDraft((d) => ({ ...d, locks: d.locks.includes(f) ? d.locks.filter((v) => v !== f) : [...d.locks, f] }));
  };
  const inspectFamily = (f) => {
    goFamily(f);
    setPanel(null);
  };
  const toggleOptional = (f) => {
    setStorageReady(true);
    setDraft((d) => ({ ...d, enabled: d.enabled.includes(f) ? d.enabled.filter((v) => v !== f) : [...d.enabled, f] }));
    setNotice(`${FAMILIES[f]} ${draft.enabled.includes(f) ? "fora da combinação. Carta e texto guardados." : "adicionada à combinação."}`);
  };
  const titles = { library: "Meus personagens", menu: "Sua mesa", help: "Uma mesa, três escolhas", families: "Mais cartas para a história", draw: "Sorteio e cartas mantidas", transfer: "Guardar e transferir", confirm: confirmation?.type === "delete" ? "Excluir personagem?" : "Abrir outra mesa?" };
  const navArrows = (e) => {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      navigate(1);
    }
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      navigate(-1);
    }
  };
  return <div className="table-app" ref={root} data-motion={reduced ? "reduced" : "full"} data-motion-count="0">
 <header className="topbar">
<a className="brand" href="#" onClick={(e) => e.preventDefault()}>
<span className="brand-mark">P</span>Persona Cards</a>
<nav className="desktop-support" aria-label="Apoios">
<button onClick={(e) => open("library", e)}>Meus personagens <span className="saved-count">{saved.length}</span>
</button>
<button onClick={(e) => open("help", e)}>Ajuda <span aria-hidden="true">?</span>
</button>
</nav>
<button className="mobile-menu" onClick={(e) => open("menu", e)}>Menu ☰</button>
</header>
 <main>
<nav className="family-navigation" aria-label="Família da carta">{CORE.map((f, i) => <button key={f} aria-current={family === f ? "step" : void 0} onClick={() => goFamily(f)}>
<span className="step-number">{draft.cards[f] ? "✓" : i + 1}</span>
<span>{f === "F" ? <>
<span className="desktop-label">Forma de agir</span>
<span className="mobile-label">Forma</span>
</> : FAMILIES[f]}</span>
</button>)}</nav>
 <div className="view-switch" role="group" aria-label="Visualização das cartas">
<button aria-pressed={view === "table"} onClick={() => setView("table")}>Mesa</button>
<button aria-pressed={view === "grid"} onClick={() => setView("grid")}>Grade</button>
</div>
 <p className="table-question">{QUESTIONS[family]}</p>
{view === "grid" && <section className="card-grid-view" aria-label={`Grade de ${FAMILIES[family]}`}>
<p className="grid-description">{cards.length} cartas · toque para conhecer na mesa. {guide ? "Guias de consulta." : "A escolha continua no botão Escolher esta carta."}</p>
<div className="illustrated-grid">{cards.map((card, cardIndex) => {
 const selected = !guide && draft.enabled.includes(family) && draft.cards[family] === card.codigo;
 return <button key={card.codigo} className={`grid-card ${selected ? "is-selected" : ""}`} aria-label={`Conhecer ${card.codigo}: ${card.titulo}${selected ? ", na combinação" : ""}`} onClick={() => inspectGridCard(card, cardIndex)}>
 <span className="grid-card-code">{card.codigo}<span>{selected ? "✓ Na combinação" : "Conhecer ↗"}</span></span>
 <Art code={card.codigo}/>
 <h2>{card.titulo}</h2>
 </button>;
})}</div>
</section>}
<div className="mesa-view" hidden={view !== "table"}>
 <section ref={hand} className="hand" aria-label={`Cartas de ${FAMILIES[family]}`} onKeyDown={navArrows} onTouchStart={(e) => {
    touch.current = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  }} onTouchEnd={(e) => {
    if (!touch.current) return;
    const dx = e.changedTouches[0].clientX - touch.current.x, dy = e.changedTouches[0].clientY - touch.current.y;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.4) navigate(dx < 0 ? 1 : -1);
    touch.current = null;
  }}>
 {[-2, -1, 1, 2].map((offset) => {
    const card = cards[(index + offset + cards.length) % cards.length];
    return <button key={offset} className={`neighbor neighbor-${offset < 0 ? "left" : "right"} depth-${Math.abs(offset)}`} onClick={() => navigate(offset)} tabIndex={-1} aria-hidden="true">
<span className="neighbor-motion"><Face card={card} /></span>
</button>;
  })}
 <article className="active-card" aria-label={`${active.codigo}: ${active.titulo}`}>
<div className="card-content">
<Face card={active} back={back} />
</div>
<button className="flip-control" aria-pressed={back} onClick={() => setBack((v) => !v)}>{back ? "Ver ilustração" : "Virar · como jogar"} <span aria-hidden="true">↶</span>
</button>
</article>
 </section>
 <div className="browse-controls" onKeyDown={navArrows}>
<button className="arrow" onClick={() => navigate(-1)} aria-label="Carta anterior">‹</button>
<span aria-live="polite">{index + 1} de {cards.length}</span>
<button className="arrow" onClick={() => navigate(1)} aria-label="Próxima carta">›</button>
</div>
 <div className="decision">
<button className="choose-button" onClick={guide ? () => setBack((v) => !v) : choose}>{guide ? back ? "Ver ilustração" : "Ler este guia" : draft.cards[family] === active.codigo ? "Carta escolhida · continuar" : "Escolher esta carta"}</button>
<p>{guide ? "Guia de consulta · não entra na sua combinação." : "Deslize ou role de lado para explorar. Escolha no seu tempo."}</p>
</div>
 </div>
 <section className="combination-tray" aria-label="Sua combinação">
<h1>Seu personagem <span>· {count} de 3</span>
</h1>
<div className="tray-cards">{CORE.map((f) => {
    const card = byCode[draft.cards[f]];
    return <button key={f} className={`tray-slot ${card ? "filled" : ""} ${changedFamilies.includes(f) ? "just-chosen" : ""}`} onClick={() => {
      goFamily(f);
      if (card) {
        const list = deck.cartas.filter((c) => c.familia === f);
        setPositions((p) => ({ ...p, [f]: list.findIndex((c) => c.codigo === card.codigo) }));
      }
    }} aria-label={`${FAMILIES[f]}: ${card ? card.titulo : "escolher carta"}`}>{card ? <>
<Art code={card.codigo} />
<span className="tray-code">{card.codigo}{draft.locks.includes(f) ? " · mantida" : ""}</span>
<strong>{card.titulo}</strong>
</> : <>
<b className="empty-code">{f}</b>
<span>{FAMILIES[f]}</span>
</>}</button>;
  })}</div>
<button className="save-button" disabled={count < 3} onClick={save}>Salvar combinação</button>
</section>
 <section className="table-tools" aria-label="Outras ações da mesa">
<div className="tool-buttons">
<button onClick={(e) => open("families", e)}>Aprofundar · guias</button>
<button onClick={(e) => open("draw", e)}>Sortear · manter</button>
<button onClick={(e) => requestAction({ type: "new" }, e)}>Nova combinação</button>
<button onClick={(e) => open("transfer", e)}>Importar · exportar</button>
</div>{draft.enabled.some((f) => !CORE.includes(f)) && <div className="optional-tray">{ORDER.filter((f) => !CORE.includes(f) && draft.enabled.includes(f)).map((f) => {
    const card = byCode[draft.cards[f]];
    return <button key={f} className={`optional-choice ${changedFamilies.includes(f) ? "just-chosen" : ""}`} onClick={() => goFamily(f)}>{card && <Art code={card.codigo} />}<span>{FAMILIES[f]}</span>
<strong>{card ? `${card.codigo} · ${card.titulo}` : "Escolher carta"}</strong>
</button>;
  })}</div>}</section>
 </main>
 <footer>
<span>Persona Cards · edição ilustrada 5.1</span>
<button aria-label={`Movimento ${reduced ? "reduzido" : "completo"}. Clique para ${reduced ? "ativar movimento completo" : "reduzir movimento"}.`} aria-pressed={!reduced} onClick={() => {
    setStorageReady(true);
    setMotionMode(reduced ? "full" : "reduced");
  }}>Movimento {reduced ? "reduzido" : "completo"}{motionMode === "auto" ? " · automático" : ""}</button>
{motionMode !== "auto" && <button className="follow-system" onClick={() => { setStorageReady(true); setMotionMode("auto"); }}>Seguir sistema</button>}
<a href="/api/docs" target="_blank" rel="noreferrer">API</a>
</footer>
 <p className={`notice ${notice ? "visible" : ""}`} role="status" aria-live="polite">{notice}</p>
 <input ref={importInput} hidden type="file" accept=".json,application/json" onChange={importFile} />
 {panel && <dialog ref={dialog} className="table-dialog" onCancel={() => {
    setPanel(null);
    setConfirmation(null);
  }} aria-labelledby="panel-title">
<div className="panel-top">
<h2 id="panel-title">{titles[panel]}</h2>
<button onClick={() => {
    setPanel(null);
    setConfirmation(null);
  }} aria-label="Fechar painel">Fechar ×</button>
</div>
<div className="panel-body">{hasRecovery && (panel === "help" || panel === "transfer") && <div className="recovery-actions"><p>Uma cópia do conteúdo original está disponível para recuperação.</p><button onClick={downloadRecovery}>Baixar dados originais</button></div>}{notice && <p className="panel-feedback" role="status">{notice}</p>}
 {panel === "menu" ? <div className="menu-options">
<button onClick={() => setPanel("library")}>Meus personagens · {saved.length}</button>
<button onClick={() => setPanel("families")}>Aprofundar · consultar guias</button>
<button onClick={() => setPanel("draw")}>Sortear · manter cartas</button>
<button onClick={() => requestAction({ type: "new" })}>Nova combinação</button>
<button onClick={() => setPanel("transfer")}>Importar · exportar</button>
<button onClick={() => setPanel("help")}>Como jogar</button>
</div> : panel === "help" ? <div className="help-copy">
<p>Escolha um Desejo, uma Forma de agir e uma Expressão. As cartas são convites para interpretar, não resultados obrigatórios.</p>
<p>Use as setas do teclado ou da mesa, deslize ou role horizontalmente na mão. Shift + rolagem também troca cartas. A rolagem vertical continua livre. Vire a carta para consultar como levá-la à cena.</p>
<p>L traz um vínculo, P uma pressão. N só entra se dois valores realmente importarem. U/G são consulta, sem entrar no sorteio.</p>
<p>Suas combinações ficam neste navegador. Dados antigos continuam guardados e saem nas exportações, mesmo sem campos de edição. Ao trocar cartas, os textos anteriores são preservados.</p>
</div> : panel === "confirm" ? <div className="confirmation">
<p>{confirmation?.type === "delete" ? "Esta ação exclui o personagem salvo. O rascunho aberto será preservado." : "O rascunho atual será substituído. Salve ou exporte antes se quiser guardá-lo. Os personagens salvos continuam na biblioteca."}</p>
<div className="action-row">
<button onClick={() => {
    setConfirmation(null);
    setPanel(confirmation?.type === "delete" ? "library" : null);
  }}>Cancelar</button>{confirmation?.type !== "delete" && <button disabled={count < 3} onClick={() => {
    save();
    setPanel(null);
    setConfirmation(null);
  }}>Salvar atual e ficar</button>}<button className="danger-action" onClick={() => perform(confirmation)}>{confirmation?.type === "delete" ? "Excluir salvo" : "Substituir rascunho"}</button>
</div>
</div> : panel === "families" ? <>
<p className="panel-description">Aprofunde quando servir à história. Retirar uma camada guarda a carta e seu texto para depois.</p>
<div className="family-choices">{["L", "P", "N"].map((f) => <article key={f}>
<button className="family-choice" onClick={() => inspectFamily(f)}>
<b>{f}</b>
<strong>{FAMILIES[f]}</strong>
<span>{QUESTIONS[f]}</span>
<span>Explorar cartas ↗</span>
</button>
<button className="chip" aria-pressed={draft.enabled.includes(f)} onClick={() => toggleOptional(f)}>{draft.enabled.includes(f) ? "✓ Na combinação · retirar" : "+ Adicionar camada"}</button>
</article>)}</div>
<h3 className="panel-subtitle">Guias de consulta</h3>
<div className="action-row">{["U", "G"].map((f) => <button key={f} onClick={() => inspectFamily(f)}>{FAMILIES[f]} ↗</button>)}</div>
</> : panel === "draw" ? <>
<p className="panel-description">Sorteie as camadas ativas. Cartas mantidas ficam no lugar. Textos anteriores continuam guardados.</p>
<div className="draw-choices">{ORDER.filter((f) => draft.enabled.includes(f)).map((f) => <article key={f}>
<div>
<strong>{FAMILIES[f]}</strong>
<p>{draft.cards[f] || "Ainda sem carta"}{byCode[draft.cards[f]] ? " · " + byCode[draft.cards[f]].titulo : ""}</p>
</div>
<button className="chip" aria-pressed={draft.locks.includes(f)} onClick={() => toggleLock(f)}>{draft.locks.includes(f) ? "✓ Mantida" : "Manter"}</button>
<button disabled={draft.locks.includes(f)} onClick={() => draw(f)}>Trocar</button>
</article>)}</div>
<h3 className="panel-subtitle">Módulos no sorteio</h3>
<div className="action-row">{Object.entries(MODULES).map(([key, label]) => <button className="chip" key={key} aria-pressed={modules.includes(key)} onClick={() => {
    setStorageReady(true);
    setModules((m) => m.includes(key) ? m.filter((v) => v !== key) : [...m, key]);
  }}>{modules.includes(key) ? "✓ " : ""}{label}</button>)}</div>{!modules.length && <p className="inline-warning">Escolha pelo menos um módulo para sortear.</p>}<button className="panel-primary" disabled={!modules.length} onClick={() => draw()}>Sortear combinação</button>
</> : panel === "transfer" ? <>
<p className="panel-description">JSON preserva a ficha completa e permite importar em outro navegador. Texto leva a combinação para suas anotações. A importação cria um salvo e mantém o rascunho atual.</p>
<div className="menu-options">
<button onClick={() => exportCharacter(draft, "json")}>Exportar combinação · JSON</button>
<button onClick={() => exportCharacter(draft, "md")}>Exportar texto · Markdown</button>
<button onClick={() => importInput.current.click()}>Importar ficha · JSON 5.0 / 5.1</button>
</div>
</> : <>
<div className="library-toolbar">
<button onClick={() => importInput.current.click()}>Importar ficha</button>
<button onClick={() => requestAction({ type: "new" })}>Nova combinação</button>
</div>
<div className="library">{saved.length ? saved.map((c) => <article className="character-card" key={c.id}>
<button className="character-open" onClick={() => requestAction({ type: "open", character: c })}>
<div className="library-art">{CORE.map((f) => c.cards?.[f] && <Art key={f} code={c.cards[f]} />)}</div>
<h3>{c.name || "Combinação sem nome"}</h3>
<p>{ORDER.filter((f) => c.enabled.includes(f)).map((f) => c.cards?.[f]).filter(Boolean).join(" · ")}</p>
<span>Abrir combinação ↗</span>
</button>
<div className="character-actions">
<button onClick={() => duplicate(c)}>Duplicar</button>
<button onClick={() => exportCharacter(c, "json")}>JSON</button>
<button onClick={() => exportCharacter(c, "md")}>Texto</button>
<button className="delete-button" onClick={() => {
    setConfirmation({ type: "delete", id: c.id });
    setPanel("confirm");
  }}>Excluir</button>
</div>
</article>) : <p>Seu elenco começa com três cartas. Escolha as suas e salve uma combinação.</p>}</div>
</>}
 </div>
</dialog>}
 </div>;
}
