
from __future__ import annotations

import html
import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="قصص القرآن",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit chrome and sidebar completely.
st.markdown(
    """
    <style>
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    #MainMenu,
    footer,
    header[data-testid="stHeader"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA MODEL
# ============================================================

@dataclass
class Story:
    number: str
    slug: str
    title_en: str
    title_ar: str
    subtitle_ar: str
    short_description_ar: str
    category_ar: str
    primary_value_ar: str
    skills_ar: List[str]
    surah_refs_ar: List[str]
    ayah_ranges_ar: List[str]
    central_message_ar: str
    secondary_values_ar: List[str]


STORY_ROWS = [
    ("001", "iblis", "Iblis", "إبليس", "قصة الكِبر والاختيار", "قراءة في منشأ العصيان وأثر الاستعلاء على القرار.", "الأخلاق", "التواضع", ["ضبط النفس", "اتخاذ القرار"], ["البقرة", "الأعراف"], ["2:34", "7:11–18"], "الكِبر يحجب البصيرة ويحوّل المعرفة إلى عصيان.", ["المسؤولية", "الوعي"]),
    ("002", "adam", "Adam", "آدم", "بداية الإنسان والاستخلاف", "قصة الخلق والتكليف والخطأ والتوبة والبدء من جديد.", "الأنبياء", "التوبة", ["التعلّم", "تحمل المسؤولية"], ["البقرة", "الأعراف"], ["2:30–39", "7:19–27"], "الإنسان يخطئ، لكن صدق التوبة يعيد توجيه المسار.", ["الإيمان", "المسؤولية"]),
    ("003", "noah", "Noah", "نوح", "الثبات في الدعوة", "رحلة طويلة من الصبر والبلاغ والعمل رغم المقاومة.", "الدعوة والصبر", "الصبر", ["التواصل", "إدارة الأزمات"], ["هود", "نوح"], ["11:25–49", "71:1–28"], "الاستمرار الواعي أهم من النتائج السريعة.", ["الثبات", "التوكل"]),
    ("004", "hud", "Hud", "هود", "مواجهة الغرور الحضاري", "دعوة قوم عاد إلى التواضع والرجوع إلى الحق.", "الأمم والمجتمعات", "التواضع", ["التواصل", "الشجاعة"], ["هود", "الأحقاف"], ["11:50–60", "46:21–26"], "القوة بلا قيم تتحول إلى مصدر هلاك.", ["العدالة", "الإيمان"]),
    ("005", "salih", "Salih", "صالح", "الآية والمسؤولية", "قصة ثمود واختبار احترام الحدود والعهود.", "الأمم والمجتمعات", "الأمانة", ["إدارة المخاطر", "اتخاذ القرار"], ["هود", "الشمس"], ["11:61–68", "91:11–15"], "تجاهل الإنذار الواضح يضاعف تكلفة القرار.", ["المسؤولية", "العدل"]),
    ("006", "abraham", "Abraham", "إبراهيم", "البحث عن اليقين", "رحلة فكرية وإيمانية في مواجهة التقليد والباطل.", "الأنبياء", "الإيمان", ["التفكير النقدي", "الشجاعة"], ["الأنعام", "الأنبياء"], ["6:74–83", "21:51–70"], "اليقين يُبنى بالوعي والصدق والشجاعة.", ["التوكل", "الحكمة"]),
    ("007", "abraham-nimrod", "Abraham and Nimrod", "إبراهيم والنمرود", "الحجة أمام السلطة", "مواجهة فكرية تكشف حدود القوة حين تفتقد الحقيقة.", "القيادة", "الشجاعة", ["التفاوض", "التواصل"], ["البقرة"], ["2:258"], "وضوح الحجة يحدّ من تضليل السلطة.", ["العدل", "الحكمة"]),
    ("008", "lot", "Lot", "لوط", "الثبات وسط الانحراف", "قصة دعوة أخلاقية في بيئة شديدة المقاومة.", "الأخلاق", "الثبات", ["التواصل", "ضبط النفس"], ["هود", "الحجر"], ["11:77–83", "15:61–77"], "الالتزام بالقيمة لا يتغير بضغط البيئة.", ["العفة", "الشجاعة"]),
    ("009", "ishmael", "Ishmael", "إسماعيل", "الوفاء والصبر", "قصة الطاعة والصدق وبناء الثقة عبر المواقف.", "الأنبياء", "الأمانة", ["التواصل", "تحمل المسؤولية"], ["مريم", "الصافات"], ["19:54–55", "37:101–107"], "الوفاء يخلق ثقة تتجاوز اللحظة.", ["الصبر", "الإيمان"]),
    ("010", "isaac-jacob", "Isaac and Jacob", "إسحاق ويعقوب", "الاستمرار عبر الأجيال", "امتداد الرسالة والقيم داخل الأسرة والنسل.", "الأنبياء", "الإيمان", ["القيادة", "التربية"], ["البقرة", "هود"], ["2:132–133", "11:71–73"], "استدامة القيم تحتاج نقلًا واعيًا بين الأجيال.", ["الحكمة", "المسؤولية"]),
    ("011", "joseph", "Joseph", "يوسف", "الصبر والتخطيط والتحول", "من المحنة إلى التمكين عبر النزاهة والرؤية وإدارة الأزمات.", "الإدارة والحكمة", "الصبر", ["التخطيط", "إدارة الأزمات", "إدارة الموارد"], ["يوسف"], ["12:4–101"], "الاستقامة والتخطيط يحولان الأزمة إلى فرصة.", ["العفة", "الحكمة", "التسامح"]),
    ("012", "job", "Job", "أيوب", "الصبر تحت الابتلاء", "قصة الصمود الروحي حين تطول المحنة.", "الابتلاء والثبات", "الصبر", ["المرونة", "ضبط النفس"], ["الأنبياء", "ص"], ["21:83–84", "38:41–44"], "الصبر الواعي يحفظ الإنسان من الانهيار الداخلي.", ["الإيمان", "الرضا"]),
    ("013", "jonah", "Jonah", "يونس", "المراجعة والعودة", "قصة قرار متعجل ثم مراجعة صادقة وتغيير للمسار.", "الأنبياء", "التوبة", ["اتخاذ القرار", "ضبط النفس"], ["الصافات", "الأنبياء"], ["37:139–148", "21:87–88"], "الاعتراف بالخطأ بداية استعادة الاتجاه.", ["الإيمان", "الأمل"]),
    ("014", "moses", "Moses", "موسى", "بناء القائد عبر التجربة", "رحلة تكوين قيادي تجمع بين الوحي والمواجهة والتعلّم.", "القيادة", "الشجاعة", ["القيادة", "التواصل", "اتخاذ القرار"], ["طه", "القصص"], ["20:9–98", "28:3–46"], "القيادة تنضج بالتجربة والتكليف والمراجعة.", ["الصبر", "العدل"]),
    ("015", "moses-pharaoh", "Moses and Pharaoh", "موسى وفرعون", "الحق أمام الاستبداد", "مواجهة بين الرسالة والسلطة المتضخمة.", "القيادة", "العدالة", ["التفاوض", "قيادة الأزمات"], ["طه", "الشعراء"], ["20:43–79", "26:10–68"], "الخوف لا يلغي المسؤولية عن قول الحق.", ["الشجاعة", "الإيمان"]),
    ("016", "moses-khidr", "Moses and Al-Khidr", "موسى والخضر", "حدود المعرفة", "رحلة تعلم تكشف أن ظاهر الحدث لا يساوي دائمًا حقيقته.", "الإدارة والحكمة", "الحكمة", ["التعلّم", "التحقق من المعلومات"], ["الكهف"], ["18:60–82"], "التسرع في الحكم يضعف جودة الفهم والقرار.", ["الصبر", "التواضع"]),
    ("017", "qarun", "Qarun", "قارون", "الثروة والغرور", "قصة المال حين ينفصل عن المسؤولية والقيم.", "الأخلاق", "التواضع", ["إدارة الموارد", "الحوكمة"], ["القصص"], ["28:76–82"], "الملكية لا تعني الاستغناء عن المساءلة.", ["العدل", "الشكر"]),
    ("018", "talut-goliath", "Talut and Goliath", "طالوت وجالوت", "اختبار الانضباط", "قصة جيش صغير ينجح بالالتزام والوضوح والثبات.", "القيادة", "الانضباط", ["القيادة", "إدارة الموارد"], ["البقرة"], ["2:246–251"], "جودة الفريق أهم من حجمه حين تتضح المهمة.", ["الصبر", "الإيمان"]),
    ("019", "david-goliath", "David and Goliath", "داود وجالوت", "الشجاعة في اللحظة الحاسمة", "تحول شاب مؤمن إلى عنصر حاسم في مواجهة كبرى.", "الأحداث والعبر", "الشجاعة", ["اتخاذ القرار", "المبادرة"], ["البقرة"], ["2:251"], "المبادرة المدروسة تغيّر موازين القوة.", ["الإيمان", "الثقة"]),
    ("020", "david", "David", "داود", "العدل والعبادة", "قصة القيادة التي تجمع بين القوة والمراجعة والإنصاف.", "القيادة", "العدالة", ["الحوكمة", "اتخاذ القرار"], ["ص", "الأنبياء"], ["38:17–26", "21:78–80"], "القائد العادل يراجع نفسه قبل أن يراجع الآخرين.", ["الحكمة", "التوبة"]),
    ("021", "solomon", "Solomon", "سليمان", "الإدارة والحكمة", "نموذج في فهم الموارد والتواصل واتخاذ القرار.", "الإدارة والحكمة", "الحكمة", ["إدارة الموارد", "التواصل", "القيادة"], ["النمل", "ص"], ["27:15–44", "38:30–40"], "تعدد الموارد يحتاج رؤية وحوكمة وشكرًا.", ["العدل", "التخطيط"]),
    ("022", "sheba", "Sheba", "سبأ", "القرار بين الاستشارة والقوة", "قصة قيادة تتعامل مع معلومة جديدة وتهديد محتمل.", "القيادة", "الحكمة", ["التحقق من المعلومات", "التفاوض"], ["النمل", "سبأ"], ["27:22–44", "34:15–19"], "الاستشارة والتحقق يرفعان جودة القرار.", ["التواضع", "العدل"]),
    ("023", "zechariah", "Zechariah", "زكريا", "الأمل مع الأسباب", "قصة دعاء هادئ وثقة لا تنفصل عن العمل.", "الأنبياء", "الأمل", ["الصبر", "التخطيط"], ["مريم", "آل عمران"], ["19:2–15", "3:38–41"], "الأمل الواقعي يجمع الدعاء والعمل.", ["الإيمان", "الصبر"]),
    ("024", "john", "John", "يحيى", "الجدية والطهارة", "قصة نضج مبكر ووضوح في الرسالة والسلوك.", "الأنبياء", "الاستقامة", ["ضبط النفس", "التواصل"], ["مريم"], ["19:7–15"], "وضوح الهوية يرفع الثبات أمام الضغط.", ["الرحمة", "الحكمة"]),
    ("025", "mary", "Mary", "مريم", "الطهارة والثبات", "قصة عبادة وابتلاء ومسؤولية في مواجهة المجتمع.", "الابتلاء والثبات", "الإيمان", ["المرونة", "ضبط النفس"], ["مريم", "آل عمران"], ["19:16–36", "3:35–47"], "السكينة الداخلية تدعم الثبات أمام الاتهام.", ["الصبر", "العفة"]),
    ("026", "jesus", "Jesus", "عيسى", "الرحمة والرسالة", "دعوة قائمة على الإيمان والرحمة وتصحيح الانحراف.", "الأنبياء", "الرحمة", ["التواصل", "القيادة"], ["آل عمران", "المائدة"], ["3:45–55", "5:110–120"], "الرسالة الأخلاقية تحتاج وضوحًا ورحمة.", ["الإيمان", "الحكمة"]),
    ("027", "cave", "People of the Cave", "أصحاب الكهف", "الثبات وحماية الإيمان", "قصة شباب اختاروا المبدأ رغم ضغط المجتمع.", "الابتلاء والثبات", "الثبات", ["اتخاذ القرار", "إدارة المخاطر"], ["الكهف"], ["18:9–26"], "الانسحاب المؤقت قد يكون قرارًا استراتيجيًا لحماية القيمة.", ["الشجاعة", "الإيمان"]),
    ("028", "dhul-qarnayn", "Dhul-Qarnayn", "ذو القرنين", "التمكين المسؤول", "قصة قائد يجمع بين القوة والعدل وخدمة المجتمعات.", "القيادة", "العدالة", ["القيادة", "إدارة الموارد", "التخطيط"], ["الكهف"], ["18:83–98"], "التمكين الحقيقي يتحول إلى خدمة وحماية.", ["الحكمة", "المسؤولية"]),
    ("029", "luqman", "Luqman", "لقمان", "الحكمة في التربية", "وصايا عملية لبناء الوعي والسلوك داخل الأسرة.", "الأخلاق", "الحكمة", ["التواصل", "التربية"], ["لقمان"], ["31:12–19"], "الحكمة تتحول إلى أثر حين تُترجم إلى تربية عملية.", ["التواضع", "الشكر"]),
    ("030", "sabbath", "People of the Sabbath", "أصحاب السبت", "التحايل على القيم", "قصة مجتمع حاول تجاوز التكليف بالتحايل.", "الأمم والمجتمعات", "الأمانة", ["الحوكمة", "ضبط النفس"], ["الأعراف"], ["7:163–166"], "التحايل القانوني لا يلغي المسؤولية الأخلاقية.", ["العدل", "المساءلة"]),
    ("031", "trench", "People of the Trench", "أصحاب الأخدود", "الثبات أمام الاضطهاد", "قصة إيمان يصمد أمام القوة والعنف.", "الابتلاء والثبات", "الثبات", ["المرونة", "الشجاعة"], ["البروج"], ["85:4–10"], "القيمة الراسخة لا تسقط تحت التهديد.", ["الإيمان", "الصبر"]),
    ("032", "elephant", "People of the Elephant", "أصحاب الفيل", "حدود القوة المادية", "حدث يوضح أن التفوق المادي لا يضمن النتيجة.", "الأحداث والعبر", "التوكل", ["إدارة المخاطر", "الوعي"], ["الفيل"], ["105:1–5"], "القوة المادية ليست العامل الوحيد في النتائج.", ["الإيمان", "التواضع"]),
    ("033", "garden", "Owners of the Garden", "أصحاب الجنة", "المال والنية", "قصة قرار اقتصادي فاسد بدأ من نية إقصاء المحتاج.", "الأخلاق", "العدالة", ["إدارة الموارد", "اتخاذ القرار"], ["القلم"], ["68:17–33"], "النية غير الأخلاقية تفسد القرار والنتيجة.", ["الشكر", "التوبة"]),
    ("034", "samiri", "Al-Samiri", "السامري", "التضليل وصناعة الوهم", "قصة استغلال الفراغ القيادي والتأثير على الجماعة.", "الأمم والمجتمعات", "الوعي", ["التحقق من المعلومات", "إدارة الأزمات"], ["طه"], ["20:83–97"], "غياب التحقق يسهّل صناعة الوهم الجماعي.", ["المسؤولية", "الإيمان"]),
    ("035", "town", "People of the Town", "أصحاب القرية", "الرسالة والمقاومة", "قصة رسل واجهوا الرفض، ورجلٍ جاء داعمًا للحق.", "الدعوة والصبر", "الشجاعة", ["التواصل", "المبادرة"], ["يس"], ["36:13–29"], "المبادرة الأخلاقية قد تبدأ من فرد واحد.", ["الإيمان", "التضحية"]),
    ("036", "tubba", "Tubba'", "تُبّع", "عبرة الحضارات", "إشارة إلى قوة تاريخية لم تمنعها من المساءلة.", "الأمم والمجتمعات", "التواضع", ["التخطيط", "الحوكمة"], ["الدخان", "ق"], ["44:37", "50:14"], "الحضارات تُقاس بقيمها لا بحجمها فقط.", ["العدل", "المسؤولية"]),
    ("037", "creation", "Beginning of Creation", "بداية الخلق", "منطلق الوجود والتكليف", "مدخل تأملي لفهم الخلق والغاية والمسؤولية.", "الأحداث والعبر", "الإيمان", ["التفكير النقدي", "التعلّم"], ["البقرة", "فصلت"], ["2:29–33", "41:9–12"], "فهم البداية يعيد صياغة معنى الغاية والمسؤولية.", ["الحكمة", "الوعي"]),
]

STORIES: List[Story] = [
    Story(
        number=row[0],
        slug=row[1],
        title_en=row[2],
        title_ar=row[3],
        subtitle_ar=row[4],
        short_description_ar=row[5],
        category_ar=row[6],
        primary_value_ar=row[7],
        skills_ar=row[8],
        surah_refs_ar=row[9],
        ayah_ranges_ar=row[10],
        central_message_ar=row[11],
        secondary_values_ar=row[12],
    )
    for row in STORY_ROWS
]

STORY_INDEX = {story.slug: story for story in STORIES}
STORY_POSITION = {story.slug: i for i, story in enumerate(STORIES)}

CATEGORY_OPTIONS = [
    "الكل",
    "الأنبياء",
    "الأخلاق",
    "القيادة",
    "الإدارة والحكمة",
    "الدعوة والصبر",
    "الابتلاء والثبات",
    "الأمم والمجتمعات",
    "الأحداث والعبر",
]

STORY_SECTIONS = [
    ("verses", "الآيات", 25),
    ("tafsir", "التفسير والتحليل", 45),
    ("summary", "خلاصة القصة", 60),
    ("transformation", "التحول الإنساني", 80),
    ("applications", "التطبيقات العملية", 100),
]

EXPLORE_BLOCKS = [
    ("القيم الأساسية", "الميزان القيمي الذي يحكم القرارات والتحولات داخل القصة."),
    ("التحليل النفسي", "الدوافع، المخاوف، الأمل، الصراع الداخلي، والتحول العاطفي."),
    ("الدروس القيادية", "الرؤية، المسؤولية، القرار تحت الضغط، والاتصال."),
    ("الدروس الأخلاقية", "المبدأ الأخلاقي، مواطن الضعف، التصحيح، والنتائج."),
    ("الدروس الإدارية", "التخطيط، الموارد، المخاطر، الحوكمة، المتابعة، والتفاوض."),
    ("الصبر والمرونة", "نوع الابتلاء، الاستجابة، مصدر الثبات، ونقطة التحول."),
    ("نموذج السبب والنتيجة", "سبب ← فكر ← قرار ← سلوك ← نتيجة فورية ← نتيجة بعيدة ← درس."),
    ("المهارات المكتسبة", "المهارات العملية المستخلصة من أحداث القصة."),
    ("نقاط التحول", "الحالة الأولية، المحفز، القرار، التحول، والنتيجة النهائية."),
]


# ============================================================
# SESSION STATE
# ============================================================

def init_state() -> None:
    defaults = {
        "route": "home",
        "selected_story": "joseph",
        "last_opened_story": None,
        "current_story_section": "verses",
        "home_slide": 0,
        "theme": "light",
        "search_query": "",
        "category_filter": "الكل",
        "value_filter": "الكل",
        "skill_filter": "الكل",
        "progress": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# ============================================================
# STYLE SYSTEM
# ============================================================

def inject_css() -> None:
    dark = st.session_state.theme == "dark"
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;500;600;700;800&family=Noto+Kufi+Arabic:wght@500;600;700&display=swap');

    :root {
        --emerald: #123F35;
        --forest: #0B2D27;
        --night: #071D19;
        --ivory: #F7F1E3;
        --parchment: #EFE4CC;
        --sand: #D9C8A9;
        --gold: #C6A15B;
        --antique-gold: #A9803A;
        --terracotta: #A9583C;
        --burgundy: #672D36;
        --text: #232722;
        --muted: #6E6759;
        --card: rgba(255, 251, 242, 0.95);
        --border: rgba(198, 161, 91, 0.30);
        --shadow: 0 18px 45px rgba(48, 34, 17, 0.10);
    }

    html, body, [class*="css"] {
        direction: rtl;
        font-family: "Cairo", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(198,161,91,.10), transparent 24%),
            radial-gradient(circle at 90% 20%, rgba(18,63,53,.08), transparent 28%),
            linear-gradient(135deg, #fbf7ed, #f5ead6);
        color: var(--text);
    }

    .block-container {
        max-width: 1480px;
        padding: 0.7rem 1.2rem 7.5rem;
    }

    .app-shell {
        border: 1px solid var(--border);
        border-radius: 28px;
        background: rgba(255,255,255,.25);
        box-shadow: var(--shadow);
        overflow: hidden;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }

    .top-header {
        position: relative;
        min-height: 112px;
        padding: 20px 28px;
        background:
            linear-gradient(rgba(7,29,25,.97), rgba(11,45,39,.97)),
            repeating-linear-gradient(45deg, transparent 0 18px, rgba(198,161,91,.04) 18px 19px);
        border: 1px solid rgba(198,161,91,.5);
        border-radius: 28px 28px 0 0;
        color: var(--ivory);
        display: grid;
        grid-template-columns: 1fr auto 1fr;
        align-items: center;
        gap: 18px;
    }

    .brand {
        text-align: center;
    }

    .brand-mark {
        width: 64px;
        height: 64px;
        margin: 0 auto 6px;
        border: 2px solid var(--gold);
        border-radius: 50% 50% 44% 44%;
        display: grid;
        place-items: center;
        font-size: 28px;
        background: radial-gradient(circle, rgba(198,161,91,.20), transparent 65%);
        box-shadow: inset 0 0 0 5px rgba(198,161,91,.08);
    }

    .brand h1 {
        margin: 0;
        font-family: "Noto Kufi Arabic", sans-serif;
        color: #e4c582;
        font-size: clamp(1.35rem, 2.4vw, 2.2rem);
    }

    .brand p {
        margin: 4px 0 0;
        color: rgba(247,241,227,.78);
        font-size: .86rem;
    }

    .header-meta {
        color: rgba(247,241,227,.86);
        font-size: .9rem;
    }

    .gold-line {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
        margin: 0;
    }

    .nav-wrap {
        background: var(--forest);
        border-bottom: 1px solid rgba(198,161,91,.45);
        padding: 12px 20px;
    }

    .section-title {
        font-family: "Noto Kufi Arabic", sans-serif;
        color: var(--forest);
        font-weight: 700;
        font-size: clamp(1.25rem, 2vw, 1.85rem);
        margin: 0 0 8px;
    }

    .section-subtitle {
        color: var(--muted);
        margin: 0 0 18px;
        line-height: 1.9;
    }

    .hero {
        min-height: 430px;
        border: 1px solid var(--border);
        border-radius: 28px;
        overflow: hidden;
        position: relative;
        display: grid;
        grid-template-columns: 1.05fr .95fr;
        align-items: stretch;
        background:
            radial-gradient(circle at 75% 35%, rgba(255,255,255,.85), rgba(255,255,255,.2) 32%, transparent 62%),
            linear-gradient(120deg, rgba(247,241,227,.98), rgba(239,228,204,.94));
        box-shadow: var(--shadow);
    }

    .hero-copy {
        padding: clamp(28px, 4vw, 58px);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .eyebrow {
        color: var(--antique-gold);
        font-weight: 800;
        letter-spacing: .02em;
        margin-bottom: 10px;
    }

    .hero h2 {
        font-family: "Noto Kufi Arabic", sans-serif;
        color: var(--forest);
        font-size: clamp(2rem, 4.5vw, 4.2rem);
        line-height: 1.35;
        margin: 0 0 16px;
    }

    .hero p {
        color: var(--muted);
        line-height: 2;
        font-size: clamp(1rem, 1.4vw, 1.18rem);
        max-width: 720px;
    }

    .arch-visual {
        min-height: 430px;
        display: grid;
        place-items: center;
        padding: 28px;
        background:
            radial-gradient(circle at center, rgba(198,161,91,.15), transparent 60%),
            linear-gradient(145deg, rgba(18,63,53,.05), rgba(169,88,60,.08));
    }

    .arch-window {
        width: min(94%, 520px);
        aspect-ratio: 4 / 5;
        border: 9px double var(--gold);
        border-radius: 52% 52% 18% 18% / 34% 34% 12% 12%;
        background:
            linear-gradient(rgba(7,29,25,.16), rgba(7,29,25,.58)),
            radial-gradient(circle at 50% 25%, #e5bd79 0 8%, transparent 9%),
            linear-gradient(165deg, #d99e59 0 34%, #8b6742 35% 48%, #2d5b4d 49% 100%);
        box-shadow:
            0 22px 50px rgba(7,29,25,.22),
            inset 0 0 0 7px rgba(11,45,39,.76);
        position: relative;
        overflow: hidden;
    }

    .arch-window::after {
        content: "۞";
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
        color: rgba(247,241,227,.25);
        font-size: 8rem;
    }

    .slide-dots {
        display: flex;
        gap: 8px;
        justify-content: center;
        margin: 14px 0 4px;
    }

    .slide-dot {
        width: 9px;
        height: 9px;
        border-radius: 999px;
        background: rgba(169,128,58,.28);
    }

    .slide-dot.active {
        width: 28px;
        background: var(--antique-gold);
    }

    .story-card {
        height: 100%;
        border: 1px solid var(--border);
        border-radius: 22px;
        background: var(--card);
        padding: 18px;
        box-shadow: 0 12px 28px rgba(48,34,17,.07);
        position: relative;
        overflow: hidden;
    }

    .story-card::before {
        content: "";
        position: absolute;
        inset: 0 auto 0 0;
        width: 5px;
        background: linear-gradient(var(--gold), var(--emerald));
    }

    .story-number {
        color: var(--antique-gold);
        font-weight: 800;
        font-size: .84rem;
    }

    .story-card h3 {
        font-family: "Noto Kufi Arabic", sans-serif;
        color: var(--forest);
        margin: 6px 0 8px;
        font-size: 1.2rem;
    }

    .story-card p {
        color: var(--muted);
        line-height: 1.8;
        font-size: .91rem;
        min-height: 76px;
    }

    .tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 10px 0;
    }

    .tag {
        border: 1px solid rgba(169,128,58,.26);
        background: rgba(239,228,204,.58);
        color: var(--forest);
        border-radius: 999px;
        padding: 5px 9px;
        font-size: .75rem;
    }

    .progress-shell {
        background: rgba(169,128,58,.15);
        height: 8px;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 12px;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--emerald), var(--gold));
        border-radius: 999px;
    }

    .story-header {
        border: 1px solid var(--border);
        border-radius: 26px;
        background:
            linear-gradient(130deg, rgba(7,29,25,.97), rgba(18,63,53,.94));
        color: var(--ivory);
        padding: clamp(24px, 4vw, 48px);
        box-shadow: var(--shadow);
        margin-bottom: 18px;
        position: relative;
        overflow: hidden;
    }

    .story-header::after {
        content: "۞";
        position: absolute;
        left: 4%;
        top: 50%;
        transform: translateY(-50%);
        font-size: 10rem;
        color: rgba(198,161,91,.08);
    }

    .story-header h2 {
        font-family: "Noto Kufi Arabic", sans-serif;
        color: #e4c582;
        font-size: clamp(1.8rem, 4vw, 3.4rem);
        margin: 6px 0 12px;
    }

    .story-header p {
        color: rgba(247,241,227,.82);
        line-height: 1.9;
        max-width: 860px;
    }

    .content-panel {
        border: 1px solid var(--border);
        border-radius: 24px;
        background: var(--card);
        padding: clamp(20px, 3vw, 34px);
        box-shadow: 0 14px 32px rgba(48,34,17,.07);
        margin-bottom: 16px;
    }

    .content-panel h3 {
        font-family: "Noto Kufi Arabic", sans-serif;
        color: var(--forest);
        margin-top: 0;
    }

    .verse-box {
        border: 1px solid rgba(169,128,58,.35);
        border-radius: 24px;
        padding: clamp(22px, 4vw, 42px);
        background:
            radial-gradient(circle at 12% 15%, rgba(198,161,91,.10), transparent 26%),
            linear-gradient(135deg, #fffdf7, #f4ead4);
        text-align: center;
        box-shadow: inset 0 0 0 5px rgba(198,161,91,.05);
    }

    .verse-box .quran {
        font-family: "Amiri", serif;
        font-size: clamp(1.7rem, 3vw, 2.8rem);
        line-height: 2.2;
        color: #2b332b;
    }

    .notice {
        border-right: 4px solid var(--gold);
        background: rgba(198,161,91,.10);
        border-radius: 14px;
        padding: 14px 16px;
        color: var(--muted);
        line-height: 1.8;
    }

    .analysis-card {
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 20px;
        background: var(--card);
        height: 100%;
        box-shadow: 0 10px 24px rgba(48,34,17,.06);
    }

    .analysis-card h4 {
        color: var(--forest);
        margin: 0 0 10px;
        font-family: "Noto Kufi Arabic", sans-serif;
    }

    .analysis-card p {
        color: var(--muted);
        line-height: 1.8;
        margin-bottom: 0;
    }

    .footer-space {
        height: 30px;
    }

    /* Streamlit controls */
    .stButton > button {
        border: 1px solid var(--gold) !important;
        background: linear-gradient(135deg, var(--emerald), var(--forest)) !important;
        color: var(--ivory) !important;
        border-radius: 14px !important;
        min-height: 44px;
        font-family: "Cairo", sans-serif !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 18px rgba(7,29,25,.14);
    }

    .stButton > button:hover {
        border-color: #e7c77f !important;
        transform: translateY(-1px);
    }

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        background: rgba(255,253,247,.92) !important;
        min-height: 46px;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: .85rem;
    }

    .mobile-nav-label {
        display: none;
    }

    @media (max-width: 900px) {
        .block-container {
            padding: .5rem .7rem 7.8rem;
        }

        .top-header {
            grid-template-columns: 1fr;
            text-align: center;
            padding: 18px;
        }

        .header-meta {
            display: none;
        }

        .hero {
            grid-template-columns: 1fr;
        }

        .arch-visual {
            min-height: 320px;
            order: -1;
            padding: 18px;
        }

        .arch-window {
            max-width: 330px;
        }

        .hero-copy {
            text-align: center;
            padding: 24px;
        }
    }

    @media (max-width: 600px) {
        .top-header {
            min-height: 88px;
            border-radius: 20px 20px 0 0;
        }

        .brand-mark {
            width: 50px;
            height: 50px;
            font-size: 22px;
        }

        .brand p {
            display: none;
        }

        .hero {
            border-radius: 20px;
            min-height: auto;
        }

        .arch-visual {
            min-height: 235px;
        }

        .arch-window {
            max-width: 220px;
        }

        .hero h2 {
            font-size: clamp(1.8rem, 10vw, 2.5rem);
        }

        .story-card p {
            min-height: auto;
        }

        .story-header {
            border-radius: 20px;
            padding: 22px;
        }

        .content-panel {
            border-radius: 18px;
            padding: 18px;
        }

        .stButton > button {
            min-height: 48px;
            font-size: .86rem;
        }
    }
    </style>
    """

    if dark:
        css += """
        <style>
        :root {
            --text: #F5ECD9;
            --muted: #CDBF9F;
            --card: rgba(16,43,37,.94);
            --border: rgba(201,166,92,.24);
        }
        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(201,166,92,.08), transparent 25%),
                linear-gradient(135deg, #071D19, #102B25);
        }
        .section-title,
        .story-card h3,
        .content-panel h3,
        .analysis-card h4 {
            color: #F5ECD9;
        }
        .story-card p,
        .analysis-card p,
        .section-subtitle {
            color: #CDBF9F;
        }
        .tag {
            background: rgba(201,166,92,.08);
            color: #F5ECD9;
        }
        .verse-box {
            background: linear-gradient(135deg, #102B25, #17372F);
        }
        .verse-box .quran {
            color: #F5ECD9;
        }
        .stTextInput input,
        .stSelectbox div[data-baseweb="select"] > div {
            background: #102B25 !important;
            color: #F5ECD9 !important;
        }
        </style>
        """

    st.markdown(css, unsafe_allow_html=True)


inject_css()


# ============================================================
# HELPERS
# ============================================================

def story_progress(slug: str) -> int:
    return int(st.session_state.progress.get(slug, 0))


def set_progress(slug: str, value: int) -> None:
    current = story_progress(slug)
    st.session_state.progress[slug] = max(current, value)


def select_story(slug: str, route: str = "story") -> None:
    st.session_state.selected_story = slug
    st.session_state.last_opened_story = slug
    st.session_state.current_story_section = "verses"
    set_progress(slug, 10)
    st.session_state.route = route


def current_story() -> Story:
    return STORY_INDEX[st.session_state.selected_story]


def safe_join(items: List[str]) -> str:
    return "، ".join(items)


def nav_button(label: str, route: str, icon: str) -> None:
    active = st.session_state.route == route
    text = f"{icon} {label}"
    if st.button(text, key=f"nav_{route}", use_container_width=True, type="primary" if active else "secondary"):
        st.session_state.route = route
        st.rerun()


def render_header() -> None:
    st.markdown(
        """
        <div class="app-shell">
          <div class="top-header">
            <div class="header-meta">تجربة قرآنية تحليلية • ٣٧ قصة</div>
            <div class="brand">
              <div class="brand-mark">📖</div>
              <h1>قصص القرآن</h1>
              <p>هدايات خالدة، وقصص تُحيي القلوب</p>
            </div>
            <div class="header-meta" style="text-align:left;">واجهة عربية متجاوبة • دون قوائم جانبية</div>
          </div>
          <div class="gold-line"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_cols = st.columns([1, 1, 1, 0.65])
    with nav_cols[0]:
        nav_button("الرئيسية", "home", "⌂")
    with nav_cols[1]:
        nav_button("القصة", "story", "◫")
    with nav_cols[2]:
        nav_button("استكشف", "explore", "✦")
    with nav_cols[3]:
        theme_label = "☀" if st.session_state.theme == "dark" else "☾"
        if st.button(theme_label, key="theme_toggle", use_container_width=True):
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()


def render_slide_dots(index: int) -> None:
    dots = "".join(
        f'<span class="slide-dot{" active" if i == index else ""}"></span>'
        for i in range(3)
    )
    st.markdown(f'<div class="slide-dots">{dots}</div>', unsafe_allow_html=True)


def home_slide_payload() -> Dict[str, str]:
    index = st.session_state.home_slide
    if index == 0:
        return {
            "eyebrow": "مدخل إلى المشروع",
            "title": "قصص القرآن",
            "body": "منصة عربية تجمع القصة، المعنى، التحليل الإنساني، والدروس القيادية والإدارية في تجربة واحدة متوازنة.",
            "button": "استكشف القصص",
            "visual": "۞",
        }
    if index == 1:
        last_slug = st.session_state.last_opened_story or "joseph"
        story = STORY_INDEX[last_slug]
        return {
            "eyebrow": "تابع رحلتك",
            "title": story.title_ar,
            "body": f"{story.subtitle_ar}. تقدّم القراءة الحالي: {story_progress(last_slug)}٪.",
            "button": "متابعة القراءة",
            "visual": "◈",
        }
    return {
        "eyebrow": "تدبر القصة واكتشف معناها",
        "title": "من الحدث إلى البصيرة",
        "body": "استكشف القيم، التحليل النفسي، القيادة، الإدارة، الصبر، ونماذج اتخاذ القرار داخل كل قصة.",
        "button": "ابدأ الاستكشاف",
        "visual": "✦",
    }


def render_home_hero() -> None:
    payload = home_slide_payload()
    st.markdown(
        f"""
        <section class="hero">
          <div class="hero-copy">
            <div class="eyebrow">{html.escape(payload["eyebrow"])}</div>
            <h2>{html.escape(payload["title"])}</h2>
            <p>{html.escape(payload["body"])}</p>
          </div>
          <div class="arch-visual">
            <div class="arch-window"></div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    action_cols = st.columns([1, 1, 1])
    with action_cols[0]:
        if st.button("السابق", key="slide_prev", use_container_width=True):
            st.session_state.home_slide = (st.session_state.home_slide - 1) % 3
            st.rerun()
    with action_cols[1]:
        if st.button(payload["button"], key="slide_action", use_container_width=True):
            if st.session_state.home_slide == 0:
                st.session_state.home_slide = 2
            elif st.session_state.home_slide == 1:
                select_story(st.session_state.last_opened_story or "joseph", "story")
            else:
                st.session_state.route = "explore"
            st.rerun()
    with action_cols[2]:
        if st.button("التالي", key="slide_next", use_container_width=True):
            st.session_state.home_slide = (st.session_state.home_slide + 1) % 3
            st.rerun()

    render_slide_dots(st.session_state.home_slide)


def get_filter_options() -> tuple[List[str], List[str]]:
    values = sorted({story.primary_value_ar for story in STORIES} | {v for story in STORIES for v in story.secondary_values_ar})
    skills = sorted({skill for story in STORIES for skill in story.skills_ar})
    return ["الكل"] + values, ["الكل"] + skills


def filtered_stories() -> List[Story]:
    query = st.session_state.search_query.strip().lower()
    category = st.session_state.category_filter
    value = st.session_state.value_filter
    skill = st.session_state.skill_filter

    result: List[Story] = []
    for story in STORIES:
        searchable = " ".join(
            [
                story.number,
                story.slug,
                story.title_en,
                story.title_ar,
                story.subtitle_ar,
                story.short_description_ar,
                story.category_ar,
                story.primary_value_ar,
                safe_join(story.secondary_values_ar),
                safe_join(story.skills_ar),
                safe_join(story.surah_refs_ar),
            ]
        ).lower()

        if query and query not in searchable:
            continue
        if category != "الكل" and story.category_ar != category:
            continue
        if value != "الكل" and value not in [story.primary_value_ar, *story.secondary_values_ar]:
            continue
        if skill != "الكل" and skill not in story.skills_ar:
            continue
        result.append(story)
    return result


def render_story_card(story: Story) -> None:
    progress = story_progress(story.slug)
    tags = [story.category_ar, story.primary_value_ar, *story.skills_ar[:2]]
    tags_html = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags)
    st.markdown(
        f"""
        <article class="story-card">
          <div class="story-number">{story.number}</div>
          <h3>{html.escape(story.title_ar)}</h3>
          <p>{html.escape(story.short_description_ar)}</p>
          <div class="tag-row">{tags_html}</div>
          <div style="font-size:.78rem;color:var(--muted);">السور: {html.escape(safe_join(story.surah_refs_ar))}</div>
          <div class="progress-shell"><div class="progress-fill" style="width:{progress}%"></div></div>
          <div style="font-size:.75rem;color:var(--muted);margin-top:6px;">التقدم: {progress}٪</div>
        </article>
        """,
        unsafe_allow_html=True,
    )
    if st.button("فتح القصة", key=f"open_{story.slug}", use_container_width=True):
        select_story(story.slug, "story")
        st.rerun()


def render_home() -> None:
    render_home_hero()

    st.markdown('<div class="section-title">ابحث داخل القصص</div>', unsafe_allow_html=True)
    st.text_input(
        "البحث",
        key="search_query",
        placeholder="ابحث عن قصة، قيمة، مهارة، شخصية، فئة، سورة أو كلمة مفتاحية...",
        label_visibility="collapsed",
    )

    value_options, skill_options = get_filter_options()
    filter_cols = st.columns([1, 1, 1, 0.55])
    with filter_cols[0]:
        st.selectbox("الفئة", CATEGORY_OPTIONS, key="category_filter")
    with filter_cols[1]:
        st.selectbox("القيمة الرئيسية", value_options, key="value_filter")
    with filter_cols[2]:
        st.selectbox("المهارة", skill_options, key="skill_filter")
    with filter_cols[3]:
        st.write("")
        if st.button("إعادة ضبط", key="reset_filters", use_container_width=True):
            st.session_state.search_query = ""
            st.session_state.category_filter = "الكل"
            st.session_state.value_filter = "الكل"
            st.session_state.skill_filter = "الكل"
            st.rerun()

    stories = filtered_stories()
    st.markdown(
        f'<div class="section-title">القصص المتاحة <span style="font-size:.9rem;color:var(--muted);">({len(stories)} من 37)</span></div>',
        unsafe_allow_html=True,
    )

    if not stories:
        st.info("لا توجد نتائج مطابقة. جرّب تعديل البحث أو إعادة ضبط عوامل التصفية.")
        return

    for start in range(0, len(stories), 3):
        cols = st.columns(3)
        for offset, story in enumerate(stories[start : start + 3]):
            with cols[offset]:
                render_story_card(story)


def render_story_header(story: Story) -> None:
    progress = story_progress(story.slug)
    tags = [story.category_ar, story.primary_value_ar, *story.skills_ar]
    tags_html = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in tags)
    st.markdown(
        f"""
        <section class="story-header">
          <div class="story-number">القصة رقم {story.number}</div>
          <h2>{html.escape(story.title_ar)}</h2>
          <p>{html.escape(story.subtitle_ar)} — {html.escape(story.central_message_ar)}</p>
          <div class="tag-row">{tags_html}</div>
          <div style="color:rgba(247,241,227,.78);font-size:.86rem;">
            السور: {html.escape(safe_join(story.surah_refs_ar))} • نطاقات الآيات: {html.escape(safe_join(story.ayah_ranges_ar))}
          </div>
          <div class="progress-shell"><div class="progress-fill" style="width:{progress}%"></div></div>
          <div style="margin-top:7px;color:rgba(247,241,227,.78);font-size:.8rem;">تقدم القراءة: {progress}٪</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_story_selector(story: Story) -> None:
    selected_idx = STORY_POSITION[story.slug]
    selected_label = st.selectbox(
        "اختر قصة",
        options=[s.slug for s in STORIES],
        index=selected_idx,
        format_func=lambda slug: f'{STORY_INDEX[slug].number} — {STORY_INDEX[slug].title_ar}',
        key="story_selector",
    )
    if selected_label != story.slug:
        select_story(selected_label, "story")
        st.rerun()


def render_story_section_tabs(story: Story) -> None:
    cols = st.columns(5)
    for i, (section_id, label, progress_value) in enumerate(STORY_SECTIONS):
        with cols[i]:
            active = st.session_state.current_story_section == section_id
            if st.button(label, key=f"section_{section_id}", use_container_width=True, type="primary" if active else "secondary"):
                st.session_state.current_story_section = section_id
                set_progress(story.slug, progress_value)
                st.rerun()


def render_story_section(story: Story) -> None:
    section = st.session_state.current_story_section

    if section == "verses":
        st.markdown(
            f"""
            <div class="content-panel">
              <h3>الآيات</h3>
              <div class="notice">
                هذا الملف يقدّم بنية الواجهة فقط. يجب تحميل النص القرآني من مصدر موثوق ومراجعته قبل النشر.
                لا تُدرج نصوصًا قرآنية تجريبية أو غير متحقق منها.
              </div>
              <br>
              <div class="verse-box">
                <div style="color:var(--antique-gold);font-weight:700;margin-bottom:16px;">
                  {html.escape(safe_join(story.surah_refs_ar))} • {html.escape(safe_join(story.ayah_ranges_ar))}
                </div>
                <div class="quran">يوضع هنا النص القرآني الموثق دون أي تعديل.</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if section == "tafsir":
        numbered_items = [
            "السياق العام للقصة",
            "الصراع الرئيسي",
            "نقطة الضعف الإنسانية",
            "الهداية الإلهية",
            "الاستجابة البشرية",
            "الدوافع والخوف والأمل",
            "الإيمان والصبر والفتنة والتوبة",
            "الصفات القيادية",
            "مسار اتخاذ القرار",
            "النتيجة الفورية والبعيدة",
            "الدرس النهائي",
        ]
        items_html = "".join(
            f"<li><strong>{i+1}.</strong> {html.escape(item)} — يُحمّل المحتوى من قاعدة بيانات القصة.</li>"
            for i, item in enumerate(numbered_items)
        )
        st.markdown(
            f"""
            <div class="content-panel">
              <h3>التفسير والتحليل</h3>
              <ol style="line-height:2.1;color:var(--muted);">{items_html}</ol>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if section == "summary":
        st.markdown(
            f"""
            <div class="content-panel">
              <h3>خلاصة القصة</h3>
              <p style="line-height:2;color:var(--muted);">{html.escape(story.short_description_ar)}</p>
              <div class="analysis-card">
                <h4>الرسالة المركزية</h4>
                <p>{html.escape(story.central_message_ar)}</p>
              </div>
              <br>
              <div class="notice">تُعرض هنا نقاط التحول، القرار الرئيسي، النتيجة النهائية، والدرس الأساسي بعد تحميل المحتوى الكامل.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    if section == "transformation":
        stages = ["السبب", "طريقة التفكير", "القرار", "السلوك", "السلوك المتكرر", "النتيجة", "الدرس"]
        cols = st.columns(len(stages))
        for i, stage in enumerate(stages):
            with cols[i]:
                st.markdown(
                    f"""
                    <div class="analysis-card" style="text-align:center;">
                      <div class="story-number">{i+1:02d}</div>
                      <h4>{stage}</h4>
                      <p>مرحلة قابلة للتحميل ديناميكيًا حسب القصة.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        return

    application_groups = [
        "الحياة الشخصية",
        "الأسرة",
        "القيادة",
        "الإدارة",
        "أخلاقيات العمل",
        "المجتمع",
        "الدعوة",
        "التعليم",
    ]
    st.markdown('<div class="content-panel"><h3>التطبيقات العملية</h3></div>', unsafe_allow_html=True)
    for start in range(0, len(application_groups), 2):
        cols = st.columns(2)
        for offset, title in enumerate(application_groups[start : start + 2]):
            with cols[offset]:
                st.markdown(
                    f"""
                    <div class="analysis-card">
                      <h4>{title}</h4>
                      <p>تُعرض التطبيقات المرتبطة بهذه القصة فقط. الفئات الفارغة يمكن استبعادها عند ربط البيانات.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def previous_next_controls(story: Story) -> None:
    idx = STORY_POSITION[story.slug]
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button("القصة السابقة", disabled=idx == 0, use_container_width=True):
            select_story(STORIES[idx - 1].slug, "story")
            st.rerun()
    with cols[1]:
        if st.button("استكشف هذه القصة", use_container_width=True):
            st.session_state.route = "explore"
            st.rerun()
    with cols[2]:
        if st.button("القصة التالية", disabled=idx == len(STORIES) - 1, use_container_width=True):
            select_story(STORIES[idx + 1].slug, "story")
            st.rerun()


def render_story() -> None:
    story = current_story()
    set_progress(story.slug, 10)
    render_story_header(story)
    render_story_selector(story)
    render_story_section_tabs(story)
    render_story_section(story)
    previous_next_controls(story)


def related_stories(story: Story) -> List[Story]:
    scored = []
    for other in STORIES:
        if other.slug == story.slug:
            continue
        score = 0
        if other.category_ar == story.category_ar:
            score += 3
        if other.primary_value_ar == story.primary_value_ar:
            score += 3
        score += len(set(other.secondary_values_ar) & set(story.secondary_values_ar))
        score += len(set(other.skills_ar) & set(story.skills_ar))
        scored.append((score, STORY_POSITION[other.slug], other))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in scored[:3]]


def render_explore() -> None:
    story = current_story()
    render_story_header(story)

    st.markdown(
        f"""
        <div class="content-panel">
          <h3>استكشف: قصة {html.escape(story.title_ar)}</h3>
          <p style="line-height:1.9;color:var(--muted);">{html.escape(story.central_message_ar)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for start in range(0, len(EXPLORE_BLOCKS), 3):
        cols = st.columns(3)
        for offset, (title, description) in enumerate(EXPLORE_BLOCKS[start : start + 3]):
            with cols[offset]:
                extra = ""
                if title == "القيم الأساسية":
                    extra = f"القيمة الرئيسية: {story.primary_value_ar}. القيم المساندة: {safe_join(story.secondary_values_ar)}."
                elif title == "المهارات المكتسبة":
                    extra = safe_join(story.skills_ar)
                st.markdown(
                    f"""
                    <div class="analysis-card">
                      <h4>{html.escape(title)}</h4>
                      <p>{html.escape(description)}</p>
                      {f'<div class="tag-row"><span class="tag">{html.escape(extra)}</span></div>' if extra else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="section-title">قصص مرتبطة</div>', unsafe_allow_html=True)
    related = related_stories(story)
    cols = st.columns(3)
    for i, other in enumerate(related):
        with cols[i]:
            relation = []
            if other.category_ar == story.category_ar:
                relation.append("الفئة المشتركة")
            if other.primary_value_ar == story.primary_value_ar:
                relation.append("القيمة المشتركة")
            relation_text = " و".join(relation) if relation else "تقاطع في المهارات أو القيم"
            st.markdown(
                f"""
                <article class="story-card">
                  <div class="story-number">{other.number}</div>
                  <h3>{html.escape(other.title_ar)}</h3>
                  <p>{html.escape(relation_text)}: {html.escape(other.primary_value_ar)} — {html.escape(other.category_ar)}</p>
                </article>
                """,
                unsafe_allow_html=True,
            )
            if st.button("فتح القصة", key=f"related_{other.slug}", use_container_width=True):
                select_story(other.slug, "story")
                st.rerun()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main() -> None:
    render_header()

    route = st.session_state.route
    if route == "home":
        render_home()
    elif route == "story":
        render_story()
    elif route == "explore":
        render_explore()
    else:
        st.session_state.route = "home"
        st.rerun()

    st.markdown('<div class="footer-space"></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
