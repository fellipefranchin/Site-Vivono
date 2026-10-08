# -*- coding: utf-8 -*-
import pickle, html
core=open("map_core.svg").read()
ctx=pickle.load(open("map_ctx.pkl","rb"))
pinX,pinY=ctx['pinX'],ctx['pinY']
backc=ctx['back_c']; busX,busY=ctx['bus'][0]
jose_ang=ctx['jose'][2]

DEFS=('<defs>'
 '<filter id="cc-soft2" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#3a1a1f" flood-opacity="0.28"/></filter>'
 '<radialGradient id="cc-paper" cx="42%" cy="30%" r="95%"><stop offset="0%" stop-color="#F5F0EA"/><stop offset="100%" stop-color="#ECE3D6"/></radialGradient>'
 '<linearGradient id="cc-pin" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#6d3038"/><stop offset="100%" stop-color="#54272E"/></linearGradient>'
 '</defs>')

def esc(s): return html.escape(s, quote=True)

def T(x,y,txt,size,color="#3a2b26",weight=600,anchor="start",rot=0,serif=False,ls=0,halo=3.4,i18n=None):
    fam="'Playfair Display',serif" if serif else "'Poppins',sans-serif"
    tr=(' transform="rotate(%s %.1f %.1f)"'%(rot,x,y)) if rot else ''
    at=(' data-i18n="%s"'%i18n) if i18n else ''
    lss=(' letter-spacing="%s"'%ls) if ls else ''
    halo_at=(' stroke="#F5F0E9" stroke-width="%s" paint-order="stroke" stroke-linejoin="round"'%halo) if halo else ''
    return ('<text x="%.1f" y="%.1f"%s text-anchor="%s" font-family="%s" font-size="%s" font-weight="%s"%s fill="%s"%s%s>%s</text>'
            %(x,y,tr,anchor,fam,size,weight,lss,color,halo_at,at,esc(txt)))

def overlay(mode):
    site = (mode=='site')
    def L(pt,en): return pt if mode!='en' else en
    def di(k): return (' data-i18n="%s"'%k) if site else ''
    o=[]
    # walking route: parking -> stairs -> door
    o.append('<path d="M%.0f,%.0f Q505,468 492,466 Q450,430 %.0f,%.0f" fill="none" stroke="#B8863C" stroke-width="5" stroke-dasharray="1.5 11" stroke-linecap="round"/>'
             %(backc[0],backc[1],pinX+4,pinY+6))
    # Palacio arrow (north, out of frame)
    o.append('<g transform="translate(430,64)"><path d="M0 -20 L9 2 L0 -5 L-9 2 Z" fill="#54272E"/></g>')
    o.append(T(452,60,L("PALÁCIO DE MAFRA","MAFRA PALACE"),15.5,"#54272E",700,"start",0,False,1.5))
    o.append(T(452,80,L("· 3 min a pé","· 3 min walk"),12.5,"#7a6a60",500,"start"))
    # Tapada (green, rotated)
    o.append(T(884,616,L("TAPADA NACIONAL","TAPADA PARK"),15,"#5d6b47",700,"middle",-90,False,2))
    # street names
    o.append(T(474,548,"Rua José Silvestre",13.5,"#8a7862",600,"middle",jose_ang,False,.5))
    o.append(T(352,560,"Av. das Forças Armadas",12.5,"#9a8a72",600,"middle",-88,False,.5))
    # free parking title + P badge + GRATIS
    o.append(T(628,300,L("Estacionamento gratuito","Free car park"),16,"#2A1C1E",600,"middle",0,False,0,3.6,('chegar.m.lot' if site else None)))
    o.append('<g transform="translate(588,432)" filter="url(#cc-soft2)"><circle r="26" fill="#1F3125"/><text x="0" y="9.5" text-anchor="middle" font-family="\'Playfair Display\',serif" font-size="30" font-weight="700" fill="#F4EFE9">P</text></g>')
    o.append('<g transform="translate(560,462)"><rect width="80" height="26" rx="13" fill="#54272E"/><text x="40" y="18" text-anchor="middle" font-family="\'Poppins\',sans-serif" font-size="14" font-weight="600" letter-spacing="1" fill="#F4EFE9"%s>%s</text></g>'
             %(di('chegar.m.free'), esc(L("GRÁTIS","FREE"))))
    # stairs pill
    o.append('<g transform="translate(506,500)"><rect width="200" height="30" rx="15" fill="#FFFFFF" stroke="#C2A878" stroke-width="1.2"/>'
             '<g transform="translate(20,15)" stroke="#54272E" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M-6 -4 L-2 -4 L-2 0 L2 0 L2 4 L6 4"/></g>'
             '<text x="36" y="20" font-family="\'Poppins\',sans-serif" font-size="14.5" font-weight="600" fill="#2A1C1E"%s>%s</text></g>'
             %(di('chegar.m.steps'), esc(L("descer as escadas · ±1 min","down the stairs · ±1 min"))))
    # bus terminal
    o.append('<g transform="translate(%.0f,%.0f)" filter="url(#cc-soft2)"><rect x="-22" y="-16" width="44" height="32" rx="8" fill="#2C4534"/>'
             '<rect x="-15" y="-9" width="9" height="10" rx="2" fill="#ECE0C6"/><rect x="-3" y="-9" width="9" height="10" rx="2" fill="#ECE0C6"/><rect x="9" y="-9" width="6" height="10" rx="2" fill="#ECE0C6"/>'
             '<circle cx="-11" cy="12" r="4" fill="#1b120f"/><circle cx="11" cy="12" r="4" fill="#1b120f"/></g>'%(busX,busY))
    o.append(T(busX,busY+34,L("Estação de autocarros","Bus station"),13.5,"#3a2b26",600,"middle",0,False,0,3.6,('chegar.m.bus' if site else None)))
    o.append(T(busX,busY+51,"Alto da Vela",11.5,"#7a6a60",500,"middle"))
    # destination pin + callout
    o.append('<g transform="translate(%.0f,%.0f)" filter="url(#cc-soft2)"><path d="M0 2 C -20 -22 -23 -32 -23 -42 A 23 23 0 1 1 23 -42 C 23 -32 20 -22 0 2 Z" fill="url(#cc-pin)" stroke="#C2A878" stroke-width="2"/>'
             '<path d="M0 -54 L3.6 -46.5 L11.5 -45.6 L5.8 -40 L7.2 -32.2 L0 -36 L-7.2 -32.2 L-5.8 -40 L-11.5 -45.6 L-3.6 -46.5 Z" fill="#F4EFE9"/></g>'%(pinX,pinY))
    o.append('<path d="M368 322 L%.0f %.0f" stroke="#54272E" stroke-width="2" stroke-dasharray="3 4" fill="none"/>'%(pinX-16,pinY-30))
    o.append('<g transform="translate(196,300)"><rect width="172" height="46" rx="10" fill="#54272E" filter="url(#cc-soft2)"/>'
             '<text x="18" y="21" font-family="\'Playfair Display\',serif" font-size="21" font-weight="700" fill="#F4EFE9">Vívono</text>'
             '<text x="18" y="38" font-family="\'Poppins\',sans-serif" font-size="12.5" font-weight="500" fill="#e7cfa0"%s>%s</text></g>'
             %(di('chegar.m.no'), esc(L("nº 12 · à sua porta","no. 12 · at your door"))))
    # compass
    o.append('<g transform="translate(936,96)"><circle r="24" fill="#F6F1E9" stroke="#C2A878" stroke-width="1.4"/><path d="M0 -16 L6 4 L0 -1 L-6 4 Z" fill="#54272E"/>'
             '<text x="0" y="-26" text-anchor="middle" font-family="\'Poppins\',sans-serif" font-size="12" font-weight="700" fill="#8b7a5f">N</text></g>')
    return "\n".join(o)

def svg_map(mode):
    return ('<svg id="cc-map" viewBox="0 0 1000 816" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Mapa Como Chegar · Vívono">'
            '<style>#cc-map text{font-family:\'Poppins\',sans-serif}</style>'+DEFS+
            '<rect x="0" y="0" width="1000" height="816" fill="url(#cc-paper)"/>'+core+'\n'+overlay(mode)+'</svg>')

open("site_map.svg","w").write(svg_map('site'))

def card(lang):
    L=lambda pt,en: pt if lang=='pt' else en
    inner=('<svg viewBox="0 0 1000 816" x="40" y="176" width="1000" height="816" xmlns="http://www.w3.org/2000/svg">'
           '<style>text{font-family:\'Poppins\',sans-serif}</style>'+DEFS+
           '<clipPath id="cc-clip"><rect x="0" y="0" width="1000" height="816" rx="18"/></clipPath>'
           '<rect x="0" y="0" width="1000" height="816" rx="18" fill="url(#cc-paper)"/>'
           '<g clip-path="url(#cc-clip)">'+core+'\n'+overlay(lang)+'</g>'
           '<rect x="1" y="1" width="998" height="814" rx="18" fill="none" stroke="#C2A878" stroke-opacity="0.55" stroke-width="1.5"/></svg>')
    head=('<text x="62" y="96" fill="#9a7b3f" font-size="20" font-weight="600" letter-spacing="4.5">VÍVONO · MAFRA</text>'
          '<text x="58" y="152" font-family="\'Playfair Display\',serif" fill="#2A1C1E" font-size="62" font-weight="700">%s</text>'
          '<g><rect x="716" y="74" width="298" height="52" rx="26" fill="#54272E"/><circle cx="746" cy="100" r="15" fill="#C2A878"/>'
          '<text x="746" y="107" text-anchor="middle" fill="#3A1A1F" font-size="19" font-weight="700">P</text>'
          '<text x="772" y="107" fill="#F4EFE9" font-size="19" font-weight="500">%s</text></g>'
          %(L("Como Chegar","How to Find Us"), L("Grátis, mesmo atrás","Free, right behind")))
    foot=('<text x="60" y="1004" fill="#6B5D56" font-size="21" font-weight="500">R. José Silvestre 12 · 2640-497 Mafra · Portugal</text>'
          '<text x="60" y="1050" font-family="\'Playfair Display\',serif" fill="#54272E" font-size="30" font-weight="800" letter-spacing="2">VÍVONO</text>'
          '<text x="1020" y="1050" text-anchor="end" fill="#6B5D56" font-size="21" font-weight="600">vivono.pt</text>')
    doc=('<!doctype html><html lang="%s"><head><meta charset="utf-8">'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@400;500;600;700&display=swap">'
         '<style>html,body{margin:0;background:#fff}#c{width:1080px;height:1080px}</style></head><body>'
         '<div id="c"><svg width="1080" height="1080" viewBox="0 0 1080 1080" xmlns="http://www.w3.org/2000/svg">'
         '<rect width="1080" height="1080" fill="#F1E7DA"/>'
         '<rect x="26" y="26" width="1028" height="1028" rx="30" fill="none" stroke="#C2A878" stroke-opacity="0.5" stroke-width="1.5"/>'
         '%s%s%s</svg></div></body></html>'%(lang,head,inner,foot))
    open("card_%s.html"%lang,"w").write(doc)

card('pt'); card('en')

def story(lang):
    L=lambda pt,en: pt if lang=='pt' else en
    W,H=1080,1920
    # map occupies middle
    mapsvg=('<svg viewBox="0 0 1000 816" x="40" y="330" width="1000" height="816" xmlns="http://www.w3.org/2000/svg">'
            '<style>text{font-family:\'Poppins\',sans-serif}</style>'+DEFS+
            '<clipPath id="cc-clip"><rect x="0" y="0" width="1000" height="816" rx="20"/></clipPath>'
            '<rect x="0" y="0" width="1000" height="816" rx="20" fill="url(#cc-paper)"/>'
            '<g clip-path="url(#cc-clip)">'+core+'\n'+overlay(lang)+'</g>'
            '<rect x="1" y="1" width="998" height="814" rx="20" fill="none" stroke="#C2A878" stroke-opacity="0.55" stroke-width="1.5"/></svg>')
    def tile(x,num,l1,l2):
        return ('<g transform="translate(%d,1352)">'
                '<rect width="404" height="120" rx="14" fill="#EDE5DA"/>'
                '<text x="28" y="80" font-family="\'Playfair Display\',serif" font-size="56" font-weight="800" fill="#54272E">%s</text>'
                '<text x="152" y="52" font-family="\'Poppins\',sans-serif" font-size="21" font-weight="500" fill="#5c4f48">%s</text>'
                '<text x="152" y="80" font-family="\'Poppins\',sans-serif" font-size="21" font-weight="500" fill="#5c4f48">%s</text>'
                '</g>'%(x,esc(num),esc(l1),esc(l2)))
    info=('<rect x="60" y="1200" width="960" height="344" rx="22" fill="#F4EFE9" stroke="#C2A878" stroke-width="1.5"/>'
          '<text x="96" y="1258" font-family="\'Poppins\',sans-serif" font-size="18" font-weight="600" letter-spacing="2" fill="#9a7b3f">%s</text>'
          '<text x="94" y="1314" font-family="\'Playfair Display\',serif" font-size="40" font-weight="700" fill="#54272E">Parque Intermodal Alto da Vela</text>'
          '%s%s'
          '<text x="96" y="1520" font-family="\'Poppins\',sans-serif" font-size="23" font-weight="300" fill="#5c4f48">%s</text>'
          '<g transform="translate(60,1600)"><circle cx="30" cy="24" r="30" fill="#C2A878"/>'
          '<g transform="translate(30,24)" fill="none" stroke="#3a1a1f" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M0 13 c-8 -10 -11 -13 -11 -18 a11 11 0 1 1 22 0 c0 5 -3 8 -11 18 z"/><circle cx="0" cy="-5" r="4"/></g>'
          '<text x="82" y="18" font-family="\'Playfair Display\',serif" font-size="28" font-weight="700" fill="#54272E">R. José Silvestre 12</text>'
          '<text x="82" y="48" font-family="\'Poppins\',sans-serif" font-size="21" font-weight="400" fill="#5c4f48">2640-497 Mafra · Portugal</text></g>'
          %(L("ESTACIONAMENTO GRATUITO · MESMO ATRÁS","FREE PARKING · RIGHT BEHIND US"),
            tile(96,"232",L("lugares para","spaces for"),L("automóveis","cars")),
            tile(520,"17",L("lugares para","spaces for"),L("autocarros","coaches")),
            L("Desça as escadas e chega à nossa porta, a cerca de 1 min a pé.","Come down the stairs, right to our door, about 1 min on foot.")))
    head=('<text x="60" y="150" font-family="\'Poppins\',sans-serif" fill="#9a7b3f" font-size="24" font-weight="600" letter-spacing="5">MAFRA · PORTUGAL</text>'
          '<text x="56" y="240" font-family="\'Playfair Display\',serif" fill="#2A1C1E" font-size="78" font-weight="700">%s</text>'
          '<g transform="translate(60,272)"><rect width="600" height="56" rx="28" fill="#54272E"/>'
          '<circle cx="34" cy="28" r="17" fill="#C2A878"/><text x="34" y="35" text-anchor="middle" font-family="\'Poppins\',sans-serif" font-size="21" font-weight="700" fill="#3A1A1F">P</text>'
          '<text x="64" y="36" font-family="\'Poppins\',sans-serif" font-size="22" font-weight="500" fill="#F4EFE9">%s</text></g>'
          %(L("Como Chegar","How to Find Us"), L("Estacionamento gratuito, mesmo atrás","Free parking, right behind us")))
    doc=('<!doctype html><html lang="%s"><head><meta charset="utf-8">'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap">'
         '<style>html,body{margin:0;background:#fff}#c{width:1080px;height:1920px}</style></head><body>'
         '<div id="c"><svg width="1080" height="1920" viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
         '<rect width="1080" height="1920" fill="#F1E7DA"/>'
         '<rect x="26" y="26" width="1028" height="1868" rx="30" fill="none" stroke="#C2A878" stroke-opacity="0.5" stroke-width="1.5"/>'
         '%s%s%s</svg></div></body></html>'%(lang,head,mapsvg,info))
    open("story_%s.html"%lang,"w").write(doc)

story('pt'); story('en')
print("wrote site_map.svg (%d bytes), card_pt/en.html, story_pt/en.html"%len(open('site_map.svg').read()))
