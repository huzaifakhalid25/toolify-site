TOOLIFY - FILE STRUCTURE (simple)
=================================
index.html            Home page (search + all categories)
about.html  contact.html  privacy.html  terms.html
style.css             All design / colors
script.js             Menu (hamburger), search, ad timer, shared helpers
favicon.svg  robots.txt  sitemap.xml  404.html   (SEO files)

categories/           One page per category (pdf-tools.html, image-tools.html ...)
tools/                One page per tool (85 tools). Each tool = 1 file
_source/              Builder (optional). Ignore it if you only want to upload the site.
    build.py          Re-creates menu, footer, SEO, category pages, sitemap
    tools.json        List of all tools + their category

BEFORE YOU GO LIVE (2 minutes)
------------------------------
1. Open _source/build.py, change   SITE_URL = "https://toolify-site-three.vercel.app"   to your real domain.
2. Run:  python3 _source/build.py     (works in Termux too)
   This updates canonical links + sitemap.xml everywhere.
3. contact.html: email is already set (CONTACT_EMAIL).
4. Upload the whole Toolify folder (everything except _source is needed).
5. Submit  https://YOURDOMAIN/sitemap.xml  in Google Search Console.

HOW TO ADD A NEW TOOL
---------------------
1. Copy any file in tools/ (for example tools/word-counter.html) and rename it.
2. Edit the tool card + script inside it (between <!--CONTENT--> and <!--/CONTENT--> and <!--TOOLJS-->).
3. Open _source/tools.json and add one entry:
   {"slug":"my-tool","title":"My Tool","icon":"fa-solid fa-star","color":"blue","desc":"One line description.","cat":"utilities","h1":"My Tool"}
   (cat = pdf-tools, image-tools, text-tools, calculators, developer-tools, media-social, utilities)
4. Run  python3 _source/build.py  -> the tool appears in the menu, its category page, home page and sitemap.

CATEGORIES (85 tools)
---------------------
PDF Tools 9 | Image Tools 10 | Text Tools 15 | Calculators 16 | Developer Tools 17 | Media & Social 6 | Daily Utilities 12

NOTES
-----
- Pages load Tailwind, Font Awesome, jsPDF, pdf-lib, marked from CDNs, so the site needs internet for those.
- QR generator uses api.qrserver.com (outside service).
- ADS: the 5-second ad wait is OFF. After Google AdSense approves you, open _source/build.py,
  set ADS_ENABLED = True and run  python3 _source/build.py  (calculators/converters will show the ad modal again).
- Pages about/contact/privacy/terms/disclaimer are normal HTML files you can edit directly (keep the <!--CONTENT--> markers).
