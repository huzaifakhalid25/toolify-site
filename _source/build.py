#!/usr/bin/env python3
"""
Toolify site builder.
Run:  python3 _source/build.py
It re-creates: header/menu, footer, SEO tags, category pages, index.html, sitemap.xml, robots.txt, favicon.svg, 404.html
Your tool logic (the tool card + script inside each tools/*.html) is NOT touched.
"""
import json, re, os, html as H
from pathlib import Path

# ======================= SETTINGS (edit these) =======================
SITE_URL = "https://toolify-site-three.vercel.app"      # <- put your real domain here (no slash at the end), then run this script again
SITE_NAME = "Toolify"
TODAY = "2026-10-22"
ADS_ENABLED = False                      # keep False until Google AdSense approves you. Then set True and run this script again.
# =====================================================================

ROOT = Path(__file__).resolve().parent.parent
TOOLS = json.load(open(ROOT / '_source' / 'tools.json', encoding='utf-8'))
BY = {t['slug']: t for t in TOOLS}

CATS = [
 dict(slug='pdf-tools', name='PDF Tools', icon='fa-solid fa-file-pdf', color='red',
      h1='Free PDF Tools Online', short='Merge, split, rotate and create PDF files.',
      intro='Merge, split, rotate and number PDFs, and convert Word, images and text to PDF.',
      about='Our free PDF tools help you handle everyday document work without installing software. You can merge several PDFs into one, extract or delete pages, rotate pages, add page numbers, convert Word to PDF, convert text PDFs to Word, turn images into a PDF and convert text to PDF. Most PDF tools here run inside your browser, so your documents are not uploaded to a server.',
      steps=['Choose your PDF file(s) or type your text.', 'Set the options you need, such as page numbers or rotation.', 'Click the button and download your new PDF.']),
 dict(slug='image-tools', name='Image Tools', icon='fa-solid fa-image', color='emerald',
      h1='Free Image Tools Online', short='Compress, resize, crop, convert and edit images.',
      intro='Compress, resize, crop, convert, rotate and edit your pictures in seconds.',
      about='Edit photos quickly with our free online image tools. Compress large pictures for faster websites, resize for social media, crop to the perfect ratio, convert between PNG, JPG and WebP, add watermarks, apply filters, pick colors and generate favicons. All image processing happens on your device for speed and privacy.',
      steps=['Select the image from your phone or computer.', 'Choose the size, format or effect you want.', 'Click the button and download the result.']),
 dict(slug='text-tools', name='Text Tools', icon='fa-solid fa-font', color='indigo',
      h1='Free Text Tools Online', short='Count, convert, clean, compare and style text.',
      intro='Count words, change case, clean text, compare versions and create stylish fonts.',
      about='Text tools save time for students, writers, bloggers and developers. Count words and characters, change letter case, remove duplicate lines, find and replace, compare two texts, generate slugs and lorem ipsum, write Markdown, convert numbers to words and more. Paste your text, click once and copy the result.',
      steps=['Paste or type your text into the box.', 'Pick the option you need.', 'Click the button and copy the result.']),
 dict(slug='calculators', name='Calculators', icon='fa-solid fa-calculator', color='teal',
      h1='Free Online Calculators', short='Age, BMI, EMI, tax, zakat, percentage and more.',
      intro='Age, BMI, EMI, GST, zakat, percentage, discount and many more everyday calculators.',
      about='Free online calculators for daily life, money and studies. Calculate your exact age, BMI, loan EMI, compound interest, discounts, profit margin, GST or VAT, zakat, GPA, calories and percentages. Enter your numbers, press calculate and get clear results instantly.',
      steps=['Enter your numbers in the fields.', 'Select any option such as tax mode or time period.', 'Click calculate to see the result instantly.']),
 dict(slug='developer-tools', name='Developer Tools', icon='fa-solid fa-code', color='violet',
      h1='Free Developer Tools Online', short='JSON, Base64, hashes, regex, UUID, CSS and more.',
      intro='Format JSON, encode Base64, test regex, generate hashes and UUIDs, and more.',
      about='Handy developer utilities for coding every day. Format and validate JSON, convert CSV and JSON, encode and decode Base64, HTML and URLs, test regular expressions, decode JWT tokens, create hashes and UUIDs, minify CSS, build gradients and convert colors or number bases.',
      steps=['Paste your code or data into the input box.', 'Choose the operation or format.', 'Click the button and copy the output.']),
 dict(slug='media-social', name='Media & Social Tools', icon='fa-solid fa-share-nodes', color='cyan',
      h1='Free Media & Social Media Tools', short='QR codes, voice tools, thumbnails and chat links.',
      intro='QR codes, voice typing, text to speech, YouTube thumbnails and WhatsApp links.',
      about='Tools for creators and social media users. Generate QR codes, download YouTube thumbnails, create WhatsApp chat links, convert text to speech, type with your voice and check the correct image sizes for every social platform.',
      steps=['Enter your link, text or choose your file.', 'Adjust the settings if needed.', 'Click the button to get your result.']),
 dict(slug='utilities', name='Daily Utilities', icon='fa-solid fa-toolbox', color='orange',
      h1='Free Daily Utility Tools', short='Passwords, timers, notepad, random pickers and more.',
      intro='Password generator, timers, notepad, tasbih counter, random pickers and more.',
      about='Small tools you use again and again. Generate strong passwords, check password strength, run a stopwatch, countdown or pomodoro timer, keep quick notes, count tasbih, flip a coin, roll dice, pick random winners, practice typing and convert numbers to Roman numerals.',
      steps=['Open the tool and set your options.', 'Press the start or generate button.', 'Use the result right away.']),
]
CAT = {c['slug']: c for c in CATS}
for c in CATS: c['tools'] = [t for t in TOOLS if t['cat'] == c['slug']]
POPULAR = ['image-compressor', 'pdf-merge', 'image-to-pdf', 'qr-generator', 'word-counter', 'age-calculator', 'emi-calculator', 'yt-thumbnail']
APPCAT = {'developer-tools': 'DeveloperApplication', 'image-tools': 'MultimediaApplication', 'media-social': 'MultimediaApplication'}
PRIVACY = {
 'qr-generator': 'QR codes are created with a free QR service (api.qrserver.com), so the text you enter is sent to that service to generate the image.',
 'yt-thumbnail': 'Only the YouTube video link you paste is used. The thumbnail image is loaded directly from YouTube.',
 'speech-to-text': 'Speech recognition is provided by your browser (for example Chrome), which may send audio to its speech service to convert it into text.',
 'text-to-speech': 'Text is spoken by your own device using its built-in voices.',
}
E = H.escape
def ver(p): return int((ROOT / p).stat().st_mtime) if (ROOT / p).exists() else 1


# ------------------------------------------------------------------ shared pieces
def head(title, desc, path, R, jsonld=(), libs=(), og='website'):
    url = f'{SITE_URL}/{path}'
    ld = ''.join(f'\n    <script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in jsonld)
    lib = ''.join(f'\n    <script src="{l}"></script>' for l in libs)
    return f'''<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{E(title)}</title>
    <meta name="description" content="{E(desc, quote=True)}">
    <link rel="canonical" href="{url}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="theme-color" content="#4f46e5">
    <link rel="icon" href="{R}favicon.svg" type="image/svg+xml">
    <meta property="og:type" content="{og}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:title" content="{E(title, quote=True)}">
    <meta property="og:description" content="{E(desc, quote=True)}">
    <meta property="og:url" content="{url}">
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{E(title, quote=True)}">
    <meta name="twitter:description" content="{E(desc, quote=True)}">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com">
    <script src="https://cdn.tailwindcss.com"></script>{lib}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{R}style.css">{ld}'''


def header(R, cur_cat=None):
    cats = ''
    for c in CATS:
        items = ''.join(f'<a href="{R}tools/{t["slug"]}.html" data-t="{E(t["title"].lower())}">{E(t["title"])}</a>' for t in c['tools'])
        op = ' open' if c['slug'] == cur_cat else ''
        cats += f'''
        <div class="m-cat{op}" data-cat="{c['slug']}">
          <button class="m-cat-btn" onclick="toggleCat(this)" aria-expanded="{'true' if op else 'false'}"><span class="m-ic bg-{c['color']}-100 text-{c['color']}-600"><i class="{c['icon']}"></i></span><span class="m-name">{c['name']}</span><span class="m-count">{len(c['tools'])}</span><i class="fa-solid fa-chevron-down m-chev"></i></button>
          <div class="m-list"><a class="m-all" href="{R}categories/{c['slug']}.html">View all {c['name']} &rarr;</a>{items}</div>
        </div>'''
    return f'''<!--HEADER-->
    <header class="site-header">
        <div class="header-inner">
            <a href="{R}index.html" class="logo"><span class="logo-mark"><i class="fa-solid fa-toolbox"></i></span>{SITE_NAME}</a>
            <div class="header-right">
                <a href="{R}index.html" class="header-link">Home</a>
                <button id="menuBtn" class="menu-btn" aria-label="Open menu" aria-controls="sideMenu" aria-expanded="false" onclick="toggleMenu()"><i class="fa-solid fa-bars"></i><span>Menu</span></button>
            </div>
        </div>
    </header>
    <div id="menuOverlay" class="menu-overlay" onclick="toggleMenu(false)"></div>
    <aside id="sideMenu" class="side-menu" aria-hidden="true" aria-label="Site menu">
        <div class="side-head"><a href="{R}index.html" class="logo"><span class="logo-mark"><i class="fa-solid fa-toolbox"></i></span>{SITE_NAME}</a><button class="side-close" aria-label="Close menu" onclick="toggleMenu(false)"><i class="fa-solid fa-xmark"></i></button></div>
        <div class="side-search"><i class="fa-solid fa-magnifying-glass"></i><input id="menuSearch" type="search" placeholder="Search {len(TOOLS)} tools..." oninput="filterMenu(this.value)"></div>
        <a class="m-home" href="{R}index.html"><i class="fa-solid fa-house"></i> Home</a>
        <p class="m-label">Tool Categories</p>{cats}
        <p class="m-label">Company</p>
        <div class="m-links"><a href="{R}about.html">About Us</a><a href="{R}contact.html">Contact Us</a><a href="{R}privacy.html">Privacy Policy</a><a href="{R}terms.html">Terms &amp; Conditions</a><a href="{R}disclaimer.html">Disclaimer</a></div>
    </aside>
    <!--/HEADER-->'''


def footer(R):
    cl = ''.join(f'<li><a href="{R}categories/{c["slug"]}.html">{c["name"]} <span>({len(c["tools"])})</span></a></li>' for c in CATS)
    pl = ''.join(f'<li><a href="{R}tools/{s}.html">{E(BY[s]["title"])}</a></li>' for s in POPULAR[:6])
    return f'''<!--FOOTER-->
    <footer class="site-footer">
        <div class="footer-grid">
            <div><a href="{R}index.html" class="logo light"><span class="logo-mark"><i class="fa-solid fa-toolbox"></i></span>{SITE_NAME}</a>
                <p class="mt-3 text-sm text-slate-400">{len(TOOLS)} free online tools for PDF, images, text, calculators and daily work. Fast, private and mobile friendly.</p></div>
            <div><h4>Categories</h4><ul>{cl}</ul></div>
            <div><h4>Popular Tools</h4><ul>{pl}</ul></div>
            <div><h4>Company</h4><ul><li><a href="{R}about.html">About Us</a></li><li><a href="{R}contact.html">Contact Us</a></li><li><a href="{R}privacy.html">Privacy Policy</a></li><li><a href="{R}terms.html">Terms &amp; Conditions</a></li><li><a href="{R}disclaimer.html">Disclaimer</a></li></ul></div>
        </div>
        <p class="footer-copy">&copy; 2026 {SITE_NAME}. All rights reserved.</p>
    </footer>
    <!--/FOOTER-->'''


def card(t, R):
    return (f'<a href="{R}tools/{t["slug"]}.html" class="tool-card" data-s="{E((t["title"] + " " + t["desc"]).lower(), quote=True)}">'
            f'<span class="tc-ic bg-{t["color"]}-100 text-{t["color"]}-600"><i class="{t["icon"]}"></i></span>'
            f'<h3>{E(t["title"])}</h3><p>{E(t["desc"])}</p></a>')


def crumbs(items):
    out = []
    for i, (n, u) in enumerate(items):
        out.append(f'<a href="{u}">{E(n)}</a>' if u else f'<span>{E(n)}</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' <i class="fa-solid fa-chevron-right"></i> '.join(out) + '</nav>'


def bc_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": f'{SITE_URL}/{u}'} for i, (n, u) in enumerate(items)]}


def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def faq_html(faqs):
    return ''.join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)


AD = '''<div id="adModal" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center hidden z-[100]">
        <div class="bg-white p-8 rounded-lg text-center max-w-sm w-full mx-4">
            <h3 class="text-xl font-bold mb-4">Advertisement</h3>
            <div class="bg-gray-200 h-40 w-full flex items-center justify-center mb-4 border border-dashed border-gray-400"><span class="text-gray-500">Google AdSense Space</span></div>
            <p class="text-sm text-gray-600">Result ready in <span id="adTimer" class="font-bold text-blue-600 text-lg">5</span>s...</p>
        </div>
    </div>'''


def between(s, a, b):
    i = s.find(a)
    if i < 0: return None
    j = s.find(b, i + len(a))
    return s[i + len(a):j] if j >= 0 else None


# ------------------------------------------------------------------ tool pages
def build_tool(t):
    p = ROOT / 'tools' / f'{t["slug"]}.html'
    s = p.read_text(encoding='utf-8')
    c = CAT[t['cat']]
    if '<!--CONTENT-->' in s:   # already built before: reuse stored parts
        content = between(s, '<!--CONTENT-->', '<!--/CONTENT-->').strip()
        js = (between(s, '<!--TOOLJS-->', '<!--/TOOLJS-->') or '').strip()
        libs = re.findall(r'<script src="(https://(?!cdn\.tailwindcss)[^"]+)"', s.split('</head>')[0])
    else:                        # first time: take apart the original page
        main = re.search(r'<main[^>]*>(.*)</main>', s, re.S).group(1)
        content = re.sub(r'<h1[^>]*>.*?</h1>', '', main, count=1, flags=re.S).strip()
        js = '\n'.join(f'<script>{x}</script>' for x in re.findall(r'<script>(.*?)</script>', s, re.S)).strip()
        libs = re.findall(r'<script src="(https://(?!cdn\.tailwindcss)[^"]+)"', s.split('</head>')[0])
    has_ad = ADS_ENABLED and t.get('ad', False)
    R = '../'
    title = f'{t["title"]} - Free Online Tool | {SITE_NAME}'
    if len(title) > 62: title = f'{t["title"]} | {SITE_NAME}'
    desc = f'{t["desc"].rstrip(".")}. Free, fast and works in your browser - no signup needed.'
    path = f'tools/{t["slug"]}.html'
    steps = ''.join(f'<li>{E(x)}</li>' for x in c['steps'])
    faqs = [(f'Is {t["title"]} free to use?', f'Yes. {t["title"]} on {SITE_NAME} is completely free. There is no registration and there are no hidden charges.'),
            ('Is my data safe and private?', PRIVACY.get(t['slug'], 'Yes. This tool runs in your own browser, so the text, images or files you use are not uploaded to our servers.')),
            ('Does this tool work on mobile phones?', 'Yes. It works in modern browsers on phones, tablets and computers. For the best experience use the latest version of Chrome, Edge, Safari or Firefox.')]
    related = [x for x in c['tools'] if x['slug'] != t['slug']][:4]
    if len(related) < 4:
        related += [BY[s2] for s2 in POPULAR if s2 != t['slug'] and BY[s2] not in related][:4 - len(related)]
    bc = [('Home', 'index.html'), (c['name'], f'categories/{c["slug"]}.html'), (t['h1'], path)]
    ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": t['h1'], "url": f'{SITE_URL}/{path}', "description": desc,
           "applicationCategory": APPCAT.get(t['cat'], 'UtilitiesApplication'), "operatingSystem": "Any", "browserRequirements": "Requires JavaScript",
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}, bc_ld(bc), faq_ld(faqs)]
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    {head(title, desc, path, R, ld, libs)}
</head>
<body class="tool-page">
    {header(R, c['slug'])}
    <section class="page-hero hero-{c['color']}">
        <div class="page-hero-inner">
            {crumbs([('Home', R + 'index.html'), (c['name'], f'{R}categories/{c["slug"]}.html'), (t['h1'], None)])}
            <h1>{E(t['h1'])}</h1>
            <p>{E(t['desc'])}</p>
        </div>
    </section>
    <main class="max-w-4xl mx-auto px-4 py-10">
        <!--CONTENT-->
{content}
        <!--/CONTENT-->
        <section class="seo-block">
            <h2>How to use {E(t['title'])}</h2>
            <ol class="steps">{steps}</ol>
        </section>
        <section class="seo-block">
            <h2>Frequently Asked Questions</h2>
            {faq_html(faqs)}
        </section>
        <section class="seo-block">
            <h2>More {c['name']}</h2>
            <div class="tool-grid">{''.join(card(x, R) for x in related)}</div>
            <p class="mt-4"><a class="text-indigo-600 font-bold" href="{R}categories/{c['slug']}.html">See all {len(c['tools'])} {c['name']} &rarr;</a></p>
        </section>
    </main>
    {AD if has_ad else ''}
    {footer(R)}
    <script src="../script.js"></script>
    <!--TOOLJS-->
{js}
    <!--/TOOLJS-->
</body>
</html>
'''
    p.write_text(out, encoding='utf-8')


# ------------------------------------------------------------------ simple pages
SIMPLE = {
 'about': ('About Us', 'Learn about Toolify, a collection of free online tools for PDF, images, text, calculators and everyday tasks.'),
 'contact': ('Contact Us', 'Contact Toolify to suggest a new tool, report a bug or ask a question.'),
 'privacy': ('Privacy Policy', 'Read the Toolify privacy policy and how your data is handled when you use our free online tools.'),
 'terms': ('Terms & Conditions', 'Read the terms and conditions for using Toolify free online tools.'),
 'disclaimer': ('Disclaimer', 'Important disclaimer about the calculators, converters and information provided by Toolify free online tools.'),
}
def build_simple(name):
    p = ROOT / f'{name}.html'
    s = p.read_text(encoding='utf-8')
    if '<!--CONTENT-->' in s:
        content = between(s, '<!--CONTENT-->', '<!--/CONTENT-->').strip()
        js = (between(s, '<!--TOOLJS-->', '<!--/TOOLJS-->') or '').strip()
    else:
        body = re.search(r'<body[^>]*>(.*)</body>', s, re.S).group(1)
        js = '\n'.join(f'<script>{x}</script>' for x in re.findall(r'<script>(.*?)</script>', body, re.S)).strip()
        content = re.sub(r'<script>.*?</script>', '', body, flags=re.S).strip()
    t, d = SIMPLE[name]
    R = ''
    ld = [bc_ld([('Home', 'index.html'), (t, f'{name}.html')])]
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    {head(f'{t} | {SITE_NAME}', d, f'{name}.html', R, ld)}
</head>
<body class="plain-page">
    {header(R)}
    <main class="px-4 py-10">
        <!--CONTENT-->
{content}
        <!--/CONTENT-->
    </main>
    {footer(R)}
    <script src="script.js"></script>
    <!--TOOLJS-->
{js}
    <!--/TOOLJS-->
</body>
</html>
'''
    p.write_text(out, encoding='utf-8')


# ------------------------------------------------------------------ category pages
def build_cat(c):
    R = '../'
    path = f'categories/{c["slug"]}.html'
    title = f'{c["h1"]} - {len(c["tools"])} Tools | {SITE_NAME}'
    desc = f'{c["intro"]} {len(c["tools"])} free tools, no signup needed.'
    faqs = [(f'Are the {c["name"].lower()} on {SITE_NAME} free?', f'Yes. All {len(c["tools"])} tools in this category are free to use, with no registration.'),
            ('Do I need to install anything?', 'No. Everything works in your web browser on phone, tablet or computer.')]
    bc = [('Home', 'index.html'), (c['name'], path)]
    ld = [bc_ld(bc), faq_ld(faqs), {"@context": "https://schema.org", "@type": "CollectionPage", "name": c['h1'], "url": f'{SITE_URL}/{path}', "description": desc,
          "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f'{SITE_URL}/tools/{t["slug"]}.html', "name": t['title']} for i, t in enumerate(c['tools'])]}}]
    others = ''.join(f'<a class="chip" href="{x["slug"]}.html"><i class="{x["icon"]}"></i> {x["name"]}</a>' for x in CATS if x is not c)
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    {head(title, desc, path, R, ld)}
</head>
<body class="cat-page">
    {header(R, c['slug'])}
    <section class="page-hero hero-{c['color']}">
        <div class="page-hero-inner">
            {crumbs([('Home', R + 'index.html'), (c['name'], None)])}
            <h1><i class="{c['icon']} mr-2"></i>{E(c['h1'])}</h1>
            <p>{E(c['intro'])}</p>
            <div class="mt-5"><input id="toolSearch" type="search" class="hero-search small" placeholder="Search in {c['name']}..."></div>
        </div>
    </section>
    <main class="max-w-6xl mx-auto px-4 py-10">
        <div class="tool-grid" id="toolGrid">{''.join(card(t, R) for t in c['tools'])}</div>
        <p id="noTools" class="hidden text-center text-slate-500 mt-6">No tools found.</p>
        <section class="seo-block">
            <h2>About {c['name']}</h2>
            <p>{E(c['about'])}</p>
        </section>
        <section class="seo-block">
            <h2>Frequently Asked Questions</h2>
            {faq_html(faqs)}
        </section>
        <section class="seo-block">
            <h2>Explore other categories</h2>
            <div class="chips">{others}</div>
        </section>
    </main>
    {footer(R)}
    <script src="../script.js"></script>
</body>
</html>
'''
    (ROOT / 'categories').mkdir(exist_ok=True)
    (ROOT / path).write_text(out, encoding='utf-8')


# ------------------------------------------------------------------ index
def build_index():
    R = ''
    n = len(TOOLS)
    title = f'{SITE_NAME} - {n} Free Online Tools: PDF, Image, Text & Calculators'
    desc = f'{n} free online tools in one place: merge PDF, compress images, word counter, QR code, age and EMI calculators and more. Fast, private, no signup.'
    faqs = [(f'Is {SITE_NAME} really free?', 'Yes. All tools are free to use. You do not need to create an account.'),
            ('Are my files uploaded to a server?', 'Most tools run entirely in your browser, so your files and text stay on your device. A few tools, such as the QR code generator, use an outside service and say so on their page.'),
            ('Does it work on mobile?', 'Yes. The website is designed for phones, tablets and desktops.'),
            ('Can I suggest a new tool?', 'Yes. Use the Contact page to send us your idea.')]
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": f'{SITE_URL}/', "description": desc},
          {"@context": "https://schema.org", "@type": "Organization", "name": SITE_NAME, "url": f'{SITE_URL}/', "logo": f'{SITE_URL}/favicon.svg'}, faq_ld(faqs)]
    cats = ''.join(f'''<a href="categories/{c['slug']}.html" class="cat-card">
            <span class="cc-ic bg-{c['color']}-100 text-{c['color']}-600"><i class="{c['icon']}"></i></span>
            <h3>{c['name']}</h3><p>{E(c['short'])}</p><span class="cc-count">{len(c['tools'])} tools &rarr;</span></a>''' for c in CATS)
    sections = ''.join(f'''
        <section class="cat-section" id="{c['slug']}" data-sec>
            <div class="sec-head"><h2><span class="sec-ic bg-{c['color']}-100 text-{c['color']}-600"><i class="{c['icon']}"></i></span>{c['name']}</h2><a href="categories/{c['slug']}.html">View all &rarr;</a></div>
            <div class="tool-grid">{''.join(card(t, R) for t in c['tools'])}</div>
        </section>''' for c in CATS)
    pop = ''.join(card(BY[s], R) for s in POPULAR)
    why = ''.join(f'<div class="why"><span class="why-ic {cl}"><i class="{ic}"></i></span><h3>{h}</h3><p>{p}</p></div>' for ic, cl, h, p in [
        ('fa-solid fa-bolt', 'bg-yellow-100 text-yellow-600', '100% Free & Fast', 'No signup, no watermark on your results, no waiting. Open a tool and use it.'),
        ('fa-solid fa-lock', 'bg-green-100 text-green-600', 'Private by Design', 'Most tools work inside your browser, so your files and text stay on your device.'),
        ('fa-solid fa-mobile-screen', 'bg-blue-100 text-blue-600', 'Works on Every Device', 'Built mobile-first so you can use every tool on your phone, tablet or laptop.')])
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    {head(title, desc, '', R, ld)}
</head>
<body class="home-page">
    {header(R)}
    <section class="hero-home">
        <div class="hero-inner">
            <span class="hero-badge"><i class="fa-solid fa-sparkles"></i> {n} free tools &middot; {len(CATS)} categories &middot; no signup</span>
            <h1>Free Online Tools for Everyday Work</h1>
            <p>PDF, image, text, calculators, developer and daily tools. Fast, private and made for your phone.</p>
            <div class="hero-searchwrap"><i class="fa-solid fa-magnifying-glass"></i><input id="toolSearch" type="search" class="hero-search" placeholder="Search tools... e.g. merge pdf, compress image, age" autocomplete="off"></div>
        </div>
    </section>
    <main class="max-w-6xl mx-auto px-4">
        <section class="py-10" id="categories" data-keep>
            <h2 class="sec-title">Browse by Category</h2>
            <div class="cat-grid">{cats}</div>
        </section>
        <section class="pb-6" id="popular" data-sec>
            <div class="sec-head"><h2><span class="sec-ic bg-amber-100 text-amber-600"><i class="fa-solid fa-fire"></i></span>Popular Tools</h2></div>
            <div class="tool-grid">{pop}</div>
        </section>
        <p id="noTools" class="hidden text-center text-slate-500 my-10">No tools found. Try a different word.</p>
        <div id="allTools">{sections}
        </div>
        <section class="py-12" data-keep>
            <h2 class="sec-title">Why {SITE_NAME}?</h2>
            <div class="why-grid">{why}</div>
        </section>
        <section class="seo-block" data-keep>
            <h2>Frequently Asked Questions</h2>
            {faq_html(faqs)}
        </section>
    </main>
    {footer(R)}
    <script src="script.js"></script>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(out, encoding='utf-8')


# ------------------------------------------------------------------ extras
def build_extras():
    urls = [('', '1.0')] + [(f'categories/{c["slug"]}.html', '0.8') for c in CATS] + [(f'tools/{t["slug"]}.html', '0.7') for t in TOOLS] + [(f'{n}.html', '0.3') for n in SIMPLE]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{SITE_URL}/{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n' for u, p in urls) + '</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(sm)
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n')
    (ROOT / 'favicon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f46e5"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="url(#g)"/><path d="M18 20h28v8H36v18h-8V28H18z" fill="#fff"/></svg>\n''')
    R = ''
    out = f'''<!DOCTYPE html>
<html lang="en">
<head>
    {head(f'Page not found | {SITE_NAME}', 'The page you are looking for was not found on Toolify. Use the menu to browse all free online tools or go back to the home page.', '404.html', R).replace('index, follow', 'noindex')}
</head>
<body class="plain-page">
    {header(R)}
    <main class="px-4 py-20 text-center">
        <p class="text-7xl font-extrabold text-indigo-600">404</p>
        <h1 class="text-3xl font-bold mt-4 mb-3">Page not found</h1>
        <p class="text-slate-600 mb-8">The page may have moved. Try the menu or go back to the home page.</p>
        <a href="index.html" class="btn-primary">Go to Home</a>
    </main>
    {footer(R)}
    <script src="script.js"></script>
</body>
</html>
'''
    (ROOT / '404.html').write_text(out, encoding='utf-8')


if __name__ == '__main__':
    for t in TOOLS: build_tool(t)
    for n in SIMPLE: build_simple(n)
    for c in CATS: build_cat(c)
    build_index(); build_extras()
    missing = [f.name for f in (ROOT / 'tools').glob('*.html') if f.stem not in BY]
    print(f'Built {len(TOOLS)} tools, {len(CATS)} categories, index, sitemap.')
    if missing: print('WARNING: these tool pages are not in _source/tools.json:', missing)
