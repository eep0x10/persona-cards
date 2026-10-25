import atlas from '../../deck/illustration_sheets_5_2.json';
import { ORDER, FAMILY_LABELS, JOURNEY_LABELS } from './model.js';
const LABELS=FAMILY_LABELS;
const ART=Object.fromEntries(atlas.sheets.flatMap(sheet=>{const columns=sheet.columns||3,rows=sheet.rows||2;return sheet.codes.map((code,index)=>[code,{file:sheet.file,columns,rows,col:index%columns,row:Math.floor(index/columns)}]);}));
const SAFE={CV02:[.04,0,0,0],N04:[0,0,.12,0],U02:[.09,0,.11,0],G02:[.09,.09,.13,0]};
const loadImage=source=>new Promise((resolve,reject)=>{const image=new Image();const timer=setTimeout(()=>reject(Error('A imagem demorou para abrir. Tente novamente.')),12000);image.onload=()=>{clearTimeout(timer);resolve(image);};image.onerror=()=>{clearTimeout(timer);reject(Error('Não foi possível carregar uma imagem da carta. Tente novamente.'));};image.src=source;});
function lines(ctx,text,width){
 const result=[];
 for(const paragraph of String(text||'').split('\n')){
  let line='';
  for(const word of paragraph.split(/\s+/).filter(Boolean)){
   if(ctx.measureText(word).width>width){
    if(line){result.push(line);line='';}
    let fragment='';for(const letter of word){if(ctx.measureText(fragment+letter).width>width){result.push(fragment);fragment=letter;}else fragment+=letter;}line=fragment;
   }else if(line&&ctx.measureText(line+' '+word).width>width){result.push(line);line=word;}else line+=(line?' ':'')+word;
  }
  result.push(line);
 }
 return result;
}
function text(ctx,rows,x,y,lineHeight){rows.forEach((row,index)=>ctx.fillText(row,x,y+index*lineHeight));return y+rows.length*lineHeight;}
function art(ctx,image,code,x,y,size){const a=ART[code];if(!a||!image)return;const cellW=image.naturalWidth/a.columns,cellH=image.naturalHeight/a.rows;const [left,right,top,bottom]=SAFE[code]||[0,0,0,0];ctx.save();ctx.beginPath();ctx.rect(x+left*size,y+top*size,size*(1-left-right),size*(1-top-bottom));ctx.clip();ctx.drawImage(image,a.col*cellW,a.row*cellH,cellW,cellH,x,y,size,size);ctx.restore();}
function cover(ctx,image,x,y,width,height){const scale=Math.max(width/image.naturalWidth,height/image.naturalHeight);const sw=width/scale,sh=height/scale;ctx.drawImage(image,(image.naturalWidth-sw)/2,(image.naturalHeight-sh)/2,sw,sh,x,y,width,height);}

/** Raster-only canvas export: actual portrait, illustrations and complete readable text. */
export async function downloadCharacterPng(character,lookup,edition){
 await document.fonts?.ready;
 const canvas=document.createElement('canvas');const ctx=canvas.getContext('2d');if(!ctx)throw Error('Este navegador não conseguiu criar a imagem.');
 const families=ORDER.filter(f=>lookup[character.cards[f]]);
 const imageFiles=[...new Set([...families.map(f=>ART[character.cards[f]]?.file),ART.G07?.file].filter(Boolean))];
 const loaded=await Promise.all(imageFiles.map(async file=>[file,await loadImage(`${import.meta.env.BASE_URL}art/${file}`)]));
 const images=Object.fromEntries(loaded);const portrait=character.portrait?await loadImage(character.portrait).catch(()=>null):null;
 ctx.font='bold 66px Georgia';const nameLines=lines(ctx,character.name,620);
 ctx.font='28px Arial';const roleLines=character.role?lines(ctx,character.role,620):[];
 ctx.font='27px Georgia';const contextLines=character.context?lines(ctx,character.context,620):[];
 ctx.font='bold 20px Arial';const codeLines=lines(ctx,families.map(f=>character.cards[f]).join('  ·  '),620);
 const headerHeight=Math.max(390,130+nameLines.length*74+roleLines.length*36+contextLines.length*36+codeLines.length*28+70);
 const layers=families.map(family=>{ctx.font='bold 34px Georgia';const title=lines(ctx,lookup[character.cards[family]].titulo,850);ctx.font='28px Arial';const body=lines(ctx,character.fields[family],850);return {family,title,body,height:Math.max(148,52+title.length*42+body.length*39+34)};});
 ctx.font='27px Arial';const journey=Object.entries(JOURNEY_LABELS).map(([key,label])=>({label,body:lines(ctx,character.journey?.[key]||'Pendente.',1040)}));
 const journeyHeight=165+journey.reduce((total,item)=>total+48+item.body.length*38,0);
 ctx.font='27px Arial';const notes=character.notes?lines(ctx,character.notes,1040):[];
 const height=64+headerHeight+layers.reduce((sum,layer)=>sum+layer.height,0)+journeyHeight+(notes.length?110+notes.length*38:0)+100;
 if(height>16000)throw Error('Há texto demais para um único PNG neste navegador. Guarde a ficha completa em JSON ou exporte texto.');
 canvas.width=1200;canvas.height=Math.ceil(height);
 ctx.fillStyle='#143e33';ctx.fillRect(0,0,1200,height);ctx.fillStyle='#f5eddb';ctx.beginPath();ctx.roundRect(26,26,1148,height-52,22);ctx.fill();
 const px=66,py=66,pw=330,ph=headerHeight-42;
 ctx.save();ctx.beginPath();ctx.roundRect(px,py,pw,ph,12);ctx.clip();ctx.fillStyle='#e5ddc6';ctx.fillRect(px,py,pw,ph);
 if(portrait)cover(ctx,portrait,px,py,pw,ph);else{const code=character.cards.D;art(ctx,images[ART[code]?.file],code,px+15,py+(ph-300)/2,300);}ctx.restore();
 ctx.fillStyle='#aa402b';ctx.font='bold 17px Arial';ctx.fillText('CARTA DO PERSONAGEM',438,94);
 ctx.fillStyle='#123b32';ctx.font='bold 66px Georgia';let y=text(ctx,nameLines,438,156,74)+8;
 ctx.font='28px Arial';y=text(ctx,roleLines,438,y,36)+12;
 ctx.fillStyle='#ad432b';ctx.font='bold 20px Arial';y=text(ctx,codeLines,438,y,28)+20;
 ctx.fillStyle='#344d40';ctx.font='27px Georgia';text(ctx,contextLines,438,y,36);
 y=64+headerHeight;
 for(const layer of layers){const code=character.cards[layer.family];ctx.strokeStyle='#c2baa0';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(66,y);ctx.lineTo(1134,y);ctx.stroke();art(ctx,images[ART[code]?.file],code,66,y+24,110);ctx.fillStyle='#a6422d';ctx.font='bold 17px Arial';ctx.fillText(`${LABELS[layer.family].toUpperCase()} · ${code}`,205,y+34);ctx.fillStyle='#123b32';ctx.font='bold 34px Georgia';let end=text(ctx,layer.title,205,y+79,42);ctx.font='28px Arial';text(ctx,layer.body,205,end+2,39);y+=layer.height;}
 y+=30;art(ctx,images[ART.G07?.file],'G07',66,y-8,86);ctx.fillStyle='#a6422d';ctx.font='bold 23px Georgia';ctx.fillText('CHAMADO/DESTINO · G07',178,y+20);y+=100;
 for(const item of journey){ctx.fillStyle='#a6422d';ctx.font='bold 17px Arial';ctx.fillText(item.label.toUpperCase(),66,y);ctx.fillStyle='#344d40';ctx.font='27px Arial';y=text(ctx,item.body,66,y+34,38)+14;}
 if(notes.length){y+=36;ctx.fillStyle='#a6422d';ctx.font='bold 17px Arial';ctx.fillText('PARA LEVAR À CENA',66,y);ctx.fillStyle='#344d40';ctx.font='27px Arial';text(ctx,notes,66,y+42,38);}
 ctx.fillStyle='#6a715d';ctx.font='bold 17px Arial';ctx.fillText(`PERSONA CARDS · ${edition}`,66,height-54);ctx.font='italic 20px Georgia';ctx.textAlign='right';ctx.fillText('Personagens vivos. Escolhas reais.',1134,height-54);
 const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));if(!blob)throw Error('Não foi possível gerar o arquivo PNG.');
 const url=URL.createObjectURL(blob);const link=document.createElement('a');link.href=url;link.download=(character.name||'personagem').replace(/[<>:"/\\|?*]/g,'-')+'.png';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 return {width:canvas.width,height:canvas.height};
}
