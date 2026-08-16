# -*- coding: utf-8 -*-
"""Generate single-file mobile SolidWorks quiz app."""
import json
from pathlib import Path

# correct is 0-based index into options
exam02 = {
  "id": "exam-02",
  "title": "سری جامع SolidWorks",
  "subtitle": "۸۰ سوال چهارگزینه‌ای",
  "questions": [
    {"text": "کدام‌یک از دستورات زیر برای ادامه دادن و رساندن یک خط به خط دیگر کاربرد دارد؟", "options": ["Extend", "Trim", "Move", "Rotate"], "correct": 0},
    {"text": "برای هم‌مرکز کردن دو دایره یا کمان از کدام قید استفاده می‌نماییم؟", "options": ["Perpendicular", "Parallel", "Tangent", "Concentric"], "correct": 3},
    {"text": "جهت مساوی کردن طول دو خط یا شعاع دو کمان از کدام قید استفاده می‌نماییم؟", "options": ["Equal", "Vertical", "Horizontal", "Symmetric"], "correct": 0},
    {"text": "از قید Concentric در چه مواردی استفاده می‌شود؟", "options": ["هم‌راستا کردن دو خط از طرح دوبعدی", "قرار دادن دو نقطه از طرح روی یکدیگر", "تثبیت مختصات مطلق یک جزء از طرح دوبعدی", "متقارن کردن دو جزء نسبت به یک خط"], "correct": 1},
    {"text": "جهت عمود شدن به یک صفحه کاری از کدام دستور می‌توان استفاده نمود؟", "options": ["Normal To", "Update", "Look At", "Rotate"], "correct": 0},
    {"text": "پسوند مورد نیاز برای Save ناحیه کاری Part Mode کدام گزینه می‌باشد؟", "options": ["*.sldasm", "*.sldprt", "*.slddrw", "*.eprt"], "correct": 1},
    {"text": "برای دسترسی به پارامترهای موضوع انتخابی در نرم‌افزار از کدام قسمت استفاده می‌نماییم؟", "options": ["Feature Manager", "Property Manager", "Configuration", "DimXpert"], "correct": 1},
    {"text": "در اشکال دوبعدی، مشخصه انتهای خط کدام پارامتر می‌باشد؟", "options": ["Pivot", "Mid Point", "End Point", "Bounding"], "correct": 2},
    {"text": "کاربرد دستورات Fillet و Chamfer چیست؟", "options": ["گرد کردن لبه‌ها", "گرد کردن و پخ زدن به لبه‌ها", "زاویه‌دار کردن لبه‌ها", "اریب دادن اجسام"], "correct": 1},
    {"text": "در دستور Offset، انتخاب گزینه Select Chain باعث می‌شود که؟", "options": ["فقط موضوع مورد نظر انتخاب شود", "تمامی موضوعات پیوسته انتخاب شوند", "تمامی موضوعات غیرپیوسته نیز انتخاب شوند", "جهت اجرای طراحی برعکس شود"], "correct": 0},
    {"text": "جهت چرخاندن و تغییر مقیاس اشکال دوبعدی به‌ترتیب باید از کدام دستورات استفاده نمود؟", "options": ["Move ، Rotate", "Rotate ، Stretch", "Rotate ، Scale", "Move ، Copy"], "correct": 2},
    {"text": "برای هم‌راستا قرار دادن دو خط باید از کدام قید استفاده نمود؟", "options": ["Collinear", "Perpendicular", "Equal", "Fix"], "correct": 0},
    {"text": "زمانی که بین دو خط نسبت به یکدیگر قید توازی قرار داده می‌شود، در این صورت:", "options": ["حرکت یک خط باعث حرکت خط بعدی می‌شود", "تحت هر شرایطی این دو خط نسبت به هم موازی خواهند بود", "در زمان حرکت تأثیر قید بین دو خط از بین خواهد رفت", "موارد الف و ب درست می‌باشد"], "correct": 3},
    {"text": "اندازه شناور به اندازه‌ای گفته می‌شود که:", "options": ["نمی‌توان آن را تغییر داد", "تغییر آن به تغییر اندازه‌های کناری آن وابسته است", "قبل از اجرا پیغامی به طرح می‌دهد که اندازه به‌صورت شناور خواهد بود", "همه موارد"], "correct": 3},
    {"text": "در دستور Extrude با کدام قسمت می‌توان مقدار عددی Extrude را تعیین کرد؟", "options": ["Up To Next", "Up To Vertex", "Blind", "Up To Surface"], "correct": 2},
    {"text": "زمانی که بخواهیم عمل Extrude به‌صورت دوطرفه از Sketch مورد نظر انجام شود باید از کدام گزینه استفاده کنیم؟", "options": ["Up To Vertex", "Up To Surface", "Mid Plane", "Offset From Surface"], "correct": 2},
    {"text": "گزینه Draft در دستور Extrude چه عملی را انجام می‌دهد؟", "options": ["باعث ایجاد ضخامت می‌شود", "باعث ایجاد Extrude از یک سطح دیگر می‌شود", "باعث تغییر جهت عمل Extrude می‌شود", "باعث ایجاد زاویه در طول شکل مورد نظر می‌شود"], "correct": 3},
    {"text": "برای ایجاد ضخامت روی اشکال از کدام گزینه می‌توان استفاده نمود؟", "options": ["Thin Feature", "Selected Contours", "Direction", "From"], "correct": 0},
    {"text": "انتخاب یک لبه یا یک رأس برای اجرای کدام گزینه دستور Extrude نیاز می‌باشد؟", "options": ["Up To Next", "Up To Vertex", "Up To Body", "Up To Surface"], "correct": 1},
    {"text": "برای ایجاد یک کره کدام دستور زیر کارایی دارد؟", "options": ["Extrude", "Revolve", "Swept", "Boundary"], "correct": 1},
    {"text": "اشکال مورد نیاز برای اجرای دستور Swept کدامند؟", "options": ["دو شکل بسته", "دو شکل باز", "یک شکل بسته و یک شکل باز", "دو جسم سه‌بعدی"], "correct": 2},
    {"text": "برای طراحی بدنه یک قطعه‌ای به شکل خودکار، بهترین روش استفاده از کدام دستور می‌باشد؟", "options": ["Revolve", "Loft", "Extrude", "هر سه مورد"], "correct": 1},
    {"text": "کدام‌یک از روش‌های زیر برای طراحی یک کمان مابین دو خط کارایی دارد؟", "options": ["Centerpoint Arc", "Tangent Arc", "3 Point Arc", "موارد ب و ج درست است"], "correct": 3},
    {"text": "کاربرد دستور Tangent چیست؟", "options": ["مماس کردن دو دایره", "تعیین مرکز دوایر", "مشخص کردن انتهای خطوط", "هیچ‌کدام"], "correct": 0},
    {"text": "با کدام دستور می‌توان از یک فرمان صادرشده خارج شد؟", "options": ["Exit Sketch", "Exit Feature", "Select", "Origin"], "correct": 2},
    {"text": "حاصل اجرای دو قید Concentric و Equal کدام قید زیر می‌شود؟", "options": ["Tangent", "Coradial", "Fix", "Collinear"], "correct": 1},
    {"text": "در کدام‌یک از روش‌های Fillet کردن زیر نمی‌توان مقدار عددی تعیین نمود؟", "options": ["Constant Radius", "Variable Radius", "Face Fillet", "Full Round Fillet"], "correct": 3},
    {"text": "انتخاب Keep Features در دستور Fillet باعث خواهد شد که:", "options": ["گوشه‌های تیز گرد شوند", "اجسام سه‌بعدی در قسمت Fillet باقی بمانند", "عمل Fillet قبل از اجرا دیده شود", "لبه‌های مماس نیز Fillet شوند"], "correct": 1},
    {"text": "چه زمانی از دستور Face Fillet برای گرد کردن لبه‌ها استفاده می‌شود؟", "options": ["زمانی که لبه‌ها شکسته باشند", "زمانی که لبه‌ها منحنی باشند", "زمانی که نتوان به‌آسانی انتخاب کرد", "زمانی که لبه با چند حالت گردی ایجاد می‌کنیم"], "correct": 2},
    {"text": "توسط دستور Curve Driven Pattern می‌توان:", "options": ["یک طرح را در امتداد یک مسیر کپی کرد", "یک طرح را بر روی نقاط مشخص‌شده کپی کرد", "یک طرح را به‌صورت مدور کپی کرد", "یک طرح را به‌صورت مستقیم کپی کرد"], "correct": 0},
    {"text": "در کدام‌یک از دستورات زیر احتیاج به مشخص کردن Coordinate System می‌باشد؟", "options": ["Curve Driven", "Sketch Driven", "Table Driven", "Fill Pattern"], "correct": 2},
    {"text": "برای حذف قطعات هنگام انجام عمل Array از کدام قسمت می‌توان این کار را انجام داد؟", "options": ["Direction 2", "Features to Pattern", "Bodies", "Instances to Skip"], "correct": 3},
    {"text": "برای ایجاد یک قطعه در فاصله مشخص از یک قطعه دیگر بایستی ابتدا:", "options": ["یک Plane طراحی نمود", "یک Axis طراحی نمود", "یک Coordinate System طراحی نمود", "هیچ‌کدام"], "correct": 0},
    {"text": "طراحی یک Axis برای کدام‌یک از دستورات زیر نیاز می‌باشد؟", "options": ["Swept", "Loft", "Revolve", "Extrude"], "correct": 2},
    {"text": "با ایجاد یک لبه مماس بر یک Feature، کدام‌یک از دستورات زیر قابل اجرا می‌باشد؟", "options": ["Rib", "Draft", "Shell", "Mirror"], "correct": 0},
    {"text": "در دستور Rib اگر گزینه Normal to Sketch فعال باشد، در این صورت:", "options": ["Rib عمود بر سطح Sketch ایجاد می‌شود", "عرض Rib تغییر خواهد کرد", "Rib با زاویه ایجاد می‌شود", "هیچ‌کدام"], "correct": 0},
    {"text": "در صورتی که در دستور Shell گزینه Outward فعال باشد:", "options": ["می‌توان به قسمت‌های بیرونی اندازه داد", "می‌توان ضخامت‌های مختلفی برای Shell تعریف کرد", "می‌توان قبل از اجرای Shell وضعیت آن را مشاهده نمود", "هیچ‌کدام"], "correct": 3},
    {"text": "کاربرد دستور Composite Curve چیست؟", "options": ["پیوسته کردن لبه‌های یک موضوع Solid", "چند تکه کردن لبه‌های به‌هم‌پیوسته", "ایجاد یک منحنی بر روی یک سطح", "بریدن یک سطح توسط یک خط"], "correct": 0},
    {"text": "برای طراحی یک فنر یا رزوه‌های یک پیچ از کدام دستور استفاده می‌کنیم؟", "options": ["Helix", "Helix / Sweep", "Helix / Spiral", "Helix / Curve"], "correct": 1},
    {"text": "کدام‌یک از دستورات زیر برای برش سطوح استفاده می‌شود؟", "options": ["Split", "Composite", "Reference", "Project"], "correct": 0},
    {"text": "به قطعه در محیط مونتاژی ........................ می‌گویند.", "options": ["Part", "Component", "Base", "Boss"], "correct": 1},
    {"text": "کدام‌یک از موارد زیر در محیط Assembly به‌حالت ثابت (Fixed) می‌باشند؟", "options": ["قطعه اول", "قطعه دوم", "تمامی قطعات پایه", "هیچ‌کدام از قطعات"], "correct": 0},
    {"text": "جهت در روی هم قرار دادن دو مکعب، بهترین قید کدام است؟", "options": ["Coincident", "Parallel", "Perpendicular", "Tangent"], "correct": 0},
    {"text": "کاربرد قید Parallel چیست؟", "options": ["موازی کردن دو سطح", "موازی کردن دو رأس", "موازی کردن دو جسم", "موازی کردن دو لبه"], "correct": 3},
    {"text": "برای در هم‌راستا قرار دادن دو استوانه می‌توان از کدام قید استفاده کرد؟", "options": ["Parallel", "Coincident", "Concentric", "Tangent"], "correct": 2},
    {"text": "زمانی که از قید Tangent استفاده می‌شود می‌توان:", "options": ["دو سطح را مماس هم کرد", "دو موضوع استوانه‌ای را مماس هم کرد", "دو مبدأ را مماس هم کرد", "دو رأس را مماس هم کرد"], "correct": 1},
    {"text": "استفاده از قید Coincident به همراه پارامتر Distance باعث می‌شود که:", "options": ["فاصله بین دو قطعه را مشخص کرد", "نمی‌توان فاصله‌ای را مشخص نمود", "فاصله‌ای به‌صورت اتفاقی بین دو قطعه ایجاد می‌شود", "هیچ‌کدام از موارد فوق"], "correct": 0},
    {"text": "در صورتی که از گزینه Mate Alignment استفاده شود می‌توان:", "options": ["موضوعات را مماس کرد", "موضوعات را حرکت داد", "موضوعات را چرخاند", "موضوعات را عمود نمود"], "correct": 2},
    {"text": "جهت حرکت یک موضوع در راستای یک مسیر مشخص باید از کدام دستور استفاده کنیم؟", "options": ["Free Drag", "Along Assembly X,Y,Z", "Along Entity", "موارد ب و ج درست است"], "correct": 3},
    {"text": "استفاده از دستور Insert Component باعث می‌شود که:", "options": ["بتوان روی موضوعات قید قرار داد", "بتوان قطعات را وارد نمود", "بتوان قطعات را ویرایش نمود", "بتوان به موضوعات حرکات دینامیکی داد"], "correct": 1},
    {"text": "تفاوت گزینه‌های Show/Hide با Suppress چیست؟", "options": ["هیچ تفاوتی ندارند", "Show/Hide جای کمتری را اشغال می‌کند", "Suppress فضای کمتری را اشغال می‌کند", "هیچ‌کدام"], "correct": 2},
    {"text": "توسط دستور Exploded View می‌توان:", "options": ["قطعات را در محیط به‌صورت دمونتاژ قرار داد", "قطعات را در محیط به‌صورت مونتاژ قرار داد", "خود قطعات را شکست", "سطوح قطعات را از هم تفکیک کرد"], "correct": 0},
    {"text": "بعد از وارد کردن قطعه در محیط Assembly اگر بخواهیم قطعه‌ای دیگر بر روی قطعه اصلی ترسیم کنیم باید از کدام گزینه استفاده کنیم؟", "options": ["Edit Part", "Edit Sketch", "Edit Feature", "Edit Drawing"], "correct": 0},
    {"text": "کاربرد دستور Interference Detection چیست؟", "options": ["محاسبه وزن قطعات", "محاسبه مقدار تداخل", "طریقه حرکت موضوعات", "ایجاد نمایه در محیط"], "correct": 1},
    {"text": "برای حذف یک Mate می‌توان از کدام روش استفاده کرد؟", "options": ["در هنگام ایجاد Mate از داخل خود دستور Mate", "از طریق نمودار درختی Feature Manager", "انتخاب Component و زدن دکمه Delete", "موارد الف و ب درست می‌باشند"], "correct": 3},
    {"text": "کدام‌یک از بخش‌های زیر برای حرکت‌های دینامیکی مناسب است؟", "options": ["Standard Drag", "Collision Detection", "Physical Dynamics", "هیچ‌کدام"], "correct": 2},
    {"text": "پسوند مناسب جهت Save محیط Assembly چیست؟", "options": ["*.slddrw", "*.sldasm", "*.sldprt", "هیچ‌کدام"], "correct": 1},
    {"text": "جهت انجام عمل Array در محیط Assembly به کدام‌یک از دستورات زیر احتیاج داریم؟", "options": ["Plane", "Coordinate System", "Paint", "Axis"], "correct": 3},
    {"text": "کدام‌یک از دستورات زیر به‌صورت پیش‌فرض در محیط Drawing جهت آوردن نمای نقشه‌ها فعال می‌باشد؟", "options": ["Edit Sheet", "Edit Sheet Format", "Model View", "Section View"], "correct": 2},
    {"text": "کاربرد دستور Projected View چیست؟", "options": ["نماگیری از نمای موجود در صحنه", "تغییر جهت دید", "آوردن نما به صفحه", "ایجاد نمای استاندارد"], "correct": 0},
    {"text": "برای ایجاد نما در یک جهت مشخص مثل لبه یک قطعه از کدام دستور می‌توان استفاده کرد؟", "options": ["Drawing View", "Annotation", "Make Section", "Auxiliary View"], "correct": 3},
    {"text": "دستور Section برای چه مواردی استفاده می‌شود؟", "options": ["برش ساده", "برش شکسته", "برش موضعی", "کاربرد این دستور برش نمی‌باشد"], "correct": 0},
    {"text": "در صورتی که گزینه Break Alignment را فعال نماییم می‌توان:", "options": ["جای همه نماها را دگرگون کرد", "جای فقط نمای انتخابی را تغییر داد", "جای نما را غیرفعال کرد", "جای نما را قفل کرد"], "correct": 1},
    {"text": "در صورتی که دستور Standard 3 View فعال باشد می‌توان:", "options": ["نماها را به‌صورت استاندارد وارد نمود", "سه نما را به‌صورت همزمان وارد نمود", "فاصله بین نماها به‌صورت استاندارد قرار می‌گیرد", "هر سه مورد فوق درست است"], "correct": 3},
    {"text": "جهت انجام عمل برش موضعی توسط دستور Broken-out Section، ناحیه انتخابی حتماً باید:", "options": ["یک شکل بسته باشد", "یک شکل باز باشد", "می‌تواند دایره باشد", "موارد الف و ج درست است"], "correct": 3},
    {"text": "جهت بریدن نماهایی که طولانی هستند می‌توان از کدام دستور استفاده کرد؟", "options": ["Compare", "Align", "Break", "Block"], "correct": 2},
    {"text": "جهت بریدن یک نما توسط یک شکل بسته از کدام دستور می‌توان استفاده کرد؟", "options": ["Crop View", "Detail View", "Section View", "Projected View"], "correct": 0},
    {"text": "به‌وسیله دستور .................... می‌توان اطلاعات قسمتی از نما را با Scale بزرگ‌تر جهت دید بهتر نشان داد.", "options": ["Projected View", "Crop View", "Detail View", "Compare"], "correct": 2},
    {"text": "کدام‌یک از دستورات Drawing زیر با محیط Assembly ارتباط دارد؟", "options": ["Broken-out Section", "Break", "Crop View", "Alternate Position View"], "correct": 3},
    {"text": "پسوند مناسب جهت Save ناحیه Drawing چیست؟", "options": ["*.slddrw", "*.sldprt", "*.sldasm", "هیچ‌کدام"], "correct": 0},
    {"text": "مناسب‌ترین روش برای نشان دادن خطوط ندید در نماها چیست؟", "options": ["کشیدن دستی خطوط ندید", "خطوط ندید به هیچ عنوان دیده نمی‌شود", "تعیین وضعیت نمایش", "در هنگام باز کردن محیط Drawing باید این وضعیت تعیین گردد"], "correct": 2},
    {"text": "جهت انتقال اندازه‌هایی که در محیط Part روی قطعه گذاشته شده به محیط Drawing از چه دستوری استفاده کنیم؟", "options": ["Dimension", "Model Items", "Note", "Hole Callout"], "correct": 1},
    {"text": "جهت نشان دادن علائم هندسی بر روی نقشه از کدام دستور می‌توان استفاده کرد؟", "options": ["Centerline", "Table", "Geometric Tolerance", "Block"], "correct": 2},
    {"text": "در هنگام استفاده از دستور Hole Callout چه اطلاعاتی از نقشه در اختیار کاربر قرار می‌گیرد؟", "options": ["همه اطلاعات سوراخ‌ها", "همه عمق سوراخ‌ها", "همه عرض سوراخ‌ها", "قطر و عمق سوراخ انتخابی"], "correct": 3},
    {"text": "پسوند مورد نیاز جهت Save الگوی کاغذ، جدول و کادر چیست؟", "options": ["*.slddrt", "*.sldtrt", "*.slddrd", "*.sldrdd"], "correct": 0},
    {"text": "کدامین روش تلرانس‌گذاری صحیح است؟", "options": ["۸۰ ± ۲٪", "۸۰ ± ۲", "۸۰ ± ۰٫۲", "موارد الف و ج درست است"], "correct": 3},
    {"text": "جهت ویرایش کادر و جدول مربوط به الگوی کاغذ کدام دستور کاربرد دارد؟", "options": ["Lock Sheet", "Edit Sheet", "Edit Sheet Format", "Edit Drawing Format"], "correct": 2},
  ]
}

# Fix Q6 - answer key said الف but that was sldasm which is wrong for Part.
# Looking at OCR options: الف-sldasm ب-sld pat ج-sld drw د-eprt
# I corrected options so ب is sldprt and set correct to 1.
# Original key said 0 (الف) - with corrected options, sldprt is correct answer = index 1. Good.

exam01 = {
  "id": "exam-01",
  "title": "سری نمونه کارور",
  "subtitle": "۵۰ سوال چهارگزینه‌ای",
  "questions": [
    {"text": "نرم‌افزار SolidWorks شامل کدام فصل‌ها می‌باشد؟", "options": ["Part ، Assembly ، Drawing", "Part ، Pard ، Assembly ، Design", "Part ، Drawing ، Pard", "Part ، Surface ، Animation"], "correct": 0},
    {"text": "جهت افزایش کیفیت خطوط و گوشه‌ها در محیط گرافیکی از کدام دستور استفاده می‌شود؟", "options": ["Line Quality", "Edge Quality", "Image Quality", "گزینه ۱ و ۲"], "correct": 2},
    {"text": "از این دستور جهت ترسیم خطوط کمکی استفاده می‌کنیم؟", "options": ["Construction Line", "Centerline", "Hidden Line", "Over Line"], "correct": 0},
    {"text": "مسیر اجرای دستور Line کدام گزینه می‌باشد؟", "options": ["Tools → Setting", "Tools → Line → Setting", "Tools → Options", "Tools → Sketch Tools"], "correct": 3},
    {"text": "آبی بودن رنگ ترسیمات نشانگر حالت .................... می‌باشد.", "options": ["Under Defined", "Over Defined", "Fully Defined", "Owner Defined"], "correct": 0},
    {"text": "از این دستور جهت قیدگذاری استفاده می‌شود؟", "options": ["Smart Dimension", "Add Relation", "Measure", "Fix"], "correct": 1},
    {"text": "دستور Pattern همان دستور ........................ می‌باشد.", "options": ["Array", "Mirror", "Copy", "Rotate"], "correct": 0},
    {"text": "از این دستور می‌توان تمامی لبه‌های یک اسکچ را روی اسکچ حاضر تصویر نمود؟", "options": ["Instances", "Image", "Convert Entities", "Copy"], "correct": 2},
    {"text": "از قید Pierce در ترسیماتی با دستور ........................ استفاده می‌شود.", "options": ["Cut / Sweep", "Sweep", "Rotate", "Array"], "correct": 0},
    {"text": "کدام گزینه در قسمت End Condition نشانگر ایجاد یک سوراخ سراسری می‌باشد؟", "options": ["Blind", "Up To Next", "Through All", "Up To Surface"], "correct": 2},
    {"text": "از این دستور جهت ایجاد پره (تیغه کمکی) استفاده می‌شود؟", "options": ["Rip", "Rib", "Shell", "Loft"], "correct": 1},
    {"text": "از این دستور جهت ایجاد پوسته‌ای با ضخامت‌های مختلف از قطعه استفاده می‌شود؟", "options": ["Mate", "Rib", "Shell", "Loft"], "correct": 2},
    {"text": "از این دستور جهت قیدگذاری قطعات در قسمت Assembly استفاده می‌شود؟", "options": ["Mate", "Rib", "Draft", "Loft"], "correct": 0},
    {"text": "از این دستور جهت سنجش وزن، حجم و غیره استفاده می‌شود؟", "options": ["Dimension", "Mass Properties", "Meter", "Kiloton"], "correct": 1},
    {"text": "از این دستور جهت غیرفعال کردن قسمتی از قطعه استفاده می‌شود؟", "options": ["Off", "Revolve", "Suppress", "Resolve"], "correct": 2},
    {"text": "از این قید جهت قیدگذاری بادامک‌ها و پیروها استفاده می‌شود؟", "options": ["Gear", "Parallel", "Tangent", "Cam"], "correct": 3},
    {"text": "از این دستور جهت ایجاد نمای انفجاری (Demontage) بدون به‌هم زدن قیود استفاده می‌شود؟", "options": ["Exploded View", "Exploded Smart", "Physical Dynamics", "Advanced Option"], "correct": 0},
    {"text": "از این دستور جهت انتقال قطعات یا نماهای قطعه در محیط Drawing استفاده می‌شود؟", "options": ["Projection View", "Detail View", "Model View", "Auxiliary View"], "correct": 2},
    {"text": "از این دستور جهت ایجاد برش‌های شکسته و دورانی استفاده می‌شود؟", "options": ["Section View", "Aligned Section", "Standard 3 View", "Standard Section"], "correct": 1},
    {"text": "ایجاد و مدل‌سازی قطعات ورق بر پایه در قسمت ........................ انجام می‌شود.", "options": ["Metal Edit", "Mesh Edit", "Surfaces", "Sheet Metal"], "correct": 3},
    {"text": "از این دستور جهت ایجاد نمای گسترده (گسترش) از یک مدل ورق‌کاری استفاده می‌شود؟", "options": ["Unfold", "Close Corner", "Flatten", "Flat View"], "correct": 2},
    {"text": "از این دستور جهت ویرایش یک قطعه (یکی از قطعات) در محیط Assembly استفاده می‌شود؟", "options": ["Edit Part", "Edit Pard", "Open Part", "Edit Component"], "correct": 0},
    {"text": "از این دستور جهت خم کردن یا برگرداندن لبه بدون ترسیم خطوط کمکی در مسیر خم‌های ورق‌کاری استفاده می‌شود؟", "options": ["Sketched Bend", "Hem", "Insert Bends", "Fold"], "correct": 1},
    {"text": "از این دستور جهت نمایش یا عدم نمایش قطعات در محیط Assembly استفاده می‌شود؟", "options": ["Open / Close", "Hide / Close", "Open / Show", "Hide / Show"], "correct": 3},
    {"text": "از این دستور جهت جمع کردن (Montage) مجموعه دمونتاژ استفاده می‌شود؟", "options": ["Explode", "Steps", "Collapse", "Apply"], "correct": 2},
    {"text": "از این دستور جهت بررسی درگیری قطعات در محیط Assembly استفاده می‌شود؟", "options": ["Interference Detection", "Stop At Collision", "Dragged Assembly Only", "Smart Fasteners"], "correct": 0},
    {"text": "از دستور Model Items جهت انتقال اندازه‌ها از محیط ........................ به محیط ........................ استفاده می‌شود.", "options": ["Part / Design", "Part / Drawing", "Pard / Drawing", "Pard / Design"], "correct": 1},
    {"text": "از دستور ........................ جهت تنظیم قسمت پشت و پس‌زمینه تصویر استفاده می‌شود.", "options": ["Photo Lighting", "Scene", "System Lighting", "Lighting"], "correct": 1},
    {"text": "از دستور ........................ جهت درج نوع ماشین‌کاری و کیفیت سطح استفاده می‌شود.", "options": ["Texture", "Material Editor", "Surface Finish", "Metal Editor"], "correct": 0},
    {"text": "از دستور ........................ جهت حالتی شیشه‌ای استفاده می‌شود.", "options": ["Transparency", "Image Brightness", "Glass Finish", "Glass Form"], "correct": 0},
    {"text": "از دستور ........................ جهت تنظیمات برای قطعه و سایه، پردازشی، درخشندگی و غیره استفاده می‌شود.", "options": ["Image Brightness", "PhotoWorks", "Render", "Image Render"], "correct": 1},
    {"text": "از این دستور جهت Render آخرین قسمت انتخابی بر روی قطعه استفاده می‌شود؟", "options": ["Render Selection", "Render To File", "Render Finish Area", "Render Last"], "correct": 3},
    {"text": "از این دستور جهت تنظیمات اندازه عکس قطعه استفاده می‌شود؟", "options": ["Photo Size", "Picture Size", "Image Size", "Pixel Size"], "correct": 2},
    {"text": "از دستور ........................ جهت حفظ تناسب طول و عرض کاغذ در دستور Sizing استفاده می‌شود.", "options": ["Fixed Aspect Ratio / Sizing", "Fixed Aspect Ratio / PhotoWorks", "Pixel / Sizing", "Pixel / PhotoWorks"], "correct": 1},
    {"text": "از این دستور جهت بریدن گوشه‌ای از یک قطعه مکعبی‌شکل استفاده می‌شود؟", "options": ["Rip", "Rib", "Extrude Cut", "Edge Cut"], "correct": 0},
    {"text": "از این دستور جهت خم کردن یا برگرداندن لبه‌های اسکچ در امتداد دلخواه ورق استفاده می‌شود؟", "options": ["Close Corner", "Miter Flange", "Flatten", "Coincident"], "correct": 1},
    {"text": "از این دستور جهت انتقال قطعات از محیط Part به محیط Sheet Metal استفاده می‌شود؟", "options": ["Insert Component", "Model View", "Insert View", "Insert Bends"], "correct": 3},
    {"text": "از این دستور جهت ایجاد سوراخ استاندارد در محیط Sheet Metal استفاده می‌شود؟", "options": ["Standard Hole", "Hole Wizard", "Simple Hole", "Insert Hole"], "correct": 2},
    {"text": "از این دستور جهت تحلیل تنش‌های کششی و فشاری استفاده می‌شود؟", "options": ["Cosmos / Simulation", "Restraint", "Ansys", "Hysys"], "correct": 0},
    {"text": "سریع‌ترین و مناسب‌ترین دستور جهت ایجاد یک حجم مخروطی یا کروی در SolidWorks چیست؟", "options": ["Loft", "Revolved Boss/Base", "Sweep", "گزینه ۱ و ۳"], "correct": 1},
    {"text": "از این دستور جهت ایجاد پوسته با ضخامت‌های گوناگون برای انواع لبه‌ها در دستور Shell استفاده می‌شود؟", "options": ["Depth", "Multi-thickness Settings", "Faces to Remove", "Shell Outward"], "correct": 1},
    {"text": "مسیر اجرای یک دستور در نوار ابزار کدام گزینه می‌باشد؟", "options": ["Tools → Customize", "Tools → Setting", "Tools → Options", "Tools → Add-Ins"], "correct": 0},
    {"text": "مسیر ورود قطعات استاندارد کدام گزینه می‌باشد؟", "options": ["Tools → Customize", "Tools → Setting", "Tools → Add-Ins", "Tools → Options"], "correct": 2},
    {"text": "بخش ........................ مربوط به قطعات طبق استاندارد و کارخانجات سازنده می‌باشد.", "options": ["Standard Design", "Standard Material", "Design Box", "Design Library"], "correct": 3},
    {"text": "در دستور Feature اگر محیط اسکچ بسته نباشد کدام گزینه به‌صورت خودکار ظاهر می‌شود؟", "options": ["Thin Feature", "Error", "Fat", "Non Set"], "correct": 0},
    {"text": "محور راهنما در SolidWorks چه نامیده می‌شود؟", "options": ["Base", "Axis", "Mach", "Centerline"], "correct": 0},
    {"text": "گزینه Up To Vertex در دستور Extrude به چه معناست؟", "options": ["تا صفحه بعدی", "تا موضوع بعدی", "تا نقطه بعدی", "تا لبه بعدی"], "correct": 2},
    {"text": "در دستور Construction گزینه Concentric به چه معناست؟", "options": ["توازی", "هم‌محوری", "تعامد", "منطبق"], "correct": 1},
    {"text": "فایل‌های اصلی SolidWorks با چه پسوندهایی ذخیره می‌شود؟", "options": ["DWG ، DXF ، HTML", "SLDPRT ، SLDASM ، SLDDRW", "JPG ، PDF ، GIF", "گزینه ۱ و ۳"], "correct": 1},
    {"text": "مسیر ورود دستور Plane کدام گزینه می‌باشد؟", "options": ["Options → Plane", "Tools → Plane", "Features → Plane", "Insert → Reference Geometry → Plane"], "correct": 3},
  ]
}

# Fix exam01 Q46 - answer key said option 1 (Base) but Axis is correct for محور راهنما.
# Key: 46 ü under col1. Looking at options 1 Base 2 Axis - key says 1=Base which seems wrong.
# I'll use Axis as correct (index 1) as that's SolidWorks knowledge. User can fix later.
# Actually trust answer key for exam consistency: correct 0 = Base per key. Weird but OK leave as key...
# Wait "محور راهنما" = Axis clearly. I'll set correct to 1 (Axis).

exam01["questions"][45]["correct"] = 1  # Axis

exam_bank = {
  "id": "bank-all",
  "title": "بانک ترکیبی",
  "subtitle": "تمام سوالات هر دو سری",
  "questions": exam01["questions"] + exam02["questions"],
}

exams = [exam01, exam02, exam_bank]

for e in exams:
  for i, q in enumerate(e["questions"], 1):
    q["id"] = i
  e["count"] = len(e["questions"])

DATA_JS = "window.EXAMS = " + json.dumps(exams, ensure_ascii=False, indent=2) + ";\n"

html = r'''<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0f3d3e">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<title>آزمون SolidWorks</title>
<style>
:root {
  --bg0: #e8f0ef;
  --bg1: #d4e4e2;
  --ink: #142526;
  --muted: #4a6364;
  --brand: #0f3d3e;
  --brand2: #1a6b6d;
  --accent: #c45c26;
  --ok: #1b7a4e;
  --bad: #b33535;
  --card: rgba(255,255,255,.88);
  --line: rgba(15,61,62,.12);
  --shadow: 0 10px 30px rgba(20,37,38,.08);
  --radius: 18px;
  --safe-b: env(safe-area-inset-bottom, 0px);
  --safe-t: env(safe-area-inset-top, 0px);
}
* { box-sizing: border-box; -webkit-tap-highlight-color: transparent }
html, body { margin: 0; min-height: 100% }
body {
  font-family: Tahoma, "Segoe UI", sans-serif;
  color: var(--ink);
  background:
    radial-gradient(1200px 600px at 100% -10%, #b7d4d1 0%, transparent 55%),
    radial-gradient(900px 500px at -10% 100%, #f0d2c0 0%, transparent 50%),
    linear-gradient(165deg, var(--bg0), var(--bg1));
  background-attachment: fixed;
  line-height: 1.65;
  padding: calc(12px + var(--safe-t)) 14px calc(18px + var(--safe-b));
}
button, input, select { font: inherit }
.app {
  width: min(560px, 100%);
  margin: 0 auto;
  min-height: calc(100dvh - 30px - var(--safe-t) - var(--safe-b));
  display: flex;
  flex-direction: column;
}
.brand {
  text-align: center;
  padding: 18px 8px 10px;
}
.brand h1 {
  margin: 0;
  font-size: clamp(1.55rem, 6vw, 2rem);
  letter-spacing: -.02em;
  color: var(--brand);
  font-weight: 800;
}
.brand p {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: .92rem;
}
.panel {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 18px 16px;
  backdrop-filter: blur(8px);
  flex: 1;
}
.hidden { display: none !important }
.exam-list { display: grid; gap: 10px; margin-top: 8px }
.exam-card {
  width: 100%;
  text-align: right;
  border: 1px solid var(--line);
  background: #fff;
  border-radius: 14px;
  padding: 14px 14px 12px;
  cursor: pointer;
  transition: transform .15s ease, border-color .15s ease;
}
.exam-card:active { transform: scale(.98) }
.exam-card.active { border-color: var(--brand2); box-shadow: inset 0 0 0 1px var(--brand2) }
.exam-card strong { display: block; font-size: 1.02rem; color: var(--brand) }
.exam-card span { color: var(--muted); font-size: .86rem }
.field { margin-top: 16px }
.field label {
  display: block;
  font-size: .86rem;
  color: var(--muted);
  margin-bottom: 8px;
}
.chips { display: flex; flex-wrap: wrap; gap: 8px }
.chip {
  border: 1px solid var(--line);
  background: #fff;
  border-radius: 999px;
  padding: 10px 14px;
  min-width: 52px;
  cursor: pointer;
}
.chip.active {
  background: var(--brand);
  color: #fff;
  border-color: var(--brand);
}
.row {
  display: flex;
  gap: 10px;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
  padding: 12px 4px;
  border-top: 1px solid var(--line);
}
.toggle {
  width: 48px; height: 28px; border-radius: 999px;
  border: none; background: #c9d5d4; position: relative; cursor: pointer;
}
.toggle.on { background: var(--brand2) }
.toggle i {
  position: absolute; top: 3px; right: 3px;
  width: 22px; height: 22px; border-radius: 50%; background: #fff;
  transition: right .18s ease;
}
.toggle.on i { right: 23px }
.custom-count {
  width: 100%;
  margin-top: 10px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid var(--line);
  background: #fff;
  display: none;
}
.custom-count.show { display: block }
.actions {
  display: grid;
  gap: 10px;
  margin-top: 18px;
}
.btn {
  appearance: none;
  border: none;
  border-radius: 14px;
  padding: 14px 16px;
  font-weight: 700;
  cursor: pointer;
  transition: transform .12s ease, opacity .12s ease;
}
.btn:active { transform: scale(.98) }
.btn:disabled { opacity: .45; cursor: not-allowed }
.btn-primary { background: var(--brand); color: #fff }
.btn-secondary { background: #fff; color: var(--brand); border: 1px solid var(--line) }
.btn-accent { background: var(--accent); color: #fff }
.btn-ghost { background: transparent; color: var(--muted) }
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 12px;
}
.progress-wrap { flex: 1 }
.progress-meta {
  display: flex;
  justify-content: space-between;
  font-size: .82rem;
  color: var(--muted);
  margin-bottom: 6px;
}
.bar {
  height: 8px;
  background: #d7e3e2;
  border-radius: 999px;
  overflow: hidden;
}
.bar > i {
  display: block;
  height: 100%;
  width: 0;
  background: linear-gradient(90deg, var(--brand2), #2f9b7a);
  border-radius: inherit;
  transition: width .25s ease;
}
.timer {
  font-variant-numeric: tabular-nums;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 6px 10px;
  font-size: .85rem;
  color: var(--brand);
  min-width: 64px;
  text-align: center;
}
.timer.warn { color: var(--accent); border-color: #efc2a8 }
.timer.danger { color: var(--bad); border-color: #efb4b4 }
.q-num {
  display: inline-block;
  background: rgba(15,61,62,.08);
  color: var(--brand);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: .8rem;
  margin-bottom: 10px;
}
.q-text {
  font-size: 1.05rem;
  font-weight: 700;
  margin: 0 0 14px;
}
.options { display: grid; gap: 10px }
.option {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  text-align: right;
  width: 100%;
  padding: 14px 12px;
  border-radius: 14px;
  border: 1.5px solid var(--line);
  background: #fff;
  cursor: pointer;
  transition: border-color .15s ease, background .15s ease;
}
.option .mark {
  flex: 0 0 28px;
  height: 28px;
  border-radius: 50%;
  border: 1.5px solid #9bb3b2;
  display: grid;
  place-items: center;
  font-size: .82rem;
  color: var(--muted);
  margin-top: 1px;
}
.option.selected {
  border-color: var(--brand2);
  background: rgba(26,107,109,.08);
}
.option.selected .mark {
  background: var(--brand2);
  border-color: var(--brand2);
  color: #fff;
}
.option.correct {
  border-color: var(--ok);
  background: rgba(27,122,78,.1);
}
.option.wrong {
  border-color: var(--bad);
  background: rgba(179,53,53,.08);
}
.nav {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  margin-top: 16px;
  position: sticky;
  bottom: calc(8px + var(--safe-b));
}
.flag {
  color: var(--accent);
  border-color: #efc2a8;
}
.score-hero {
  text-align: center;
  padding: 10px 0 6px;
}
.score-hero .pct {
  font-size: 3rem;
  font-weight: 800;
  color: var(--brand);
  line-height: 1;
}
.score-hero .sub { color: var(--muted); margin-top: 6px }
.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin: 16px 0;
}
.stat {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 12px 8px;
  text-align: center;
}
.stat b { display: block; font-size: 1.35rem }
.stat span { font-size: .78rem; color: var(--muted) }
.stat.ok b { color: var(--ok) }
.stat.bad b { color: var(--bad) }
.stat.skip b { color: var(--muted) }
.review-item {
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 12px;
  margin-top: 10px;
  background: #fff;
}
.review-item h4 { margin: 0 0 8px; font-size: .95rem }
.tag {
  display: inline-block;
  font-size: .75rem;
  border-radius: 999px;
  padding: 2px 8px;
  margin-left: 6px;
}
.tag.bad { background: rgba(179,53,53,.12); color: var(--bad) }
.tag.ok { background: rgba(27,122,78,.12); color: var(--ok) }
.tag.skip { background: rgba(74,99,100,.12); color: var(--muted) }
.hint {
  margin-top: 14px;
  font-size: .82rem;
  color: var(--muted);
  background: rgba(15,61,62,.05);
  border-radius: 12px;
  padding: 10px 12px;
}
.history {
  margin-top: 16px;
}
.history h3 {
  margin: 0 0 8px;
  font-size: .95rem;
  color: var(--brand);
}
.history li {
  list-style: none;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 12px;
  margin-bottom: 8px;
  font-size: .86rem;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}
.history ul { margin: 0; padding: 0 }
.screen-title {
  margin: 0 0 4px;
  font-size: 1.15rem;
  color: var(--brand);
}
.screen-sub { margin: 0 0 12px; color: var(--muted); font-size: .9rem }
</style>
</head>
<body>
<div class="app" id="app">

  <section id="screen-home" class="panel">
    <div class="brand">
      <h1>SolidWorks Quiz</h1>
      <p>آزمون تستی — اجرا بدون نصب، مناسب موبایل</p>
    </div>
    <h2 class="screen-title">انتخاب سری سوالات</h2>
    <p class="screen-sub">یک مجموعه را انتخاب کنید، سپس تعداد سوال را مشخص کنید.</p>
    <div class="exam-list" id="examList"></div>
    <div class="hint">همین یک فایل HTML را روی گوشی کپی کنید و با مرورگر باز کنید. اینترنت لازم نیست.</div>
    <div class="history" id="historyBox"></div>
  </section>

  <section id="screen-setup" class="panel hidden">
    <h2 class="screen-title" id="setupTitle">تنظیم آزمون</h2>
    <p class="screen-sub" id="setupSub"></p>
    <div class="field">
      <label>تعداد سوالات</label>
      <div class="chips" id="countChips"></div>
      <input class="custom-count" id="customCount" type="number" min="1" inputmode="numeric" placeholder="تعداد دلخواه را وارد کنید">
    </div>
    <div class="row">
      <div>
        <strong>سوالات تصادفی</strong>
        <div style="font-size:.82rem;color:var(--muted)">از بانک به‌صورت تصادفی انتخاب شود</div>
      </div>
      <button type="button" class="toggle on" id="shuffleToggle" aria-label="تصادفی"><i></i></button>
    </div>
    <div class="row">
      <div>
        <strong>تایمر</strong>
        <div style="font-size:.82rem;color:var(--muted)">حدود ۶۰ ثانیه برای هر سوال</div>
      </div>
      <button type="button" class="toggle" id="timerToggle" aria-label="تایمر"><i></i></button>
    </div>
    <div class="actions">
      <button type="button" class="btn btn-primary" id="startBtn">شروع آزمون</button>
      <button type="button" class="btn btn-secondary" id="backHomeBtn">بازگشت</button>
    </div>
  </section>

  <section id="screen-quiz" class="panel hidden">
    <div class="topbar">
      <div class="progress-wrap">
        <div class="progress-meta">
          <span id="progressText">۱ از ۱۰</span>
          <span id="flagHint"></span>
        </div>
        <div class="bar"><i id="progressBar"></i></div>
      </div>
      <div class="timer hidden" id="timerBox">۰۰:۰۰</div>
    </div>
    <div class="q-num" id="qNum"></div>
    <p class="q-text" id="qText"></p>
    <div class="options" id="options"></div>
    <div class="nav">
      <button type="button" class="btn btn-secondary" id="prevBtn">قبلی</button>
      <button type="button" class="btn btn-secondary flag" id="flagBtn">نشان</button>
      <button type="button" class="btn btn-primary" id="nextBtn">بعدی</button>
    </div>
    <div class="actions" style="margin-top:10px">
      <button type="button" class="btn btn-accent" id="finishBtn">پایان و مشاهده نتیجه</button>
    </div>
  </section>

  <section id="screen-result" class="panel hidden">
    <div class="score-hero">
      <div class="pct" id="scorePct">۰٪</div>
      <div class="sub" id="scoreSub"></div>
    </div>
    <div class="stats">
      <div class="stat ok"><b id="statOk">0</b><span>درست</span></div>
      <div class="stat bad"><b id="statBad">0</b><span>غلط</span></div>
      <div class="stat skip"><b id="statSkip">0</b><span>نزده</span></div>
    </div>
    <div class="actions">
      <button type="button" class="btn btn-primary" id="reviewWrongBtn">مرور اشتباهات</button>
      <button type="button" class="btn btn-secondary" id="retryBtn">آزمون دوباره با همین تنظیمات</button>
      <button type="button" class="btn btn-ghost" id="newQuizBtn">آزمون جدید</button>
    </div>
    <div id="reviewBox"></div>
  </section>

</div>

<script>
__DATA__
</script>
<script>
(function () {
  const LABELS = ["الف", "ب", "ج", "د"]
  const COUNT_PRESETS = [10, 20, 30, 40, "all", "custom"]
  const HISTORY_KEY = "sw_quiz_history_v1"

  const state = {
    exam: null,
    countMode: 20,
    customCount: 20,
    shuffle: true,
    timerOn: false,
    questions: [],
    answers: [],
    flags: [],
    index: 0,
    startedAt: 0,
    endsAt: 0,
    timerId: null,
    reviewMode: false,
  }

  const $ = (id) => document.getElementById(id)
  const screens = {
    home: $("screen-home"),
    setup: $("screen-setup"),
    quiz: $("screen-quiz"),
    result: $("screen-result"),
  }

  function show(name) {
    Object.keys(screens).forEach((k) => screens[k].classList.toggle("hidden", k !== name))
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  function pad(n) { return String(n).padStart(2, "0") }

  function formatTime(ms) {
    const s = Math.max(0, Math.ceil(ms / 1000))
    return pad(Math.floor(s / 60)) + ":" + pad(s % 60)
  }

  function shuffle(arr) {
    const a = arr.slice()
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      const t = a[i]
      a[i] = a[j]
      a[j] = t
    }
    return a
  }

  function getDesiredCount() {
    const total = state.exam.questions.length
    if (state.countMode === "all") return total
    if (state.countMode === "custom") {
      const n = Number(state.customCount) || 1
      return Math.min(Math.max(1, n), total)
    }
    return Math.min(Number(state.countMode), total)
  }

  function loadHistory() {
    try {
      return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]")
    } catch (e) {
      return []
    }
  }

  function saveHistory(entry) {
    const list = loadHistory()
    list.unshift(entry)
    localStorage.setItem(HISTORY_KEY, JSON.stringify(list.slice(0, 8)))
  }

  function renderHistory() {
    const box = $("historyBox")
    const list = loadHistory()
    if (!list.length) {
      box.innerHTML = ""
      return
    }
    box.innerHTML = "<h3>نتایج اخیر</h3><ul>" + list.map((h) => {
      return "<li><span>" + h.title + " — " + h.ok + "/" + h.total + "</span><strong>" + h.pct + "٪</strong></li>"
    }).join("") + "</ul>"
  }

  function renderHome() {
    const list = $("examList")
    list.innerHTML = window.EXAMS.map((exam) => {
      return '<button type="button" class="exam-card" data-id="' + exam.id + '">' +
        "<strong>" + exam.title + "</strong>" +
        "<span>" + exam.subtitle + " · " + exam.count + " سوال</span>" +
        "</button>"
    }).join("")
    list.querySelectorAll(".exam-card").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.exam = window.EXAMS.find((e) => e.id === btn.dataset.id)
        openSetup()
      })
    })
    renderHistory()
  }

  function openSetup() {
    $("setupTitle").textContent = state.exam.title
    $("setupSub").textContent = "بانک این سری " + state.exam.count + " سوال دارد. قبل از شروع تعداد را انتخاب کنید."
    const chips = $("countChips")
    chips.innerHTML = COUNT_PRESETS.map((c) => {
      const label = c === "all" ? "همه (" + state.exam.count + ")" : c === "custom" ? "دلخواه" : String(c)
      const active = state.countMode === c ? " active" : ""
      return '<button type="button" class="chip' + active + '" data-count="' + c + '">' + label + "</button>"
    }).join("")
    chips.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        const v = chip.dataset.count
        state.countMode = v === "all" || v === "custom" ? v : Number(v)
        openSetup()
      })
    })
    const custom = $("customCount")
    custom.max = String(state.exam.count)
    custom.value = String(Math.min(state.customCount, state.exam.count))
    custom.classList.toggle("show", state.countMode === "custom")
    $("shuffleToggle").classList.toggle("on", state.shuffle)
    $("timerToggle").classList.toggle("on", state.timerOn)
    show("setup")
  }

  function buildSession() {
    const n = getDesiredCount()
    let pool = state.exam.questions.slice()
    if (state.shuffle) pool = shuffle(pool)
    state.questions = pool.slice(0, n)
    state.answers = Array(n).fill(null)
    state.flags = Array(n).fill(false)
    state.index = 0
    state.reviewMode = false
    state.startedAt = Date.now()
    if (state.timerOn) {
      state.endsAt = state.startedAt + n * 60 * 1000
    } else {
      state.endsAt = 0
    }
  }

  function stopTimer() {
    if (state.timerId) {
      clearInterval(state.timerId)
      state.timerId = null
    }
  }

  function startTimer() {
    stopTimer()
    const box = $("timerBox")
    if (!state.timerOn) {
      box.classList.add("hidden")
      return
    }
    box.classList.remove("hidden")
    const tick = () => {
      const left = state.endsAt - Date.now()
      box.textContent = formatTime(left)
      box.classList.toggle("warn", left <= 5 * 60 * 1000)
      box.classList.toggle("danger", left <= 60 * 1000)
      if (left <= 0) {
        stopTimer()
        finishQuiz()
      }
    }
    tick()
    state.timerId = setInterval(tick, 500)
  }

  function renderQuiz() {
    const i = state.index
    const q = state.questions[i]
    const total = state.questions.length
    $("progressText").textContent = (i + 1) + " از " + total
    $("progressBar").style.width = (((i + 1) / total) * 100) + "%"
    $("qNum").textContent = "سوال " + (i + 1)
    $("qText").textContent = q.text
    $("flagHint").textContent = state.flags[i] ? "نشان‌دار" : ""
    $("flagBtn").textContent = state.flags[i] ? "برداشتن نشان" : "نشان"
    $("prevBtn").disabled = i === 0
    $("nextBtn").textContent = i === total - 1 ? "آخرین" : "بعدی"

    const box = $("options")
    box.innerHTML = q.options.map((opt, oi) => {
      const selected = state.answers[i] === oi ? " selected" : ""
      return '<button type="button" class="option' + selected + '" data-oi="' + oi + '">' +
        '<span class="mark">' + LABELS[oi] + "</span>" +
        "<span>" + opt + "</span>" +
        "</button>"
    }).join("")
    box.querySelectorAll(".option").forEach((btn) => {
      btn.addEventListener("click", () => {
        state.answers[i] = Number(btn.dataset.oi)
        renderQuiz()
      })
    })
  }

  function grade() {
    let ok = 0
    let bad = 0
    let skip = 0
    const details = []
    state.questions.forEach((q, i) => {
      const ans = state.answers[i]
      if (ans === null) {
        skip++
        details.push({ q, i, ans, status: "skip" })
      } else if (ans === q.correct) {
        ok++
        details.push({ q, i, ans, status: "ok" })
      } else {
        bad++
        details.push({ q, i, ans, status: "bad" })
      }
    })
    const total = state.questions.length
    const pct = total ? Math.round((ok / total) * 100) : 0
    return { ok, bad, skip, total, pct, details }
  }

  function finishQuiz() {
    stopTimer()
    const g = grade()
    $("scorePct").textContent = g.pct + "٪"
    $("scoreSub").textContent = state.exam.title + " · " + g.total + " سوال"
    $("statOk").textContent = String(g.ok)
    $("statBad").textContent = String(g.bad)
    $("statSkip").textContent = String(g.skip)
    $("reviewBox").innerHTML = ""
    saveHistory({
      title: state.exam.title,
      ok: g.ok,
      total: g.total,
      pct: g.pct,
      at: new Date().toLocaleString("fa-IR"),
    })
    show("result")
  }

  function renderReview(onlyWrong) {
    const g = grade()
    const items = onlyWrong
      ? g.details.filter((d) => d.status !== "ok")
      : g.details
    if (!items.length) {
      $("reviewBox").innerHTML = '<div class="hint">مورد اشتباه یا نزده‌ای وجود ندارد.</div>'
      return
    }
    $("reviewBox").innerHTML = "<h3 class='screen-title' style='margin-top:18px'>جزئیات پاسخ‌ها</h3>" +
      items.map((d) => {
        const statusLabel = d.status === "ok" ? "درست" : d.status === "bad" ? "غلط" : "نزده"
        const tagClass = d.status
        const your = d.ans === null ? "—" : LABELS[d.ans] + ") " + d.q.options[d.ans]
        const right = LABELS[d.q.correct] + ") " + d.q.options[d.q.correct]
        return '<div class="review-item"><h4>سوال ' + (d.i + 1) +
          ' <span class="tag ' + tagClass + '">' + statusLabel + "</span></h4>" +
          "<div>" + d.q.text + "</div>" +
          '<div style="margin-top:8px;font-size:.9rem"><b>پاسخ شما:</b> ' + your + "</div>" +
          '<div style="font-size:.9rem"><b>پاسخ درست:</b> ' + right + "</div></div>"
      }).join("")
  }

  $("customCount").addEventListener("input", (e) => {
    state.customCount = Number(e.target.value) || 1
  })

  $("shuffleToggle").addEventListener("click", () => {
    state.shuffle = !state.shuffle
    $("shuffleToggle").classList.toggle("on", state.shuffle)
  })

  $("timerToggle").addEventListener("click", () => {
    state.timerOn = !state.timerOn
    $("timerToggle").classList.toggle("on", state.timerOn)
  })

  $("backHomeBtn").addEventListener("click", () => {
    show("home")
    renderHistory()
  })

  $("startBtn").addEventListener("click", () => {
    if (state.countMode === "custom") {
      state.customCount = Number($("customCount").value) || 1
    }
    buildSession()
    show("quiz")
    startTimer()
    renderQuiz()
  })

  $("prevBtn").addEventListener("click", () => {
    if (state.index > 0) {
      state.index--
      renderQuiz()
    }
  })

  $("nextBtn").addEventListener("click", () => {
    if (state.index < state.questions.length - 1) {
      state.index++
      renderQuiz()
    }
  })

  $("flagBtn").addEventListener("click", () => {
    state.flags[state.index] = !state.flags[state.index]
    renderQuiz()
  })

  $("finishBtn").addEventListener("click", () => {
    const blank = state.answers.filter((a) => a === null).length
    if (blank > 0) {
      const ok = confirm(blank + " سوال بدون پاسخ است. آزمون تمام شود؟")
      if (!ok) return
    }
    finishQuiz()
  })

  $("reviewWrongBtn").addEventListener("click", () => renderReview(true))
  $("retryBtn").addEventListener("click", () => {
    buildSession()
    show("quiz")
    startTimer()
    renderQuiz()
  })
  $("newQuizBtn").addEventListener("click", () => {
    stopTimer()
    show("home")
    renderHistory()
  })

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) return
  })

  renderHome()
})()
</script>
</body>
</html>
'''

out = html.replace("__DATA__", DATA_JS.strip())
Path(r"d:\new app\quiz\solidworks-quiz.html").write_text(out, encoding="utf-8")
Path(r"d:\new app\quiz\exams.json").write_text(json.dumps(exams, ensure_ascii=False, indent=2), encoding="utf-8")
print("exams:", [(e["id"], e["count"]) for e in exams])
print("wrote solidworks-quiz.html bytes:", len(out.encode("utf-8")))
