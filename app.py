from __future__ import annotations

import html
import math
import re
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from data_loader import StoryRepository
from style import build_css


APP_DIR = Path(__file__).parent
CONTENT_DIR = APP_DIR / "Quran_Stories"
WORKBOOK_PATH = APP_DIR / ".streamlit" / "Stories included in holy (Quran).xlsx"

VIEW_LABELS = {"home": "الرئيسية", "story": "القصة", "explore": "استكشف"}
STORY_TABS = {
    "verses": "الآيات",
    "tafsir": "التفسير والتحليل",
    "summary": "خلاصة القصة",
    "transformation": "التحول الإنساني",
    "applications": "التطبيقات العملية",
}
TAB_PROGRESS = {"verses": 25, "tafsir": 45, "summary": 60, "transformation": 80, "applications": 100}
EXPLORE_BLOCKS = [
    "القيم الأساسية",
    "التحليل النفسي",
    "الدروس القيادية",
    "الدروس الأخلاقية",
    "الدروس الإدارية",
    "الصبر والمرونة",
    "نموذج السبب والنتيجة",
    "المهارات المكتسبة",
    "نقاط التحول",
]
DEFAULT_STATE = {
    "active_view": "home",
    "selected_story_id": None,
    "selected_surah": None,
    "active_story_tab": "verses",
    "home_slide": 0,
    "last_opened_story_id": None,
    "story_progress": {},
    "search_query": "",
    "category_filter": "الكل",
    "value_filter": "الكل",
    "skill_filter": "الكل",
}


st.set_page_config(
    page_title="اِبْتِهَال",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value))


def is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, float) and math.isnan(value):
        return False
    text = str(value).strip()
    return bool(text and text.lower() not in {"nan", "none", "null", "[]", "{}"})


def clean(value: Any) -> str:
    return str(value).strip() if is_present(value) else ""


def ui_label(value: Any) -> str:
    text = clean(value)
    text = re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0E\uFE0F]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize(value: Any) -> str:
    text = clean(value)
    text = re.sub(r"[\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06ed]", "", text)
    text = text.replace("ـ", "")
    text = re.sub("[إأآٱا]", "ا", text)
    text = text.replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي")
    text = re.sub(r"[^\w\s\u0600-\u06ff]", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def split_list(value: Any) -> list[str]:
    text = clean(value)
    if not text:
        return []
    return [part.strip() for part in re.split(r"\s*[|،,؛]\s*|\s+[–—-]\s+", text) if part.strip()]


def split_refs(value: Any) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for part in str(clean(value)).split("|"):
        item = part.strip()
        if not item:
            continue
        match = re.match(r"(.+?)\s+([\d\-–]+)$", item)
        if match:
            refs.append({"surah": match.group(1).strip(), "ayah_range": match.group(2).replace("–", "-").strip(), "reference": item})
        else:
            refs.append({"surah": item, "ayah_range": "", "reference": item})
    return refs


def story_id(number: int) -> str:
    return f"story-{number:03d}"


@st.cache_data(show_spinner=False)
def load_excel_catalog() -> list[dict[str, Any]]:
    df = pd.read_excel(WORKBOOK_PATH, sheet_name="Overall Stories")
    rows: list[dict[str, Any]] = []
    for _, row in df[df["#"].notna()].iterrows():
        number = int(row["#"])
        skills = split_list(row.get("Skill to be gained", ""))
        rows.append(
            {
                "id": story_id(number),
                "number": number,
                "character": clean(row.get("Character")),
                "title": clean(row.get("Story")) or clean(row.get("Character")),
                "subtitle": clean(row.get("1-line Summary")),
                "surah_references": clean(row.get("السور والآيات")),
                "ayah_count": clean(row.get("عدد الآيات")),
                "significance": clean(row.get("Significance")),
                "core_value": clean(row.get("Core Value")),
                "category": clean(row.get("Category")),
                "skills": skills,
                "refs": split_refs(row.get("السور والآيات")),
            }
        )
    return rows


@st.cache_data(show_spinner=False)
def load_iblis_excel_passages() -> list[dict[str, Any]]:
    try:
        df = pd.read_excel(WORKBOOK_PATH, sheet_name="1- أبليس")
    except Exception:
        return []
    col = df.columns[0]
    values = [clean(v) for v in df[col].tolist() if clean(v)]
    passages: list[dict[str, Any]] = []
    i = 0
    while i < len(values):
        text = values[i]
        if text.startswith("- سورة") or text.startswith("سورة"):
            surah_match = re.search(r"سورة\s+([^\(\n]+)", text)
            surah = surah_match.group(1).strip() if surah_match else ""
            ayah_numbers = re.findall(r"\((\d+)\)", text)
            ayah_range = ""
            if ayah_numbers:
                ayah_range = ayah_numbers[0] if len(ayah_numbers) == 1 else f"{ayah_numbers[0]}-{ayah_numbers[-1]}"
            explanation = values[i + 1] if i + 1 < len(values) and not values[i + 1].startswith("- سورة") else ""
            passages.append(
                {
                    "surah": surah,
                    "ayah_number": ayah_range,
                    "ayah_range": ayah_range,
                    "reference": f"{surah} {ayah_range}".strip(),
                    "text": text,
                    "tafsir": explanation,
                }
            )
            i += 2 if explanation else 1
        else:
            i += 1
    return passages


@st.cache_data(show_spinner=False)
def load_docx_story(story_id_value: str) -> dict[str, Any] | None:
    try:
        return StoryRepository(CONTENT_DIR).get_story(story_id_value)
    except Exception:
        return None


def get_story(index: list[dict[str, Any]], selected_id: str | None) -> dict[str, Any] | None:
    if not selected_id:
        return None
    meta = next((item for item in index if item["id"] == selected_id), None)
    if not meta:
        return None
    docx = load_docx_story(selected_id) or {}
    story = {**meta}
    story["summary"] = clean(docx.get("summary")) or meta.get("subtitle", "")
    story["overview"] = docx.get("overview", [])
    story["reflections"] = docx.get("reflections", [])
    story["transformation_chain"] = docx.get("transformation_chain", [])
    story["practical_applications"] = docx.get("practical_applications", {})
    story["turning_points"] = docx.get("turning_points", [])
    story["source_file"] = docx.get("source_file")
    if selected_id == "story-001":
        story["passages"] = load_iblis_excel_passages()
    else:
        story["passages"] = normalize_docx_passages(docx.get("verses", []), meta)
    return story


def normalize_docx_passages(verses: list[dict[str, Any]], meta: dict[str, Any]) -> list[dict[str, Any]]:
    refs = meta.get("refs", [])
    passages: list[dict[str, Any]] = []
    for idx, verse in enumerate(verses):
        ref = refs[min(idx, len(refs) - 1)] if refs else {}
        text = clean(verse.get("text"))
        surah = clean(ref.get("surah"))
        match = re.search(r"سورة\s+([^\-\–\(\n|]+)", text)
        if match:
            surah = match.group(1).strip()
        nums = re.findall(r"\((\d+)\)", text)
        ayah = clean(ref.get("ayah_range"))
        if nums:
            ayah = nums[0] if len(nums) == 1 else f"{nums[0]}-{nums[-1]}"
        explanation = "\n".join(clean(item) for item in verse.get("explanation", []) if clean(item))
        passages.append(
            {
                "surah": surah or "غير محدد",
                "ayah_number": ayah,
                "ayah_range": ayah,
                "reference": clean(ref.get("reference")) or f"{surah} {ayah}".strip(),
                "text": text,
                "tafsir": explanation,
            }
        )
    return passages


def initialize_state(index: list[dict[str, Any]]) -> None:
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, dict) else value
    if st.session_state.active_view not in VIEW_LABELS:
        st.session_state.active_view = "home"
    if st.session_state.active_story_tab not in STORY_TABS:
        st.session_state.active_story_tab = "verses"


def set_view(view: str) -> None:
    st.session_state.active_view = view
    st.rerun()


def set_progress(story_id_value: str | None, value: int) -> None:
    if not story_id_value:
        return
    progress = dict(st.session_state.story_progress)
    progress[story_id_value] = max(int(progress.get(story_id_value, 0)), value)
    st.session_state.story_progress = progress


def progress_for(story_id_value: str | None) -> int:
    if not story_id_value:
        return 0
    return int(st.session_state.story_progress.get(story_id_value, 0))


def previous_next_ids(index: list[dict[str, Any]], story_id_value: str) -> tuple[str | None, str | None]:
    ids = [item["id"] for item in index]
    if story_id_value not in ids:
        return None, None
    position = ids.index(story_id_value)
    previous_id = ids[position - 1] if position > 0 else None
    next_id = ids[position + 1] if position < len(ids) - 1 else None
    return previous_id, next_id


def select_story(story_id_value: str, view: str | None = None) -> None:
    st.session_state.selected_story_id = story_id_value
    st.session_state.last_opened_story_id = story_id_value
    st.session_state.selected_surah = None
    st.session_state.active_story_tab = "verses"
    set_progress(story_id_value, 10)
    if view:
        st.session_state.active_view = view
    st.rerun()


def reset_filters() -> None:
    st.session_state.search_query = ""
    st.session_state.category_filter = "الكل"
    st.session_state.value_filter = "الكل"
    st.session_state.skill_filter = "الكل"


def story_options(index: list[dict[str, Any]]) -> list[str]:
    query = normalize(st.session_state.search_query)
    selected_category = st.session_state.category_filter
    selected_value = st.session_state.value_filter
    selected_skill = st.session_state.skill_filter
    ids: list[str] = []
    for item in index:
        haystack = normalize(" ".join([item["title"], item.get("subtitle", ""), item.get("category", ""), item.get("core_value", ""), " ".join(item.get("skills", [])), item.get("surah_references", "")]))
        if query and query not in haystack:
            continue
        if selected_category != "الكل" and item.get("category") != selected_category:
            continue
        if selected_value != "الكل" and item.get("core_value") != selected_value:
            continue
        if selected_skill != "الكل" and selected_skill not in item.get("skills", []):
            continue
        ids.append(item["id"])
    return ids


def render_nav(index: list[dict[str, Any]]) -> None:
    active_view = st.session_state.active_view
    selected = next((item for item in index if item["id"] == st.session_state.selected_story_id), None)
    selected_title = selected["title"] if selected else "اختر القصة"
    st.markdown(
        f"""
<header class="app-top-frame view-{active_view}">
  <div class="top-pattern"></div>
  <div class="brand-lockup">
    <span class="brand-mark" aria-hidden="true"></span>
    <div>
      <h1>اِبْتِهَال</h1>
      <p>قصص تُحيي القلب، وهدايات تصنع الوعي</p>
    </div>
  </div>
</header>
""",
        unsafe_allow_html=True,
    )
    with st.container(key="desktop_nav"):
        for view in ["home", "story", "explore"]:
            active = st.session_state.active_view == view
            if st.button(VIEW_LABELS[view], key=f"nav_desktop_{view}", type="primary" if active else "secondary"):
                set_view(view)
    with st.container(key="mobile_nav"):
        for view in ["home", "story", "explore"]:
            active = st.session_state.active_view == view
            if st.button(VIEW_LABELS[view], key=f"nav_mobile_{view}", type="primary" if active else "secondary"):
                set_view(view)
    if active_view in {"story", "explore"}:
        st.markdown(
            f"""
<section class="mobile-screen-bar">
  <span class="screen-menu"></span>
  <h2>{VIEW_LABELS[active_view]}</h2>
  <div><small>القصة المختارة</small><strong>{esc(selected_title)}</strong></div>
</section>
""",
            unsafe_allow_html=True,
        )


def render_story_selector(index: list[dict[str, Any]], key: str, filtered: bool = False, target_view: str | None = None) -> None:
    ids = story_options(index) if filtered else [item["id"] for item in index]
    if not ids:
        st.warning("لا توجد قصص مطابقة لمعايير البحث الحالية")
        st.button("إعادة ضبط", key=f"reset_{key}", on_click=reset_filters)
        return
    selected_index = ids.index(st.session_state.selected_story_id) if st.session_state.selected_story_id in ids else None
    selected = st.selectbox(
        "اختر القصة",
        ids,
        index=selected_index,
        format_func=lambda item_id: next((item["title"] for item in index if item["id"] == item_id), item_id),
        key=key,
        placeholder="اختر القصة",
    )
    if selected and selected != st.session_state.selected_story_id:
        select_story(selected, target_view)


def render_home(index: list[dict[str, Any]]) -> None:
    render_home_carousel(index)
    st.markdown('<section class="control-panel">', unsafe_allow_html=True)
    render_story_selector(index, "home_story_selector", filtered=False, target_view="story")
    st.markdown("</section>", unsafe_allow_html=True)


def render_home_carousel(index: list[dict[str, Any]]) -> None:
    last = get_story(index, st.session_state.last_opened_story_id) or get_story(index, st.session_state.selected_story_id) or (index[0] if index else None)
    progress = progress_for(last["id"]) if last else 0
    slide = int(st.session_state.home_slide) % 3
    slide_html = [
        """
<article class="brand-slide">
  <div>
    <span class="brand-emblem"></span>
    <h1>اِبْتِهَال</h1>
    <p>قصص تُحيي القلب، وهدايات تصنع الوعي</p>
    <span class="gold-cta">استكشف القصص</span>
  </div>
  <div class="andalusian-arch"></div>
</article>
""",
        f"""
<article class="brand-slide">
  <div>
    <span class="brand-emblem"></span>
    <h1>تابع رحلتك</h1>
    <p>{esc(last["title"] if last else "اختر قصة")}</p>
    <div class="slide-progress"><span style="width:{progress}%"></span></div>
    <span class="gold-cta">متابعة القراءة</span>
  </div>
  <div class="lantern-panel"></div>
</article>
""",
        """
<article class="brand-slide">
  <div>
    <span class="brand-emblem"></span>
    <h1>تدبر القصة واكتشف معناها</h1>
    <p>القيم والتحولات النفسية والقيادية والدروس العملية في قصة واحدة</p>
    <div class="indicator-cloud"><span>القيم</span><span>التحليل النفسي</span><span>القيادة</span><span>الإدارة</span><span>الصبر</span><span>اتخاذ القرار</span></div>
  </div>
  <div class="star-panel"></div>
</article>
""",
    ]
    st.markdown(f'<section class="carousel-shell">{slide_html[slide]}</section>', unsafe_allow_html=True)
    with st.container(key="slide_controls"):
        if st.button("السابق", key="slide_prev"):
            st.session_state.home_slide = (slide - 1) % 3
            st.rerun()
        for idx in range(3):
            if st.button("●" if idx == slide else "○", key=f"slide_dot_{idx}"):
                st.session_state.home_slide = idx
                st.rerun()
        if st.button("التالي", key="slide_next"):
            st.session_state.home_slide = (slide + 1) % 3
            st.rerun()
    if slide == 1 and st.button("متابعة القراءة", key="continue_slide"):
        select_story((last or {})["id"], "story")
    if slide == 2 and st.button("ابدأ الاستكشاف", key="explore_slide"):
        set_view("explore")


def render_preview_card(story: dict[str, Any]) -> None:
    progress = progress_for(story["id"])
    skills = story.get("skills", [])[:3]
    skill_html = "".join(f"<span>{esc(skill)}</span>" for skill in skills)
    st.markdown(
        f"""
<section class="selected-card">
  <div class="story-visual {story_art_class(story)}"><span>{int(story["number"]):02d}</span></div>
  <div class="selected-content">
    <h2>{esc(story["title"])}</h2>
    <p>{esc(story.get("subtitle", ""))}</p>
    <div class="meta-row"><span>{esc(ui_label(story.get("category", "")))}</span><span>{esc(ui_label(story.get("core_value", "")))}</span></div>
    <div class="skill-row">{skill_html}</div>
    <p class="refs">{esc(story.get("surah_references", ""))}</p>
    <div class="slide-progress"><span style="width:{progress}%"></span></div>
    <small>تقدم القراءة: {progress}%</small>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )
    if st.button("فتح القصة", key="open_selected_story"):
        select_story(story["id"], "story")


def story_art_class(story: dict[str, Any]) -> str:
    return f"art-{(int(story.get('number', 0)) % 6) + 1}"


def render_story_view(index: list[dict[str, Any]]) -> None:
    story = get_story(index, st.session_state.selected_story_id)
    if not story:
        st.warning("لم يتم اختيار قصة بعد")
        if st.button("اختيار قصة", key="choose_from_empty_story"):
            set_view("home")
        return
    set_progress(story["id"], 10)
    render_story_selector(index, "global_story_selector_story")
    render_story_header(story)
    render_story_tabs(story)
    render_previous_next(index, story)


def render_story_header(story: dict[str, Any]) -> None:
    progress = progress_for(story["id"])
    skills = "، ".join(story.get("skills", [])[:4])
    st.markdown(
        f"""
<section class="story-header">
  <div class="story-visual {story_art_class(story)}"><span>{int(story["number"]):02d}</span></div>
  <div>
    <span class="story-medallion">{int(story["number"]):02d}</span>
    <h1>{esc(story["title"])}</h1>
    <p>{esc(story.get("subtitle", ""))}</p>
    <div class="meta-row"><span>{esc(ui_label(story.get("category", "")))}</span><span>{esc(ui_label(story.get("core_value", "")))}</span><span>{progress}%</span></div>
    <p class="refs">{esc(story.get("surah_references", ""))}</p>
    <p class="refs">{esc(skills)}</p>
  </div>
  <div class="progress-ring" style="--value:{progress}%;"><strong>{progress}%</strong><small>القراءة</small></div>
</section>
""",
        unsafe_allow_html=True,
    )


def render_previous_next(index: list[dict[str, Any]], story: dict[str, Any]) -> None:
    previous_id, next_id = previous_next_ids(index, story["id"])
    previous_story = next((item for item in index if item["id"] == previous_id), None)
    next_story = next((item for item in index if item["id"] == next_id), None)
    with st.container(key="story_prev_next"):
        if previous_story and st.button(f"السابق: {previous_story['title']}", key=f"previous_{story['id']}"):
            select_story(previous_story["id"], "story")
        if next_story and st.button(f"التالي: {next_story['title']}", key=f"next_{story['id']}"):
            select_story(next_story["id"], "story")


def render_story_tabs(story: dict[str, Any]) -> None:
    with st.container(key="story_tabs"):
        cols = st.columns(len(STORY_TABS))
        for col, (tab, label) in zip(cols, STORY_TABS.items()):
            with col:
                active = st.session_state.active_story_tab == tab
                if st.button(label, key=f"tab_{tab}", type="primary" if active else "secondary"):
                    st.session_state.active_story_tab = tab
                    set_progress(story["id"], TAB_PROGRESS[tab])
                    st.rerun()
    set_progress(story["id"], TAB_PROGRESS.get(st.session_state.active_story_tab, 10))
    if st.session_state.active_story_tab == "verses":
        render_verses_tab(story)
    elif st.session_state.active_story_tab == "tafsir":
        render_analysis_tab(story)
    elif st.session_state.active_story_tab == "summary":
        render_summary_tab(story)
    elif st.session_state.active_story_tab == "transformation":
        render_transformation_tab(story)
    elif st.session_state.active_story_tab == "applications":
        render_applications_tab(story)


def related_surahs(story: dict[str, Any]) -> list[str]:
    surahs = []
    seen = set()
    for passage in story.get("passages", []):
        key = normalize(passage.get("surah"))
        if key and key not in seen:
            surahs.append(passage["surah"])
            seen.add(key)
    for ref in story.get("refs", []):
        key = normalize(ref.get("surah"))
        if key and key not in seen:
            surahs.append(ref["surah"])
            seen.add(key)
    return surahs


def render_verses_tab(story: dict[str, Any]) -> None:
    surahs = related_surahs(story)
    if not surahs:
        st.warning("النص القرآني غير متاح في مصدر البيانات الحالي، ويجب مراجعته قبل النشر.")
        return
    selected = st.selectbox("اختر السورة", surahs, key=f"surah_{story['id']}")
    st.session_state.selected_surah = selected
    passages = [p for p in story.get("passages", []) if normalize(p.get("surah")) == normalize(selected)]
    if not passages:
        st.warning("النص القرآني غير متاح في مصدر البيانات الحالي، ويجب مراجعته قبل النشر.")
        refs = [ref for ref in story.get("refs", []) if normalize(ref.get("surah")) == normalize(selected)]
        for ref in refs:
            st.markdown(f'<section class="manuscript-panel"><strong>{esc(ref.get("reference"))}</strong></section>', unsafe_allow_html=True)
        return
    for idx, passage in enumerate(passages, 1):
        st.markdown(
            f"""
<article class="ayah-card">
  <header><span>{esc(passage.get("ayah_number") or str(idx))}</span><strong>{esc(passage.get("surah"))}</strong><small>{esc(passage.get("reference"))}</small></header>
  <div class="quran-text">{esc(passage.get("text"))}</div>
  <section class="tafsir-under"><strong>التفسير</strong><p>{esc(passage.get("tafsir")) if clean(passage.get("tafsir")) else "لا يوجد تفسير موثق لهذه الآية في مصدر البيانات الحالي."}</p></section>
</article>
""",
            unsafe_allow_html=True,
        )


def render_analysis_tab(story: dict[str, Any]) -> None:
    blocks = []
    for row in story.get("overview", []):
        if clean(row.get("value")):
            blocks.append((clean(row.get("label")), clean(row.get("value"))))
    for text in story.get("reflections", [])[:8]:
        if clean(text):
            blocks.append(("تأمل وتحليل", clean(text)))
    if not blocks:
        st.info("لا توجد بيانات موثقة لهذا القسم")
        return
    for title, body in blocks:
        st.markdown(f'<section class="analysis-block"><h3>{esc(title)}</h3><p>{esc(body)}</p></section>', unsafe_allow_html=True)


def render_summary_tab(story: dict[str, Any]) -> None:
    items = [story.get("summary"), story.get("significance"), *story.get("turning_points", [])[:5]]
    rendered = False
    for item in items:
        if clean(item):
            rendered = True
            st.markdown(f'<section class="manuscript-panel"><p>{esc(item)}</p></section>', unsafe_allow_html=True)
    if not rendered:
        st.info("لا توجد بيانات موثقة لهذا القسم")


def render_transformation_tab(story: dict[str, Any]) -> None:
    chain = story.get("transformation_chain", [])
    if not chain:
        st.info("لا توجد بيانات موثقة لهذا القسم")
        return
    st.markdown('<section class="transformation-flow">', unsafe_allow_html=True)
    for idx, item in enumerate(chain, 1):
        st.markdown(f'<article><span>{idx}</span><h3>{esc(item.get("stage"))}</h3><p>{esc(item.get("text"))}</p><small>{esc(item.get("application"))}</small></article>', unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)


def render_applications_tab(story: dict[str, Any]) -> None:
    apps = story.get("practical_applications", {})
    rendered = False
    st.markdown('<section class="applications-grid">', unsafe_allow_html=True)
    for title, body in apps.items():
        if clean(body):
            rendered = True
            st.markdown(f'<article class="application-card"><span></span><h3>{esc(title)}</h3><p>{esc(body)}</p></article>', unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)
    if not rendered:
        st.info("لا توجد بيانات موثقة لهذا القسم")


def render_explore_view(index: list[dict[str, Any]]) -> None:
    story = get_story(index, st.session_state.selected_story_id)
    if not story:
        st.warning("اختر قصة أولاً لاستكشاف قيمها ودروسها")
        if st.button("اختيار قصة", key="choose_from_empty_explore"):
            set_view("home")
        return
    render_story_selector(index, "global_story_selector_explore")
    cards = []
    for block in EXPLORE_BLOCKS:
        content = explore_content(story, block)
        cards.append(
            f'<article class="explore-card"><h3>{esc(block)}</h3><p>{esc(content or "لا توجد بيانات موثقة لهذا القسم")}</p></article>'
        )
    st.markdown(
        f"""
<section class="explore-shell">
  <section class="explore-header">
    <h1>استكشف: قصة {esc(story["title"])}</h1>
    <p>{esc(ui_label(story.get("core_value")))} | {esc(ui_label(story.get("category")))}</p>
    <p>{esc(story.get("subtitle"))}</p>
  </section>
  <section class="explore-grid">{"".join(cards)}</section>
</section>
""",
        unsafe_allow_html=True,
    )
    render_related(index, story)


def explore_content(story: dict[str, Any], block: str) -> str:
    overview = " | ".join(clean(row.get("value")) for row in story.get("overview", [])[:3] if clean(row.get("value")))
    if block == "القيم الأساسية":
        labels = [ui_label(v) for v in [story.get("core_value"), story.get("category"), story.get("significance")] if clean(v)]
        return " | ".join(label for label in labels if label)
    if block == "التحليل النفسي":
        return overview or " | ".join(story.get("reflections", [])[:2])
    if block in {"الدروس القيادية", "الدروس الأخلاقية", "الدروس الإدارية", "الصبر والمرونة"}:
        return overview or clean(story.get("summary"))
    if block == "نموذج السبب والنتيجة":
        return " ← ".join(clean(item.get("stage")) for item in story.get("transformation_chain", []) if clean(item.get("stage")))
    if block == "المهارات المكتسبة":
        return "، ".join(story.get("skills", []))
    if block == "نقاط التحول":
        return "، ".join(story.get("turning_points", [])[:6])
    return ""


def render_related(index: list[dict[str, Any]], story: dict[str, Any]) -> None:
    related = [
        item
        for item in index
        if item["id"] != story["id"] and (item.get("category") == story.get("category") or item.get("core_value") == story.get("core_value"))
    ][:3]
    if not related:
        return
    st.markdown('<h2 class="section-title">قصص ذات صلة</h2>', unsafe_allow_html=True)
    cols = st.columns(len(related))
    for col, item in zip(cols, related):
        with col:
            st.markdown(
                f"""
<section class="related-card">
  <strong>{int(item["number"]):02d} - {esc(item["title"])}</strong>
  <p>{esc(ui_label(item.get("core_value")))} | {esc(ui_label(item.get("category")))}</p>
  <small>تشترك مع القصة المختارة في القيمة أو التصنيف.</small>
</section>
""",
                unsafe_allow_html=True,
            )
            if st.button("فتح القصة", key=f"related_{item['id']}"):
                select_story(item["id"], "story")


def main() -> None:
    index = load_excel_catalog()
    initialize_state(index)
    st.markdown(build_css("light"), unsafe_allow_html=True)
    render_nav(index)
    if st.session_state.active_view == "home":
        render_home(index)
    elif st.session_state.active_view == "story":
        render_story_view(index)
    elif st.session_state.active_view == "explore":
        render_explore_view(index)


if __name__ == "__main__":
    main()
