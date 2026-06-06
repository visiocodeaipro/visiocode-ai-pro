import os
import time
import pyautogui
import ollama
import customtkinter as ctk
from threading import Thread
from tkinter import messagebox
from plyer import notification
from deep_translator import GoogleTranslator

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

اسم_الأداة = "Visiocode AI Pro"

class VisiocodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{اسم_الأداة} v4.7 🔥 [Multi-Model & Content Shadow Agent]")
        self.geometry("960x990") # زدنا شوية ف الطول باش يستوعب الـ Footer بـ أناقة
        self.resizable(False, False)
        self.configure(fg_color="#0F172A") 

        self.current_lang = "AR"  
        self.notifications_enabled = True  
        self.shadow_mode_enabled = False  
        self.chat_history = []
        self.current_screenshot = None

        self.translations = {
            "AR": {
                "subtitle": "أول وكيل ذكي فالعالم يربط الكود بالتسويق المحلي (Build in Public Automation)",
                "control_title": "🎯 :اختر مسار التحليل أو فعل 'الوضع الخفي' للفحص المستمر",
                "btn_ui": "📱 واجهة التطبيق UI/UX",
                "btn_code": "💻 مراجعة كود البرمجة",
                "chat_title": "💬 :نافذة المحادثة والتحليل العميق المترجم",
                "code_title": "🚀 سكريبت الفيديو التسويقي الجاهز والمخرجات السريعة:",
                "ready_status": "🟢 جاهز لبدء جلسة ذكاء اصطناعي محلي خفيف %100",
                "placeholder_input": "سول المساعد ديالك هنا... (مثلا: عاوني نزيد نطور هاد البلان)",
                "btn_send": "إرسال 🚀",
                "notif_toggle": "الإشعارات تفعيل",
                "model_lbl": "🤖 الموديل:"
            },
            "EN": {
                "subtitle": "World's 1st Code-to-Content Local Shadow Agent (Build in Public Automation)",
                "control_title": "🎯 Choose a manual path or enable 'Shadow Mode' for background auditing",
                "btn_ui": "📱 UI/UX Interface",
                "btn_code": "💻 Source Code Review",
                "chat_title": "💬 Direct Agent Chat Window:",
                "code_title": "🚀 Instant Video Script & Marketing Outputs:",
                "ready_status": "🟢 Ready for a 100% local smart session",
                "placeholder_input": "Ask your Agent here...",
                "btn_send": "Send 🚀",
                "notif_toggle": "Enable Notifications",
                "model_lbl": "🤖 Model:"
            }
        }

        self.system_prompts = {
            "UI": (
                "Act as a Senior UI/UX Engineer and Growth Hacker. Analyze this screenshot. "
                "Provide 3 specific design flaws. Then, generate an engaging 'Build in Public' "
                "social media short video script (Reel/TikTok) explaining how you are fixing this UI for your users. "
                "Structure it clearly with analysis first, then the Script."
            ),
            "CODE": (
                "Act as a Lead Software Architect. Review this source code screenshot. "
                "Provide technical feedback and performance tips. Then, generate an exciting social media Reel script "
                "under 'Build in Public' style explaining this feature to users. Structure it clearly."
            ),
            "MARKETING": (
                "Act as an expert Growth Hacker. Analyze this visual asset. "
                "Write a killer caption and viral video hook to drive immediate app installations. Structure it clearly."
            )
        }

        # ---- Top Bar ----
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.pack(pady=(15, 0), fill="x", padx=40)

        self.lang_btn = ctk.CTkButton(
            self.top_bar, text="🌐 English", width=80, height=28,
            fg_color="#334155", hover_color="#475569", font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_language
        )
        self.lang_btn.pack(side="left")

        self.model_label = ctk.CTkLabel(
            self.top_bar, text=self.translations["AR"]["model_lbl"], 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), text_color="#94A3B8"
        )
        self.model_label.pack(side="left", padx=(20, 5))

        الموديلات_المتاحة = self.get_local_ollama_models()
        self.model_selector = ctk.CTkComboBox(
            self.top_bar, values=الموديلات_المتاحة,
            width=180, height=28, fg_color="#1E293B", border_color="#334155",
            button_color="#2563EB", button_hover_color="#1D4ED8", font=ctk.CTkFont(size=12)
        )
        self.model_selector.set("moondream")
        self.model_selector.pack(side="left")

        self.shadow_switch = ctk.CTkSwitch(
            self.top_bar, text="وضع الفحص الصامت (Shadow Mode)", font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#F59E0B", progress_color="#F59E0B", command=self.toggle_shadow_mode
        )
        self.shadow_switch.pack(side="left", padx=(30, 5))

        self.notif_switch = ctk.CTkSwitch(
            self.top_bar, text="الإشعارات تفعيل", font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#94A3B8", progress_color="#38BDF8", command=self.toggle_notifications
        )
        self.notif_switch.select()  
        self.notif_switch.pack(side="right")

        # ---- Header ----
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(15, 5), fill="x", padx=40)

        self.title_label = ctk.CTkLabel(
            self.header_frame, text=f"⚡ {اسم_الأداة}", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color="#38BDF8"
        )
        self.title_label.pack(anchor="e")

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame, text=self.translations["AR"]["subtitle"], 
            font=ctk.CTkFont(family="Segoe UI", size=13), text_color="#94A3B8", justify="right"
        )
        self.subtitle_label.pack(anchor="e", pady=(5, 0))

        self.separator = ctk.CTkFrame(self, height=2, fg_color="#334155")
        self.separator.pack(fill="x", padx=40, pady=10)

        # ---- Controls ----
        self.control_label = ctk.CTkLabel(
            self, text=self.translations["AR"]["control_title"], 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color="#F8FAFC"
        )
        self.control_label.pack(anchor="e", padx=45, pady=(5, 5))

        self.button_frame = ctk.CTkFrame(self, fg_color="#1E293B", corner_radius=12, border_width=1, border_color="#334155")
        self.button_frame.pack(pady=5, fill="x", padx=40)

        btn_font = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        
        self.ui_btn = ctk.CTkButton(
            self.button_frame, text=self.translations["AR"]["btn_ui"], 
            height=50, font=btn_font, fg_color="#2563EB", hover_color="#1D4ED8",
            command=lambda: self.start_new_analysis_thread("UI")
        )
        self.ui_btn.grid(row=0, column=2, padx=10, pady=15, sticky="ew")

        self.code_btn = ctk.CTkButton(
            self.button_frame, text=self.translations["AR"]["btn_code"], 
            height=50, font=btn_font, fg_color="#0EA5E9", hover_color="#0284C7",
            command=lambda: self.start_new_analysis_thread("CODE")
        )
        self.code_btn.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        text_social_ar = "📣 السوشيل ميديا\n(FB, IG, TikTok, YT)"
        self.video_btn = ctk.CTkButton(
            self.button_frame, text=text_social_ar, 
            height=50, font=btn_font, fg_color="#10B981", hover_color="#059669",
            command=lambda: self.start_new_analysis_thread("MARKETING")
        )
        self.video_btn.grid(row=0, column=0, padx=10, pady=15, sticky="ew")

        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # ---- Status ----
        self.status_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.status_frame.pack(fill="x", padx=45, pady=3)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, text=self.translations["AR"]["ready_status"], 
            font=ctk.CTkFont(family="Segoe UI", size=12), text_color="#64748B"
        )
        self.status_label.pack(anchor="e")

        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal", height=4, progress_color="#38BDF8", fg_color="#334155")
        self.progress_bar.set(0)

        # ---- Workspace ----
        self.work_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.work_frame.pack(padx=40, fill="both", expand=True, pady=5)

        self.text_panel_left = ctk.CTkFrame(self.work_frame, fg_color="transparent")
        self.text_panel_left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.text_panel_right = ctk.CTkFrame(self.work_frame, fg_color="transparent")
        self.text_panel_right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # ---- Left Panel ----
        self.chat_title_lbl = ctk.CTkLabel(
            self.text_panel_left, text=self.translations["AR"]["chat_title"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#38BDF8"
        )
        self.chat_title_lbl.pack(anchor="e", pady=2)

        self.result_textbox = ctk.CTkTextbox(
            self.text_panel_left, font=ctk.CTkFont(family="Segoe UI", size=13), 
            text_color="#E2E8F0", fg_color="#0F172A", border_width=1, border_color="#334155", corner_radius=8
        )
        self.result_textbox.pack(fill="both", expand=True)
        self.result_textbox.insert("0.0", "اختر مساراً أو فعل الفحص الصامت المستمر للعمل فـ الخلفية... 🚀")

        # ---- Right Panel ----
        self.code_title_lbl = ctk.CTkLabel(
            self.text_panel_right, text=self.translations["AR"]["code_title"],
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color="#10B981"
        )
        self.code_title_lbl.pack(anchor="e", pady=2)

        self.code_textbox = ctk.CTkTextbox(
            self.text_panel_right, font=ctk.CTkFont(family="Segoe UI", size=13), 
            text_color="#A7F3D0", fg_color="#1E293B", border_width=1, border_color="#10B981", corner_radius=8
        )
        self.code_textbox.pack(fill="both", expand=True)
        self.code_textbox.insert("0.0", "# السكريبت التسويقي المترجم غايبان هنا نقي ديريكت...")

        # ---- Utilities ----
        self.utils_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.utils_frame.pack(fill="x", padx=40, pady=5)

        self.copy_btn = ctk.CTkButton(
            self.utils_frame, text="📋 Copy Analysis", width=120, height=28, 
            fg_color="#334155", hover_color="#475569", command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side="left", padx=5)

        self.copy_code_btn = ctk.CTkButton(
            self.utils_frame, text="⚡ Copy Video Script", width=140, height=28, 
            fg_color="#059669", hover_color="#047857", command=self.copy_code_to_clipboard
        )
        self.copy_code_btn.pack(side="left", padx=5)

        # ---- Input Box ----
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=40, pady=(10, 10))

        self.user_input = ctk.CTkEntry(
            self.input_frame, placeholder_text=self.translations["AR"]["placeholder_input"], 
            font=ctk.CTkFont(family="Segoe UI", size=13), height=40,
            fg_color="#1E293B", border_color="#334155", text_color="#F8FAFC"
        )
        self.user_input.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        self.user_input.bind("<Return>", lambda event: self.send_chat_message_thread())

        self.send_btn = ctk.CTkButton(
            self.input_frame, text=self.translations["AR"]["btn_send"], 
            width=110, height=40, font=btn_font, fg_color="#38BDF8", text_color="#0F172A", hover_color="#0EA5E9",
            command=self.send_chat_message_thread, state="disabled" 
        )
        self.send_btn.grid(row=0, column=0, sticky="w")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # ---- 👑 Official Footer Core Branding 👑 ----
        self.footer_separator = ctk.CTkFrame(self, height=1, fg_color="#1E293B")
        self.footer_separator.pack(fill="x", padx=40, pady=(5, 5))

        بصمة_المطور = (
            "Founded & Developed & Designed with ❤️ in Morocco by \"ANOUAR BOUDEHBI\"\n"
            "© 2026 Visiocode AI Pro. All rights reserved."
        )
        self.footer_label = ctk.CTkLabel(
            self, text=بصمة_المطور, 
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"), 
            text_color="#64748B", justify="center"
        )
        self.footer_label.pack(pady=(0, 15))

    def get_local_ollama_models(self):
        الاقتراحات_الأساسية = ["moondream", "llava", "bakllava", "llama3.2-vision"]
        try:
            list_data = ollama.list()
            extracted_models = []
            models_list = list_data.get('models', []) if isinstance(list_data, dict) else getattr(list_data, 'models', [])
            
            for m in models_list:
                name = m.get('name', '') if isinstance(m, dict) else getattr(m, 'name', '')
                if name:
                    clean_name = name.split(":")[0]
                    if clean_name not in extracted_models:
                        extracted_models.append(clean_name)
            
            for model in الاقتراحات_الأساسية:
                if model not in extracted_models:
                    extracted_models.append(model)
            return extracted_models
        except:
            return الاقتراحات_الأساسية

    def check_and_pull_model(self, model_name):
        self.status_label.configure(text=f"🔄 جاري التحقق من وجود الموديل [{model_name}] فـ جهازك وطبخه فـ الخلفية...", text_color="#F59E0B")
        try:
            ollama.pull(model_name)
            return True
        except Exception as e:
            print(f"Pull error: {e}")
            return True

    def toggle_language(self):
        if self.current_lang == "AR":
            self.current_lang = "EN"
            self.lang_btn.configure(text="🌐 العربية")
            self.title_label.pack(anchor="w")
            self.subtitle_label.pack(anchor="w")
            self.control_label.pack(anchor="w", padx=45)
            self.chat_title_lbl.pack(anchor="w")
            self.code_title_lbl.pack(anchor="w")
            self.status_label.pack(anchor="w")
            self.video_btn.configure(text="📣 Social Media\n(FB, IG, TikTok, YT)")
        else:
            self.current_lang = "AR"
            self.lang_btn.configure(text="🌐 English")
            self.title_label.pack(anchor="e")
            self.subtitle_label.pack(anchor="e")
            self.control_label.pack(anchor="e", padx=45)
            self.chat_title_lbl.pack(anchor="e")
            self.code_title_lbl.pack(anchor="e")
            self.status_label.pack(anchor="e")
            self.video_btn.configure(text="📣 السوشيل ميديا\n(FB, IG, TikTok, YT)")

        lang = self.current_lang
        self.subtitle_label.configure(text=self.translations[lang]["subtitle"])
        self.control_label.configure(text=self.translations[lang]["control_title"])
        self.ui_btn.configure(text=self.translations[lang]["btn_ui"])
        self.code_btn.configure(text=self.translations[lang]["btn_code"])
        self.chat_title_lbl.configure(text=self.translations[lang]["chat_title"])
        self.code_title_lbl.configure(text=self.translations[lang]["code_title"])
        self.status_label.configure(text=self.translations[lang]["ready_status"])
        self.user_input.configure(placeholder_text=self.translations[lang]["placeholder_input"])
        self.send_btn.configure(text=self.translations[lang]["btn_send"])
        self.notif_switch.configure(text=self.translations[lang]["notif_toggle"])
        self.model_label.configure(text=self.translations[lang]["model_lbl"])

    def toggle_notifications(self):
        self.notifications_enabled = self.notif_switch.get()

    def toggle_shadow_mode(self):
        self.shadow_mode_enabled = self.shadow_switch.get()
        if self.shadow_mode_enabled:
            self.status_label.configure(text="🟠 وضع Shadow Mode نشط: الأداة تفحص الشاشة صامتاً كل 30 ثانية بحثاً عن أخطاء...", text_color="#F59E0B")
            self.show_smart_notification("Shadow Mode Active", "الأداة دابا حاضية الخدمة ديالك ف الصمت!")
            Thread(target=self.shadow_auditor_loop, daemon=True).start()
        else:
            self.status_label.configure(text=self.translations[self.current_lang]["ready_status"], text_color="#64748B")

    def shadow_auditor_loop(self):
        while self.shadow_mode_enabled:
            time.sleep(30)
            if not self.shadow_mode_enabled:
                break
            
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            shadow_img = f"shadow_ctx_{timestamp}.png"
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save(shadow_img)
                
                selected_model = self.model_selector.get()
                self.check_and_pull_model(selected_model)
                
                prompt = "Analyze this workspace. If there is a noticeable UI error or bug, state it in 1 short sentence. Otherwise say CLEAR."
                response = ollama.generate(model=selected_model, prompt=prompt, images=[shadow_img])
                result = response['response'].strip()
                
                if "CLEAR" not in result.upper():
                    try: translated_error = GoogleTranslator(source='en', target='ar').translate(result)
                    except: translated_error = result
                    self.show_smart_notification("🚨 فحص تلقائي خفي", translated_error[:100])
                
                if os.path.exists(shadow_img):
                    os.remove(shadow_img)
            except:
                pass

    def show_smart_notification(self, title, message):
        if self.notifications_enabled:
            try: notification.notify(title=title, message=message, app_name=اسم_الأداة, timeout=3)
            except: pass

    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.result_textbox.get("0.0", "end").strip())
        self.show_smart_notification("Visiocode AI", "تم نسخ التقرير بنجاح 📋")

    def copy_code_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.code_textbox.get("0.0", "end").strip())
        self.show_smart_notification("Visiocode AI", "تم نسخ السكريبت التسويقي ⚡")

    def toggle_ui(self, state):
        self.ui_btn.configure(state=state)
        self.code_btn.configure(state=state)
        self.video_btn.configure(state=state)
        if state == "normal" and self.current_screenshot:
            self.send_btn.configure(state="normal")
        else:
            self.send_btn.configure(state="disabled")

    def start_new_analysis_thread(self, mode):
        Thread(target=self.run_initial_analysis, args=(mode,)).start()

    def run_initial_analysis(self, mode):
        self.toggle_ui("disabled")
        self.progress_bar.pack(fill="x", padx=45, pady=(5, 10))
        self.progress_bar.start()

        self.chat_history = []
        selected_model = self.model_selector.get()
        self.check_and_pull_model(selected_model)
        
        prompt = self.system_prompts.get(mode, self.system_prompts["UI"])

        self.withdraw()
        time.sleep(2)
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.current_screenshot = f"visiocode_ctx_{timestamp}.png"
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(self.current_screenshot)
            self.deiconify()

            response = ollama.generate(model=selected_model, prompt=prompt, images=[self.current_screenshot])
            full_response = response['response']

            analysis_parts = full_response.split("Script:") if "Script:" in full_response else full_response.split("Script")
            tech_text_en = analysis_parts[0].strip()
            script_text_en = analysis_parts[1].strip() if len(analysis_parts) > 1 else full_response

            try:
                tech_text_ar = GoogleTranslator(source='en', target='ar').translate(tech_text_en)
                script_text_ar = GoogleTranslator(source='en', target='ar').translate(script_text_en)
            except:
                tech_text_ar = tech_text_en
                script_text_ar = script_text_en

            self.chat_history.append({'role': 'assistant', 'content': full_response})
            
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("end", f"[AGENT - تحليل الديزاين والكود]:\n{tech_text_ar}\n")
            
            self.code_textbox.delete("0.0", "end")
            self.code_textbox.insert("end", f"🎬 [محتوى فيديو Build in Public واجد]:\n{script_text_ar}\n\n#توصيل_القرب #MoroccoTech #BuildInPublic")
            
            self.status_label.configure(text="🟢 تم صنع المحتوى والتحليل بنجاح واختيار الموديل ناضي!", text_color="#10B981")
            self.show_smart_notification("Visiocode AI", "🎯 السكريبت التسويقي والتحليل واجدين!")
            
        except Exception as e:
            self.deiconify()
            self.result_textbox.delete("0.0", "end")
            self.result_textbox.insert("0.0", f"🚨 Error: {e}")
            self.status_label.configure(text="❌ فشل التحليل الفوري.", text_color="#EF4444")
            self.current_screenshot = None
            
        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.toggle_ui("normal")

    def send_chat_message_thread(self):
        msg = self.user_input.get().strip()
        if not msg or self.ui_btn.cget("state") == "disabled":
            return
        Thread(target=self.process_chat_turn, args=(msg,)).start()

    def process_chat_turn(self, user_msg):
        self.toggle_ui("disabled")
        self.user_input.delete(0, "end")
        self.progress_bar.pack(fill="x", padx=45, pady=(5, 10))
        self.progress_bar.start()

        self.result_textbox.insert("end", f"\n[YOU]: {user_msg}\n\n")
        self.result_textbox.see("end")

        try:
            translated_user_msg = GoogleTranslator(source='auto', target='en').translate(user_msg)
        except:
            translated_user_msg = user_msg

        self.chat_history.append({'role': 'user', 'content': translated_user_msg})
        selected_model = self.model_selector.get()

        try:
            response = ollama.chat(model=selected_model, messages=self.chat_history)
            agent_reply = response['message']['content']
            self.chat_history.append({'role': 'assistant', 'content': agent_reply})
            
            try: translated_agent_reply = GoogleTranslator(source='en', target='ar').translate(agent_reply)
            except: translated_agent_reply = agent_reply
            
            self.result_textbox.insert("end", f"[AGENT]:\n{translated_agent_reply}\n\n" + "-"*40 + "\n")
            self.result_textbox.see("end")
            self.status_label.configure(text="🟢 جاهز لمتابعة الأفكار بالترجمة الذكية...", text_color="#10B981")
            
        except Exception as e:
            self.result_textbox.insert("end", f"🚨 خطأ أثناء المحادثة: {e}\n\n")
            
        finally:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
            self.toggle_ui("normal")

    def __del__(self):
        if self.current_screenshot and os.path.exists(self.current_screenshot):
            try: os.remove(self.current_screenshot)
            except: pass

if __name__ == "__main__":
    app = VisiocodeApp()
    app.mainloop()