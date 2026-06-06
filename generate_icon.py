import os
from PIL import Image, ImageDraw

def create_visiocode_icon():
    # حجم الأيقونة الاحترافي للـ Windows Desktop
    size = (256, 256)
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 1. رسم الخلفية: مربع بحواف دائرية (Premium Dark Blue)
    top_left = (10, 10)
    bottom_right = (246, 246)
    radius = 50
    draw.rounded_rectangle([top_left, bottom_right], radius=radius, fill="#0F172A")
    
    # 2. رسم إطار خارجي مشع وخفيف (Cyan Border)
    draw.rounded_rectangle([top_left, bottom_right], radius=radius, outline="#38BDF8", width=4)
    
    # 3. رسم رمز البرمجة والرؤية الذكية (The Neon Lightning / Code Symbol)
    # إحداثيات الصاعقة المدموجة بشكل متناسق فـ السنتر
    lightning_points = [
        (140, 40),   # الرأس الفوقاني
        (75, 130),   # الانعطاف الأيسر
        (130, 130),  # المركز
        (116, 216),  # السهم التحتاني
        (181, 126),  # الانعطاف الأيمن
        (126, 126)   # العودة للمركز
    ]
    
    # رسم الصاعقة بلون زرق هربان مشع (Neon Cyan)
    draw.polygon(lightning_points, fill="#38BDF8")
    
    # 4. إضافة لمسة فنية: نقطة ذكية مشعة (AI Node)
    draw.ellipse([145, 85, 160, 100], fill="#F8FAFC", outline="#2563EB", width=2)

    # حفظ الملف بصيغة ICO الرسمية للويندوز
    icon_path = "icon.ico"
    image.save(icon_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"✨ تم بنجاح إنشاء الأيقونة الاحترافية وحفظها باسم: {os.path.abspath(icon_path)}")

if __name__ == "__main__":
    create_visiocode_icon()