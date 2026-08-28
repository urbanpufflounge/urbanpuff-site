"""
Original SVG artwork for Urban Puff.

Each illustration is drawn on a 1:1 or 4:5 viewBox, uses only the brand palette
via CSS custom properties, and is animated with CSS (see styles.css .art-*).
Every piece is returned inside an `.art` wrapper so a real photograph can
replace it later without touching layout — see art_slot().
"""

GRAD = """
  <defs>
    <linearGradient id="g-{id}" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="#f0cf7a"/>
      <stop offset="0.55" stop-color="#d4af55"/>
      <stop offset="1" stop-color="#8d6a16"/>
    </linearGradient>
    <linearGradient id="glass-{id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f0cf7a" stop-opacity=".30"/>
      <stop offset="1" stop-color="#e0632c" stop-opacity=".16"/>
    </linearGradient>
    <radialGradient id="glow-{id}" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#d4af55" stop-opacity=".30"/>
      <stop offset="1" stop-color="#d4af55" stop-opacity="0"/>
    </radialGradient>
  </defs>
"""


def _wrap(inner, view="0 0 320 400", cls=""):
    return (f'<svg class="art__svg {cls}" viewBox="{view}" role="img" '
            f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">{inner}</svg>')


def hookah(idn="hk"):
    """Tall hookah with vase, stem, bowl, hose and rising smoke."""
    s = GRAD.format(id=idn) + f'''
  <ellipse cx="160" cy="378" rx="120" ry="26" fill="url(#glow-{idn})"/>

  <!-- smoke -->
  <g class="art-smoke" stroke="url(#g-{idn})" fill="none" stroke-linecap="round">
    <path class="art-smoke__a" d="M160 74c-15-13-15-27 0-40s15-27 0-40" stroke-width="2.6" opacity=".55"/>
    <path class="art-smoke__b" d="M132 84c-11-10-11-21 0-31s11-21 0-31" stroke-width="2" opacity=".34"/>
    <path class="art-smoke__c" d="M188 84c11-10 11-21 0-31s-11-21 0-31" stroke-width="2" opacity=".26"/>
  </g>

  <!-- bowl -->
  <path d="M136 118h48l-7 30h-34z" fill="url(#g-{idn})"/>
  <rect x="130" y="110" width="60" height="9" rx="4.5" fill="url(#g-{idn})"/>
  <path d="M143 148h34l-4 12h-26z" fill="url(#g-{idn})" opacity=".7"/>

  <!-- stem -->
  <rect x="153" y="160" width="14" height="96" rx="7" fill="url(#g-{idn})"/>
  <!-- plate -->
  <path d="M96 186h128a6 6 0 010 12H96a6 6 0 010-12z" fill="url(#g-{idn})" opacity=".85"/>
  <path d="M96 198h128l-10 10H106z" fill="url(#g-{idn})" opacity=".35"/>

  <!-- vase -->
  <path d="M160 256c-38 0-62 28-62 62s28 56 62 56 62-24 62-56-24-62-62-62z"
        fill="url(#glass-{idn})" stroke="url(#g-{idn})" stroke-width="3"/>
  <path d="M160 300c-26 0-42 18-42 36 0 16 18 28 42 28s42-12 42-28c0-18-16-36-42-36z"
        fill="url(#g-{idn})" opacity=".20"/>
  <ellipse class="art-shine" cx="132" cy="300" rx="10" ry="22" fill="#f0cf7a" opacity=".16" transform="rotate(-18 132 300)"/>

  <!-- hose -->
  <path class="art-hose" d="M160 214c56 0 92 20 108 58 12 30 4 56-18 68"
        fill="none" stroke="url(#g-{idn})" stroke-width="4" stroke-linecap="round" opacity=".9"/>
  <rect x="238" y="336" width="16" height="34" rx="8" fill="url(#g-{idn})"/>

  <!-- coals -->
  <g class="art-ember">
    <circle cx="149" cy="104" r="4" fill="#e0632c"/>
    <circle cx="162" cy="101" r="3.4" fill="#f0cf7a"/>
    <circle cx="173" cy="105" r="3.8" fill="#e0632c"/>
  </g>
'''
    return _wrap(s)


def grill(idn="gr"):
    """Skewers of tikka and kababs over flame."""
    s = GRAD.format(id=idn) + f'''
  <ellipse cx="160" cy="356" rx="128" ry="30" fill="url(#glow-{idn})"/>

  <!-- flames -->
  <g class="art-flame">
    <path d="M120 312c-16-18-10-38 6-50-4 18 10 20 12 34 2-12 10-18 8-32 14 12 22 32 8 48z"
          fill="#e0632c" opacity=".8"/>
    <path d="M196 312c-16-18-10-38 6-50-4 18 10 20 12 34 2-12 10-18 8-32 14 12 22 32 8 48z"
          fill="#e0632c" opacity=".6"/>
  </g>

  <!-- grill bars -->
  <g stroke="url(#g-{idn})" stroke-width="3" stroke-linecap="round" opacity=".7">
    <path d="M56 322h208M56 336h208"/>
  </g>

  <!-- skewer 1 -->
  <g class="art-skewer art-skewer--a">
    <path d="M40 148h240" stroke="#f0cf7a" stroke-width="5" stroke-linecap="round" opacity=".95"/>
    <path d="M280 148l16 0" stroke="#f0cf7a" stroke-width="2" stroke-linecap="round" opacity=".7"/>
    <rect x="86" y="130" width="40" height="38" rx="13" fill="url(#g-{idn})"/>
    <rect x="134" y="132" width="34" height="34" rx="12" fill="url(#g-{idn})" opacity=".75"/>
    <rect x="176" y="130" width="40" height="38" rx="13" fill="url(#g-{idn})"/>
    <rect x="224" y="134" width="26" height="30" rx="11" fill="#e0632c" opacity=".55"/>
  </g>

  <!-- skewer 2 -->
  <g class="art-skewer art-skewer--b">
    <path d="M40 212h240" stroke="#f0cf7a" stroke-width="5" stroke-linecap="round" opacity=".95"/>
    <path d="M280 212l16 0" stroke="#f0cf7a" stroke-width="2" stroke-linecap="round" opacity=".7"/>
    <rect x="74" y="196" width="30" height="32" rx="12" fill="#e0632c" opacity=".55"/>
    <path d="M116 194h64a10 10 0 0110 10v16a10 10 0 01-10 10h-64a10 10 0 01-10-10v-16a10 10 0 0110-10z" fill="url(#g-{idn})"/>
    <rect x="196" y="196" width="32" height="32" rx="12" fill="url(#g-{idn})" opacity=".7"/>
    <rect x="238" y="198" width="26" height="28" rx="11" fill="url(#g-{idn})"/>
  </g>

  <!-- skewer 3 -->
  <g class="art-skewer art-skewer--c">
    <path d="M40 274h240" stroke="#f0cf7a" stroke-width="5" stroke-linecap="round" opacity=".95"/>
    <path d="M280 274l16 0" stroke="#f0cf7a" stroke-width="2" stroke-linecap="round" opacity=".7"/>
    <rect x="92" y="258" width="38" height="34" rx="13" fill="url(#g-{idn})" opacity=".8"/>
    <rect x="138" y="256" width="42" height="38" rx="14" fill="url(#g-{idn})"/>
    <rect x="188" y="260" width="30" height="30" rx="12" fill="#e0632c" opacity=".45"/>
  </g>

  <!-- heat shimmer -->
  <g class="art-heat" stroke="#e0632c" stroke-width="2" fill="none" opacity=".3" stroke-linecap="round">
    <path d="M104 106c-8-8-8-16 0-24"/>
    <path d="M160 100c-8-8-8-16 0-24"/>
    <path d="M216 106c-8-8-8-16 0-24"/>
  </g>
'''
    return _wrap(s)


def mocktail(idn="mk"):
    """Tall glass, layered fruit pour, mint, straw and rising bubbles."""
    s = GRAD.format(id=idn) + f'''
  <ellipse cx="160" cy="368" rx="104" ry="24" fill="url(#glow-{idn})"/>

  <!-- straw -->
  <path d="M196 96l-22 74" stroke="#e0632c" stroke-width="7" stroke-linecap="round" opacity=".8"/>

  <!-- mint -->
  <g class="art-mint">
    <path d="M132 104c-20 2-32 16-30 34 18 2 32-12 30-34z" fill="url(#g-{idn})" opacity=".8"/>
    <path d="M150 92c-14 12-16 30-4 42 14-10 16-28 4-42z" fill="url(#g-{idn})" opacity=".55"/>
  </g>

  <!-- glass -->
  <path d="M104 132h112l-14 196a16 16 0 01-16 14h-52a16 16 0 01-16-14z"
        fill="url(#glass-{idn})" stroke="url(#g-{idn})" stroke-width="3.5" stroke-linejoin="round"/>
  <!-- liquid -->
  <path d="M112 186h96l-11 142a14 14 0 01-14 12h-46a14 14 0 01-14-12z" fill="url(#g-{idn})" opacity=".34"/>
  <path d="M116 244h88l-8 84a14 14 0 01-14 12h-44a14 14 0 01-14-12z" fill="#e0632c" opacity=".26"/>
  <path d="M112 186h96" stroke="url(#g-{idn})" stroke-width="2.5" opacity=".8"/>

  <!-- bubbles -->
  <g class="art-bubbles" fill="#f0cf7a">
    <circle class="art-bubble art-bubble--1" cx="136" cy="300" r="4" opacity=".5"/>
    <circle class="art-bubble art-bubble--2" cx="160" cy="316" r="3" opacity=".4"/>
    <circle class="art-bubble art-bubble--3" cx="182" cy="292" r="3.6" opacity=".45"/>
    <circle class="art-bubble art-bubble--4" cx="150" cy="330" r="2.4" opacity=".35"/>
  </g>

  <!-- citrus wheel -->
  <g transform="translate(214 158)">
    <circle r="26" fill="url(#g-{idn})" opacity=".85"/>
    <circle r="20" fill="#0b0a09" opacity=".35"/>
    <g stroke="#0b0a09" stroke-width="2.2" opacity=".45">
      <path d="M0-20V20M-20 0H20M-14-14l28 28M14-14l-28 28"/>
    </g>
  </g>
  <ellipse class="art-shine" cx="124" cy="240" rx="6" ry="52" fill="#f0cf7a" opacity=".12"/>
'''
    return _wrap(s)


def dessert(idn="ds"):
    """Kulfi / dessert plate with drizzle."""
    s = GRAD.format(id=idn) + f'''
  <ellipse cx="160" cy="344" rx="112" ry="26" fill="url(#glow-{idn})"/>
  <!-- plate -->
  <ellipse cx="160" cy="316" rx="104" ry="26" fill="none" stroke="url(#g-{idn})" stroke-width="3"/>
  <ellipse cx="160" cy="312" rx="78" ry="18" fill="url(#g-{idn})" opacity=".14"/>

  <!-- scoops -->
  <circle cx="126" cy="272" r="38" fill="url(#g-{idn})" opacity=".85"/>
  <circle cx="192" cy="278" r="32" fill="url(#g-{idn})" opacity=".6"/>
  <circle cx="160" cy="228" r="34" fill="url(#g-{idn})"/>

  <!-- drizzle -->
  <path class="art-drizzle" d="M120 200c14 10 30 10 44 0s30-10 44 2"
        fill="none" stroke="#e0632c" stroke-width="4" stroke-linecap="round" opacity=".7"/>

  <!-- pistachio flecks -->
  <g fill="#f0cf7a" opacity=".8">
    <circle cx="146" cy="214" r="3"/><circle cx="176" cy="222" r="2.4"/>
    <circle cx="160" cy="240" r="2.6"/><circle cx="118" cy="266" r="2.6"/>
    <circle cx="200" cy="276" r="2.2"/>
  </g>

  <!-- steam / sparkle -->
  <g class="art-smoke" stroke="url(#g-{idn})" fill="none" stroke-linecap="round" opacity=".45">
    <path class="art-smoke__a" d="M160 178c-10-9-10-19 0-28" stroke-width="2.2"/>
    <path class="art-smoke__b" d="M132 186c-8-7-8-15 0-22" stroke-width="1.8"/>
  </g>
'''
    return _wrap(s)


def lounge(idn="lg"):
    """Wide lounge scene: banquette, low table, hookah, screen and pendants."""
    s = GRAD.format(id=idn) + f'''
  <ellipse cx="300" cy="308" rx="288" ry="40" fill="url(#glow-{idn})"/>

  <!-- screen on the back wall -->
  <g opacity=".62">
    <rect x="440" y="40" width="140" height="86" rx="7" fill="none" stroke="url(#g-{idn})" stroke-width="2.5"/>
    <path d="M440 110h140" stroke="url(#g-{idn})" stroke-width="1.2" opacity=".45"/>
    <circle cx="510" cy="76" r="15" fill="none" stroke="url(#g-{idn})" stroke-width="2"/>
    <path d="M505 69l13 7-13 7z" fill="url(#g-{idn})"/>
  </g>

  <!-- pendant lights over the booth -->
  <g>
    <path d="M80 0v40M150 0v58M220 0v28" stroke="url(#g-{idn})" stroke-width="1.4" opacity=".45"/>
    <path d="M64 40h32l-8 16H72z" fill="url(#g-{idn})"/>
    <path d="M134 58h32l-8 16h-16z" fill="url(#g-{idn})"/>
    <path d="M204 28h32l-8 16h-16z" fill="url(#g-{idn})"/>
    <circle class="art-lamp" cx="80" cy="64" r="24" fill="url(#glow-{idn})"/>
    <circle class="art-lamp" cx="150" cy="82" r="28" fill="url(#glow-{idn})"/>
    <circle class="art-lamp" cx="220" cy="52" r="22" fill="url(#glow-{idn})"/>
  </g>

  <!-- banquette: back -->
  <path d="M42 146h216a14 14 0 0114 14v88H28v-88a14 14 0 0114-14z" fill="url(#g-{idn})" opacity=".13"/>
  <path d="M42 146h216a14 14 0 0114 14v88H28v-88a14 14 0 0114-14z" fill="none" stroke="url(#g-{idn})" stroke-width="2.5"/>
  <!-- tufting -->
  <g fill="url(#g-{idn})" opacity=".38">
    <circle cx="86" cy="180" r="2.6"/><circle cx="150" cy="180" r="2.6"/><circle cx="214" cy="180" r="2.6"/>
    <circle cx="118" cy="210" r="2.6"/><circle cx="182" cy="210" r="2.6"/>
  </g>
  <g stroke="url(#g-{idn})" stroke-width="1" opacity=".22">
    <path d="M86 180l32 30M150 180l-32 30M150 180l32 30M214 180l-32 30"/>
  </g>
  <!-- seat -->
  <path d="M24 248h252a10 10 0 0110 10v14a8 8 0 01-8 8H22a8 8 0 01-8-8v-14a10 10 0 0110-10z"
        fill="url(#g-{idn})" opacity=".3"/>
  <path d="M24 248h252a10 10 0 0110 10v14a8 8 0 01-8 8H22a8 8 0 01-8-8v-14a10 10 0 0110-10z"
        fill="none" stroke="url(#g-{idn})" stroke-width="2"/>
  <!-- base -->
  <path d="M36 280h228v20H36z" fill="url(#g-{idn})" opacity=".16"/>
  <path d="M36 300h228" stroke="url(#g-{idn})" stroke-width="2" opacity=".5"/>
  <!-- cushions -->
  <g fill="url(#g-{idn})" opacity=".34">
    <rect x="48" y="196" width="40" height="44" rx="11"/>
    <rect x="214" y="200" width="36" height="40" rx="11"/>
  </g>

  <!-- low table -->
  <rect x="300" y="252" width="186" height="9" rx="4.5" fill="url(#g-{idn})"/>
  <path d="M318 261v38M468 261v38" stroke="url(#g-{idn})" stroke-width="4" stroke-linecap="round"/>
  <path d="M318 299h150" stroke="url(#g-{idn})" stroke-width="2" opacity=".4"/>

  <!-- hookah standing on the table -->
  <g transform="translate(368 122) scale(.42)">
    <g class="art-smoke" stroke="url(#g-{idn})" fill="none" stroke-linecap="round">
      <path class="art-smoke__a" d="M60 40c-16-14-16-28 0-42s16-28 0-42" stroke-width="5" opacity=".5"/>
      <path class="art-smoke__b" d="M22 52c-12-11-12-22 0-33s12-22 0-33" stroke-width="4" opacity=".28"/>
    </g>
    <path d="M36 86h48l-7 30H43z" fill="url(#g-{idn})"/>
    <rect x="30" y="78" width="60" height="9" rx="4.5" fill="url(#g-{idn})"/>
    <rect x="53" y="118" width="14" height="86" rx="7" fill="url(#g-{idn})"/>
    <path d="M-2 150h124a6 6 0 010 12H-2a6 6 0 010-12z" fill="url(#g-{idn})" opacity=".8"/>
    <path d="M60 204c-34 0-56 24-56 54s26 52 56 52 56-22 56-52-22-54-56-54z"
          fill="url(#glass-{idn})" stroke="url(#g-{idn})" stroke-width="4"/>
    <path d="M60 240c-22 0-36 16-36 32 0 14 16 24 36 24s36-10 36-24c0-16-14-32-36-32z" fill="url(#g-{idn})" opacity=".22"/>
    <!-- hose loops down to the left, toward the booth -->
    <path d="M56 176c-46 4-74 22-84 54-8 26 2 46 22 54" fill="none" stroke="url(#g-{idn})" stroke-width="5" stroke-linecap="round" opacity=".85"/>
    <rect x="-16" y="282" width="16" height="30" rx="8" fill="url(#g-{idn})" transform="rotate(14 -8 297)"/>
    <g class="art-ember">
      <circle cx="48" cy="72" r="4.5" fill="#e0632c"/>
      <circle cx="60" cy="69" r="4" fill="#f0cf7a"/>
      <circle cx="72" cy="73" r="4.2" fill="#e0632c"/>
    </g>
  </g>

  <!-- plate and glass on the table -->
  <g>
    <ellipse cx="440" cy="248" rx="26" ry="7" fill="url(#g-{idn})" opacity=".45"/>
    <path d="M428 236h24l-3 11h-18z" fill="url(#g-{idn})" opacity=".7"/>
    <path d="M466 216h18l-3 33h-12z" fill="url(#glass-{idn})" stroke="url(#g-{idn})" stroke-width="2"/>
    <path d="M467 228h16" stroke="url(#g-{idn})" stroke-width="1.5" opacity=".6"/>
  </g>

  <!-- floor -->
  <path d="M0 300h600" stroke="url(#g-{idn})" stroke-width="1.5" opacity=".22"/>
'''
    return _wrap(s, view="0 0 600 340", cls="art__svg--wide")


ART = {
    "hookah": hookah,
    "grill": grill,
    "mocktail": mocktail,
    "dessert": dessert,
    "lounge": lounge,
}


def art_slot(kind, alt, photo=None, cls=""):
    """
    Illustration wrapper that a real photo can take over.

    Drop a JPG at assets/img/<photo> and uncomment the <img> line — the artwork
    hides itself automatically when an image is present.
    """
    fn = ART[kind]
    img_hint = ""
    if photo:
        img_hint = (f'\n        <!-- Real photo? Uncomment and the artwork steps aside:\n'
                    f'        <img class="art__photo" src="assets/img/{photo}" alt="{alt}" loading="lazy"> -->')
    return f'''<div class="art {cls}" role="img" aria-label="{alt}">{img_hint}
        {fn(kind[:2] + str(abs(hash(alt)) % 997))}
      </div>'''
