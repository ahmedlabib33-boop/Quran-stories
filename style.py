from __future__ import annotations


def build_css(theme_key: str = "light") -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;500;700;800;900&family=Noto+Kufi+Arabic:wght@500;600;700;800&family=Tajawal:wght@400;500;700;800&display=swap');

:root {
  --emerald-950: #071D19;
  --emerald-900: #0B2D27;
  --emerald-800: #123F35;
  --emerald-700: #194E42;
  --ivory-50: #FFFDF7;
  --ivory-100: #F7F1E3;
  --parchment-200: #EFE4CC;
  --sand-300: #D9C8A9;
  --gold-400: #D8B76A;
  --gold-500: #C6A15B;
  --gold-600: #A9803A;
  --terracotta-500: #A9583C;
  --burgundy-700: #672D36;
  --text-main: #232722;
  --text-secondary: #6E6759;
  --text-on-dark: #F7F1E3;
  --gold-border: rgba(198, 161, 91, 0.42);
  --gold-border-soft: rgba(198, 161, 91, 0.24);
  --dark-shadow: rgba(7, 29, 25, 0.22);
  --warm-shadow: rgba(74, 50, 25, 0.12);
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.block-container {
  direction: rtl;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

*,
*::before,
*::after {
  box-sizing: border-box;
  min-width: 0;
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  color: var(--text-main);
  font-family: "Cairo", "Tajawal", sans-serif;
  background:
    radial-gradient(circle at 12% 4%, rgba(216, 183, 106, .22), transparent 24rem),
    radial-gradient(circle at 90% 10%, rgba(217, 200, 169, .32), transparent 22rem),
    linear-gradient(45deg, rgba(198,161,91,.045) 25%, transparent 25%) 0 0/28px 28px,
    linear-gradient(135deg, var(--ivory-50), var(--ivory-100) 55%, #f3ead7);
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"],
#MainMenu,
footer,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
  display: none !important;
  visibility: hidden !important;
  height: 0 !important;
}

.stAppToolbar,
[data-testid="stToolbarActions"],
.stAppDeployButton,
[data-testid="stAppDeployButton"],
button[kind="header"] {
  display: none !important;
  visibility: hidden !important;
}

.block-container {
  max-width: 1500px;
  margin-inline: auto;
  padding: 14px clamp(14px, 2.2vw, 28px) 104px;
}

h1, h2, h3, p, span, label, div, button {
  direction: rtl;
  letter-spacing: 0;
  overflow-wrap: anywhere;
}

p {
  font-family: "Tajawal", sans-serif;
  font-size: clamp(.92rem, 1.2vw, 1.06rem);
  line-height: 1.85;
}

div[data-testid="stVerticalBlock"],
div[data-testid="column"],
[data-testid="stHorizontalBlock"],
[data-testid="stElementContainer"] {
  max-width: 100%;
  min-width: 0;
}

.app-top-frame {
  position: relative;
  min-height: 104px;
  margin: 0 0 10px;
  overflow: hidden;
  border: 1px solid rgba(216,183,106,.48);
  border-radius: 0 0 26px 26px;
  background:
    linear-gradient(45deg, transparent 48%, rgba(216,183,106,.10) 49%, transparent 50%) 0 0/34px 34px,
    radial-gradient(circle at 8% 18%, rgba(216,183,106,.24), transparent 16rem),
    linear-gradient(135deg, var(--emerald-950), var(--emerald-800));
  box-shadow: 0 18px 42px var(--dark-shadow);
}

.app-top-frame::before,
.app-top-frame::after {
  content: "";
  position: absolute;
  width: 148px;
  height: 148px;
  border: 1px solid rgba(216,183,106,.38);
  border-radius: 50% 50% 12px 12px / 42% 42% 12px 12px;
  opacity: .62;
}

.app-top-frame::before {
  right: 22px;
  bottom: -68px;
}

.app-top-frame::after {
  left: 22px;
  bottom: -82px;
}

.brand-lockup {
  position: relative;
  z-index: 1;
  min-height: 104px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  color: var(--text-on-dark);
  text-align: center;
}

.brand-lockup h1 {
  margin: 0;
  color: var(--ivory-100);
  font-family: "Noto Kufi Arabic", "Amiri", serif;
  font-size: clamp(2rem, 5vw, 4.4rem);
  font-weight: 700;
  line-height: 1.05;
  text-align: center;
}

.brand-lockup p {
  margin: 4px 0 0;
  color: rgba(247,241,227,.88);
  font-weight: 700;
  text-align: center;
}

.brand-mark,
.brand-emblem,
.application-card span {
  display: inline-flex;
  width: 42px;
  height: 42px;
  flex: 0 0 42px;
  border: 1px solid rgba(216,183,106,.70);
  border-radius: 50%;
  background:
    conic-gradient(from 45deg, transparent 0 12.5%, rgba(216,183,106,.95) 12.5% 18%, transparent 18% 31%, rgba(216,183,106,.95) 31% 36%, transparent 36% 50%, rgba(216,183,106,.95) 50% 56%, transparent 56% 69%, rgba(216,183,106,.95) 69% 74%, transparent 74% 100%),
    radial-gradient(circle, rgba(216,183,106,.18) 0 38%, transparent 39%);
}

.html-desktop-nav {
  position: sticky;
  top: 10px;
  z-index: 90;
  max-width: 760px;
  margin: -28px auto 20px;
  padding: 7px;
  border: 1px solid rgba(216,183,106,.62);
  border-radius: 999px;
  background: rgba(7,29,25,.98);
  box-shadow: 0 16px 34px rgba(7,29,25,.28);
  backdrop-filter: blur(16px);
}

.html-desktop-nav {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 6px;
}

.html-mobile-nav,
.st-key-mobile_nav {
  display: none;
}

.html-desktop-nav a {
  min-height: 50px;
  display: grid;
  place-items: center;
  border: 1px solid transparent;
  border-radius: 999px;
  color: rgba(247,241,227,.86);
  text-decoration: none;
  font-family: "Cairo", sans-serif;
  font-weight: 900;
}

.html-desktop-nav a.active {
  color: var(--ivory-100);
  background: linear-gradient(180deg, rgba(25,78,66,.96), rgba(18,63,53,.96));
  border-color: rgba(216,183,106,.72);
}

.mobile-screen-bar {
  display: none;
}

.stButton > button {
  width: 100%;
  min-height: 48px;
  border-radius: 999px !important;
  border: 1px solid rgba(198,161,91,.42) !important;
  color: var(--emerald-800) !important;
  background: linear-gradient(180deg, var(--ivory-50), var(--parchment-200)) !important;
  box-shadow: 0 8px 18px rgba(74,50,25,.08) !important;
  font-family: "Cairo", sans-serif !important;
  font-weight: 900 !important;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}

.stButton > button:hover {
  transform: translateY(-1px);
  border-color: rgba(216,183,106,.82) !important;
  box-shadow: 0 12px 26px rgba(74,50,25,.14) !important;
}

.stButton > button[kind="primary"] {
  color: var(--ivory-100) !important;
  background: linear-gradient(135deg, var(--emerald-900), var(--emerald-800)) !important;
  border-color: var(--gold-400) !important;
  box-shadow: inset 0 0 0 1px rgba(216,183,106,.18), 0 12px 26px rgba(7,29,25,.25) !important;
}

.st-key-desktop_nav .stButton > button,
.st-key-mobile_nav .stButton > button {
  min-height: 50px;
  color: rgba(247,241,227,.86) !important;
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
}

.st-key-desktop_nav .stButton > button[kind="primary"],
.st-key-mobile_nav .stButton > button[kind="primary"] {
  color: var(--ivory-100) !important;
  background: linear-gradient(180deg, rgba(25,78,66,.96), rgba(18,63,53,.96)) !important;
  border-color: rgba(216,183,106,.72) !important;
}

.carousel-shell {
  width: 100%;
  overflow: hidden;
  border-radius: 26px;
}

.brand-slide {
  position: relative;
  min-height: clamp(330px, 37vw, 520px);
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(280px, .82fr);
  align-items: center;
  gap: clamp(22px, 4vw, 52px);
  padding: clamp(24px, 5vw, 58px);
  overflow: hidden;
  color: var(--text-on-dark);
  border: 1px solid rgba(216,183,106,.58);
  border-bottom: 4px solid var(--gold-500);
  border-radius: 26px;
  background:
    radial-gradient(circle at 20% 20%, rgba(216,183,106,.16), transparent 16rem),
    linear-gradient(45deg, transparent 48%, rgba(216,183,106,.09) 49%, transparent 50%) 0 0/34px 34px,
    linear-gradient(135deg, rgba(7,29,25,.98), rgba(18,63,53,.96));
  box-shadow: 0 20px 52px var(--dark-shadow);
}

.brand-slide::before {
  content: "";
  position: absolute;
  inset: 13px;
  pointer-events: none;
  border: 1px solid rgba(216,183,106,.34);
  border-radius: 21px;
}

.brand-slide h1 {
  margin: 0 0 10px;
  color: var(--ivory-100);
  font-family: "Noto Kufi Arabic", "Amiri", serif;
  font-size: clamp(2rem, 3.4vw, 3.8rem);
  font-weight: 700;
  line-height: 1.22;
}

.brand-slide p {
  max-width: 620px;
  margin: 0 0 20px;
  color: rgba(247,241,227,.92);
  font-family: "Tajawal", sans-serif;
  font-weight: 700;
  line-height: 1.9;
}

.brand-emblem {
  margin-bottom: 14px;
  background-color: rgba(7,29,25,.32);
}

.gold-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 8px 30px;
  border-radius: 999px;
  color: var(--emerald-900);
  font-family: "Cairo", sans-serif;
  font-weight: 900;
  background: linear-gradient(180deg, var(--gold-400), var(--gold-500));
  box-shadow: inset 0 1px 0 rgba(255,255,255,.42), 0 14px 28px rgba(7,29,25,.24);
}

.andalusian-arch,
.lantern-panel,
.star-panel,
.story-visual {
  position: relative;
  min-height: 270px;
  border: 2px solid rgba(216,183,106,.58);
  border-radius: 50% 50% 16px 16px / 42% 42% 16px 16px;
  background:
    radial-gradient(circle at 68% 18%, rgba(255,225,151,.95) 0 7%, transparent 8%),
    linear-gradient(180deg, rgba(255,236,187,.78), rgba(255,236,187,0) 32%),
    linear-gradient(135deg, rgba(82,116,82,.78), rgba(18,63,53,.18) 45%, rgba(169,88,60,.45)),
    repeating-linear-gradient(90deg, rgba(216,183,106,.14) 0 1px, transparent 1px 17px);
  box-shadow: inset 0 0 0 9px rgba(7,29,25,.24), 0 18px 34px rgba(0,0,0,.20);
}

.lantern-panel {
  border-radius: 22px;
  background:
    radial-gradient(circle at 50% 30%, rgba(255,224,139,.98), transparent 15%),
    radial-gradient(circle at 55% 65%, rgba(198,161,91,.55), transparent 24%),
    linear-gradient(135deg, rgba(7,29,25,.35), rgba(7,29,25,.78));
}

.star-panel {
  border-radius: 22px;
  background:
    repeating-conic-gradient(from 45deg, rgba(216,183,106,.30) 0 8deg, transparent 8deg 18deg),
    linear-gradient(135deg, rgba(7,29,25,.30), rgba(216,183,106,.22));
}

.indicator-cloud,
.meta-row,
.skill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.indicator-cloud {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  max-width: 560px;
}

.indicator-cloud span,
.meta-row span,
.skill-row span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 34px;
  padding: 5px 12px;
  border-radius: 999px;
  color: var(--emerald-900);
  font-family: "Cairo", sans-serif;
  font-size: .84rem;
  font-weight: 900;
  background: rgba(255,253,247,.84);
  border: 1px solid rgba(198,161,91,.38);
}

.slide-progress {
  width: 100%;
  height: 8px;
  margin: 12px 0;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(217,200,169,.80);
}

.slide-progress span {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--emerald-800), var(--gold-500));
}

.control-panel,
.selected-card,
.story-header,
.explore-header,
.analysis-block,
.manuscript-panel,
.ayah-card,
.related-card,
.application-card {
  width: 100%;
  max-width: 100%;
  margin: 16px 0;
  padding: clamp(16px, 3vw, 26px);
  border: 1px solid var(--gold-border);
  border-radius: 24px;
  background:
    radial-gradient(circle at 100% 0, rgba(216,183,106,.12), transparent 32%),
    linear-gradient(180deg, rgba(255,253,247,.95), rgba(247,241,227,.92));
  box-shadow: 0 16px 34px var(--warm-shadow);
}

.control-panel {
  max-width: 720px;
  margin-inline: auto;
  padding: 20px;
}

.selected-card,
.story-header {
  display: grid;
  grid-template-columns: minmax(210px, .38fr) minmax(0, 1fr);
  gap: clamp(18px, 3vw, 34px);
  align-items: center;
}

.story-header {
  position: relative;
  grid-template-columns: minmax(220px, .34fr) minmax(0, 1fr) minmax(98px, .16fr);
  overflow: hidden;
}

.story-header::after {
  content: "";
  position: absolute;
  top: 18px;
  left: 34px;
  width: 30px;
  height: 54px;
  border: 1px solid rgba(169,128,58,.50);
  border-radius: 15px 15px 8px 8px;
  background: radial-gradient(circle at 50% 70%, rgba(216,183,106,.85), transparent 42%), rgba(7,29,25,.10);
}

.story-visual {
  min-height: 224px;
  border-radius: 50% 50% 18px 18px / 38% 38% 18px 18px;
}

.story-visual span,
.story-medallion,
.ayah-card header span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--emerald-900);
  font-family: "Cairo", sans-serif;
  font-weight: 900;
  background: linear-gradient(180deg, #f3dda1, var(--gold-500));
  border: 1px solid var(--gold-600);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.45);
}

.story-visual span {
  position: absolute;
  top: 14px;
  left: 14px;
  width: 46px;
  height: 46px;
  border-radius: 16px;
}

.story-medallion {
  width: 54px;
  height: 54px;
  margin-bottom: 10px;
  border-radius: 18px;
}

.selected-card h2,
.story-header h1,
.explore-header h1,
.section-title {
  margin: 0 0 10px;
  color: var(--emerald-800);
  font-family: "Noto Kufi Arabic", "Amiri", serif;
  font-size: clamp(1.2rem, 2vw, 1.8rem);
  font-weight: 700;
  line-height: 1.35;
}

.story-header h1 {
  font-size: clamp(2rem, 3.4vw, 3.8rem);
  text-align: center;
}

.selected-card p,
.story-header p,
.explore-header p,
.analysis-block p,
.manuscript-panel p,
.related-card p,
.application-card p {
  color: var(--text-secondary);
  line-height: 1.85;
  margin: 6px 0;
}

.refs {
  white-space: normal;
  overflow-wrap: anywhere;
  word-break: normal;
}

.progress-ring {
  width: 96px;
  height: 96px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background:
    radial-gradient(circle, var(--ivory-50) 0 57%, transparent 58%),
    conic-gradient(var(--gold-500) var(--value), rgba(217,200,169,.75) 0);
  border: 1px solid rgba(198,161,91,.45);
}

.progress-ring strong,
.progress-ring small {
  grid-area: 1 / 1;
  text-align: center;
  color: var(--emerald-900);
  font-family: "Cairo", sans-serif;
}

.progress-ring small {
  margin-top: 38px;
  font-size: .72rem;
}

.stSelectbox,
.stTextInput,
.stExpander {
  max-width: 100%;
}

.stSelectbox label,
.stTextInput label {
  color: var(--emerald-900) !important;
  font-family: "Cairo", sans-serif !important;
  font-weight: 900 !important;
  text-align: right !important;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
  direction: rtl;
  min-height: 50px;
  border-radius: 14px !important;
  border: 1px solid var(--gold-border) !important;
  color: var(--emerald-900) !important;
  background: rgba(255,253,247,.94) !important;
  font-family: "Cairo", sans-serif !important;
  box-shadow: 0 8px 18px rgba(74,50,25,.06) !important;
}

.st-key-story_tabs {
  max-width: 100%;
  overflow-x: auto;
  padding: 8px 0 10px;
  scrollbar-width: thin;
}

.st-key-story_tabs > div > [data-testid="stVerticalBlock"] {
  display: grid !important;
  grid-template-columns: repeat(5, minmax(128px, 1fr));
  gap: 8px;
  min-width: 700px;
  padding: 8px;
  border: 1px solid rgba(198,161,91,.24);
  border-radius: 22px;
  background: rgba(239,228,204,.55);
}

.st-key-story_tabs .stButton > button {
  min-height: 58px;
  border-radius: 18px !important;
}

.st-key-story_prev_next > div > [data-testid="stVerticalBlock"] {
  display: grid !important;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.st-key-slide_controls {
  max-width: 560px;
  margin: 12px auto 6px;
  display: grid !important;
  grid-template-columns: minmax(86px, 1fr) 46px 46px 46px minmax(86px, 1fr);
  align-items: center;
  gap: 8px;
}

.stVerticalBlock.st-key-slide_controls {
  display: grid !important;
  grid-template-columns: minmax(86px, 1fr) 46px 46px 46px minmax(86px, 1fr) !important;
  align-items: center !important;
  gap: 8px !important;
}

.st-key-slide_controls .stButton > button {
  min-height: 42px;
  padding: 4px 8px !important;
}

.st-key-slide_controls [data-testid="stElementContainer"]:nth-child(2) .stButton > button,
.st-key-slide_controls [data-testid="stElementContainer"]:nth-child(3) .stButton > button,
.st-key-slide_controls [data-testid="stElementContainer"]:nth-child(4) .stButton > button {
  min-height: 42px;
  width: 42px;
  margin-inline: auto;
  padding: 0 !important;
  color: var(--emerald-800) !important;
  background: rgba(255,253,247,.78) !important;
}

.ayah-card {
  position: relative;
  background:
    linear-gradient(45deg, rgba(198,161,91,.055) 25%, transparent 25%) 0 0/22px 22px,
    linear-gradient(180deg, rgba(255,253,247,.96), rgba(239,228,204,.82));
}

.ayah-card::before {
  content: "";
  position: absolute;
  inset: 10px;
  pointer-events: none;
  border: 1px solid rgba(198,161,91,.22);
  border-radius: 18px;
}

.ayah-card header {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 14px;
}

.ayah-card header span {
  min-width: 42px;
  height: 42px;
  border-radius: 50%;
}

.ayah-card header strong {
  color: var(--emerald-800);
  font-family: "Noto Kufi Arabic", sans-serif;
  font-weight: 800;
}

.ayah-card header small {
  color: var(--text-secondary);
  font-family: "Cairo", sans-serif;
}

.quran-text {
  position: relative;
  padding: clamp(18px, 3.2vw, 34px);
  border-radius: 18px;
  color: var(--text-main);
  text-align: center;
  font-family: "Amiri", "Noto Naskh Arabic", serif;
  font-size: clamp(1.65rem, 2.8vw, 2.8rem);
  line-height: 2.15;
  background: rgba(247,241,227,.74);
  border: 1px solid rgba(198,161,91,.30);
}

.tafsir-under {
  position: relative;
  margin-top: 12px;
  padding: 16px 18px;
  border-radius: 16px;
  background: rgba(239,228,204,.66);
  border: 1px solid rgba(198,161,91,.22);
  border-top: 3px solid rgba(198,161,91,.50);
}

.tafsir-under strong {
  color: var(--emerald-800);
  font-family: "Noto Kufi Arabic", sans-serif;
}

.tafsir-under p {
  margin: 6px 0 0;
  color: var(--text-secondary);
  line-height: 1.95;
}

.analysis-block,
.manuscript-panel {
  position: relative;
  border-radius: 22px;
}

.analysis-block h3,
.application-card h3 {
  margin: 0 0 8px;
  color: var(--emerald-800);
  font-family: "Noto Kufi Arabic", sans-serif;
  font-size: clamp(1rem, 1.4vw, 1.32rem);
}

.analysis-block::before {
  content: "";
  display: inline-flex;
  width: 30px;
  height: 30px;
  margin-bottom: 8px;
  border-radius: 50%;
  background: radial-gradient(circle, var(--gold-400) 0 34%, transparent 35%), conic-gradient(from 45deg, var(--gold-600), var(--gold-400), var(--gold-600));
}

.transformation-flow {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 154px), 1fr));
  gap: 14px;
  align-items: stretch;
}

.transformation-flow article {
  position: relative;
  min-height: 150px;
  padding: 18px;
  border-radius: 20px;
  border: 1px solid var(--gold-border);
  background: rgba(255,253,247,.90);
}

.transformation-flow span {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  color: var(--ivory-100);
  border-radius: 50%;
  background: var(--emerald-800);
  border: 1px solid var(--gold-500);
}

.applications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr));
  gap: 14px;
}

.application-card {
  min-height: 160px;
}

.explore-shell {
  margin: 0 -8px;
  padding: clamp(16px, 3vw, 28px);
  border-radius: 28px;
  background:
    linear-gradient(45deg, transparent 48%, rgba(216,183,106,.08) 49%, transparent 50%) 0 0/32px 32px,
    linear-gradient(135deg, var(--emerald-950), var(--emerald-800));
  box-shadow: 0 18px 44px var(--dark-shadow);
}

.explore-shell .stSelectbox label {
  color: var(--ivory-100) !important;
}

.explore-header {
  color: var(--text-on-dark);
  background:
    radial-gradient(circle at 90% 50%, rgba(216,183,106,.20), transparent 14rem),
    linear-gradient(135deg, rgba(7,29,25,.84), rgba(18,63,53,.78));
  border-color: rgba(216,183,106,.45);
}

.explore-header h1,
.explore-header p {
  color: var(--ivory-100);
}

.explore-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.explore-card {
  width: 100%;
  min-height: 178px;
  padding: 20px 16px;
  text-align: center;
  border: 1px solid rgba(198,161,91,.34);
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(255,253,247,.97), rgba(247,241,227,.94));
  box-shadow: 0 12px 26px rgba(7,29,25,.16);
}

.explore-card h3,
.explore-card p {
  text-align: center;
}

.explore-card::before {
  content: "";
  display: block;
  width: 42px;
  height: 42px;
  margin: 0 auto 10px;
  border: 1px solid var(--gold-border);
  border-radius: 50%;
  background:
    conic-gradient(from 45deg, transparent 0 12%, var(--gold-600) 12% 18%, transparent 18% 31%, var(--gold-600) 31% 36%, transparent 36% 50%, var(--gold-600) 50% 56%, transparent 56% 69%, var(--gold-600) 69% 74%, transparent 74% 100%),
    radial-gradient(circle, rgba(216,183,106,.20), transparent 55%);
}

.explore-card h3 {
  margin: 6px 0;
  color: var(--emerald-800);
  font-family: "Noto Kufi Arabic", sans-serif;
  font-size: clamp(1rem, 1.4vw, 1.32rem);
}

.explore-card p {
  margin: 0;
  color: var(--text-secondary);
  font-size: .9rem;
  line-height: 1.7;
}

.related-card {
  background: linear-gradient(180deg, rgba(255,253,247,.96), rgba(239,228,204,.86));
  min-height: 146px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

@media (max-width: 1023px) {
  .explore-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1180px) {
  .block-container {
    max-width: 100%;
    padding: 6px 12px calc(124px + env(safe-area-inset-bottom));
  }

  .app-top-frame {
    display: none;
  }

  .mobile-screen-bar {
    position: sticky;
    top: 6px;
    z-index: 80;
    min-height: 50px;
    display: grid;
    grid-template-columns: 34px minmax(0, 1fr) minmax(78px, .52fr);
    align-items: center;
    gap: 7px;
    margin: -64px 0 8px;
    padding: 6px 8px;
    border: 1px solid rgba(216,183,106,.62);
    border-bottom: 2px solid var(--gold-500);
    border-radius: 18px;
    color: var(--ivory-100);
    background:
      linear-gradient(45deg, transparent 48%, rgba(216,183,106,.08) 49%, transparent 50%) 0 0/28px 28px,
      linear-gradient(135deg, var(--emerald-950), var(--emerald-800));
    box-shadow: 0 12px 26px rgba(7,29,25,.20);
  }

  .mobile-screen-bar h2,
  .mobile-screen-bar small,
  .mobile-screen-bar strong {
    margin: 0;
    color: var(--ivory-100);
    text-align: center;
    font-family: "Cairo", sans-serif;
  }

  .mobile-screen-bar h2 {
    font-size: .98rem;
    font-weight: 900;
  }

  .mobile-screen-bar div {
    display: grid;
    gap: 1px;
    padding: 4px 6px;
    border: 1px solid rgba(216,183,106,.46);
    border-radius: 999px;
    background: rgba(7,29,25,.28);
  }

  .mobile-screen-bar small {
    display: none;
    font-size: .54rem;
    opacity: .75;
  }

  .mobile-screen-bar strong {
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: .66rem;
  }

  .screen-menu {
    width: 22px;
    height: 16px;
    display: inline-block;
    margin-inline: auto;
    border-top: 2px solid var(--gold-400);
    border-bottom: 2px solid var(--gold-400);
    position: relative;
  }

  .screen-menu::before {
    content: "";
    position: absolute;
    inset-inline: 0;
    top: 7px;
    border-top: 2px solid var(--gold-400);
  }

  .brand-lockup {
    min-height: 56px;
    gap: 10px;
  }

  .brand-lockup h1 {
    font-size: clamp(1.55rem, 7vw, 2.15rem);
  }

  .brand-lockup p {
    display: none;
  }

  .brand-mark {
    width: 30px;
    height: 30px;
    flex-basis: 30px;
  }

  .html-desktop-nav,
  .st-key-desktop_nav,
  .st-key-mobile_nav {
    display: none !important;
  }

  div[data-testid="stElementContainer"]:has(.st-key-desktop_nav),
  div[data-testid="stElementContainer"]:has(.st-key-mobile_nav) {
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
  }

  .html-mobile-nav {
    position: fixed;
    left: 12px;
    right: 12px;
    bottom: calc(10px + env(safe-area-inset-bottom));
    width: auto;
    max-width: none;
    min-width: 0;
    z-index: 99999;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    align-items: stretch;
    gap: 4px;
    padding: 7px;
    border: 1px solid rgba(198, 161, 91, 0.62);
    border-radius: 24px;
    background: rgba(7, 29, 25, 0.98);
    box-shadow: 0 14px 34px rgba(7, 29, 25, 0.32);
    backdrop-filter: blur(16px);
  }

  .html-mobile-nav a {
    min-height: 56px;
    display: grid;
    place-items: center;
    padding: 4px 2px;
    border: 1px solid transparent;
    border-radius: 18px;
    color: rgba(247,241,227,.84);
    text-align: center;
    text-decoration: none;
    font-family: "Cairo", sans-serif;
    font-size: .78rem;
    font-weight: 900;
  }

  .html-mobile-nav a.active {
    color: var(--ivory-100);
    background: linear-gradient(180deg, rgba(25,78,66,.96), rgba(18,63,53,.96));
    border-color: rgba(216,183,106,.72);
  }

  .brand-slide {
    grid-template-columns: 1fr;
    min-height: 0;
    height: clamp(178px, 34vh, 218px);
    padding: 10px 14px;
    gap: 6px;
  }

  .carousel-shell {
    margin-top: -64px;
  }

  .brand-slide h1 {
    text-align: center;
    font-size: clamp(1.42rem, 7vw, 1.95rem);
    margin-bottom: 2px;
  }

  .brand-slide p {
    text-align: center;
    margin-inline: auto;
    margin-bottom: 5px;
    font-size: .78rem;
    line-height: 1.42;
  }

  .brand-emblem,
  .gold-cta {
    margin-inline: auto;
  }

  .andalusian-arch,
  .lantern-panel,
  .star-panel {
    min-height: 34px;
    max-height: 42px;
  }

  .gold-cta {
    min-height: 34px;
    padding: 5px 18px;
    font-size: .82rem;
  }

  .stVerticalBlock.st-key-slide_controls,
  div[data-testid="stVerticalBlock"].st-key-slide_controls {
    margin: 6px auto 4px !important;
    gap: 5px !important;
    grid-template-columns: minmax(64px, 1fr) 34px 34px 34px minmax(64px, 1fr) !important;
  }

  .st-key-slide_controls .stButton > button {
    min-height: 34px;
    padding: 2px 6px !important;
    font-size: .78rem !important;
  }

  .control-panel {
    margin: 6px 0 4px;
    padding: 8px;
  }

  .indicator-cloud {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .selected-card,
  .story-header {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .story-header {
    gap: 8px;
    padding: 10px;
    margin: 8px 0 10px;
  }

  .story-visual {
    display: none;
  }

  .story-visual span {
    width: 38px;
    height: 38px;
    top: 10px;
    left: 10px;
    border-radius: 14px;
  }

  .story-medallion {
    width: 36px;
    height: 36px;
    margin: 0 auto 4px;
    border-radius: 12px;
    font-size: .9rem;
  }

  .story-header h1 {
    font-size: clamp(1.42rem, 7vw, 1.9rem);
    margin-bottom: 2px;
  }

  .story-header p {
    font-size: .82rem;
    line-height: 1.35;
    margin: 2px 0;
  }

  .story-header .refs {
    display: none;
  }

  .story-header .meta-row span {
    min-height: 28px;
    padding: 3px 8px;
    font-size: .72rem;
  }

  .progress-ring {
    display: none;
  }

  .progress-ring {
    margin-inline: auto;
  }

  .meta-row,
  .skill-row {
    justify-content: center;
  }

  .selected-card h2,
  .selected-card p,
  .story-header h1,
  .story-header p {
    text-align: center;
  }

  .st-key-story_tabs > div > [data-testid="stVerticalBlock"] {
    grid-template-columns: repeat(5, minmax(136px, 1fr));
    min-width: 720px;
  }

  .stVerticalBlock.st-key-story_tabs,
  div[data-testid="stVerticalBlock"].st-key-story_tabs {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    padding: 4px 0 6px !important;
  }

  .stVerticalBlock.st-key-story_tabs [data-testid="stHorizontalBlock"],
  div[data-testid="stVerticalBlock"].st-key-story_tabs [data-testid="stHorizontalBlock"] {
    display: grid !important;
    grid-template-columns: repeat(5, 116px) !important;
    grid-auto-flow: column !important;
    gap: 6px !important;
    width: max-content !important;
    min-width: max-content !important;
    flex-wrap: nowrap !important;
  }

  .stVerticalBlock.st-key-story_tabs [data-testid="column"],
  div[data-testid="stVerticalBlock"].st-key-story_tabs [data-testid="column"] {
    width: 116px !important;
    min-width: 116px !important;
    flex: 0 0 116px !important;
  }

  .st-key-story_prev_next > div > [data-testid="stVerticalBlock"],
  .explore-grid,
  .transformation-flow,
  .applications-grid {
    grid-template-columns: 1fr;
  }

  .quran-text {
    font-size: clamp(1.45rem, 7vw, 2.05rem);
    line-height: 2.05;
  }

  .explore-shell {
    margin: 0;
    padding: 14px;
    border-radius: 22px;
  }
}

@media (min-width: 1181px) {
  .st-key-mobile_nav {
    display: none !important;
  }
}

div.stVerticalBlock.st-key-slide_controls,
div[data-testid="stVerticalBlock"].st-key-slide_controls {
  display: grid !important;
  grid-template-columns: minmax(82px, 1fr) 42px 42px 42px minmax(82px, 1fr) !important;
  align-items: center !important;
  gap: 8px !important;
  max-width: 560px !important;
  margin: 12px auto 8px !important;
}

div.stVerticalBlock.st-key-slide_controls > div,
div[data-testid="stVerticalBlock"].st-key-slide_controls > div {
  width: 100% !important;
}
</style>
"""
