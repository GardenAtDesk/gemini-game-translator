import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import tkinter.ttk as tk_ttk
import threading
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import GenerationConfig, HarmCategory, HarmBlockThreshold
import re
import os
import json
import csv
import sys
import math
import time

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
except ImportError:
    import tkinter.ttk as ttk

# --- [修复] 路径处理逻辑：兼容 Script 和 PyInstaller EXE ---
if getattr(sys, 'frozen', False):
    # 如果是打包后的 exe，使用 exe 所在的真实路径
    application_path = os.path.dirname(sys.executable)
else:
    # 如果是脚本运行，使用脚本所在的路径
    application_path = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(application_path, "config_v7.json")
# --------------------------------------------------------

PAGE_SIZE = 50 

DEFAULT_MODELS = [
    "models/gemini-2.0-flash-lite-preview-02-05",
    "models/gemini-2.0-flash-lite",
    "models/gemini-1.5-flash",
    "models/gemini-1.5-flash-latest",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-pro-latest",
]

TARGET_LANGS = [
    "English", "Simplified Chinese", "Traditional Chinese", "Japanese", 
    "Korean", "Russian", "French", "German", "Spanish", "Portuguese", 
    "Italian", "Other (Manual Input)"
]

UI_TEXTS = {
    "en": {
        "title": "Game Translator Helper v7.6.1 (Width Check + Bugfix)",
        "api_key": "API Key:",
        "model_std": "Std Model:",
        "model_adv": "Adv Model:",
        "check_models": "🔍 Detect Models",
        "ui_lang": "UI Lang:",
        "target_lang": "Target Lang:",
        "custom_lang_ph": "Enter Language...",
        "load_csv": "1. Load Source",
        "import_trans": "📂 Import Trans", 
        "export_csv": "2. Export CSV",
        "ready": "Ready",
        "source_col": "Source (Original)",
        "target_col": "Target (Translation)",
        "copy": "Copy",
        "paste": "Paste (Replace)", 
        "copy_src": "⬇️ Copy Source",
        "clean": "🧹 Clean Breaks",
        "insert_br": "⤵️ Insert Break",
        "prev": "<< Prev", 
        "next": "Next >>", 
        "save_only": "💾 Save Line",
        "retry_std": "✨ Retry (Std)",
        "retry_adv": "🚀 Retry (Adv)",
        "save_next": "✅ Save & Next",
        "auto_trans": "⚡ Auto Next", 
        "safe_exit": "🚪 Safe Exit",
        "save_all": "💾 FORCE SAVE ALL", 
        "instr_title": "📢 Custom Instructions (Prompt)",
        "glossary_title": "Glossary (Term=Trans)",
        "btn_add": "+",
        "btn_update": "Update", 
        "btn_del": "Del",
        "btn_export": "Export",
        "btn_import": "Import",
        "regex_title": "Regex Protection",
        "settings_title": "⚙️ Settings",
        "cost_title": "💰 Cost Monitor (Est.)", 
        "price_std": "Std ($/1M In/Out):", 
        "price_adv": "Adv ($/1M In/Out):", 
        "total_cost": "Est. Total: $",
        "cost_note": "*Ref only. Input vs Output prices differ.",
        "safety_unlock": "Unlock Safety Filters (Risk)",
        "newline_symbol": "Newline Code:",
        "status_s": "St",
        "preview": "Source Preview",
        "idx": "#",
        "lines": "Lines: ",
        "msg_model_ok": "Success! Found {} available models.\nAuto-selected the best ones.",
        "msg_model_err": "Failed to fetch models.\nCheck API Key or Network.",
        "warn_safety_title": "⚠️ Security Warning",
        "warn_safety_msg": "Are you sure you want to disable safety filters?\n\nThis will bypass Google's blocking of Harassment, Hate Speech, and Violence.\n\nUse at your own risk. This may violate Google's Terms of Service.",
        "config_err": "Config file corrupted or missing.\nSettings reset to defaults.",
        "btn_batch": "✨ Translate Page",
        "btn_stop": "🛑 Stop Batch",
        "batch_done": "Batch Complete!\nSuccess: {}\nFailed: {}", 
        "ctx_copy_source": "📄 Copy Source Text (Selected)",
        "batch_progress": "Translating... ({}/{})", 
        "err_api": "❌ API Key Error",
        "err_429": "⏳ Rate Limit (429). Waiting...",
        "err_net": "🌐 Network Error",
        "err_gen": "❌ Error",
        "qa_btn": "🔍 Visual QA (Editor)",
        "qa_title": "Interactive Visual Editor",
        "qa_width": "Width(px):",
        "qa_lines": "MaxLines:",
        "qa_font": "Font:",
        "qa_msg_ok": "✅ Safe: {} lines",
        "qa_msg_err": "⚠️ Overflow: {} / {} lines",
        "qa_msg_wide": "⚠️ Width Warning: Target is wider than Source!",
        "import_msg": "Success! Imported {} translations.\nProgress has been SAVED to disk.",
        "save_all_msg": "All progress saved to:\n{}"
    },
    "zh": {
        "title": "游戏文本翻译助手 v7.6.1 (横向爆框检测 + Bug修复)",
        "api_key": "API 密钥:",
        "model_std": "常用模型:",
        "model_adv": "高级模型:",
        "check_models": "🔍 检测模型",
        "ui_lang": "界面语言:",
        "target_lang": "目标语言:",
        "custom_lang_ph": "手动输入语言...",
        "load_csv": "1. 加载源文件",
        "import_trans": "📂 导入译文", 
        "export_csv": "2. 导出成品",
        "ready": "就绪",
        "source_col": "原文 (Source)",
        "target_col": "译文 (Target)",
        "copy": "复制",
        "paste": "粘贴 (覆盖)", 
        "copy_src": "⬇️ 照搬原文",
        "clean": "🧹 清除换行",
        "insert_br": "⤵️ 插入换行",
        "prev": "<< 上一句", 
        "next": "下一句 >>", 
        "save_only": "💾 保存当前行",
        "retry_std": "✨ 普通重翻",
        "retry_adv": "🚀 高级重翻",
        "save_next": "✅ 保存并下一句",
        "auto_trans": "⚡ 自动翻下一句", 
        "safe_exit": "🚪 安全退出",
        "save_all": "💾 全局强制保存", 
        "instr_title": "📢 额外指令 (Prompt)",
        "glossary_title": "术语表 (原文=译文)",
        "btn_add": "+",
        "btn_update": "更新", 
        "btn_del": "删除",
        "btn_export": "导出",
        "btn_import": "导入",
        "regex_title": "代码保护 (正则)",
        "settings_title": "⚙️ 高级设置",
        "cost_title": "💰 成本估算 (仅供参考)", 
        "price_std": "常用 ($/百万 输入/输出):", 
        "price_adv": "高级 ($/百万 输入/输出):", 
        "total_cost": "预估花费: $",
        "cost_note": "*价格分开计算。In=输入, Out=输出。",
        "safety_unlock": "解锁安全限制 (慎用)",
        "newline_symbol": "换行符代码:",
        "status_s": "状态",
        "preview": "原文预览",
        "idx": "序号",
        "lines": "行数: ",
        "msg_model_ok": "检测成功！\n发现 {} 个可用模型。\n已自动为您优选最佳模型。",
        "msg_model_err": "检测失败。\n请检查 API Key 或网络连接。",
        "warn_safety_title": "⚠️ 安全警告",
        "warn_safety_msg": "确定要关闭安全过滤吗？\n\n这将绕过 Google 对骚扰、仇恨言论及暴力内容的拦截。\n\n请自行承担风险，这可能违反 Google 的服务条款 (ToS)。",
        "config_err": "配置文件损坏或丢失。\n已重置为默认设置。",
        "btn_batch": "✨ 翻译当前页",
        "btn_stop": "🛑 停止批量",
        "batch_done": "本页批量翻译完成！\n成功: {}\n失败: {}", 
        "ctx_copy_source": "📄 复制选中行原文",
        "batch_progress": "批量翻译中... ({}/{})", 
        "err_api": "❌ API Key 错误",
        "err_429": "⏳ 调用太快 (429)，稍候...",
        "err_net": "🌐 网络连接失败",
        "err_gen": "❌ 翻译失败",
        "qa_btn": "🔍 Visual QA (编辑器)",
        "qa_title": "交互式 UI 检视器",
        "qa_width": "宽度(px):",
        "qa_lines": "最大行数:",
        "qa_font": "字号:",
        "qa_msg_ok": "✅ 正常: {} 行",
        "qa_msg_err": "⚠️ 纵向爆框: {} / {} 行",
        "qa_msg_wide": "⚠️ 横向警告: 译文比原文更宽，可能超出！",
        "import_msg": "导入成功！\n共匹配更新了 {} 条译文。\n所有进度已自动保存到硬盘✅",
        "save_all_msg": "所有进度已强制保存至:\n{}"
    },
    "ja": {
        "title": "ゲームテキスト翻訳アシスタント v7.6.1 (Width Check + Bugfix)",
        "api_key": "APIキー:",
        "model_std": "通常モデル:",
        "model_adv": "高度モデル:",
        "check_models": "🔍 モデル確認",
        "ui_lang": "表示言語:",
        "target_lang": "翻訳先言語:",
        "custom_lang_ph": "言語を入力...",
        "load_csv": "1. CSV読込",
        "import_trans": "📂 訳文取込", 
        "export_csv": "2. CSV出力",
        "ready": "準備完了",
        "source_col": "原文 (Source)",
        "target_col": "訳文 (Target)",
        "copy": "コピー",
        "paste": "貼り付け", 
        "copy_src": "⬇️ 原文コピー",
        "clean": "🧹 改行削除",
        "insert_br": "⤵️ 改行挿入",
        "prev": "<< 前へ", 
        "next": "次へ >>", 
        "save_only": "💾 行を保存",
        "retry_std": "✨ 再翻訳 (通常)",
        "retry_adv": "🚀 再翻訳 (高度)",
        "save_next": "✅ 保存して次へ",
        "auto_trans": "⚡ 次行を自動翻訳", 
        "safe_exit": "🚪 安全終了",
        "save_all": "💾 全保存 (強制)", 
        "instr_title": "📢 追加指示 (Prompt)",
        "glossary_title": "用語集 (原文=訳文)",
        "btn_add": "+",
        "btn_update": "更新", 
        "btn_del": "削除",
        "btn_export": "出力",
        "btn_import": "取込",
        "regex_title": "コード保護 (Regex)",
        "settings_title": "⚙️ 高度な設定",
        "cost_title": "💰 コスト見積 (参考)", 
        "price_std": "通常 ($/100万 In/Out):", 
        "price_adv": "高度 ($/100万 In/Out):", 
        "total_cost": "推定費用: $",
        "cost_note": "*In=入力, Out=出力。価格は異なります。",
        "safety_unlock": "セーフティ解除 (注意)",
        "newline_symbol": "改行コード:",
        "status_s": "状態",
        "preview": "プレビュー",
        "idx": "No.",
        "lines": "行数: ",
        "msg_model_ok": "成功！\n利用可能なモデルが {} 個見つかりました。\n最適なモデルを自動選択しました。",
        "msg_model_err": "取得失敗。\nAPIキーまたはネットワークを確認してください。",
        "warn_safety_title": "⚠️ セキュリティ警告",
        "warn_safety_msg": "本当にセーフティフィルタを無効にしますか？\n\nこれにより、ハラスメント、ヘイトスピーチ、暴力表現のブロックが無効化されます。\n\n自己責任で使用してください。利用規約に違反する可能性があります。",
        "config_err": "設定ファイルが破損しているか見つかりません。\n初期設定にリセットしました。",
        "btn_batch": "✨ ページ一括翻訳",
        "btn_stop": "🛑 停止",
        "batch_done": "完了！\n成功: {}\n失敗: {}", 
        "ctx_copy_source": "📄 選択行の原文をコピー",
        "batch_progress": "翻訳中... ({}/{})", 
        "err_api": "❌ APIキー エラー",
        "err_429": "⏳ 制限超過 (429)、待機中...",
        "err_net": "🌐 ネットワークエラー",
        "err_gen": "❌ エラー",
        "qa_btn": "🔍 Visual QA (エディタ)",
        "qa_title": "インタラクティブ UI エディタ",
        "qa_width": "幅 (px):",
        "qa_lines": "最大行数:",
        "qa_font": "フォント:",
        "qa_msg_ok": "✅ 正常: {} 行",
        "qa_msg_err": "⚠️ オーバーフロー: {} / {} 行",
        "qa_msg_wide": "⚠️ 幅警告: 訳文が原文より幅広です！",
        "import_msg": "インポート成功！\n{} 件の翻訳を更新し、保存しました。",
        "save_all_msg": "全データを保存しました:\n{}"
    }
}

# --- Visual QA Window Class (v7.6 Width Check) ---
class VisualQAWindow(tk.Toplevel):
    def __init__(self, master_widget, app_instance, ui_lang="en"):
        super().__init__(master_widget)
        self.app = app_instance 
        self.current_ui_lang = ui_lang
        self.current_prefix = "" 
        t = UI_TEXTS[self.current_ui_lang]
        
        self.title(t["qa_title"])
        self.geometry("650x650") # Slightly taller for warning msg
        self.attributes('-topmost', True) 
        
        # 1. Settings Bar
        ctrl_frame = ttk.Frame(self, padding=10)
        ctrl_frame.pack(fill=tk.X)
        
        ttk.Label(ctrl_frame, text=t["qa_width"]).pack(side=tk.LEFT)
        self.spin_width = ttk.Spinbox(ctrl_frame, from_=100, to=2000, width=5, command=self.update_layout)
        self.spin_width.set(400)
        self.spin_width.pack(side=tk.LEFT, padx=5)
        self.spin_width.bind("<Return>", lambda e: self.update_layout())
        
        ttk.Label(ctrl_frame, text=t["qa_lines"]).pack(side=tk.LEFT, padx=(10, 0))
        self.spin_lines = ttk.Spinbox(ctrl_frame, from_=1, to=50, width=3, command=self.update_layout)
        self.spin_lines.set(3)
        self.spin_lines.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(ctrl_frame, text=t["qa_font"]).pack(side=tk.LEFT, padx=(10, 0))
        self.spin_font = ttk.Spinbox(ctrl_frame, from_=8, to=72, width=3, command=self.update_layout)
        self.spin_font.set(12)
        self.spin_font.pack(side=tk.LEFT, padx=5)

        # 2. Main Canvas Area
        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas_frame = tk.Frame(self.main_frame, bg="#333333") 
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Container
        self.box_container = tk.Frame(self.canvas_frame, bg="#333333")
        self.box_container.pack(pady=20, fill=tk.NONE, expand=False)
        self.box_container.pack_propagate(False) 
        
        # Elements
        self.lbl_src = tk.Label(self.box_container, text="Source", fg="#aaaaaa", bg="#333333", font=("Arial", 9, "bold"))
        self.lbl_tgt = tk.Label(self.box_container, text="Target (EDITABLE)", fg="white", bg="#333333", font=("Arial", 9, "bold"))
        
        self.txt_source = tk.Text(self.box_container, height=4, bg="#e0e0e0", wrap=tk.WORD, bd=0, padx=5, pady=5)
        self.txt_source.config(state="disabled") 
        
        self.txt_target = tk.Text(self.box_container, height=4, bg="white", wrap=tk.WORD, bd=0, padx=5, pady=5)
        self.txt_target.bind("<KeyRelease>", self.on_target_edit)
        
        # 3. Bottom Navigation
        nav_frame = ttk.Frame(self, padding=10)
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.btn_prev = ttk.Button(nav_frame, text="<< Prev", command=self.app.go_prev_pure)
        self.btn_prev.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        # Save button in the middle
        self.btn_save_qa = ttk.Button(nav_frame, text="💾 Save", command=self.manual_save_notify, bootstyle="success")
        self.btn_save_qa.pack(side=tk.LEFT, padx=5)
        
        self.lbl_status = ttk.Label(nav_frame, text="Ready", anchor="center", width=40) # Wider for warning
        self.lbl_status.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.btn_next = ttk.Button(nav_frame, text="Next >>", command=self.app.go_next_pure)
        self.btn_next.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        try:
            self.btn_prev.configure(bootstyle="secondary")
            self.btn_next.configure(bootstyle="secondary")
            self.lbl_status.configure(bootstyle="inverse-dark")
        except: pass
        
        self.update_layout()

    def manual_save_notify(self):
        # Trigger force save on main app
        self.app.manual_force_save(silent=True)
        self.lbl_status.configure(text="Saved ✅", bootstyle="success")
        self.app.root.after(1500, self.check_overflow) # Restore status after 1.5s

    def update_content(self, src, dst, prefix=""):
        self.current_prefix = prefix
        
        self.txt_source.config(state="normal")
        self.txt_source.delete("1.0", tk.END)
        self.txt_source.insert("1.0", src)
        self.txt_source.config(state="disabled")
        
        if self.focus_get() != self.txt_target:
            self.txt_target.delete("1.0", tk.END)
            self.txt_target.insert("1.0", dst)
            self.check_overflow()

    def on_target_edit(self, event=None):
        try:
            qa_text = self.txt_target.get("1.0", tk.END).strip()
            nl_code = self.app.newline_symbol_var.get()
            if nl_code:
                # v7.6.1: 改进 - 处理所有类型的换行符
                text_for_save = qa_text.replace("\r\n", nl_code).replace("\r", nl_code).replace("\n", nl_code)
            else:
                text_for_save = qa_text
                
            full_text = self.current_prefix + text_for_save
            self.app.receive_qa_update(full_text)
            self.check_overflow()
        except Exception as e:
            print(f"Sync error: {e}")

    def update_layout(self):
        try:
            f_size = int(self.spin_font.get())
            max_l = int(self.spin_lines.get())
            w_px = int(self.spin_width.get())
            
            new_font = font.Font(family="Microsoft YaHei", size=f_size)
            self.txt_source.config(font=new_font)
            self.txt_target.config(font=new_font)
            
            line_h = int(f_size * 1.6) 
            box_h = (line_h * max_l) + 10 
            
            lbl_h = 20
            gap = 5
            y_pos = 0
            
            self.lbl_src.place(x=0, y=y_pos)
            y_pos += lbl_h + gap
            self.txt_source.place(x=0, y=y_pos, width=w_px, height=box_h)
            y_pos += box_h + 15 
            
            self.lbl_tgt.place(x=0, y=y_pos)
            y_pos += lbl_h + gap
            self.txt_target.place(x=0, y=y_pos, width=w_px, height=box_h)
            y_pos += box_h
            
            self.box_container.config(width=w_px, height=y_pos + 10)
            self.check_overflow()
        except: pass

    # Helper: Get max visual width of text (pixel based)
    def get_max_line_width(self, text_widget):
        try:
            content = text_widget.get("1.0", tk.END).strip()
            if not content: return 0
            
            # v7.6.1: 添加字体fallback
            try:
                f = font.Font(font=text_widget['font'])
            except:
                # Fallback to default font if widget font fails
                f = font.Font(family="Microsoft YaHei", size=12)
                
            lines = content.split('\n')
            max_w = 0
            for line in lines:
                w = f.measure(line)
                if w > max_w: max_w = w
            return max_w
        except Exception as e:
            print(f"Font measure error: {e}")
            return 0

    def check_overflow(self):
        try:
            # 1. Check Vertical Overflow (Lines)
            lines = self.txt_target.count("1.0", "end", "displaylines")
            if lines is None: lines = 1
            else: lines = int(lines[0]) if isinstance(lines, tuple) else int(lines)
            
            max_l = int(self.spin_lines.get())
            t = UI_TEXTS[self.current_ui_lang]
            
            # 2. Check Horizontal Overflow (Width vs Source)
            w_src = self.get_max_line_width(self.txt_source)
            w_tgt = self.get_max_line_width(self.txt_target)
            
            is_wider = w_tgt > w_src
            is_taller = lines > max_l
            
            if is_taller:
                # Priority 1: Vertical Overflow (Red)
                self.txt_target.configure(bg="#ffcccc") # Red
                try: self.lbl_status.configure(text=t["qa_msg_err"].format(lines, max_l), bootstyle="danger")
                except: self.lbl_status.configure(text=t["qa_msg_err"].format(lines, max_l), fg="red")
            
            elif is_wider:
                # Priority 2: Horizontal Width Warning (Pink/Orange)
                self.txt_target.configure(bg="#ffe5e5") # Light Pink
                try: self.lbl_status.configure(text=t["qa_msg_wide"], bootstyle="warning")
                except: self.lbl_status.configure(text=t["qa_msg_wide"], fg="orange")
                
            else:
                # All Good (Green)
                self.txt_target.configure(bg="white")
                try: self.lbl_status.configure(text=t["qa_msg_ok"].format(lines), bootstyle="success")
                except: self.lbl_status.configure(text=t["qa_msg_ok"].format(lines), fg="green")
        except: pass


# --- Main Application ---
class GameTranslatorEditor:
    def __init__(self, root):
        self.root = root
        self.current_ui_lang = "en"
        self.ui_elements = {}
        
        self.root.title(UI_TEXTS[self.current_ui_lang]["title"])
        self.root.geometry("1600x1000")
        
        self.api_key_var = tk.StringVar()
        self.model_std_var = tk.StringVar()
        self.model_adv_var = tk.StringVar()
        self.source_file_path = tk.StringVar()
        
        self.ui_lang_var = tk.StringVar(value="English")
        self.target_lang_var = tk.StringVar()
        self.custom_target_lang_var = tk.StringVar()
        
        self.safety_unlock_var = tk.BooleanVar(value=False)
        self.newline_symbol_var = tk.StringVar(value="{换行}")
        self.auto_translate_next_var = tk.BooleanVar(value=False)
        
        self.price_std_in_var = tk.DoubleVar(value=0.075) 
        self.price_std_out_var = tk.DoubleVar(value=0.30)
        self.price_adv_in_var = tk.DoubleVar(value=3.50)
        self.price_adv_out_var = tk.DoubleVar(value=10.50)
        
        self.tokens_std_in = 0
        self.tokens_std_out = 0
        self.tokens_adv_in = 0
        self.tokens_adv_out = 0
        
        self.est_cost_var = tk.StringVar(value="0.0000")
        
        self.data_list = [] 
        self.total_rows = 0
        self.current_index = -1 
        self.current_page = 0
        self.total_pages = 0
        
        self.glossary_data = [] 
        self.regex_data = []
        self.working_csv = "" 
        self.final_csv = ""
        
        self.is_batch_running = False
        self.preview_window = None 
        
        self._create_ui()
        self.load_config()
        self.update_ui_text()
        self.update_cost_display() 
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _create_ui(self):
        # Top Bar
        top_bar = ttk.Frame(self.root, padding=5)
        top_bar.pack(fill=tk.X)
        
        row1 = ttk.Frame(top_bar)
        row1.pack(fill=tk.X, pady=2)
        
        self.ui_elements["lbl_api"] = ttk.Label(row1, text="")
        self.ui_elements["lbl_api"].pack(side=tk.LEFT)
        ttk.Entry(row1, textvariable=self.api_key_var, width=12, show="*").pack(side=tk.LEFT, padx=5)
        
        self.ui_elements["lbl_std"] = ttk.Label(row1, text="", bootstyle="info")
        self.ui_elements["lbl_std"].pack(side=tk.LEFT, padx=5)
        self.combo_std = ttk.Combobox(row1, textvariable=self.model_std_var, values=DEFAULT_MODELS, width=22)
        self.combo_std.pack(side=tk.LEFT)
        
        self.ui_elements["lbl_adv"] = ttk.Label(row1, text="", bootstyle="warning")
        self.ui_elements["lbl_adv"].pack(side=tk.LEFT, padx=5)
        self.combo_adv = ttk.Combobox(row1, textvariable=self.model_adv_var, values=DEFAULT_MODELS, width=22)
        self.combo_adv.pack(side=tk.LEFT)
        
        self.ui_elements["btn_check_models"] = ttk.Button(row1, text="", command=self.check_models, style="Outline.TButton", width=20)
        self.ui_elements["btn_check_models"].pack(side=tk.LEFT, padx=10)
        
        self.ui_elements["lbl_ui_lang"] = ttk.Label(row1, text="")
        self.ui_elements["lbl_ui_lang"].pack(side=tk.LEFT, padx=(15, 5))
        self.combo_ui_lang = ttk.Combobox(row1, textvariable=self.ui_lang_var, values=["English", "中文", "日本語"], width=8, state="readonly")
        self.combo_ui_lang.pack(side=tk.LEFT)
        self.combo_ui_lang.bind("<<ComboboxSelected>>", self.on_ui_lang_change)

        row2 = ttk.Frame(top_bar)
        row2.pack(fill=tk.X, pady=5)
        
        self.ui_elements["lbl_target"] = ttk.Label(row2, text="", bootstyle="success")
        self.ui_elements["lbl_target"].pack(side=tk.LEFT)
        self.combo_lang = ttk.Combobox(row2, textvariable=self.target_lang_var, values=TARGET_LANGS, width=20, state="readonly")
        self.combo_lang.pack(side=tk.LEFT, padx=5)
        self.combo_lang.current(0)
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_target_lang_change)
        
        self.entry_custom_lang = ttk.Entry(row2, textvariable=self.custom_target_lang_var, width=15)
        
        ttk.Label(row2, text="|").pack(side=tk.LEFT, padx=10)
        self.ui_elements["btn_load"] = ttk.Button(row2, text="", command=self.load_source_file_fast, bootstyle="primary")
        self.ui_elements["btn_load"].pack(side=tk.LEFT, padx=5)
        
        self.ui_elements["btn_import_trans"] = ttk.Button(row2, text="", command=self.import_translations_csv, bootstyle="secondary-outline")
        self.ui_elements["btn_import_trans"].pack(side=tk.LEFT, padx=5)
        
        self.ui_elements["btn_export"] = ttk.Button(row2, text="", command=self.export_final_csv, bootstyle="info")
        self.ui_elements["btn_export"].pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(row2, text="", font=("Arial", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # === Main ===
        self.paned = tk_ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left
        left_frame = ttk.Frame(self.paned, padding=5)
        self.paned.add(left_frame, weight=1)

        columns = ("idx", "status", "preview")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("idx", text="#")
        self.tree.heading("status", text="St")
        self.tree.heading("preview", text="Preview")
        self.tree.column("idx", width=40)
        self.tree.column("status", width=40)
        self.tree.column("preview", width=350) 
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-3>", self.show_tree_context_menu)
        self.tree.bind("<Button-2>", self.show_tree_context_menu)

        page_ctrl = ttk.Frame(left_frame, padding=5)
        page_ctrl.pack(side=tk.BOTTOM, fill=tk.X)
        self.ui_elements["btn_prev"] = ttk.Button(page_ctrl, text="<", width=3, command=self.prev_page)
        self.ui_elements["btn_prev"].pack(side=tk.LEFT)
        self.lbl_page = ttk.Label(page_ctrl, text="0 / 0", width=10, anchor="center")
        self.lbl_page.pack(side=tk.LEFT, padx=5)
        self.ui_elements["btn_next"] = ttk.Button(page_ctrl, text=">", width=3, command=self.next_page)
        self.ui_elements["btn_next"].pack(side=tk.LEFT)
        
        jump_frame = ttk.Frame(left_frame, padding=5)
        jump_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.entry_jump = ttk.Entry(jump_frame, width=6)
        self.entry_jump.pack(side=tk.LEFT)
        ttk.Button(jump_frame, text="Go", command=self.jump_to_line_btn, style="Outline.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(jump_frame, text="Next", command=self.jump_to_first_pending, bootstyle="warning").pack(side=tk.RIGHT)

        # Center
        center_frame = ttk.Frame(self.paned, padding=10)
        self.paned.add(center_frame, weight=4)

        lbl_src = ttk.Frame(center_frame)
        lbl_src.pack(fill=tk.X)
        self.ui_elements["lbl_src_title"] = ttk.Label(lbl_src, text="", bootstyle="info", font=("Arial", 12, "bold"))
        self.ui_elements["lbl_src_title"].pack(side=tk.LEFT)
        self.lbl_count_a = ttk.Label(lbl_src, text="Lines: 0", font=("Arial", 10), bootstyle="secondary")
        self.lbl_count_a.pack(side=tk.LEFT, padx=15)
        self.ui_elements["btn_copy1"] = ttk.Button(lbl_src, text="", command=lambda: self.copy_text(self.txt_original), style="link")
        self.ui_elements["btn_copy1"].pack(side=tk.RIGHT)
        
        self.txt_original = tk.Text(center_frame, height=6, font=("Microsoft YaHei", 12), bg="#f5f5f5", wrap=tk.WORD)
        self.txt_original.pack(fill=tk.X, pady=(0, 15))
        
        lbl_dst_row = ttk.Frame(center_frame)
        lbl_dst_row.pack(fill=tk.X)
        self.ui_elements["lbl_dst_title"] = ttk.Label(lbl_dst_row, text="", bootstyle="success", font=("Arial", 12, "bold"))
        self.ui_elements["lbl_dst_title"].pack(side=tk.LEFT)
        self.lbl_count_b = ttk.Label(lbl_dst_row, text="Lines: 0", font=("Arial", 10), bootstyle="success")
        self.lbl_count_b.pack(side=tk.LEFT, padx=15)

        tools_row = ttk.Frame(center_frame, padding=(0, 2))
        tools_row.pack(fill=tk.X)
        
        self.ui_elements["btn_copy_src"] = ttk.Button(tools_row, text="", command=self.copy_source_to_target, bootstyle="primary-outline")
        self.ui_elements["btn_copy_src"].pack(side=tk.LEFT, padx=2)
        self.ui_elements["btn_clean"] = ttk.Button(tools_row, text="", command=self.clean_line_breaks, style="secondary-link")
        self.ui_elements["btn_clean"].pack(side=tk.LEFT, padx=2)
        self.ui_elements["btn_br"] = ttk.Button(tools_row, text="", command=self.insert_line_break, style="secondary-outline")
        self.ui_elements["btn_br"].pack(side=tk.LEFT, padx=2)
        
        self.ui_elements["btn_paste"] = ttk.Button(tools_row, text="", command=self.paste_to_target, style="link")
        self.ui_elements["btn_paste"].pack(side=tk.RIGHT, padx=2)
        self.ui_elements["btn_copy2"] = ttk.Button(tools_row, text="", command=lambda: self.copy_text(self.txt_trans), style="link")
        self.ui_elements["btn_copy2"].pack(side=tk.RIGHT, padx=2)

        self.txt_trans = tk.Text(center_frame, height=6, font=("Microsoft YaHei", 12), wrap=tk.WORD, spacing1=5, spacing2=2)
        self.txt_trans.pack(fill=tk.X, pady=(0, 15))
        self.txt_trans.bind("<KeyRelease>", self.update_line_counts)
        self.txt_trans.bind("<Control-Return>", lambda e: self.insert_line_break())
        self.txt_trans.bind("<Control-v>", lambda e: self.paste_replace())
        self.txt_trans.bind("<Control-V>", lambda e: self.paste_replace())
        self.txt_trans.bind("<Control-Shift-V>", lambda e: self.paste_insert())
        self.txt_trans.bind("<Control-Shift-v>", lambda e: self.paste_insert())

        ctrl_frame = ttk.Labelframe(center_frame, text="Console", padding=15)
        ctrl_frame.pack(fill=tk.X, pady=10)
        
        row_batch = ttk.Frame(ctrl_frame)
        row_batch.pack(fill=tk.X, pady=(0, 5))
        self.ui_elements["btn_batch"] = ttk.Button(row_batch, text="", command=self.start_batch_page, bootstyle="primary")
        self.ui_elements["btn_batch"].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.ui_elements["btn_stop"] = ttk.Button(row_batch, text="", command=self.stop_batch, bootstyle="danger", state="disabled")
        self.ui_elements["btn_stop"].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        row_nav = ttk.Frame(ctrl_frame)
        row_nav.pack(fill=tk.X, pady=2)
        self.ui_elements["btn_prev"] = ttk.Button(row_nav, text="", command=self.go_prev_pure, bootstyle="secondary-outline")
        self.ui_elements["btn_prev"].pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.ui_elements["btn_qa"] = ttk.Button(row_nav, text="🔍 Visual QA", command=self.toggle_qa_window, bootstyle="info")
        self.ui_elements["btn_qa"].pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.ui_elements["btn_next"] = ttk.Button(row_nav, text="", command=self.go_next_pure, bootstyle="secondary-outline")
        self.ui_elements["btn_next"].pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        row_act = ttk.Frame(ctrl_frame)
        row_act.pack(fill=tk.X, pady=5)
        self.ui_elements["btn_save"] = ttk.Button(row_act, text="", command=self.save_current_stay, bootstyle="info-outline")
        self.ui_elements["btn_save"].pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.ui_elements["btn_retry_std"] = ttk.Button(row_act, text="", command=self.retry_std, bootstyle="secondary")
        self.ui_elements["btn_retry_std"].pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        self.ui_elements["btn_retry_adv"] = ttk.Button(row_act, text="", command=self.retry_adv, bootstyle="warning")
        self.ui_elements["btn_retry_adv"].pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)

        row_main = ttk.Frame(ctrl_frame)
        row_main.pack(fill=tk.X, pady=5)
        self.ui_elements["btn_save_next"] = ttk.Button(row_main, text="", command=self.save_and_go_next, bootstyle="success")
        self.ui_elements["btn_save_next"].pack(fill=tk.X, padx=5)
        
        self.ui_elements["chk_auto_trans"] = ttk.Checkbutton(row_main, text="", variable=self.auto_translate_next_var, bootstyle="square-toggle")
        self.ui_elements["chk_auto_trans"].pack(fill=tk.X, padx=5, pady=2)

        row_exit = ttk.Frame(ctrl_frame)
        row_exit.pack(fill=tk.X, pady=(15, 0))
        self.ui_elements["btn_save_all"] = ttk.Button(row_exit, text="", command=self.manual_force_save, bootstyle="warning-outline", width=15)
        self.ui_elements["btn_save_all"].pack(side=tk.LEFT, padx=5)
        
        self.ui_elements["btn_exit"] = ttk.Button(row_exit, text="", command=self.save_and_exit_app, bootstyle="danger-link")
        self.ui_elements["btn_exit"].pack(side=tk.RIGHT)

        # Right
        right_frame = ttk.Frame(self.paned, padding=5)
        self.paned.add(right_frame, weight=2)

        self.ui_elements["frame_cost"] = ttk.Labelframe(right_frame, text="", padding=5, bootstyle="info")
        self.ui_elements["frame_cost"].pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        c_row1 = ttk.Frame(self.ui_elements["frame_cost"])
        c_row1.pack(fill=tk.X, pady=2)
        self.ui_elements["lbl_price_std"] = ttk.Label(c_row1, text="Std(In/Out):")
        self.ui_elements["lbl_price_std"].pack(side=tk.LEFT)
        ttk.Entry(c_row1, textvariable=self.price_std_out_var, width=5).pack(side=tk.RIGHT)
        ttk.Label(c_row1, text="/").pack(side=tk.RIGHT, padx=2)
        ttk.Entry(c_row1, textvariable=self.price_std_in_var, width=5).pack(side=tk.RIGHT)
        
        c_row2 = ttk.Frame(self.ui_elements["frame_cost"])
        c_row2.pack(fill=tk.X, pady=2)
        self.ui_elements["lbl_price_adv"] = ttk.Label(c_row2, text="Adv(In/Out):")
        self.ui_elements["lbl_price_adv"].pack(side=tk.LEFT)
        ttk.Entry(c_row2, textvariable=self.price_adv_out_var, width=5).pack(side=tk.RIGHT)
        ttk.Label(c_row2, text="/").pack(side=tk.RIGHT, padx=2)
        ttk.Entry(c_row2, textvariable=self.price_adv_in_var, width=5).pack(side=tk.RIGHT)
        
        c_row3 = ttk.Frame(self.ui_elements["frame_cost"])
        c_row3.pack(fill=tk.X, pady=5)
        self.ui_elements["lbl_total_cost"] = ttk.Label(c_row3, text="Total: $", font=("Arial", 10, "bold"))
        self.ui_elements["lbl_total_cost"].pack(side=tk.LEFT)
        ttk.Label(c_row3, textvariable=self.est_cost_var, font=("Arial", 10, "bold"), bootstyle="success").pack(side=tk.LEFT)
        self.ui_elements["lbl_cost_note"] = ttk.Label(self.ui_elements["frame_cost"], text="*Ref only", font=("Arial", 7), bootstyle="secondary")
        self.ui_elements["lbl_cost_note"].pack(anchor=tk.W)
        self.price_std_in_var.trace_add("write", lambda *args: self.update_cost_display())
        self.price_std_out_var.trace_add("write", lambda *args: self.update_cost_display())
        self.price_adv_in_var.trace_add("write", lambda *args: self.update_cost_display())
        self.price_adv_out_var.trace_add("write", lambda *args: self.update_cost_display())

        self.ui_elements["frame_settings"] = ttk.Labelframe(right_frame, text="", padding=5, bootstyle="secondary")
        self.ui_elements["frame_settings"].pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        nl_frame = ttk.Frame(self.ui_elements["frame_settings"])
        nl_frame.pack(fill=tk.X, pady=2)
        self.ui_elements["lbl_newline"] = ttk.Label(nl_frame, text="Newline:")
        self.ui_elements["lbl_newline"].pack(side=tk.LEFT)
        ttk.Entry(nl_frame, textvariable=self.newline_symbol_var, width=10).pack(side=tk.LEFT, padx=5)
        self.ui_elements["chk_safety"] = ttk.Checkbutton(
            self.ui_elements["frame_settings"], 
            text="", 
            variable=self.safety_unlock_var, 
            bootstyle="round-toggle",
            command=self.on_safety_toggle 
        )
        self.ui_elements["chk_safety"].pack(fill=tk.X, pady=5)

        self.ui_elements["frame_instr"] = ttk.Labelframe(right_frame, text="", padding=5, bootstyle="warning")
        self.ui_elements["frame_instr"].pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        self.txt_instruction = tk.Text(self.ui_elements["frame_instr"], height=4, font=("Microsoft YaHei", 9), wrap=tk.WORD)
        self.txt_instruction.pack(fill=tk.X, pady=5)
        self.txt_instruction.bind("<FocusIn>", self._clear_placeholder)

        self.ui_elements["frame_gloss"] = ttk.Labelframe(right_frame, text="", padding=5)
        self.ui_elements["frame_gloss"].pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(0, 10))
        g_input = ttk.Frame(self.ui_elements["frame_gloss"])
        g_input.pack(fill=tk.X)
        self.entry_g_src = ttk.Entry(g_input, width=10)
        self.entry_g_src.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(g_input, text="=").pack(side=tk.LEFT)
        self.entry_g_dst = ttk.Entry(g_input, width=10)
        self.entry_g_dst.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ui_elements["btn_g_add"] = ttk.Button(g_input, text="+", width=2, command=self.add_glossary)
        self.ui_elements["btn_g_add"].pack(side=tk.LEFT, padx=2)
        self.glossary_listbox = tk.Listbox(self.ui_elements["frame_gloss"], height=6)
        self.glossary_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.glossary_listbox.bind("<<ListboxSelect>>", self.on_glossary_select)
        g_btn = ttk.Frame(self.ui_elements["frame_gloss"])
        g_btn.pack(fill=tk.X)
        self.ui_elements["btn_g_del"] = ttk.Button(g_btn, text="", command=self.del_glossary, style="danger-link")
        self.ui_elements["btn_g_del"].pack(side=tk.LEFT)
        self.ui_elements["btn_g_upd"] = ttk.Button(g_btn, text="", command=self.update_glossary, style="success-outline", width=6)
        self.ui_elements["btn_g_upd"].pack(side=tk.LEFT, padx=5)
        self.ui_elements["btn_g_exp"] = ttk.Button(g_btn, text="", command=self.export_glossary, style="outline")
        self.ui_elements["btn_g_exp"].pack(side=tk.RIGHT, padx=2)
        self.ui_elements["btn_g_imp"] = ttk.Button(g_btn, text="", command=self.import_glossary, style="outline")
        self.ui_elements["btn_g_imp"].pack(side=tk.RIGHT, padx=2)

        self.ui_elements["frame_regex"] = ttk.Labelframe(right_frame, text="", padding=5)
        self.ui_elements["frame_regex"].pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        r_input = ttk.Frame(self.ui_elements["frame_regex"])
        r_input.pack(fill=tk.X)
        self.entry_regex = ttk.Entry(r_input)
        self.entry_regex.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ui_elements["btn_r_add"] = ttk.Button(r_input, text="+", width=2, command=self.add_regex)
        self.ui_elements["btn_r_add"].pack(side=tk.LEFT, padx=2)
        self.regex_listbox = tk.Listbox(self.ui_elements["frame_regex"], height=5)
        self.regex_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.regex_listbox.bind("<<ListboxSelect>>", self.on_regex_select)
        r_btn = ttk.Frame(self.ui_elements["frame_regex"])
        r_btn.pack(fill=tk.X)
        self.ui_elements["btn_r_del"] = ttk.Button(r_btn, text="", command=self.del_regex, style="danger-link")
        self.ui_elements["btn_r_del"].pack(side=tk.LEFT)
        self.ui_elements["btn_r_upd"] = ttk.Button(r_btn, text="", command=self.update_regex, style="success-outline", width=6)
        self.ui_elements["btn_r_upd"].pack(side=tk.LEFT, padx=5)
        self.ui_elements["btn_r_exp"] = ttk.Button(r_btn, text="", command=self.export_regex, style="outline")
        self.ui_elements["btn_r_exp"].pack(side=tk.RIGHT, padx=2)
        self.ui_elements["btn_r_imp"] = ttk.Button(r_btn, text="", command=self.import_regex, style="outline")
        self.ui_elements["btn_r_imp"].pack(side=tk.RIGHT, padx=2)

        self.tree_menu = tk.Menu(self.root, tearoff=0)
        self.tree_menu.add_command(label="Copy Source", command=self.copy_selected_tree_source)

    # --- QA Logic (Fixed v7.5.1) ---
    def toggle_qa_window(self):
        if self.preview_window is None or not tk.Toplevel.winfo_exists(self.preview_window):
            self.preview_window = VisualQAWindow(self.root, self, self.current_ui_lang)
            self.sync_qa_content()
        else:
            self.preview_window.lift()

    def sync_qa_content(self):
        if self.preview_window is None or not tk.Toplevel.winfo_exists(self.preview_window):
            return
        
        try:
            src = self.txt_original.get("1.0", tk.END).strip()
            dst = self.txt_trans.get("1.0", tk.END).strip()
            
            prefix_src = self._extract_prefix(src)
            prefix_dst = ""
            
            if prefix_src and src.startswith(prefix_src):
                src = src[len(prefix_src):]
            
            raw_prefix_dst = self._extract_prefix(dst)
            if raw_prefix_dst and dst.startswith(raw_prefix_dst):
                prefix_dst = raw_prefix_dst
                dst = dst[len(raw_prefix_dst):]
            elif prefix_src: 
                prefix_dst = prefix_src
                
            nl_code = self.newline_symbol_var.get()
            if nl_code:
                src = src.replace(nl_code, "\n")
                dst = dst.replace(nl_code, "\n")

            self.preview_window.update_content(src, dst, prefix_dst)
        except: pass

    # Callback for QA window
    def receive_qa_update(self, full_text):
        self.txt_trans.delete("1.0", tk.END)
        self.txt_trans.insert("1.0", full_text)
        self.update_line_counts() 
        self.save_current_row_memory() 

    def manual_force_save(self, silent=False):
        if not self.working_csv: return
        self.force_save_all_progress()
        if not silent:
            t = UI_TEXTS[self.current_ui_lang]
            msg = t.get("save_all_msg", "Saved to:\n{}").format(os.path.basename(self.working_csv))
            messagebox.showinfo("Saved", msg)

    # --- UI Logic ---

    def on_ui_lang_change(self, event=None):
        sel = self.combo_ui_lang.get()
        if sel == "中文": self.current_ui_lang = "zh"
        elif sel == "日本語": self.current_ui_lang = "ja"
        else: self.current_ui_lang = "en"
        self.update_ui_text()

    def update_ui_text(self):
        t = UI_TEXTS[self.current_ui_lang]
        self.root.title(t["title"])
        self.ui_elements["lbl_api"].config(text=t["api_key"])
        self.ui_elements["lbl_std"].config(text=t["model_std"])
        self.ui_elements["lbl_adv"].config(text=t["model_adv"])
        self.ui_elements["btn_check_models"].config(text=t["check_models"])
        self.ui_elements["lbl_ui_lang"].config(text=t["ui_lang"])
        self.ui_elements["lbl_target"].config(text=t["target_lang"])
        self.ui_elements["btn_load"].config(text=t["load_csv"])
        self.ui_elements["btn_import_trans"].config(text=t.get("import_trans", "Import Trans")) 
        self.ui_elements["btn_export"].config(text=t["export_csv"])
        self.status_label.config(text=t["ready"])
        
        self.ui_elements["lbl_src_title"].config(text=t["source_col"])
        self.ui_elements["lbl_dst_title"].config(text=t["target_col"])
        self.ui_elements["btn_copy1"].config(text=t["copy"])
        self.ui_elements["btn_copy2"].config(text=t["copy"])
        self.ui_elements["btn_copy_src"].config(text=t["copy_src"])
        self.ui_elements["btn_clean"].config(text=t["clean"])
        self.ui_elements["btn_br"].config(text=t["insert_br"])
        self.ui_elements["btn_paste"].config(text=t["paste"])
        
        self.ui_elements["btn_batch"].config(text=t["btn_batch"])
        self.ui_elements["btn_stop"].config(text=t["btn_stop"])
        
        self.ui_elements["btn_prev"].config(text=t["prev"])
        self.ui_elements["btn_next"].config(text=t["next"])
        self.ui_elements["btn_save"].config(text=t["save_only"])
        self.ui_elements["btn_retry_std"].config(text=t["retry_std"])
        self.ui_elements["btn_retry_adv"].config(text=t["retry_adv"])
        self.ui_elements["btn_save_next"].config(text=t["save_next"])
        self.ui_elements["chk_auto_trans"].config(text=t["auto_trans"])
        self.ui_elements["btn_exit"].config(text=t["safe_exit"])
        self.ui_elements["btn_save_all"].config(text=t.get("save_all", "SAVE ALL"))
        
        self.ui_elements["frame_instr"].config(text=t["instr_title"])
        self.ui_elements["frame_gloss"].config(text=t["glossary_title"])
        self.ui_elements["frame_regex"].config(text=t["regex_title"])
        self.ui_elements["frame_settings"].config(text=t["settings_title"])
        
        self.ui_elements["btn_g_add"].config(text=t["btn_add"])
        self.ui_elements["btn_g_del"].config(text=t["btn_del"])
        self.ui_elements["btn_g_upd"].config(text=t["btn_update"])
        self.ui_elements["btn_g_exp"].config(text=t["btn_export"])
        self.ui_elements["btn_g_imp"].config(text=t["btn_import"])
        
        self.ui_elements["btn_r_add"].config(text=t["btn_add"])
        self.ui_elements["btn_r_del"].config(text=t["btn_del"])
        self.ui_elements["btn_r_upd"].config(text=t["btn_update"])
        self.ui_elements["btn_r_exp"].config(text=t["btn_export"])
        self.ui_elements["btn_r_imp"].config(text=t["btn_import"])
        
        self.ui_elements["chk_safety"].config(text=t["safety_unlock"])
        self.ui_elements["lbl_newline"].config(text=t["newline_symbol"])
        
        self.ui_elements["frame_cost"].config(text=t["cost_title"])
        self.ui_elements["lbl_price_std"].config(text=t["price_std"])
        self.ui_elements["lbl_price_adv"].config(text=t["price_adv"])
        self.ui_elements["lbl_total_cost"].config(text=t["total_cost"])
        self.ui_elements["lbl_cost_note"].config(text=t["cost_note"])
        
        self.ui_elements["btn_qa"].config(text=t["qa_btn"])
        
        self.tree_menu.entryconfig(0, label=t["ctx_copy_source"])
        
        self.tree.heading("status", text=t["status_s"])
        self.tree.heading("preview", text=t["preview"])
        self.tree.heading("idx", text=t["idx"])
        self.update_line_counts()

    def on_safety_toggle(self):
        if self.safety_unlock_var.get():
            t = UI_TEXTS[self.current_ui_lang]
            warn_title = t.get("warn_safety_title", "Warning")
            warn_msg = t.get("warn_safety_msg", "Use at own risk.")
            confirm = messagebox.askyesno(warn_title, warn_msg, icon='warning', default='no')
            if not confirm:
                self.safety_unlock_var.set(False)

    def on_target_lang_change(self, event=None):
        val = self.target_lang_var.get()
        if "Other" in val:
            self.entry_custom_lang.pack(side=tk.LEFT, padx=5)
        else:
            self.entry_custom_lang.pack_forget()

    # --- Core Helpers ---
    
    def _clear_placeholder(self, event):
        current = self.txt_instruction.get("1.0", tk.END).strip()
        if "(" in current and ")" in current: self.txt_instruction.delete("1.0", tk.END)

    def copy_source_to_target(self):
        try:
            src_text = self.txt_original.get("1.0", tk.END).strip()
            self.txt_trans.delete("1.0", tk.END)
            self.txt_trans.insert("1.0", src_text)
            self.update_line_counts()
        except: pass

    # Paste Replace
    def paste_to_target(self):
        self.paste_replace()

    def paste_replace(self):
        try:
            clipboard = self.root.clipboard_get()
            self.txt_trans.delete("1.0", tk.END)
            self.txt_trans.insert("1.0", clipboard)
            self.update_line_counts()
            return "break"
        except: pass

    def paste_insert(self):
        try:
            clipboard = self.root.clipboard_get()
            self.txt_trans.insert(tk.INSERT, clipboard)
            self.update_line_counts()
            return "break"
        except: pass

    def update_line_counts(self, event=None):
        try:
            newline_code = self.newline_symbol_var.get()
            text_a = self.txt_original.get("1.0", tk.END)
            text_b = self.txt_trans.get("1.0", tk.END)
            count_a = text_a.count(newline_code)
            count_b = text_b.count(newline_code)
            
            prefix = UI_TEXTS[self.current_ui_lang]["lines"]
            self.lbl_count_a.config(text=f"{prefix}{count_a}")
            self.lbl_count_b.config(text=f"{prefix}{count_b}")
            
            if count_b > count_a: self.lbl_count_b.config(bootstyle="danger")
            else: self.lbl_count_b.config(bootstyle="success")
            
            # Sync QA
            if self.preview_window and self.preview_window.winfo_exists():
                self.sync_qa_content()
                
        except: pass

    def insert_line_break(self):
        try:
            code = self.newline_symbol_var.get()
            self.txt_trans.insert(tk.INSERT, code)
            self.txt_trans.focus_set()
            self.update_line_counts() 
            return "break" 
        except: pass

    def clean_line_breaks(self):
        try:
            code = self.newline_symbol_var.get()
            current = self.txt_trans.get("1.0", tk.END).strip()
            if not current: return
            cleaned = current.replace(code, "")
            self.txt_trans.delete("1.0", tk.END)
            self.txt_trans.insert("1.0", cleaned)
            self.update_line_counts()
        except: pass

    def load_source_file_fast(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path: return
        self.source_file_path.set(path)
        self.save_config()
        self.status_label.config(text="Loading...")
        threading.Thread(target=self._background_loader, args=(path,), daemon=True).start()

    def _background_loader(self, path):
        try:
            base_name = os.path.splitext(path)[0]
            self.working_csv = f"{base_name}_working_progress.csv"
            self.final_csv = f"{base_name}_final_export.csv"
            try: df = pd.read_csv(path, header=None, encoding='utf-8-sig')
            except: df = pd.read_csv(path, header=None, encoding='gbk')
            self.total_rows = len(df)
            saved_map = {}
            if os.path.exists(self.working_csv):
                try:
                    with open(self.working_csv, 'r', encoding='utf-8-sig') as f:
                        reader = csv.reader(f)
                        for row in reader:
                            if len(row) >= 3: saved_map[int(row[0])] = row[2]
                except: pass
            temp_list = []
            for idx, row in df.iterrows():
                raw = str(row[0]) if pd.notna(row[0]) else ""
                clean_raw = raw.strip()
                status = 0
                trans = ""
                if not clean_raw: status = 2; trans = raw
                if idx in saved_map: trans = saved_map[idx]; status = 1
                temp_list.append({"orig": raw, "trans": trans, "status": status, "prefix": self._extract_prefix(raw)})
            self.data_list = temp_list
            self.total_pages = math.ceil(self.total_rows / PAGE_SIZE)
            self.root.after(0, lambda: self.go_to_page(0))
            self.root.after(0, lambda: self.status_label.config(text=f"Rows: {self.total_rows}"))
            self.root.after(0, self.jump_to_first_pending)
        except Exception as e: self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

    # --- v7.3 Import + v7.4 AutoSave ---
    def import_translations_csv(self):
        if not self.data_list:
            messagebox.showwarning("Warning", "Please load a source file first.")
            return
            
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path: return
        
        try:
            try: df = pd.read_csv(path, header=None, encoding='utf-8-sig')
            except: df = pd.read_csv(path, header=None, encoding='gbk')
            
            trans_map = {}
            count = 0
            skipped_rows = 0  # v7.6.1: 新增 - 跳过的行数
            cols = len(df.columns)
            
            for row_num, row in df.iterrows():
                src = ""
                tgt = ""
                
                if cols >= 2:
                    if pd.notna(row[0]) and pd.notna(row[1]):
                        src = str(row[0]).strip()
                        tgt = str(row[1])
                        
                    if cols >= 3 and pd.notna(row[1]) and pd.notna(row[2]):
                         try:
                             int(row[0])
                             src = str(row[1]).strip()
                             tgt = str(row[2])
                         except:
                             skipped_rows += 1  # v7.6.1: 记录跳过
                             print(f"Skipped row {row_num}: first column not numeric")
                             pass 
                
                if src and tgt:
                    trans_map[src] = tgt

            for item in self.data_list:
                s_text = item["orig"].strip()
                if s_text in trans_map:
                    item["trans"] = trans_map[s_text]
                    item["status"] = 1 
                    count += 1
                    
            # v7.4 AUTO SAVE TRIGGER
            self.force_save_all_progress()
            
            self.go_to_page(self.current_page)
            t = UI_TEXTS[self.current_ui_lang]
            msg = t.get("import_msg", "Imported {}").format(count)
            
            # v7.6.1: 如果有跳过的行，提示用户
            if skipped_rows > 0:
                msg += f"\n\nNote: {skipped_rows} rows were skipped (invalid format)"
            
            messagebox.showinfo("Success", msg)
            
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

    # --- v7.4 Force Save All ---
    def force_save_all_progress(self):
        if not self.working_csv: return
        try:
            # Re-write the entire working csv with current in-memory status
            with open(self.working_csv, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                for i, item in enumerate(self.data_list):
                    if item["status"] == 1:
                        # Format: idx, orig, trans
                        writer.writerow([i, item["orig"], item["trans"]])
        except Exception as e:
            print(f"Auto-save failed: {e}")

    def go_to_page(self, page_num):
        if page_num < 0: page_num = 0
        if page_num >= self.total_pages: page_num = self.total_pages - 1
        self.current_page = page_num
        self.lbl_page.config(text=f"{self.current_page + 1} / {self.total_pages}")
        self.tree.delete(*self.tree.get_children())
        start_idx = page_num * PAGE_SIZE
        end_idx = min(start_idx + PAGE_SIZE, self.total_rows)
        for i in range(start_idx, end_idx):
            item = self.data_list[i]
            preview = item["orig"].strip()[:25].replace('\n', ' ') 
            icon = "⚪"
            if item["status"] == 1: icon = "✅"
            elif item["status"] == 2: icon = "🚫"
            self.tree.insert("", tk.END, iid=str(i), values=(i+1, icon, preview))

    def prev_page(self): self.go_to_page(self.current_page - 1)
    def next_page(self): self.go_to_page(self.current_page + 1)
    def jump_to_line_btn(self):
        try:
            line = int(self.entry_jump.get()) - 1
            if 0 <= line < self.total_rows: self.jump_to_line(line)
        except: pass

    def jump_to_line(self, line_idx):
        target_page = line_idx // PAGE_SIZE
        self.go_to_page(target_page)
        self.tree.selection_set(str(line_idx))
        self.tree.see(str(line_idx))
        self.load_row_to_editor(line_idx)

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if sel: self.load_row_to_editor(int(sel[0]))

    def show_tree_context_menu(self, event):
        try:
            self.tree_menu.post(event.x_root, event.y_root)
        except: pass

    def copy_selected_tree_source(self):
        try:
            selected_items = self.tree.selection()
            if not selected_items: return
            text_to_copy = []
            for item_id in selected_items:
                idx = int(item_id) # item_id is str(index)
                if 0 <= idx < len(self.data_list):
                    text_to_copy.append(self.data_list[idx]["orig"])
            
            final_str = "\n".join(text_to_copy)
            self.root.clipboard_clear()
            self.root.clipboard_append(final_str)
        except: pass

    def load_row_to_editor(self, idx):
        self.current_index = idx
        data = self.data_list[idx]
        self.txt_original.config(state='normal')
        self.txt_original.delete("1.0", tk.END)
        self.txt_original.insert("1.0", data["orig"])
        self.txt_original.config(state='disabled')
        self.txt_trans.delete("1.0", tk.END)
        if data["status"] == 1: self.txt_trans.insert("1.0", data["trans"])
        elif data["status"] == 2: self.txt_trans.insert("1.0", data["orig"])
        else:
            self.txt_trans.insert("1.0", "")

        self.root.after(10, self.update_line_counts)

    def save_current_row_memory(self):
        if self.current_index < 0: return
        current_trans = self.txt_trans.get("1.0", tk.END).strip()
        current_orig = self.data_list[self.current_index]["orig"]
        self.data_list[self.current_index]["trans"] = current_trans
        self.data_list[self.current_index]["status"] = 1
        if self.tree.exists(str(self.current_index)):
            self.tree.item(str(self.current_index), values=(self.current_index+1, "✅", current_orig[:25]))
        self.append_row_to_disk(self.current_index, current_orig, current_trans)

    def save_current_stay(self):
        self.save_current_row_memory()
        self.status_label.config(text="Saved ✅")
        
    def save_and_exit_app(self):
        if self.current_index >= 0: self.save_current_row_memory()
        self.save_config()
        if messagebox.askyesno("Confirm", "Quit now?"): self.root.destroy()

    def go_next_pure(self):
        next_idx = self.current_index + 1
        while next_idx < self.total_rows:
            if self.data_list[next_idx]["status"] != 2: self.jump_to_line(next_idx); return
            next_idx += 1
        messagebox.showinfo("Info", "End of file.")

    def go_prev_pure(self):
        prev_idx = self.current_index - 1
        while prev_idx >= 0:
            if self.data_list[prev_idx]["status"] != 2: self.jump_to_line(prev_idx); return
            prev_idx -= 1
        messagebox.showinfo("Info", "Start of file.")

    def save_and_go_next(self):
        self.save_current_row_memory()
        self.go_next_pure()
        # 800ms auto translate check
        if self.auto_translate_next_var.get() and self.current_index >= 0:
            item = self.data_list[self.current_index]
            if item["status"] == 0: 
                self.root.after(800, lambda: self.fetch_ai(item["orig"], self.current_index, self.model_std_var.get()))

    def jump_to_first_pending(self):
        for i in range(self.total_rows):
            if self.data_list[i]["status"] == 0: self.jump_to_line(i); return
        messagebox.showinfo("Info", "All Done!")

    def _extract_prefix(self, text):
        match = re.match(r"^([0-9A-Za-z_\-\.]+,\d+,)(.*)$", text)
        if match: return match.group(1)
        return ""

    def append_row_to_disk(self, idx, orig, trans):
        """v7.6.1: 改进版 - 避免重复写入"""
        if not self.working_csv: return
        try:
            # 读取现有数据
            existing_data = {}
            if os.path.exists(self.working_csv):
                with open(self.working_csv, 'r', encoding='utf-8-sig') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 3:
                            existing_data[int(row[0])] = (row[1], row[2])
            
            # 更新当前行
            existing_data[idx] = (orig, trans)
            
            # 重新写入
            with open(self.working_csv, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                for i in sorted(existing_data.keys()):
                    writer.writerow([i, existing_data[i][0], existing_data[i][1]])
        except Exception as e:
            print(f"Save error: {e}")

    def export_final_csv(self):
        if not self.data_list: return
        try:
            export_data = []
            for item in self.data_list: export_data.append([item["orig"], item["trans"]])
            df = pd.DataFrame(export_data)
            df.to_csv(self.final_csv, index=False, header=False, encoding='utf-8-sig')
            messagebox.showinfo("Export", f"File saved:\n{self.final_csv}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def refresh_glossary_ui(self):
        self.glossary_listbox.delete(0, tk.END)
        for s, d in self.glossary_data: self.glossary_listbox.insert(tk.END, f"{s} = {d}")
    def add_glossary(self):
        src = self.entry_g_src.get().strip(); dst = self.entry_g_dst.get().strip()
        if src and dst:
            self.glossary_data.append((src, dst))
            self.entry_g_src.delete(0, tk.END); self.entry_g_dst.delete(0, tk.END)
            self.refresh_glossary_ui(); self.save_config()
    def del_glossary(self):
        sel = self.glossary_listbox.curselection()
        if sel: del self.glossary_data[sel[0]]; self.refresh_glossary_ui(); self.save_config()
    
    def on_glossary_select(self, event):
        sel = self.glossary_listbox.curselection()
        if sel:
            idx = sel[0]
            src, dst = self.glossary_data[idx]
            self.entry_g_src.delete(0, tk.END); self.entry_g_src.insert(0, src)
            self.entry_g_dst.delete(0, tk.END); self.entry_g_dst.insert(0, dst)
    def update_glossary(self):
        sel = self.glossary_listbox.curselection()
        src = self.entry_g_src.get().strip(); dst = self.entry_g_dst.get().strip()
        if sel and src and dst:
            idx = sel[0]
            self.glossary_data[idx] = (src, dst)
            self.refresh_glossary_ui(); self.save_config()

    def import_glossary(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path:
            try:
                df = pd.read_csv(path, header=None)
                for _, row in df.iterrows():
                    if pd.notna(row[0]) and pd.notna(row[1]): self.glossary_data.append((str(row[0]), str(row[1])))
                self.refresh_glossary_ui(); self.save_config(); messagebox.showinfo("OK", "Done")
            except Exception as e: messagebox.showerror("Error", str(e))
    def export_glossary(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            try: pd.DataFrame(self.glossary_data).to_csv(path, header=False, index=False, encoding='utf-8-sig'); messagebox.showinfo("OK", "Done")
            except Exception as e: messagebox.showerror("Error", str(e))

    def refresh_regex_ui(self):
        self.regex_listbox.delete(0, tk.END)
        for r in self.regex_data: self.regex_listbox.insert(tk.END, r)
    def add_regex(self):
        reg = self.entry_regex.get().strip()
        if reg and reg not in self.regex_data: self.regex_data.append(reg); self.entry_regex.delete(0, tk.END); self.refresh_regex_ui(); self.save_config()
    def del_regex(self):
        sel = self.regex_listbox.curselection()
        if sel: del self.regex_data[sel[0]]; self.refresh_regex_ui(); self.save_config()
    
    def on_regex_select(self, event):
        sel = self.regex_listbox.curselection()
        if sel:
            idx = sel[0]
            self.entry_regex.delete(0, tk.END)
            self.entry_regex.insert(0, self.regex_data[idx])
    def update_regex(self):
        sel = self.regex_listbox.curselection()
        reg = self.entry_regex.get().strip()
        if sel and reg:
            idx = sel[0]
            self.regex_data[idx] = reg
            self.refresh_regex_ui(); self.save_config()

    def import_regex(self):
        path = filedialog.askopenfilename(filetypes=[("Text", "*.txt")])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                        r = line.strip()
                        if r and r not in self.regex_data: self.regex_data.append(r)
                self.refresh_regex_ui(); self.save_config(); messagebox.showinfo("OK", "Done")
            except Exception as e: messagebox.showerror("Error", str(e))
    def export_regex(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text", "*.txt")])
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    for r in self.regex_data: f.write(r + '\n')
                messagebox.showinfo("OK", "Done")
            except Exception as e: messagebox.showerror("Error", str(e))

    # --- AI Core ---

    def check_models(self):
        k = self.api_key_var.get()
        if not k:
            messagebox.showwarning("Warning", "Please enter API Key first.")
            return
        
        self.ui_elements["btn_check_models"].config(text="Checking...", state="disabled")
        threading.Thread(target=self._fetch_models, args=(k,), daemon=True).start()

    def _fetch_models(self, key):
        try:
            genai.configure(api_key=key)
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            if not models:
                self.root.after(0, lambda: messagebox.showwarning("No Models", "No models found for this API Key."))
            else:
                combined = list(set(DEFAULT_MODELS + models))
                combined.sort(key=lambda x: (not "2.0-flash-lite" in x, x)) 
                
                self.root.after(0, lambda: self.combo_std.config(values=combined))
                self.root.after(0, lambda: self.combo_adv.config(values=combined))
                
                current_std = self.model_std_var.get()
                if not current_std or current_std not in combined:
                    self.root.after(0, lambda: self.model_std_var.set(combined[0]))
                    
                msg = UI_TEXTS[self.current_ui_lang]["msg_model_ok"].format(len(models))
                self.root.after(0, lambda: messagebox.showinfo("OK", msg))

        except Exception as e:
            err_msg = UI_TEXTS[self.current_ui_lang]["msg_model_err"] + f"\n({str(e)})"
            self.root.after(0, lambda: messagebox.showerror("Error", err_msg))
        finally:
            default_text = UI_TEXTS[self.current_ui_lang]["check_models"]
            self.root.after(0, lambda: self.ui_elements["btn_check_models"].config(text=default_text, state="normal"))

    # Batch Logic
    def start_batch_page(self):
        if self.is_batch_running: return
        self.is_batch_running = True
        
        self.auto_translate_next_var.set(False) # 防呆
        
        self.ui_elements["btn_batch"].config(state="disabled")
        self.ui_elements["btn_stop"].config(state="normal")
        threading.Thread(target=self._run_batch, daemon=True).start()

    def stop_batch(self):
        self.is_batch_running = False
        self.ui_elements["btn_stop"].config(state="disabled")
        self.ui_elements["btn_batch"].config(state="normal")

    def _run_batch(self):
        start_idx = self.current_page * PAGE_SIZE
        end_idx = min(start_idx + PAGE_SIZE, self.total_rows)
        
        pending_indices = []
        for i in range(start_idx, end_idx):
            if self.data_list[i]["status"] == 0:
                pending_indices.append(i)
        
        total_tasks = len(pending_indices)
        if total_tasks == 0:
            self.root.after(0, self.stop_batch)
            self.root.after(0, lambda: messagebox.showinfo("Info", "Page already translated!"))
            return

        success_count = 0
        
        for count, idx in enumerate(pending_indices):
            if not self.is_batch_running: break
            
            # Progress
            prog_txt = UI_TEXTS[self.current_ui_lang]["batch_progress"].format(count+1, total_tasks)
            self.root.after(0, lambda p=prog_txt: self.status_label.config(text=p))
            
            # Rate Limit control
            last_call = time.time()
            
            text = self.data_list[idx]["orig"]
            # Sync call
            success = self._fetch_ai_sync_batch(text, idx, self.model_std_var.get())
            if success: success_count += 1
            
            # 4s rule
            elapsed = time.time() - last_call
            wait_time = max(0, 4.0 - elapsed)
            time.sleep(wait_time)
        
        self.root.after(0, self.stop_batch)
        if self.is_batch_running:
            done_msg = UI_TEXTS[self.current_ui_lang]["batch_done"].format(success_count, total_tasks - success_count)
            self.root.after(0, lambda: messagebox.showinfo("Report", done_msg))
            self.root.after(0, lambda: self.status_label.config(text="Batch Finished"))

    # Batch Sync Logic
    def _fetch_ai_sync_batch(self, text, target_idx, specific_model):
        """v7.6.1: 添加429错误重试逻辑"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                prefix = self.data_list[target_idx]["prefix"]
                content = text[len(prefix):] if prefix and text.startswith(prefix) else text
                if not content.strip(): return True

                genai.configure(api_key=self.api_key_var.get())
                model_name = specific_model if specific_model else self.model_std_var.get()
                model = genai.GenerativeModel(model_name)
                
                safety_settings = None
                if self.safety_unlock_var.get():
                    safety_settings = {
                        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    }

                config = GenerationConfig(temperature=0.0)
                glossary_text = "\n".join([f"{src}={dst}" for src, dst in self.glossary_data])
                extra_inst = self.txt_instruction.get("1.0", tk.END).strip()
                if "(" in extra_inst and ")" in extra_inst: extra_inst = ""
                
                target_lang = self.target_lang_var.get()
                if "Other" in target_lang:
                    target_lang = self.custom_target_lang_var.get() or "English"
                newline_code = self.newline_symbol_var.get()

                base_prompt = f"""You are a professional game localization machine.
TASK: Translate the source text into [{target_lang}].
RULES:
1. If text is in [{target_lang}], output AS IS.
2. Translate if NOT in [{target_lang}].
3. Keep symbols (like {newline_code}) exactly.
4. Output ONLY translation.
"""
                extra_prompt_part = ""
                if extra_inst: extra_prompt_part = f"\n[INSTRUCTIONS]:\n{extra_inst}\n"
                prompt = f"{base_prompt}{extra_prompt_part}\n[GLOSSARY]:\n{glossary_text}\n[SOURCE]:\n{content}"
                
                response = model.generate_content(prompt, generation_config=config, safety_settings=safety_settings)
                final = prefix + response.text.strip()
                
                # Track Cost
                self._track_tokens(response, model_name)
                
                # Silent Update
                self.root.after(0, lambda: self._update_batch_result(final, target_idx))
                return True
                
            except Exception as e:
                err = str(e)
                t = UI_TEXTS[self.current_ui_lang]
                err_ui = t["err_gen"]
                
                # v7.6.1: 检测429错误并重试
                if "429" in err:
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 15 * retry_count  # 递增等待时间
                        print(f"Rate limit hit, waiting {wait_time}s before retry {retry_count}/{max_retries}")
                        time.sleep(wait_time)
                        continue  # 重试
                    else:
                        err_ui = t["err_429"]
                elif "API key" in err:
                    err_ui = t["err_api"]
                
                self.root.after(0, lambda: self._update_batch_result(f"[{err_ui}]", target_idx))
                return False
        
        return False

    def _update_batch_result(self, text, idx):
        self.data_list[idx]["trans"] = text
        self.data_list[idx]["status"] = 1
        
        if self.tree.exists(str(idx)):
            preview = self.data_list[idx]["orig"].strip()[:25].replace('\n', ' ')
            self.tree.item(str(idx), values=(idx+1, "✅", preview))
            
        if self.current_index == idx:
            self.txt_trans.delete("1.0", tk.END)
            self.txt_trans.insert("1.0", text)
            self.update_line_counts()
        
        self.append_row_to_disk(idx, self.data_list[idx]["orig"], text)

    # --- Standard AI (Single) ---
    def _fetch_ai_sync(self, text, target_idx, specific_model):
        try:
            prefix = self.data_list[target_idx]["prefix"]
            content = text[len(prefix):] if prefix and text.startswith(prefix) else text
            if not content.strip(): return

            genai.configure(api_key=self.api_key_var.get())
            model_name = specific_model if specific_model else self.model_std_var.get()
            model = genai.GenerativeModel(model_name)
            
            safety_settings = None
            if self.safety_unlock_var.get():
                safety_settings = {
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                }

            config = GenerationConfig(temperature=0.0)
            glossary_text = "\n".join([f"{src}={dst}" for src, dst in self.glossary_data])
            extra_inst = self.txt_instruction.get("1.0", tk.END).strip()
            if "(" in extra_inst and ")" in extra_inst: extra_inst = ""
            
            target_lang = self.target_lang_var.get()
            if "Other" in target_lang:
                target_lang = self.custom_target_lang_var.get() or "English"
            newline_code = self.newline_symbol_var.get()

            base_prompt = f"""You are a professional game localization machine.
TASK: Translate the source text into [{target_lang}].
RULES:
1. If text is in [{target_lang}], output AS IS.
2. Translate if NOT in [{target_lang}].
3. Keep symbols (like {newline_code}) exactly.
4. Output ONLY translation.
"""
            extra_prompt_part = ""
            if extra_inst: extra_prompt_part = f"\n[INSTRUCTIONS]:\n{extra_inst}\n"
            prompt = f"{base_prompt}{extra_prompt_part}\n[GLOSSARY]:\n{glossary_text}\n[SOURCE]:\n{content}"
            
            response = model.generate_content(prompt, generation_config=config, safety_settings=safety_settings)
            final = prefix + response.text.strip()
            
            self._track_tokens(response, model_name)
            self.root.after(0, lambda: self._update_trans_ui_sync(final, target_idx))
            
        except Exception as e:
            err = str(e)
            t = UI_TEXTS[self.current_ui_lang]
            msg = t["err_gen"]
            if "429" in err: msg = t["err_429"]
            elif "API key" in err: msg = t["err_api"]
            elif "network" in err.lower(): msg = t["err_net"]
            
            self.root.after(0, lambda: self._update_trans_ui_sync(f"[{msg}] {str(e)[:50]}...", target_idx))

    # Token Tracking
    def _track_tokens(self, response, model_name):
        try:
            if hasattr(response, "usage_metadata"):
                usage = response.usage_metadata
                p_cnt = usage.prompt_token_count
                c_cnt = usage.candidates_token_count
                
                if "flash-lite" in model_name:
                    self.tokens_std_in += p_cnt
                    self.tokens_std_out += c_cnt
                else:
                    self.tokens_adv_in += p_cnt
                    self.tokens_adv_out += c_cnt
                
                self.root.after(0, self.update_cost_display)
        except: pass

    def update_cost_display(self, *args):
        """v7.6.1: 添加输入验证"""
        try:
            # 使用max确保非负数
            p_std_in = max(0, float(self.price_std_in_var.get()))
            p_std_out = max(0, float(self.price_std_out_var.get()))
            cost_std = (self.tokens_std_in / 1000000 * p_std_in) + (self.tokens_std_out / 1000000 * p_std_out)
            
            p_adv_in = max(0, float(self.price_adv_in_var.get()))
            p_adv_out = max(0, float(self.price_adv_out_var.get()))
            cost_adv = (self.tokens_adv_in / 1000000 * p_adv_in) + (self.tokens_adv_out / 1000000 * p_adv_out)
            
            total = cost_std + cost_adv
            self.est_cost_var.set(f"{total:.4f}")
        except ValueError:
            # 输入无效时显示0
            self.est_cost_var.set("0.0000")
        except: 
            pass

    def _update_trans_ui_sync(self, text, target_idx):
        if self.current_index == target_idx:
            self.txt_trans.delete("1.0", tk.END)
            self.txt_trans.insert("1.0", text)
            self.update_line_counts()

    # Async AI (Single Button)
    def retry_std(self):
        orig = self.txt_original.get("1.0", tk.END).strip()
        if orig:
            self.txt_trans.delete("1.0", tk.END); self.txt_trans.insert("1.0", "⏳ AI...")
            threading.Thread(target=self.fetch_ai, args=(orig, self.current_index, self.model_std_var.get()), daemon=True).start()

    def retry_adv(self):
        orig = self.txt_original.get("1.0", tk.END).strip()
        if orig:
            self.txt_trans.delete("1.0", tk.END); self.txt_trans.insert("1.0", "🚀 AI...")
            threading.Thread(target=self.fetch_ai, args=(orig, self.current_index, self.model_adv_var.get()), daemon=True).start()

    def fetch_ai(self, text, target_idx, specific_model):
        self._fetch_ai_sync(text, target_idx, specific_model)

    def update_trans_box(self, text, target_idx):
        if self.current_index != target_idx: return
        if self.data_list[target_idx]["status"] == 1: return 
        self.txt_trans.delete("1.0", tk.END); self.txt_trans.insert("1.0", text)
        self.update_line_counts()

    def copy_text(self, widget):
        self.root.clipboard_clear(); self.root.clipboard_append(widget.get("1.0", tk.END).strip())

    def save_config(self):
        try:
            inst_text = self.txt_instruction.get("1.0", tk.END).strip()
            if "(" in inst_text and ")" in inst_text: inst_text = ""
            config = {
                "api_key": self.api_key_var.get(),
                "model_std": self.model_std_var.get(),
                "model_adv": self.model_adv_var.get(),
                "ui_lang": self.ui_lang_var.get(),
                "target_lang": self.target_lang_var.get(),
                "custom_target": self.custom_target_lang_var.get(),
                "newline_code": self.newline_symbol_var.get(),
                "safety_unlock": self.safety_unlock_var.get(),
                "auto_translate": self.auto_translate_next_var.get(),
                "price_std_in": self.price_std_in_var.get(),
                "price_std_out": self.price_std_out_var.get(),
                "price_adv_in": self.price_adv_in_var.get(),
                "price_adv_out": self.price_adv_out_var.get(),
                "glossary": self.glossary_data,
                "regex": self.regex_data,
                "extra_instruction": inst_text
            }
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(f"[Config] Saved to: {CONFIG_FILE}")
        except Exception as e:
            print(f"[Config] Save failed: {e}")

    def load_config(self):
        # 设置默认值
        self.model_std_var.set("models/gemini-2.0-flash-lite")
        self.model_adv_var.set("models/gemini-1.5-pro")
        self.ui_lang_var.set("English")
        self.current_ui_lang = "en"
        self.target_lang_var.set(TARGET_LANGS[0])
        self.newline_symbol_var.set("{换行}")
        self.safety_unlock_var.set(False)
        self.auto_translate_next_var.set(False)
        self.txt_instruction.delete("1.0", tk.END)
        self.txt_instruction.insert("1.0", "(e.g., Use RPG terminology...)")
        self.regex_data = [r"\{.*?\}", r"<.*?>", r"\@.*?\@"]

        # v7.6.1: 改进 - 显示配置文件路径
        print(f"[Config] Looking for: {CONFIG_FILE}")
        
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    c = json.load(f)
                    print(f"[Config] Successfully loaded config with {len(c)} keys")
                    
                    self.api_key_var.set(c.get("api_key", ""))
                    self.model_std_var.set(c.get("model_std", "models/gemini-2.0-flash-lite"))
                    self.model_adv_var.set(c.get("model_adv", "models/gemini-1.5-pro"))
                    loaded_ui_lang = c.get("ui_lang", "English")
                    self.ui_lang_var.set(loaded_ui_lang)
                    if loaded_ui_lang == "中文": self.current_ui_lang = "zh"
                    elif loaded_ui_lang == "日本語": self.current_ui_lang = "ja"
                    else: self.current_ui_lang = "en"
                    self.target_lang_var.set(c.get("target_lang", TARGET_LANGS[0]))
                    self.custom_target_lang_var.set(c.get("custom_target", ""))
                    self.newline_symbol_var.set(c.get("newline_code", "{换行}"))
                    self.safety_unlock_var.set(c.get("safety_unlock", False))
                    self.auto_translate_next_var.set(c.get("auto_translate", False))
                    
                    self.price_std_in_var.set(c.get("price_std_in", 0.075))
                    self.price_std_out_var.set(c.get("price_std_out", 0.30))
                    self.price_adv_in_var.set(c.get("price_adv_in", 3.50))
                    self.price_adv_out_var.set(c.get("price_adv_out", 10.50))
                    
                    self.glossary_data = c.get("glossary", [])
                    self.regex_data = c.get("regex", [r"\{.*?\}", r"<.*?>", r"\@.*?\@"]) 
                    saved_inst = c.get("extra_instruction", "")
                    if saved_inst: 
                        self.txt_instruction.delete("1.0", tk.END)
                        self.txt_instruction.insert("1.0", saved_inst)
                    self.on_target_lang_change()
                    
                    print(f"[Config] API Key loaded: {'Yes' if self.api_key_var.get() else 'No'}")
                    print(f"[Config] UI Language: {loaded_ui_lang}")
                    print(f"[Config] Glossary items: {len(self.glossary_data)}")
                    
            except Exception as e:
                print(f"[Config] Load failed: {e}")
                t = UI_TEXTS[self.current_ui_lang]
                err_msg = t.get("config_err", "Config file corrupted.\nSettings reset.")
                messagebox.showwarning("Config Error", err_msg)
        else:
            print(f"[Config] File not found, using defaults")
        
        self.refresh_glossary_ui()
        self.refresh_regex_ui()

    def on_closing(self): self.save_config(); self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    if 'ttkbootstrap' in globals(): style = ttk.Style(theme="cosmo") 
    app = GameTranslatorEditor(root)
    root.mainloop()