A desktop game localization helper with visual UI overflow QA, glossary control, and Gemini-powered translation.

# Game Text Translator | 游戏文本翻译助手 | ゲームテキスト翻訳アシスタント

> **Latest Version: v7.9.6** - Visual QA Final Edition with Auto-Wrap, Safety Protection & More!
>
> [Download on itch.io](https://gardenatdesk.itch.io/game-translator-helper) | [GitHub Releases](https://github.com/GardenAtDesk/gemini-game-translator/releases/latest)

> A free, open-source translation tool for indie game developers using Google Gemini AI
>
> 一个免费开源的游戏文本翻译工具，使用Google Gemini AI
>
> Google Gemini AIを使用した無料のオープンソースゲームテキスト翻訳ツール

[![Download on itch.io](https://img.shields.io/badge/Download-itch.io-FA5C5C?style=for-the-badge&logo=itch.io&logoColor=white)](https://gardenatdesk.itch.io/game-translator-helper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Latest Release](https://img.shields.io/github/v/release/GardenAtDesk/gemini-game-translator)](https://github.com/GardenAtDesk/gemini-game-translator/releases/latest)

Made by an indie game dev who got tired of translating game text manually.

一个厌倦了手动翻译游戏文本的独立游戏开发者制作。

ゲームテキストを手動で翻訳することに疲れたインディーゲーム開発者によって作成されました。

---

## What's New in v7.9.6

### Visual QA Enhancements
- **Auto-Wrap** - Intelligently wrap text at punctuation marks to match source line count
- **Find Next Issue** - Automatically scan and jump to overflow problems
- **Ignore Line** - Mark lines that don't need checking
- **Visual Filter** - Filter Ruby text and special codes for accurate width measurement
- **Dynamic Window Height** - Window auto-resizes when content grows

### Safety & Stability
- **API Safety Protection** - Daily translation limits and cost caps
- **Undo/Redo Support** - Ctrl+Z/Y in Visual QA editor
- **Bug Fixes** - Fixed auto-wrap adding extra lines, find next issue false positives

[See full changelog](https://github.com/GardenAtDesk/gemini-game-translator/releases/tag/v7.9.6)

---

## Download

### For Windows Users (Recommended):
**Download:** [itch.io - Windows Version](https://gardenatdesk.itch.io/game-translator-helper) (~64MB)
- Standalone .exe - **No Python needed!**
- Just extract and run

### For Developers / Mac / Linux:
**Download:** [itch.io - Python Version](https://gardenatdesk.itch.io/game-translator-helper) (~100KB)
- Full source code
- Cross-platform

**Or clone this repository:**
```bash
git clone https://github.com/GardenAtDesk/gemini-game-translator.git
cd gemini-game-translator
pip install pandas google-generativeai ttkbootstrap
python GameTranslator7_9_6.py
```

---

## Language

- [English](#english)
- [中文](#中文)
- [日本語](#日本語)

---

## English

### Important Disclaimers

**API Usage:**
- Requires **Google Gemini API key** (free at [Google AI Studio](https://aistudio.google.com/app/apikey))
- API calls charged by Google after free tier (~15 RPM free)
- I'm NOT responsible for your API costs

**Safety Settings:**
- "Unlock Safety Filters" may violate Google's TOS
- Could result in **account suspension**
- Use at your own risk

**No Support:**
- Code is open-source, fork freely
- No technical support
- No feature requests
- No maintenance guarantees

**Privacy:**
- API key and data stay on YOUR computer
- Config files are local only
- Never commit `config_v7.json` to Git

### Key Features

- **Visual QA Editor** - Preview text width/overflow in simulated game window
  - Auto-wrap text at punctuation marks
  - Find next overflow issue automatically
  - Ignore specific lines from checking
  - Filter Ruby text for accurate measurement
- **Multi-language UI** (English, 中文, 日本語)
- **Translate to 100+ languages** via Gemini
- **Batch translation** with auto-retry
- **API Safety Protection** - Daily limits and cost caps
- **Real-time cost monitoring** (estimate only)
- **Custom glossary** for consistent terminology
- **Regex protection** for game variables (`{tag}`, `@var@`)
- **Auto-save progress** (`_working_progress.csv`)

### Quick Start

**1. Get API Key:**
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create free API key

**2. Install (Python version only):**
```bash
pip install pandas google-generativeai ttkbootstrap
```

**3. Run:**
- **Windows .exe:** Just double-click
- **Python:** `python GameTranslator7_9_6.py`

**4. Configure:**
- Paste API key in top-left field
- Select UI language
- Click "Detect Models" to verify

### Basic Usage

1. Click **"Load Source"** → Select CSV file
2. Click **"Translate Page"** for batch (50 lines)
3. Or navigate with `<< Prev` / `Next >>` for single lines
4. Use **Visual QA** to check text overflow
   - Click **"Auto Wrap"** to fix long lines
   - Click **"Find Next Issue"** to jump to problems
5. Click **"Export CSV"** when done

**CSV Format:**
```csv
Source,Translation
Hello,你好
HP: {value},生命值: {value}
```

### Cost Estimate

Using Gemini 2.0 Flash Lite (recommended):
- **~$0.60 per 10,000 lines** (extremely cheap!)
- Free tier covers most small/medium indie games

Cost monitor is ESTIMATE ONLY. Check official billing at [Google Cloud Console](https://console.cloud.google.com/).

### Support My Work

I'm an indie game dev making **The Sheepdog** - a cozy tactics game.

If this tool helps you:
- Star this repo
- [Buy me a coffee on Ko-fi](https://ko-fi.com/gardenatdesk)
- Follow [@GardenAtDesk on TikTok](https://www.tiktok.com/@gardenatdesk)

### License

MIT License - use freely, don't sue me.

### FAQ

**Q: Feature requests?**
A: No. Fork it yourself.

**Q: Errors?**
A: Check API key, network, quota.

**Q: Better than DeepL/ChatGPT?**
A: Gemini is cheaper. Try it.

**Q: Account banned?**
A: Told you not to unlock safety filters.

**Q: Mac/Linux support?**
A: Should work, only tested on Windows.

---

## 中文

### 重要声明

**API使用：**
- 需要**Google Gemini API密钥**（[Google AI Studio](https://aistudio.google.com/app/apikey)免费获取）
- 超过免费额度后按量收费（~15 RPM免费）
- 我不对你的API费用负责

**安全设置：**
- "解锁安全限制"可能违反Google TOS
- 可能导致**账号封禁**
- 风险自负

**无技术支持：**
- 开源代码，随意Fork
- 不提供技术支持
- 不接受功能请求
- 不保证维护

**隐私：**
- API密钥和数据保存在你的电脑
- 配置文件仅本地存储
- 切勿提交`config_v7.json`到Git

### 主要功能

- **Visual QA编辑器** - 在模拟游戏窗口预览文本宽度/溢出
  - 自动换行 - 智能在标点处换行
  - 查找下一个问题 - 自动扫描溢出问题
  - 忽略功能 - 跳过不需要检查的行
  - 视觉过滤器 - 过滤注音等特殊代码
- **多语言界面**（英文、中文、日文）
- **翻译到100+种语言**（Gemini支持）
- **批量翻译**带自动重试
- **API安全保护** - 每日配额和费用上限
- **实时成本监控**（仅供参考）
- **自定义术语表**保证一致性
- **正则保护**游戏变量（`{tag}`、`@var@`）
- **自动保存**进度（`_working_progress.csv`）

### 快速开始

**1. 获取API密钥：**
- 访问[Google AI Studio](https://aistudio.google.com/app/apikey)
- 创建免费密钥

**2. 安装（仅Python版本）：**
```bash
pip install pandas google-generativeai ttkbootstrap
```

**3. 运行：**
- **Windows .exe：**直接双击
- **Python：**`python GameTranslator7_9_6.py`

**4. 配置：**
- 在左上角粘贴API密钥
- 选择UI语言
- 点击"检测模型"验证

### 基本使用

1. 点击**"加载源文件"** → 选择CSV
2. 点击**"翻译本页"**批量翻译（50行）
3. 或用`<< 上一条` / `下一条 >>`单行翻译
4. 用**Visual QA**检查文本溢出
   - 点击**"自动换行"**修复过长的行
   - 点击**"查找下一个问题"**跳转到问题
5. 完成后点击**"导出成品"**

**CSV格式：**
```csv
原文,译文
Hello,你好
HP: {value},生命值: {value}
```

### 成本估算

使用Gemini 2.0 Flash Lite（推荐）：
- **每10,000行约$0.60**（极其便宜！）
- 免费额度覆盖大多数中小型游戏

成本监控仅供参考。查看官方账单：[Google Cloud控制台](https://console.cloud.google.com/)。

### 支持我的工作

我正在制作独立游戏**The Sheepdog**（牧羊犬）- 温馨战术游戏。

如果这个工具帮到你：
- 给仓库点Star
- [在Ko-fi请我喝咖啡](https://ko-fi.com/gardenatdesk)
- 关注[@GardenAtDesk的TikTok](https://www.tiktok.com/@gardenatdesk)

### 许可证

MIT许可证 - 随便用，别告我。

---

## 日本語

### 重要な免責事項

**API使用：**
- **Google Gemini APIキー**必要（[Google AI Studio](https://aistudio.google.com/app/apikey)で無料取得）
- 無料枠超過後は従量課金（~15 RPM無料）
- APIコストは自己責任

**安全設定：**
- 「セーフティ解除」はGoogle TOS違反の可能性
- **アカウント停止**のリスク
- 自己責任で使用

**サポートなし：**
- オープンソース、自由にFork
- 技術サポートなし
- 機能リクエスト不可
- メンテナンス保証なし

**プライバシー：**
- APIキーとデータはあなたのPC内
- 設定ファイルはローカルのみ
- `config_v7.json`をGitにコミットしない

### 主な機能

- **Visual QAエディター** - シミュレート画面でテキスト幅/溢れをプレビュー
  - 自動改行 - 句読点で賢く改行
  - 次の問題を検索 - 自動でオーバーフロー箇所へジャンプ
  - 無視機能 - チェック不要な行をスキップ
  - 視覚フィルタ - ルビテキストなどをフィルタ
- **多言語UI**（英語、中国語、日本語）
- **100以上の言語に翻訳**（Gemini対応）
- **一括翻訳**自動リトライ付き
- **API安全保護** - 日次制限とコスト上限
- **リアルタイムコスト監視**（参考値）
- **カスタム用語集**で一貫性確保
- **正規表現保護**でゲーム変数守る（`{tag}`、`@var@`）
- **自動保存**（`_working_progress.csv`）

### クイックスタート

**1. APIキー取得：**
- [Google AI Studio](https://aistudio.google.com/app/apikey)にアクセス
- 無料キー作成

**2. インストール（Python版のみ）：**
```bash
pip install pandas google-generativeai ttkbootstrap
```

**3. 実行：**
- **Windows .exe：**ダブルクリック
- **Python：**`python GameTranslator7_9_6.py`

**4. 設定：**
- 左上にAPIキーを貼り付け
- UI言語選択
- 「モデル検出」で確認

### 基本的な使い方

1. **「CSV読込」**クリック → CSVファイル選択
2. **「ページ翻訳」**で一括翻訳（50行）
3. または`<< 前へ` / `次へ >>`で1行ずつ
4. **Visual QA**でテキスト溢れチェック
   - **「自動改行」**で長い行を修正
   - **「次の問題を検索」**で問題箇所へジャンプ
5. 完了したら**「CSV出力」**クリック

**CSV形式：**
```csv
原文,訳文
Hello,こんにちは
HP: {value},HP: {value}
```

### コスト見積もり

Gemini 2.0 Flash Lite使用時（推奨）：
- **10,000行あたり約$0.60**（非常に安価！）
- 無料枠で中小規模ゲームカバー可能

コスト監視は参考値のみ。公式請求確認：[Google Cloudコンソール](https://console.cloud.google.com/)。

### サポート

インディーゲーム**The Sheepdog**（羊飼いの犬）制作中 - 心温まる戦術ゲーム。

このツールが役立ったら：
- リポジトリにスター
- [Ko-fiでコーヒーを奢る](https://ko-fi.com/gardenatdesk)
- [TikTok @GardenAtDeskフォロー](https://www.tiktok.com/@gardenatdesk)

### ライセンス

MITライセンス - 自由に使用、訴えないで。

---

**Made with love by a game dev who values efficiency over perfection**
