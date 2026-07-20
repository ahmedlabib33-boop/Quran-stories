from __future__ import annotations


THEMES = {
    "light": {
        "emerald": "#123F35",
        "forest": "#0B2D27",
        "night_green": "#071D19",
        "ivory": "#F7F1E3",
        "parchment": "#EFE4CC",
        "sand": "#D9C8A9",
        "gold": "#C6A15B",
        "antique_gold": "#A9803A",
        "terracotta": "#A9583C",
        "burgundy": "#672D36",
        "text_primary": "#232722",
        "text_secondary": "#6E6759",
    },
    "qibla": {
        "emerald": "#123F35",
        "forest": "#0B2D27",
        "night_green": "#071D19",
        "ivory": "#F7F1E3",
        "parchment": "#EFE4CC",
        "sand": "#D9C8A9",
        "gold": "#C6A15B",
        "antique_gold": "#A9803A",
        "terracotta": "#A9583C",
        "burgundy": "#672D36",
        "text_primary": "#232722",
        "text_secondary": "#6E6759",
    },
}


def build_css(theme_key: str) -> str:
    theme = THEMES.get(theme_key) or THEMES["light"]
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;500;700;800;900&family=Tajawal:wght@400;500;700;800&display=swap');

:root {{
  --emerald: {theme["emerald"]};
  --forest: {theme["forest"]};
  --night-green: {theme["night_green"]};
  --ivory: {theme["ivory"]};
  --parchment: {theme["parchment"]};
  --sand: {theme["sand"]};
  --gold: {theme["gold"]};
  --antique-gold: {theme["antique_gold"]};
  --terracotta: {theme["terracotta"]};
  --burgundy: {theme["burgundy"]};
  --text-primary: {theme["text_primary"]};
  --text-secondary: {theme["text_secondary"]};
  --border: rgba(166, 125, 54, .26);
  --soft-border: rgba(166, 125, 54, .18);
  --shadow: 0 18px 44px rgba(18, 45, 39, .13);
  --card-shadow: 0 12px 28px rgba(32, 31, 23, .08);
}}

html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
  direction: rtl;
  background:
    radial-gradient(circle at 8% 0%, rgba(198, 161, 91, .18), transparent 22rem),
    radial-gradient(circle at 85% 4%, rgba(239, 228, 204, .92), transparent 20rem),
    linear-gradient(180deg, #fbf6ea 0%, var(--ivory) 58%, #faf4e7 100%);
  color: var(--text-primary);
  font-family: "Cairo", "Tajawal", sans-serif;
}}

html {{
  scroll-behavior: smooth;
}}

.block-container {{
  max-width: 580px;
  padding: .55rem .72rem 7.8rem;
}}

#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stToolbar"], [data-testid="stStatusWidget"], [data-testid="stSidebar"], [data-testid="collapsedControl"] {{
  visibility: hidden;
  height: 0;
  display: none !important;
}}

h1, h2, h3, h4, h5, h6, p, div, label, span, th, td {{
  direction: rtl;
  text-align: right;
  letter-spacing: 0;
}}

.top-nav {{
  position: sticky;
  top: .5rem;
  z-index: 90;
  min-height: 56px;
  display: grid;
  grid-template-columns: 44px 1fr auto;
  align-items: center;
  gap: .75rem;
  padding: .45rem .7rem;
  margin: 0 0 .55rem;
  border-radius: 18px 18px 0 0;
  border: 1px solid rgba(198, 161, 91, .40);
  border-bottom: 2px solid var(--gold);
  background:
    linear-gradient(135deg, rgba(255,255,255,.05), rgba(255,255,255,0)),
    linear-gradient(135deg, var(--night-green), var(--emerald));
  box-shadow: var(--shadow);
}}

.hamburger {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  color: var(--gold) !important;
  text-decoration: none !important;
  font-size: 1.35rem;
}}

.screen-title {{
  color: #fff;
  text-align: center;
  font-family: "Amiri", serif;
  font-size: clamp(1.35rem, 3vw, 1.72rem);
  line-height: 1;
}}

.selected-mini {{
  color: rgba(255,255,255,.72);
  font-size: .72rem;
  white-space: nowrap;
}}

.top-nav .nav-links {{
  display: none;
}}

.nav-links {{
  display: grid;
  align-items: center;
  gap: .35rem;
}}

.nav-link {{
  min-height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .35rem;
  padding: .35rem .8rem;
  border-radius: 999px;
  color: rgba(255,255,255,.78) !important;
  text-decoration: none !important;
  font-weight: 900;
  border: 1px solid transparent;
}}

.nav-link.active {{
  color: var(--gold) !important;
  background: rgba(0,0,0,.20);
  border-color: rgba(198, 161, 91, .46);
  box-shadow: inset 0 -3px 0 var(--gold);
}}

.nav-icon {{
  font-size: 1rem;
}}

.bottom-nav {{
  position: fixed;
  left: 50%;
  bottom: calc(.75rem + env(safe-area-inset-bottom));
  z-index: 110;
  width: min(calc(100vw - 1.1rem), 560px);
  transform: translateX(-50%);
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .28rem;
  padding: .5rem;
  border-radius: 18px;
  border: 1px solid rgba(198, 161, 91, .40);
  background: linear-gradient(135deg, var(--night-green), var(--emerald));
  box-shadow: 0 18px 44px rgba(7, 29, 25, .28);
}}

.bottom-nav .nav-link {{
  min-height: 48px;
  padding: .15rem .25rem;
  color: rgba(255,255,255,.86) !important;
}}

.target-hero {{
  position: relative;
  overflow: hidden;
  min-height: 230px;
  display: grid;
  grid-template-columns: 1.15fr .85fr;
  align-items: center;
  gap: 1rem;
  padding: 1.08rem;
  border-radius: 18px 18px 0 0;
  border: 1px solid rgba(198, 161, 91, .34);
  border-bottom: 3px solid rgba(198, 161, 91, .74);
  background:
    radial-gradient(circle at 18% 20%, rgba(198, 161, 91, .14), transparent 13rem),
    linear-gradient(110deg, rgba(7, 29, 25, .94) 0%, rgba(18, 63, 53, .96) 54%, rgba(11, 45, 39, .98) 100%);
  color: #fff;
  box-shadow: var(--shadow);
}}

.target-hero:before {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(45deg, transparent 48%, rgba(198, 161, 91, .11) 49%, transparent 50%),
    linear-gradient(-45deg, transparent 48%, rgba(198, 161, 91, .08) 49%, transparent 50%);
  background-size: 34px 34px;
  opacity: .46;
}}

.target-hero:after {{
  content: "";
  position: absolute;
  inset: .65rem;
  pointer-events: none;
  border: 1px solid rgba(198, 161, 91, .25);
  border-radius: 14px 14px 0 0;
}}

.hero-copy, .hero-arch {{
  position: relative;
  z-index: 1;
}}

.hero-copy h1 {{
  margin: 0 0 .45rem;
  color: #fff;
  font-family: "Amiri", serif;
  font-size: clamp(2.65rem, 8vw, 3.85rem);
  font-weight: 700;
  line-height: 1.04;
}}

.hero-copy p {{
  margin: .25rem 0 1rem;
  color: rgba(255,255,255,.92);
  font-weight: 800;
  font-size: clamp(1rem, 2.2vw, 1.18rem);
}}

.hidden-slide-state {{
  display: none !important;
}}

.gold-cta {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 10rem;
  min-height: 2.75rem;
  padding: .35rem 1.4rem;
  border-radius: 999px;
  color: var(--forest);
  font-weight: 900;
  background: linear-gradient(180deg, #f6df9d, var(--gold));
  box-shadow: inset 0 1px 0 rgba(255,255,255,.62), 0 12px 26px rgba(0,0,0,.18);
}}

.ghost-cta {{
  margin-top: .15rem;
}}

.slide-story-mini {{
  width: min(100%, 18rem);
  padding: .75rem .9rem;
  border-radius: 14px;
  color: #fff;
  background: rgba(0, 0, 0, .18);
  border: 1px solid rgba(198, 161, 91, .38);
}}

.slide-story-mini strong, .slide-story-mini span {{
  display: block;
  color: #fff;
}}

.mini-indicators {{
  display: flex;
  flex-wrap: wrap;
  gap: .45rem;
  margin-top: .8rem;
}}

.mini-indicators span {{
  display: inline-flex;
  align-items: center;
  min-height: 2rem;
  padding: .25rem .65rem;
  border-radius: 999px;
  color: #fff;
  font-weight: 900;
  border: 1px solid rgba(198, 161, 91, .35);
  background: rgba(255, 255, 255, .12);
}}

.hero-arch {{
  min-height: 178px;
  border: 2px solid rgba(198, 161, 91, .48);
  border-radius: 50% 50% 8px 8px / 42% 42% 8px 8px;
  background:
    radial-gradient(circle at 65% 18%, #f7d88c 0 9%, transparent 10%),
    linear-gradient(180deg, rgba(255,236,187,.85), rgba(255,236,187,0) 35%),
    linear-gradient(135deg, rgba(80, 111, 75, .78), rgba(18,63,53,.15) 40%, rgba(169, 88, 60, .46)),
    repeating-linear-gradient(90deg, rgba(198,161,91,.16) 0 1px, transparent 1px 14px);
  box-shadow: inset 0 0 0 8px rgba(18,63,53,.28), 0 16px 32px rgba(0,0,0,.22);
}}

.story-hero {{
  grid-template-columns: .92fr 1.08fr;
  min-height: 258px;
}}

.story-copy h1 {{
  font-size: clamp(2.05rem, 6vw, 3rem);
}}

.story-medallion {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  margin-bottom: .5rem;
  border-radius: 16px;
  color: #f8e8b5;
  font-weight: 900;
  border: 1px solid rgba(198, 161, 91, .70);
  background: rgba(0,0,0,.20);
}}

.hero-meta {{
  display: flex;
  flex-wrap: wrap;
  gap: .45rem;
  margin-top: .85rem;
}}

.hero-meta span, .category-strip span {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.15rem;
  border-radius: 999px;
  padding: .25rem .75rem;
  font-size: .82rem;
  font-weight: 900;
}}

.hero-meta span {{
  color: #fff;
  background: rgba(255,255,255,.13);
  border: 1px solid rgba(255,255,255,.20);
}}

.category-strip {{
  display: flex;
  gap: .65rem;
  overflow-x: auto;
  padding: .15rem 0 .35rem;
  margin: .55rem 0 .85rem;
}}

.clone-chips span {{
  min-width: 5.5rem;
  border-radius: 14px;
}}

.category-strip span {{
  flex: 0 0 auto;
  color: var(--forest);
  background: rgba(255,255,255,.78);
  border: 1px solid var(--soft-border);
  box-shadow: var(--card-shadow);
}}

.section-title {{
  margin: .9rem 0 .55rem;
  color: var(--emerald);
  font-family: "Amiri", serif;
  font-size: clamp(1.55rem, 4vw, 2.15rem);
  font-weight: 700;
  text-align: right;
}}

.section-title.tight {{
  margin-top: .85rem;
}}

.story-card, .detail-panel, .empty-panel, .continue-card, .manuscript-panel, .tafsir-panel, .lesson-row, .flow-step, .explore-card {{
  border: 1px solid var(--border);
  border-radius: 14px;
  background:
    radial-gradient(circle at 0 0, rgba(198, 161, 91, .12), transparent 44%),
    rgba(255,253,247,.82);
  box-shadow: var(--card-shadow);
}}

.visual-card {{
  overflow: hidden;
  min-height: 150px;
  margin: .35rem 0 .25rem;
  background: #fff7e8;
}}

.story-art {{
  position: relative;
  min-height: 98px;
  overflow: hidden;
  border-radius: 13px 13px 0 0;
  background:
    radial-gradient(circle at 20% 25%, rgba(255,225,143,.92), transparent 16%),
    linear-gradient(140deg, rgba(18,63,53,.10), rgba(18,63,53,.82)),
    linear-gradient(40deg, #486b56, #d5a969);
}}

.story-art:before {{
  content: "";
  position: absolute;
  inset: 13px 25% 0 16%;
  border: 6px solid rgba(247, 224, 159, .45);
  border-bottom: 0;
  border-radius: 50% 50% 0 0 / 55% 55% 0 0;
  box-shadow: inset 0 0 0 1px rgba(18,63,53,.38);
}}

.story-art:after {{
  content: "";
  position: absolute;
  inset: auto 0 0 0;
  height: 56%;
  background:
    linear-gradient(180deg, transparent, rgba(3, 15, 13, .78)),
    repeating-linear-gradient(90deg, rgba(255,255,255,.06) 0 1px, transparent 1px 18px);
}}

.art-2 {{ background: radial-gradient(circle at 74% 17%, #f7cf81 0 8%, transparent 9%), linear-gradient(135deg, #44593e, #132d28 56%, #ba8f45); }}
.art-3 {{ background: radial-gradient(circle at 17% 18%, #f5d991 0 9%, transparent 10%), linear-gradient(135deg, #213d4d, #071d19 58%, #a9583c); }}
.art-4 {{ background: radial-gradient(circle at 70% 20%, #f8d791 0 10%, transparent 11%), linear-gradient(135deg, #6c5e45, #123f35 55%, #d1ad69); }}
.art-5 {{ background: radial-gradient(circle at 30% 18%, #f0c477 0 8%, transparent 9%), linear-gradient(135deg, #334936, #0b2d27 60%, #8b5635); }}
.art-6 {{ background: radial-gradient(circle at 68% 18%, #f8dc98 0 10%, transparent 11%), linear-gradient(135deg, #2d4b53, #103b32 57%, #b58d4b); }}

.story-badge {{
  position: absolute;
  top: .45rem;
  left: .45rem;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 12px;
  color: #fff7d5;
  font-weight: 900;
  background: rgba(18,63,53,.86);
  border: 1px solid rgba(198,161,91,.72);
}}

.story-card-body {{
  padding: .5rem .62rem .6rem;
}}

.story-card h3, .detail-panel h3, .continue-card h3, .explore-card h3 {{
  margin: .05rem 0 .25rem;
  color: var(--emerald);
  font-family: "Cairo", "Tajawal", sans-serif;
  font-size: clamp(.94rem, 2.8vw, 1.12rem);
  font-weight: 900;
  line-height: 1.35;
}}

.story-card p, .detail-panel p, .empty-panel p, .continue-card p, .manuscript-panel p, .tafsir-panel p, .lesson-row p, .explore-card p {{
  margin: .25rem 0;
  color: var(--text-secondary);
  font-size: clamp(.78rem, 2.25vw, .92rem);
  line-height: 1.58;
}}

.active-story {{
  border-color: rgba(198, 161, 91, .90);
  box-shadow: 0 0 0 3px rgba(198, 161, 91, .22), 0 18px 34px rgba(18, 63, 53, .18);
}}

.reference-card {{
  position: relative;
  min-height: 108px;
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: .85rem;
  align-items: center;
  padding: .8rem;
  margin: 1.25rem 0 0;
}}

.mini-art {{
  width: 76px;
  height: 76px;
  border-radius: 14px;
  border: 1px solid rgba(198,161,91,.40);
  background: linear-gradient(135deg, #d0a85b, #123f35);
}}

.progress-line {{
  position: absolute;
  right: 7.1rem;
  left: 8.5rem;
  bottom: 1rem;
  height: 6px;
  border-radius: 999px;
  background: rgba(217, 200, 169, .75);
}}

.compact-progress, .inline-progress {{
  position: relative;
  right: auto;
  left: auto;
  bottom: auto;
  width: 100%;
  margin-top: .5rem;
}}

.story-card small {{
  display: block;
  color: var(--text-secondary);
  font-size: .72rem;
  line-height: 1.55;
  margin-top: .25rem;
}}

.progress-line span {{
  display: block;
  height: 100%;
  border-radius: inherit;
  background: var(--gold);
}}

.quran-block {{
  position: relative;
  margin: .85rem auto .6rem;
  max-width: 100%;
  padding: clamp(1.15rem, 3.8vw, 1.8rem);
  border: 1px solid rgba(198, 161, 91, .40);
  border-radius: 16px;
  background:
    linear-gradient(180deg, rgba(255,253,247,.86), rgba(239,228,204,.74)),
    var(--parchment);
  box-shadow: inset 0 0 0 8px rgba(255,255,255,.24), var(--card-shadow);
}}

.quran-block:before {{
  content: "بِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيم";
  display: block;
  margin-bottom: .9rem;
  color: var(--forest);
  text-align: center;
  font-family: "Amiri", serif;
  font-size: clamp(1.05rem, 3vw, 1.32rem);
}}

.quran-block p {{
  margin: 0;
  color: #2a2e25;
  text-align: center;
  font-family: "Amiri", "Noto Naskh Arabic", serif;
  font-size: clamp(1.22rem, 4.2vw, 1.72rem);
  line-height: 2.18;
}}

.tafsir-panel, .detail-panel, .manuscript-panel, .lesson-row {{
  padding: 1rem;
  margin: .7rem 0;
}}

.tafsir-panel {{
  max-width: 840px;
  margin-inline: auto;
  background: rgba(255,250,240,.86);
}}

.tafsir-panel strong, .lesson-row strong, .flow-step strong {{
  color: var(--emerald);
  font-weight: 900;
}}

.manuscript-panel {{
  max-width: 820px;
  margin-inline: auto;
  background:
    linear-gradient(180deg, rgba(255,253,247,.88), rgba(239,228,204,.78)),
    var(--parchment);
}}

.flow-chain {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 13rem), 1fr));
  gap: .75rem;
  margin: .8rem 0;
}}

.flow-step {{
  padding: .9rem;
  min-height: 124px;
}}

.flow-step small {{
  display: block;
  color: var(--text-secondary);
  line-height: 1.75;
}}

.book-medallion, .empty-symbol {{
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: .4rem auto;
  border-radius: 50%;
  color: var(--antique-gold);
  border: 1px solid rgba(198, 161, 91, .46);
  background: rgba(255,253,247,.84);
}}

.centered-state {{
  max-width: 34rem;
  margin: 3rem auto;
  padding: 1.4rem;
  text-align: center;
}}

.centered-state h2, .centered-state p {{
  text-align: center;
}}

.explore-banner {{
  min-height: 198px;
  display: grid;
  grid-template-columns: 1fr 240px;
  align-items: center;
  gap: 1rem;
  padding: clamp(1rem, 3vw, 1.65rem);
  margin-bottom: 1rem;
  border-radius: 0 0 16px 16px;
  border: 1px solid rgba(198, 161, 91, .32);
  background:
    linear-gradient(90deg, rgba(7,29,25,.92), rgba(18,63,53,.76)),
    radial-gradient(circle at 82% 28%, rgba(198,161,91,.38), transparent 12rem);
  color: #fff;
  box-shadow: var(--shadow);
}}

.explore-banner h1 {{
  color: #fff;
  font-family: "Cairo", sans-serif;
  font-size: clamp(1.45rem, 4.5vw, 2.1rem);
  font-weight: 900;
}}

.explore-banner p {{
  color: rgba(255,255,255,.86);
  font-weight: 800;
}}

.lantern-art {{
  height: 154px;
  border-radius: 18px;
  background:
    radial-gradient(circle at 50% 26%, rgba(255,224,139,.95), transparent 18%),
    radial-gradient(circle at 52% 58%, rgba(198,161,91,.52), transparent 24%),
    linear-gradient(135deg, rgba(0,0,0,.18), rgba(0,0,0,.56));
  border: 1px solid rgba(198,161,91,.36);
}}

.explore-grid {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: .65rem;
  margin: 1rem 0;
}}

.explore-card {{
  min-height: 124px;
  padding: .85rem .6rem;
  text-align: center;
}}

.explore-card span {{
  display: block;
  color: var(--antique-gold);
  text-align: center;
  font-size: 2rem;
  line-height: 1;
}}

.explore-card h3, .explore-card p {{
  text-align: center;
}}

.related-card {{
  overflow: hidden;
  padding-bottom: .75rem;
}}

.related-card .story-art {{
  min-height: 96px;
}}

.related-card h3, .related-card p {{
  padding-inline: .75rem;
}}

.stTextInput label, .stSelectbox label, .stMultiSelect label, .stRadio label {{
  color: var(--text-primary);
  font-weight: 900;
  font-size: .86rem;
}}

.stTextInput input {{
  direction: rtl;
  min-height: 2.6rem;
  border-radius: 999px;
  border: 1px solid var(--soft-border);
  background: rgba(255,255,255,.82);
  box-shadow: var(--card-shadow);
  text-align: right;
  font-family: "Cairo", sans-serif;
}}

.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {{
  direction: rtl;
  min-height: 2.6rem;
  border-radius: 999px;
  border-color: var(--soft-border);
  background: rgba(255,255,255,.84);
  box-shadow: var(--card-shadow);
}}

.stButton > button {{
  width: 100%;
  min-height: 2.38rem;
  border-radius: 14px;
  border: 1px solid rgba(198, 161, 91, .38);
  background: linear-gradient(180deg, rgba(255,253,247,.96), rgba(239,228,204,.86));
  color: var(--emerald);
  font-family: "Cairo", sans-serif;
  font-weight: 900;
  box-shadow: 0 8px 16px rgba(18,63,53,.08);
}}

.stButton > button:hover {{
  border-color: var(--gold);
  color: var(--forest);
  box-shadow: 0 10px 20px rgba(18,63,53,.13);
}}

[role="radiogroup"] {{
  width: 100%;
  display: grid !important;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: .35rem;
  padding: .45rem;
  margin: .8rem 0;
  border-radius: 16px;
  background: rgba(255,253,247,.74);
  border: 1px solid var(--soft-border);
  box-shadow: var(--card-shadow);
}}

[role="radiogroup"] label {{
  min-height: 58px;
  justify-content: center;
  border-radius: 12px;
  padding: .25rem !important;
  border: 1px solid transparent;
}}

[role="radiogroup"] label:has(input:checked) {{
  color: var(--gold);
  background: var(--emerald);
  border-color: var(--gold);
}}

@media (max-width: 860px) {{
  .block-container {{
    max-width: 560px;
  }}
  .top-nav {{
    grid-template-columns: 44px 1fr auto;
  }}
  .top-nav .nav-links {{
    display: none;
  }}
  .selected-mini {{
    display: none;
  }}
  .target-hero, .story-hero, .explore-banner {{
    grid-template-columns: 1fr;
  }}
  .hero-arch, .lantern-art {{
    min-height: 150px;
  }}
  .explore-grid {{
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }}
  [role="radiogroup"] {{
    grid-template-columns: repeat(5, minmax(86px, 1fr));
    overflow-x: auto;
  }}
}}

@media (max-width: 640px) {{
  .block-container {{
    padding: .55rem .55rem calc(6.8rem + env(safe-area-inset-bottom));
  }}
  .top-nav {{
    top: 0;
    border-radius: 16px 16px 0 0;
    min-height: 54px;
  }}
  .bottom-nav {{
    position: fixed;
    left: .55rem;
    right: .55rem;
    bottom: calc(.55rem + env(safe-area-inset-bottom));
    z-index: 110;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: .28rem;
    padding: .45rem;
    border-radius: 18px;
    border: 1px solid rgba(198, 161, 91, .36);
    background: linear-gradient(135deg, var(--night-green), var(--emerald));
    box-shadow: 0 18px 40px rgba(7, 29, 25, .28);
  }}
  .bottom-nav .nav-link {{
    min-height: 46px;
    flex-direction: column;
    gap: .04rem;
    padding: .1rem .2rem;
    font-size: .78rem;
  }}
  .target-hero {{
    min-height: 250px;
    padding: 1rem;
  }}
  .hero-copy h1 {{
    font-size: clamp(2.2rem, 13vw, 3.1rem);
  }}
  .story-art {{
    min-height: 108px;
  }}
  .explore-grid {{
    grid-template-columns: 1fr 1fr;
    gap: .55rem;
  }}
  .explore-card {{
    min-height: 126px;
    padding: .8rem .5rem;
  }}
  .reference-card {{
    grid-template-columns: 70px 1fr;
  }}
  .mini-art {{
    width: 62px;
    height: 62px;
  }}
  .progress-line {{
    right: 5.6rem;
    left: 1rem;
  }}
}}

@media (max-width: 380px) {{
  .block-container {{
    padding-inline: .45rem;
  }}
  .screen-title {{
    font-size: 1.2rem;
  }}
  .explore-grid {{
    grid-template-columns: 1fr;
  }}
  .story-card h3, .detail-panel h3, .explore-card h3 {{
    font-size: 1rem;
  }}
}}
</style>
"""
