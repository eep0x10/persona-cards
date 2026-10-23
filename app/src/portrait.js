// Portraits are processed locally and stored in the character's browser data.
export const MAX_PORTRAIT_FILE_BYTES = 10 * 1024 * 1024;
export const MAX_PORTRAIT_DATA_URL_LENGTH = 350000;
const MIME_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);

function matchesSignature(bytes, mime) {
  if (mime === "image/jpeg") return bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255;
  if (mime === "image/png") return [137, 80, 78, 71, 13, 10, 26, 10].every((v, i) => bytes[i] === v);
  if (mime === "image/webp") return bytes.length >= 12 &&
    [82, 73, 70, 70].every((v, i) => bytes[i] === v) &&
    [87, 69, 66, 80].every((v, i) => bytes[i + 8] === v);
  return false;
}

export function validatePortrait(value) {
  if (value === undefined || value === "") return true;
  if (typeof value !== "string" || value.length > MAX_PORTRAIT_DATA_URL_LENGTH) return false;
  const match = /^data:(image\/(?:jpeg|png|webp));base64,/.exec(value);
  if (!match) return false;
  const payload = value.slice(match[0].length);
  if (!payload || payload.length % 4 !== 0 || !/^[A-Za-z0-9+/]+={0,2}$/.test(payload)) return false;
  try {
    const prefix = atob(payload.slice(0, 16));
    return matchesSignature(Uint8Array.from(prefix, (c) => c.charCodeAt(0)), match[1]);
  } catch { return false; }
}

async function decodeImage(file) {
  if (typeof createImageBitmap === "function") return createImageBitmap(file);
  const url = URL.createObjectURL(file);
  try {
    return await new Promise((resolve, reject) => {
      const image = new Image();
      image.onload = () => resolve(image);
      image.onerror = () => reject(new Error("Não foi possível ler essa imagem."));
      image.src = url;
    });
  } finally { URL.revokeObjectURL(url); }
}

export async function preparePortrait(file) {
  if (!file) return null;
  if (!MIME_TYPES.has(file.type)) throw new Error("Escolha uma foto JPEG, PNG ou WebP.");
  if (!file.size || file.size > MAX_PORTRAIT_FILE_BYTES) throw new Error("A foto deve ter até 10 MB.");
  const signature = new Uint8Array(await file.slice(0, 12).arrayBuffer());
  if (!matchesSignature(signature, file.type)) throw new Error("O conteúdo da imagem não corresponde ao formato informado.");
  let image;
  try {
    try { image = await decodeImage(file); }
    catch { throw new Error("Não foi possível ler essa imagem. Escolha outro arquivo JPEG, PNG ou WebP."); }
    if (!image.width || !image.height) throw new Error("Imagem sem dimensões válidas.");
    let scale = Math.min(1, 960 / Math.max(image.width, image.height));
    const canvas = document.createElement("canvas");
    for (let attempt = 0; attempt < 8; attempt++) {
      canvas.width = Math.max(1, Math.round(image.width * scale));
      canvas.height = Math.max(1, Math.round(image.height * scale));
      const context = canvas.getContext("2d");
      if (!context) throw new Error("Não foi possível preparar a foto neste navegador.");
      context.fillStyle = "#ffffff";
      context.fillRect(0, 0, canvas.width, canvas.height);
      context.drawImage(image, 0, 0, canvas.width, canvas.height);
      for (const quality of [0.82, 0.7, 0.58, 0.46]) {
        const result = canvas.toDataURL("image/jpeg", quality);
        if (validatePortrait(result) && result.startsWith("data:image/jpeg;")) return result;
      }
      scale *= 0.75;
    }
    throw new Error("A foto continua muito grande. Escolha uma imagem mais simples.");
  } catch (error) {
    throw new Error(error?.message || "Não foi possível ler essa imagem.");
  } finally { image?.close?.(); }
}
