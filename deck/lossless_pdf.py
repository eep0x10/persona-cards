"""Lossless PDF image encoding: preserve every RGB/alpha sample, add PNG predictors.

ReportLab's unfiltered RGB streams are larger than the source PNG spritesheets.
This changes PDF storage only; it does not resize, recolor or edit the artwork.
"""
from __future__ import annotations
import hashlib
from io import BytesIO
from pathlib import Path
import struct

from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, NumberObject


def optimize(path:Path)->dict:
    original_size=path.stat().st_size
    reader=PdfReader(str(path))
    writer=PdfWriter();writer.clone_document_from_reader(reader)
    seen=set();checked=0
    def visit(obj):
        nonlocal checked
        obj=obj.get_object()
        if id(obj) in seen:return
        seen.add(id(obj))
        if obj.get('/Subtype')=='/Image':
            mode={'/DeviceRGB':'RGB','/DeviceGray':'L'}.get(str(obj.get('/ColorSpace')))
            if mode and obj.get('/BitsPerComponent')==8:
                width,height=int(obj['/Width']),int(obj['/Height'])
                pixels=obj.get_data()
                image=Image.frombytes(mode,(width,height),pixels)
                png=BytesIO();image.save(png,format='PNG',compress_level=9)
                encoded=png.getvalue();offset=8;idat=[]
                while offset<len(encoded):
                    size=struct.unpack('>I',encoded[offset:offset+4])[0]
                    if encoded[offset+4:offset+8]==b'IDAT':idat.append(encoded[offset+8:offset+8+size])
                    offset+=12+size
                obj._data=b''.join(idat)
                obj[NameObject('/Filter')]=NameObject('/FlateDecode')
                obj[NameObject('/DecodeParms')]=DictionaryObject({
                    NameObject('/Predictor'):NumberObject(15),NameObject('/Colors'):NumberObject(3 if mode=='RGB' else 1),
                    NameObject('/BitsPerComponent'):NumberObject(8),NameObject('/Columns'):NumberObject(width)})
                if hasattr(obj,'decoded_self'):obj.decoded_self=None
                if hashlib.sha256(obj.get_data()).digest()!=hashlib.sha256(pixels).digest():
                    raise ValueError('PDF image encoding changed pixel samples')
                checked+=1
            if obj.get('/SMask'):visit(obj['/SMask'])
        resources=obj.get('/Resources')
        if resources:
            for child in resources.get('/XObject',{}).values():visit(child)
    for page in writer.pages:visit(page)
    temp=path.with_suffix('.optimized.pdf')
    with temp.open('wb') as output:writer.write(output)
    reader.close()
    if temp.stat().st_size>=original_size:
        temp.unlink()
    else:temp.replace(path)
    return dict(images_pixel_verified=checked,before_bytes=original_size,after_bytes=path.stat().st_size)
