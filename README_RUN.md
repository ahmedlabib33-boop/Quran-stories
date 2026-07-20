# Quran Stories Streamlit App

## تشغيل التطبيق

افتح PowerShell داخل هذا المجلد ثم شغل:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

أو شغل مباشرة:

```powershell
.\RUN_APP.bat
```

## المحتوى

- ملف Excel هو فهرس القصص الرئيسي.
- ملفات Word هي الدروس التفصيلية.
- أي ملف Word جديد باسم مثل `003-نوح.docx` سيظهر تلقائيًا كدرس كامل إذا كان اسم القصة مطابقًا للفهرس.
- الملفات المؤقتة التي تبدأ بـ `~$` يتم تجاهلها.
