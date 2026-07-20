from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any

import streamlit as st

from data_loader import StoryRepository
from style import build_css


APP_DIR = Path(__file__).parent
CONTENT_DIR = APP_DIR / "Quran_Stories"

DEFAULT_STATE = {
    "current_view": "home",
    "selected_story_id": None,
    "selected_section": "verses",
    "landing_slide": 0,
    "search_query": "",
    "selected_category": "الكل",
    "selected_value": "الكل",
    "selected_skill": "الكل",
    "reading_progress": {},
    "last_opened_story_id": None,
    "theme": "light",
}

VIEW_LABELS = {
    "home": "الرئيسية",
    "story": "القصة",
    "explore": "استكشف",
}

VIEW_ICONS = {
    "home": "⌂",
    "story": "▤",
    "explore": "✦",
}

SECTION_OPTIONS = {
    "verses": "الآيات",
    "tafsir": "التفسير والتحليل",
    "summary": "خلاصة القصة",
    "transformation": "التحول الإنساني",
    "applications": "التطبيقات العملية",
}

SECTION_PROGRESS = {
    "verses": 25,
    "tafsir": 45,
    "summary": 60,
    "transformation": 80,
    "applications": 100,
}

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

EMPTY_BLOCK = "لا توجد عناصر مسجلة لهذا الجانب في القصة الحالية"


st.set_page_config(
    page_title="اِبْتِهَال",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value))


def content_root() -> Path:
    return CONTENT_DIR if CONTENT_DIR.exists() else APP_DIR


def repository() -> StoryRepository:
    return StoryRepository(content_root())


@st.cache_data(show_spinner=False)
def load_story_index_cached() -> list[dict[str, Any]]:
    return repository().get_index()


@st.cache_data(show_spinner=False)
def search_story_index_cached(query: str, category: str, value: str, skill: str) -> list[dict[str, Any]]:
    return repository().search(query=query, category=category, value=value, skill=skill)


@st.cache_data(show_spinner=False)
def load_story_content_cached(story_id: str) -> dict[str, Any] | None:
    try:
        return repository().get_story(story_id)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_related_cached(story_id: str) -> list[dict[str, Any]]:
    return repository().get_related(story_id)


@st.cache_data(show_spinner=False)
def load_previous_next_cached(story_id: str) -> tuple[str | None, str | None]:
    return repository().get_previous_next(story_id)


def initialize_state() -> None:
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, dict) else value
    requested_view = st.query_params.get("view")
    if requested_view in VIEW_LABELS:
        st.session_state.current_view = requested_view
    if st.session_state.current_view not in VIEW_LABELS:
        st.session_state.current_view = "home"
    if st.session_state.selected_section not in SECTION_OPTIONS:
        st.session_state.selected_section = "verses"
    st.session_state.landing_slide = int(st.session_state.landing_slide) % 3


def navigate(view: str) -> None:
    st.session_state.current_view = view if view in VIEW_LABELS else "home"
    st.query_params["view"] = st.session_state.current_view
    st.rerun()


def progress_for(story_id: str | None) -> int:
    if not story_id:
        return 0
    return int(st.session_state.reading_progress.get(story_id, 0))


def set_progress(story_id: str | None, value: int) -> None:
    if not story_id:
        return
    progress = dict(st.session_state.reading_progress)
    progress[story_id] = max(int(progress.get(story_id, 0)), value)
    st.session_state.reading_progress = progress


def select_story(story_id: str, view: str = "story") -> None:
    st.session_state.selected_story_id = story_id
    st.session_state.last_opened_story_id = story_id
    st.session_state.selected_section = "verses"
    st.session_state.current_view = view
    st.query_params["view"] = view
    set_progress(story_id, 10)
    st.rerun()


def set_story_state(story_id: str, view: str = "story") -> None:
    st.session_state.selected_story_id = story_id
    st.session_state.last_opened_story_id = story_id
    st.session_state.selected_section = "verses"
    st.session_state.current_view = view
    st.query_params["view"] = view
    set_progress(story_id, 10)


def change_selected_story(story_id: str, view: str = "story") -> None:
    st.session_state.selected_story_id = story_id
    st.session_state.last_opened_story_id = story_id
    st.session_state.selected_section = "verses"
    st.session_state.current_view = view
    set_progress(story_id, 10)
    st.rerun()


def reset_filters_state() -> None:
    st.session_state.search_query = ""
    st.session_state.selected_category = "الكل"
    st.session_state.selected_value = "الكل"
    st.session_state.selected_skill = "الكل"


def reset_search_state() -> None:
    st.session_state.search_query = ""


def reset_classification_state() -> None:
    st.session_state.selected_category = "الكل"
    st.session_state.selected_value = "الكل"
    st.session_state.selected_skill = "الكل"


def story_by_id(index: list[dict[str, Any]], story_id: str | None) -> dict[str, Any] | None:
    if not story_id:
        return None
    return next((story for story in index if story["id"] == story_id), None)


def split_skills(value: str | list[str] | None) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = "" if value is None else str(value)
    return [part.strip() for part in re.split(r"[-–—،,]+", text) if part.strip()]


def unique_options(items: list[str]) -> list[str]:
    return ["الكل"] + sorted({item for item in items if item})


def story_art_class(story: dict[str, Any]) -> str:
    number = int(story.get("number", 0) or 0)
    return f"art-{(number % 6) + 1}"


def render_navigation() -> None:
    current = st.session_state.current_view
    links = []
    for view, label in VIEW_LABELS.items():
        active = "active" if view == current else ""
        links.append(
            f'<a class="nav-link {active}" href="?view={view}">'
            f'<span class="nav-icon">{VIEW_ICONS[view]}</span><b>{label}</b></a>'
        )
    top_nav = "" if current == "home" else f"""
<nav class="top-nav" aria-label="التنقل الرئيسي">
  <a class="hamburger" href="?view=home" aria-label="الرئيسية">☰</a>
  <strong class="screen-title">{VIEW_LABELS[current]}</strong>
  <div class="selected-mini">القصة المختارة</div>
  <div class="nav-links">{''.join(links)}</div>
</nav>
"""
    st.markdown(
        f"""
{top_nav}
<nav class="bottom-nav" aria-label="تنقل الجوال">
  {''.join(links)}
</nav>
""",
        unsafe_allow_html=True,
    )


def render_empty_state(message: str = "لم يتم اختيار قصة بعد", subtitle: str = "اختر قصة من الصفحة الرئيسية لبدء القراءة") -> None:
    st.markdown(
        f"""
<section class="empty-panel centered-state">
  <div class="empty-symbol">☪</div>
  <h2>{esc(message)}</h2>
  <p>{esc(subtitle)}</p>
</section>
""",
        unsafe_allow_html=True,
    )
    if st.button("اختيار قصة", key=f"empty_home_{message}"):
        navigate("home")


def render_slide_dots(active: int) -> None:
    cols = st.columns([1, 1, 1])
    for idx, col in enumerate(cols):
        with col:
            label = "●" if idx == active else "○"
            if st.button(label, key=f"landing_dot_{idx}"):
                st.session_state.landing_slide = idx
                st.rerun()


def render_landing_slides(index: list[dict[str, Any]]) -> None:
    last_story = story_by_id(index, st.session_state.last_opened_story_id)
    featured = last_story or (index[10] if len(index) > 10 else index[0])
    progress = progress_for(featured["id"]) if featured else 0

    st.markdown(
        f"""
<section class="target-hero home-hero landing-slide">
  <div class="hero-copy">
    <h1>اِبْتِهَال</h1>
    <p>قصص تُحيي القلب، وهدايات تصنع الوعي</p>
    <span class='gold-cta ghost-cta'>استكشف القصص</span>
  </div>
  <div class="hero-arch" aria-hidden="true"></div>
</section>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
<div class="hidden-slide-state" aria-hidden="true">
  <span>آخر قصة: {esc(featured.get('title', ''))}</span>
  <span>التقدم {progress}%</span>
</div>
""",
        unsafe_allow_html=True,
    )


def render_filters(index: list[dict[str, Any]]) -> list[dict[str, Any]]:
    value_options = unique_options([story.get("core_value", "") for story in index])
    skill_options = unique_options([skill for story in index for skill in split_skills(story.get("skills", ""))])
    category_options = unique_options([story.get("category", "") for story in index])

    cols = st.columns([1.05, 3.2])
    with cols[0]:
        st.selectbox("تصفية", category_options, key="selected_category", label_visibility="collapsed")
    with cols[1]:
        st.text_input(
            "بحث",
            placeholder="ابحث عن قصة...",
            key="search_query",
            label_visibility="collapsed",
        )
    st.markdown(
        "<section class='category-strip clone-chips'>"
        + "".join(f"<span>{esc(item)}</span>" for item in category_options[1:6])
        + "</section>",
        unsafe_allow_html=True,
    )

    return search_story_index_cached(
        st.session_state.search_query,
        st.session_state.selected_category,
        st.session_state.selected_value,
        st.session_state.selected_skill,
    )


def render_story_card(story: dict[str, Any]) -> None:
    progress = progress_for(story["id"])
    skills = "، ".join(split_skills(story.get("skills", ""))[:2])
    st.markdown(
        f"""
<article class="story-card visual-card">
  <div class="story-art {story_art_class(story)}">
    <span class="story-badge">{int(story["number"]):02d}</span>
  </div>
  <div class="story-card-body">
    <h3>{esc(story.get("title", ""))}</h3>
    <p>{esc(story.get("subtitle") or story.get("core_value", ""))}</p>
    <div class="card-meta">
      <span class="card-chip">{esc(story.get("category", ""))}</span>
      <span class="card-chip">{esc(story.get("core_value", ""))}</span>
    </div>
    <small>{esc(skills)}</small>
    <small>{esc(story.get("surah_references", ""))}</small>
    <div class="progress-line inline-progress"><span style="width:{progress}%"></span></div>
  </div>
</article>
""",
        unsafe_allow_html=True,
    )
    if st.button("فتح القصة", key=f"open_{story['id']}"):
        select_story(story["id"], "story")


def render_continue_reading(index: list[dict[str, Any]]) -> None:
    last_id = st.session_state.last_opened_story_id or (index[11]["id"] if len(index) > 11 else index[0]["id"])
    story = story_by_id(index, last_id)
    if not story:
        return
    progress = progress_for(last_id)
    st.markdown(
        f"""
<section class="continue-card reference-card">
  <div class="mini-art {story_art_class(story)}"></div>
  <div>
    <strong>آخر قصة قرأتها</strong>
    <h3>{esc(story["title"])}</h3>
    <p>القصة رقم {int(story["number"]):02d} | التقدم {progress}%</p>
  </div>
  <div class="progress-line"><span style="width:{progress}%"></span></div>
</section>
""",
        unsafe_allow_html=True,
    )
    if st.button("متابعة القراءة", key="continue_reading"):
        st.session_state.selected_story_id = last_id
        st.session_state.last_opened_story_id = last_id
        set_progress(last_id, 10)
        navigate("story")


def render_home(index: list[dict[str, Any]]) -> None:
    render_landing_slides(index)
    filtered = render_filters(index)
    st.markdown(f'<h2 class="section-title tight">القصص المتاحة <span>({len(filtered)})</span></h2>', unsafe_allow_html=True)
    if not filtered:
        st.warning("لا توجد قصص مطابقة لمعايير البحث الحالية")
        reset_cols = st.columns(2)
        with reset_cols[0]:
            st.button("إعادة ضبط البحث", key="reset_search", on_click=reset_search_state)
        with reset_cols[1]:
            st.button("إعادة ضبط التصنيفات", key="reset_classifications", on_click=reset_classification_state)
    if not st.session_state.search_query and st.session_state.selected_category == "الكل":
        target_ids = ["story-012", "story-015", "story-007", "story-004", "story-013", "story-011"]
        target_stories = [story_by_id(index, story_id) for story_id in target_ids]
        visible_stories = [story for story in target_stories if story]
    else:
        visible_stories = filtered[:6]
    for start in range(0, len(visible_stories), 3):
        cols = st.columns(3)
        for col, story in zip(cols, visible_stories[start : start + 3]):
            with col:
                render_story_card(story)
    render_continue_reading(index)


def render_story_selector(story: dict[str, Any], index: list[dict[str, Any]], key: str, view: str) -> None:
    ids = [item["id"] for item in index]
    if story["id"] not in ids:
        return
    selected = st.selectbox(
        "القصة المختارة",
        options=ids,
        index=ids.index(story["id"]),
        format_func=lambda item_id: story_by_id(index, item_id)["title"],
        key=f"{key}_{story['id']}",
        label_visibility="collapsed",
    )
    if selected != story["id"]:
        change_selected_story(selected, view)


def render_story_header(story: dict[str, Any], index: list[dict[str, Any]]) -> None:
    progress = progress_for(story["id"])
    skills = "، ".join(story.get("skills", []))
    render_story_selector(story, index, "story_changer", "story")
    st.markdown(
        f"""
<section class="target-hero story-hero">
  <div class="hero-arch story-arch {story_art_class(story)}" aria-hidden="true"></div>
  <div class="hero-copy story-copy">
    <span class="story-medallion">{int(story["number"]):02d}</span>
    <h1>{esc(story["title"])}</h1>
    <p>{esc(story.get("subtitle", ""))}</p>
    <div class="hero-meta">
      <span>{esc(story.get("category", ""))}</span>
      <span>{esc(story.get("core_value", ""))}</span>
      <span>التقدم {progress}%</span>
    </div>
    <p class="hero-ref">{esc(story.get("surah_references", ""))}</p>
    <p class="hero-ref">{esc(skills)}</p>
  </div>
</section>
""",
        unsafe_allow_html=True,
    )


def render_section_control(story_id: str) -> None:
    labels = list(SECTION_OPTIONS.values())
    keys = list(SECTION_OPTIONS)
    selected_label = st.radio(
        "أقسام القصة",
        labels,
        index=keys.index(st.session_state.selected_section),
        horizontal=True,
        key="section_control",
        label_visibility="collapsed",
    )
    new_section = next(key for key, value in SECTION_OPTIONS.items() if value == selected_label)
    if new_section != st.session_state.selected_section:
        st.session_state.selected_section = new_section
    set_progress(story_id, SECTION_PROGRESS.get(st.session_state.selected_section, 10))


def render_verses(story: dict[str, Any]) -> None:
    st.markdown('<h2 class="section-title">الآيات</h2>', unsafe_allow_html=True)
    verses = story.get("verses", [])
    if not verses:
        st.info("يوجد مرجع لهذه القصة دون نص قرآني مفصل في البيانات الحالية. لا يتم إنشاء نص بديل.")
        st.markdown(f'<section class="detail-panel"><p>{esc(story.get("surah_references", ""))}</p></section>', unsafe_allow_html=True)
        return
    for passage in verses:
        st.markdown(f'<section class="quran-block"><p>{esc(passage.get("text", ""))}</p></section>', unsafe_allow_html=True)
        for explanation in passage.get("explanation", []):
            st.markdown(f'<section class="tafsir-panel"><strong>التفسير</strong><p>{esc(explanation)}</p></section>', unsafe_allow_html=True)


def render_tafsir(story: dict[str, Any]) -> None:
    st.markdown('<h2 class="section-title">التفسير والتحليل</h2>', unsafe_allow_html=True)
    rendered = False
    for row in story.get("overview", []):
        rendered = True
        st.markdown(f'<section class="detail-panel"><h3>{esc(row.get("label", ""))}</h3><p>{esc(row.get("value", ""))}</p></section>', unsafe_allow_html=True)
    for reflection in story.get("reflections", [])[:8]:
        rendered = True
        st.markdown(f'<section class="detail-panel"><p>{esc(reflection)}</p></section>', unsafe_allow_html=True)
    if not rendered:
        st.info("لا توجد عناصر مسجلة لهذا الجانب في القصة الحالية")


def render_summary(story: dict[str, Any]) -> None:
    st.markdown('<h2 class="section-title">خلاصة القصة</h2>', unsafe_allow_html=True)
    summary = story.get("summary") or story.get("subtitle") or story.get("significance")
    if summary:
        st.markdown(f'<section class="manuscript-panel"><p>{esc(summary)}</p></section>', unsafe_allow_html=True)
    else:
        st.info("لا توجد عناصر مسجلة لهذا الجانب في القصة الحالية")


def render_transformation(story: dict[str, Any]) -> None:
    st.markdown('<h2 class="section-title">التحول الإنساني</h2>', unsafe_allow_html=True)
    chain = story.get("transformation_chain", [])
    if not chain:
        st.info("لا توجد عناصر مسجلة لهذا الجانب في القصة الحالية")
        return
    st.markdown('<section class="flow-chain">', unsafe_allow_html=True)
    for item in chain:
        st.markdown(
            f"""
<div class="flow-step">
  <strong>{esc(item.get("stage", ""))}</strong>
  <p>{esc(item.get("text", ""))}</p>
  <small>{esc(item.get("application", ""))}</small>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("</section>", unsafe_allow_html=True)


def render_applications(story: dict[str, Any]) -> None:
    st.markdown('<h2 class="section-title">التطبيقات العملية</h2>', unsafe_allow_html=True)
    applications = story.get("practical_applications", {})
    if not applications:
        st.info("لا توجد عناصر مسجلة لهذا الجانب في القصة الحالية")
        return
    for title, body in applications.items():
        if body:
            st.markdown(f'<section class="lesson-row"><strong>{esc(title)}</strong><p>{esc(body)}</p></section>', unsafe_allow_html=True)


def render_story_screen(index: list[dict[str, Any]]) -> None:
    selected_id = st.session_state.selected_story_id
    if not selected_id:
        render_empty_state()
        return
    story = load_story_content_cached(selected_id)
    if not story:
        render_empty_state("تعذر تحميل محتوى هذه القصة حالياً", "اختر قصة أخرى أو عد إلى الصفحة الرئيسية")
        return
    set_progress(selected_id, 10)
    render_story_header(story, index)
    render_section_control(selected_id)
    section = st.session_state.selected_section
    if section == "verses":
        render_verses(story)
    elif section == "tafsir":
        render_tafsir(story)
    elif section == "summary":
        render_summary(story)
    elif section == "transformation":
        render_transformation(story)
    elif section == "applications":
        render_applications(story)

    previous_id, next_id = load_previous_next_cached(selected_id)
    cols = st.columns([1, .7, 1])
    with cols[0]:
        st.button(
            "القصة السابقة",
            key="previous_story",
            disabled=previous_id is None,
            on_click=set_story_state,
            args=(previous_id or selected_id, "story"),
        )
    with cols[1]:
        if st.button("استكشف", key="story_to_explore"):
            navigate("explore")
    with cols[2]:
        st.button(
            "القصة التالية",
            key="next_story",
            disabled=next_id is None,
            on_click=set_story_state,
            args=(next_id or selected_id, "story"),
        )


def block_items(story: dict[str, Any], block: str) -> list[str]:
    overview_values = [f'{row.get("label", "")}: {row.get("value", "")}' for row in story.get("overview", []) if row.get("value")]
    if block == "القيم الأساسية":
        return [item for item in [story.get("core_value", ""), story.get("category", ""), story.get("significance", "")] if item]
    if block == "التحليل النفسي":
        return overview_values[:3] or story.get("reflections", [])[:3]
    if block == "الدروس القيادية":
        return [item for item in overview_values + story.get("reflections", []) if any(word in item for word in ["قياد", "قرار", "مسؤول", "حكم"])]
    if block == "الدروس الأخلاقية":
        return [item for item in [story.get("core_value", ""), story.get("summary", ""), *story.get("reflections", [])[:2]] if item]
    if block == "الدروس الإدارية":
        applications = story.get("practical_applications", {})
        return [f"{key}: {value}" for key, value in applications.items() if value and any(word in key + value for word in ["إدار", "عمل", "قياد", "تخطيط"])]
    if block == "الصبر والمرونة":
        return [item for item in [story.get("significance", ""), *story.get("reflections", [])] if any(word in item for word in ["صبر", "ثبات", "ابتلاء", "مرونة"])]
    if block == "نموذج السبب والنتيجة":
        return [f'{row.get("stage", "")}: {row.get("text", "")}' for row in story.get("transformation_chain", []) if row.get("stage") or row.get("text")]
    if block == "المهارات المكتسبة":
        return story.get("skills", [])
    if block == "نقاط التحول":
        return story.get("turning_points", [])
    return []


def render_explore_screen(index: list[dict[str, Any]]) -> None:
    selected_id = st.session_state.selected_story_id
    if not selected_id:
        render_empty_state("اختر قصة أولاً لاستكشاف قيمها ودروسها", "عد إلى الصفحة الرئيسية واختر قصة واحدة")
        return
    story = load_story_content_cached(selected_id)
    if not story:
        render_empty_state("تعذر تحميل محتوى هذه القصة حالياً", "اختر قصة أخرى أو عد إلى الصفحة الرئيسية")
        return
    render_story_selector(story, index, "explore_changer", "explore")
    st.markdown(
        f"""
<section class="explore-banner">
  <div>
    <h1>استكشف: قصة {esc(story["title"])}</h1>
    <p>{esc(story.get("core_value", ""))} | {esc(story.get("category", ""))}</p>
  </div>
  <div class="lantern-art" aria-hidden="true"></div>
</section>
""",
        unsafe_allow_html=True,
    )
    st.markdown('<section class="explore-grid">', unsafe_allow_html=True)
    for block in EXPLORE_BLOCKS:
        items = block_items(story, block)
        body = " | ".join(items[:3]) if items else EMPTY_BLOCK
        st.markdown(f'<article class="explore-card"><span>✦</span><h3>{esc(block)}</h3><p>{esc(body)}</p></article>', unsafe_allow_html=True)
    st.markdown("</section>", unsafe_allow_html=True)

    related = load_related_cached(selected_id)[:3]
    if related:
        st.markdown('<h2 class="section-title">قصص ذات صلة</h2>', unsafe_allow_html=True)
        cols = st.columns(3)
        for col, item in zip(cols, related):
            with col:
                st.markdown(
                    f"""
<article class="story-card related-card">
  <div class="story-art {story_art_class(item)}"><span class="story-badge">{int(item["number"]):02d}</span></div>
  <h3>{esc(item["title"])}</h3>
  <p>{esc(item.get("core_value", ""))} | {esc(item.get("category", ""))}</p>
</article>
""",
                    unsafe_allow_html=True,
                )
                if st.button("فتح القصة", key=f"related_{item['id']}"):
                    select_story(item["id"], "story")


def main() -> None:
    initialize_state()
    st.markdown(build_css(st.session_state.theme), unsafe_allow_html=True)
    render_navigation()
    index = load_story_index_cached()

    if st.session_state.current_view == "home":
        render_home(index)
    elif st.session_state.current_view == "story":
        render_story_screen(index)
    elif st.session_state.current_view == "explore":
        render_explore_screen(index)
    else:
        st.session_state.current_view = "home"
        st.rerun()


if __name__ == "__main__":
    main()
