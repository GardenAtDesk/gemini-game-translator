# Game Text Translator | 游戏文本翻译助手 | ゲームテキスト翻訳アシスタント

> 📢 **Latest Version: v6.9** - Now with batch translation improvements & cost tracking!
>
> 👉 [Download Latest Release](https://github.com/GardenAtDesk/gemini-game-translator/releases/latest)

> A free, open-source translation tool for indie game developers using Google Gemini AI
> 
> 一个免费开源的游戏文本翻译工具，使用Google Gemini AI
>
> Google Gemini AIを使用した無料のオープンソースゲームテキスト翻訳ツール

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Latest Release](https://img.shields.io/github/v/release/GardenAtDesk/gemini-game-translator)](https://github.com/GardenAtDesk/gemini-game-translator/releases/latest)
[![GitHub Stars](https://img.shields.io/github/stars/GardenAtDesk/gemini-game-translator)](https://github.com/GardenAtDesk/gemini-game-translator/stargazers)

Made by an indie game dev who got tired of translating game text manually.

一个厌倦了手动翻译游戏文本的独立游戏开发者制作。

ゲームテキストを手動で翻訳することに疲れたインディーゲーム開発者によって作成されました。

---

## 📥 Download / 下载 / ダウンロード

### For Non-Tech Users (Windows):
1. Go to [**Releases**](https://github.com/GardenAtDesk/gemini-game-translator/releases) page
2. Download **v6.9** (latest)
3. Extract and run (No Python required!)

### 给普通用户（Windows）：
1. 访问 [**Releases**](https://github.com/GardenAtDesk/gemini-game-translator/releases) 页面
2. 下载 **v6.9**（最新版）
3. 解压后运行（无需安装Python！）

### 一般ユーザー向け（Windows）：
1. [**Releases**](https://github.com/GardenAtDesk/gemini-game-translator/releases) ページへ
2. **v6.9**（最新版）をダウンロード
3. 解凍して実行（Python不要！）

### For Developers:
Clone this repository or download `GameTranslator6_9.py` directly.

---

## 🌍 Language / 语言 / 言語

- [English](#english)
- [中文](#中文)
- [日本語](#日本語)

---

## English

### ⚠️ Important Disclaimers

**API Usage:**
- This tool requires a **Google Gemini API key** (you must obtain your own for free at [Google AI Studio](https://aistudio.google.com/app/apikey))
- API calls are **charged by Google** after free tier (typically ~15 RPM for free accounts)
- I am NOT responsible for your API costs or quota limits

**Safety Settings:**
- The "Unlock Safety Filters" option may violate Google's Terms of Service
- Using it could result in **account suspension or API key revocation**
- Use at your own risk - I recommend keeping filters enabled

**No Support:**
- ✅ Code is open-source, modify as you wish
- ❌ No technical support provided
- ❌ No feature requests accepted
- ❌ Not guaranteed to be maintained

**Privacy:**
- Your API key and translations stay on YOUR computer
- Config files are stored locally only
- Never commit `config_v6.json` to Git (it's in .gitignore)

### ✨ Features

- 🌍 **Multi-language UI** (English, 中文, 日本語)
- 🎯 **Translate to 12+ languages** (English, Chinese, Japanese, Korean, French, German, Spanish, Portuguese, Russian, Italian, and more)
- ⚡ **Batch translation** with progress tracking (v6.9+)
- 💰 **Real-time cost monitoring** - estimate only (v6.9+)
- 📊 **Success/failure statistics** for batch operations (v6.9+)
- 📚 **Custom glossary support** (define your own term translations)
- 🔒 **Regex protection** (preserve variables like `{player_name}`, `@value@`)
- 💾 **Auto-save progress** (resume anytime with `_working_progress.csv`)
- 🎨 **Clean, modern interface** (built with ttkbootstrap)
- 🚀 **Powered by Gemini API** (much cheaper than GPT-4)

### 🚀 Quick Start

**1. Get API Key:**
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a free API key (Google account required)

**2. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure:**
```bash
# Copy template
cp config_template.json config_v6.json

# Edit config_v6.json and add your API key
```

**4. Run:**
```bash
python GameTranslator6_9.py
```

### 📖 Usage

1. Click **"Load CSV"** and select your game text file
   - CSV format: Column A = source text, Column B = translation (optional)
2. Click **"Translate Page"** for batch translation
3. Edit translations manually if needed
4. Use glossary to define consistent terminology
5. Click **"Export CSV"** when done

**CSV Format Example:**
```csv
Hello,你好
Attack,攻击
HP: {value},生命值: {value}
Welcome to @TOWN@,欢迎来到@TOWN@
```

### 💰 Cost Estimate

Using Gemini 2.0 Flash Lite (recommended):
- **~$0.02 per 1,000 lines** (extremely cheap)
- **10,000 lines ≈ $0.60 USD** (input + output)
- Free tier covers most small/medium indie games

### 💵 Cost Monitoring (v6.9+)

The tool includes a **rough cost estimator** based on token usage.

**⚠️ Important:**
- This is an **ESTIMATE ONLY**
- Input and output token prices are different
- Actual costs may vary significantly
- Always check your official billing from Google
- We are NOT responsible for any billing discrepancies

**How to Use:**
1. Check official Gemini pricing: https://ai.google.dev/gemini-api/docs/pricing
2. Enter your own prices in the Cost Monitor panel
3. Monitor estimated usage during translation
4. Verify actual costs in Google Cloud Console

**Example Pricing (as of Jan 2025):**
- Gemini 2.0 Flash Lite: $0.075/1M input, $0.30/1M output
- Gemini 1.5 Pro: $3.50/1M input, $10.50/1M output

### 🛠️ Advanced Features

**Glossary:**
- Define term pairs: `HP=生命值`, `Attack=攻击`
- Ensures consistent translation across entire project

**Regex Protection:**
- Protects special codes: `{变量}`, `<tag>`, `@placeholder@`
- Prevents AI from translating game variables

**Custom Instructions:**
- Add game-specific context in the prompt box
- Example: "Use casual tone", "This is a fantasy RPG"

**Batch Translation:**
- Translate entire pages at once
- See progress in real-time
- Get success/failure statistics

### 💝 Support My Work

I'm an indie game developer working on **The Sheepdog** - a cozy tactics game.

If this tool saves you time:
- ⭐ Star this repo
- ☕ [Buy me a coffee on Ko-fi](https://ko-fi.com/gardenatdesk)
- 🐦 Follow [@GardenAtDesk on TikTok](https://www.tiktok.com/@gardenatdesk)

### 📝 License

MIT License - do whatever you want, just don't sue me.

### ❓ FAQ

**Q: Can you add feature X?**  
A: No. This is a personal tool I'm sharing. Fork it if you need changes.

**Q: Why am I getting errors?**  
A: Check your API key, network connection, and quota limits.

**Q: Is this better than DeepL/ChatGPT?**  
A: Gemini is cheaper. Quality depends on your use case. Try it yourself.

**Q: My account got banned!**  
A: I warned you about the safety unlock feature. Don't use it.

**Q: Does this work on Mac/Linux?**  
A: Should work anywhere Python runs, but only tested on Windows.

**Q: How accurate is the cost estimator?**  
A: It's a rough estimate. Always check your actual Google Cloud billing.

---

## 中文

### ⚠️ 重要声明

**API使用：**
- 本工具需要 **Google Gemini API密钥**（需要自己在[Google AI Studio](https://aistudio.google.com/app/apikey)免费申请）
- API调用在免费额度后**按量收费**（免费账户通常约15 RPM）
- 我不对你的API费用或配额限制负责

**安全设置：**
- "解锁安全限制"选项可能违反Google服务条款
- 使用可能导致**账号被封或API密钥被撤销**
- 风险自负 - 建议保持过滤器开启

**无技术支持：**
- ✅ 代码开源，随意修改
- ❌ 不提供技术支持
- ❌ 不接受功能请求
- ❌ 不保证持续更新

**隐私：**
- 你的API密钥和翻译数据保存在你的电脑上
- 配置文件仅本地存储
- 切勿将`config_v6.json`提交到Git（已在.gitignore中）

### ✨ 功能特点

- 🌍 **多语言界面**（英文、中文、日文）
- 🎯 **支持12+种目标语言**（英语、中文、日语、韩语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语等）
- ⚡ **批量翻译**带进度显示（v6.9+）
- 💰 **实时成本估算** - 仅供参考（v6.9+）
- 📊 **成功/失败统计**（v6.9+）
- 📚 **自定义术语表**（定义专属术语翻译）
- 🔒 **正则表达式保护**（保护变量如`{player_name}`、`@value@`）
- 💾 **自动保存进度**（随时恢复，保存为`_working_progress.csv`）
- 🎨 **简洁现代的界面**（基于ttkbootstrap）
- 🚀 **Gemini API驱动**（比GPT-4便宜得多）

### 🚀 快速开始

**1. 获取API密钥：**
- 访问[Google AI Studio](https://aistudio.google.com/app/apikey)
- 创建免费API密钥（需要Google账号）

**2. 安装依赖：**
```bash
pip install -r requirements.txt
```

**3. 配置：**
```bash
# 复制模板
cp config_template.json config_v6.json

# 编辑config_v6.json并添加你的API密钥
```

**4. 运行：**
```bash
python GameTranslator6_9.py
```

### 📖 使用方法

1. 点击**"加载源文件"**并选择游戏文本CSV文件
   - CSV格式：A列=原文，B列=译文（可选）
2. 点击**"翻译当前页"**进行批量翻译
3. 需要时手动编辑译文
4. 使用术语表定义一致的术语翻译
5. 完成后点击**"导出成品"**

**CSV格式示例：**
```csv
Hello,你好
Attack,攻击
HP: {value},生命值: {value}
Welcome to @TOWN@,欢迎来到@TOWN@
```

### 💰 成本估算

使用Gemini 2.0 Flash Lite（推荐）：
- **每1000行约$0.02**（极其便宜）
- **10,000行 ≈ $0.60美元**（包含输入+输出）
- 免费额度足够覆盖大多数中小型独立游戏

### 💵 成本监控（v6.9+）

工具包含基于token使用的**粗略成本估算器**。

**⚠️ 重要说明：**
- 这**仅供参考**
- 输入和输出token价格不同
- 实际成本可能有显著差异
- 请务必查看Google官方账单
- 我们不对任何账单差异负责

**使用方法：**
1. 查看Gemini官方定价：https://ai.google.dev/gemini-api/docs/pricing
2. 在成本监控面板输入你的价格
3. 翻译时监控预估使用量
4. 在Google Cloud控制台验证实际成本

**参考价格（截至2025年1月）：**
- Gemini 2.0 Flash Lite: $0.075/百万输入, $0.30/百万输出
- Gemini 1.5 Pro: $3.50/百万输入, $10.50/百万输出

### 💝 支持我的工作

我是一名独立游戏开发者，正在制作**The Sheepdog**（牧羊犬）- 一款温馨的战术游戏。

如果这个工具帮到了你：
- ⭐ 给这个仓库点个Star
- ☕ [在Ko-fi上请我喝杯咖啡](https://ko-fi.com/gardenatdesk)
- 🐦 关注[@GardenAtDesk的TikTok](https://www.tiktok.com/@gardenatdesk)

### 📝 许可证

MIT许可证 - 随便用，但别告我。

---

## 日本語

### ⚠️ 重要な免責事項

**API使用について：**
- このツールには**Google Gemini APIキー**が必要です（[Google AI Studio](https://aistudio.google.com/app/apikey)で無料取得）
- API呼び出しは無料枠超過後に**従量課金**されます（無料アカウントは通常約15 RPM）
- APIコストや制限については一切責任を負いません

**安全設定：**
- 「セーフティ解除」オプションはGoogleの利用規約に違反する可能性があります
- 使用すると**アカウント停止またはAPIキー取り消し**の可能性があります
- 自己責任で使用してください - フィルターは有効のままにすることをお勧めします

**サポートなし：**
- ✅ コードはオープンソース、自由に改変可
- ❌ 技術サポートは提供しません
- ❌ 機能リクエストは受け付けません
- ❌ 継続的なメンテナンスは保証しません

**プライバシー：**
- APIキーと翻訳データはあなたのコンピュータに保存されます
- 設定ファイルはローカルのみに保存
- `config_v6.json`をGitにコミットしないでください（.gitignoreに含まれています）

### ✨ 機能

- 🌍 **多言語UI**（英語、中国語、日本語）
- 🎯 **12以上の言語に翻訳可能**（英語、中国語、日本語、韓国語、フランス語、ドイツ語、スペイン語、ポルトガル語、ロシア語、イタリア語など）
- ⚡ **一括翻訳**進捗表示付き（v6.9+）
- 💰 **リアルタイムコスト監視** - 参考のみ（v6.9+）
- 📊 **成功/失敗統計**（v6.9+）
- 📚 **カスタム用語集サポート**（独自の用語翻訳を定義）
- 🔒 **正規表現保護**（`{player_name}`、`@value@`などの変数を保護）
- 💾 **自動進捗保存**（`_working_progress.csv`でいつでも再開可能）
- 🎨 **クリーンでモダンなインターフェース**（ttkbootstrapベース）
- ⚡ **Gemini API駆動**（GPT-4より遥かに安価）

### 🚀 クイックスタート

**1. APIキーを取得：**
- [Google AI Studio](https://aistudio.google.com/app/apikey)にアクセス
- 無料APIキーを作成（Googleアカウント必要）

**2. 依存関係をインストール：**
```bash
pip install -r requirements.txt
```

**3. 設定：**
```bash
# テンプレートをコピー
cp config_template.json config_v6.json

# config_v6.jsonを編集してAPIキーを追加
```

**4. 実行：**
```bash
python GameTranslator6_9.py
```

### 📖 使い方

1. **「CSV読込」**をクリックしてゲームテキストファイルを選択
   - CSV形式：A列=原文、B列=訳文（オプション）
2. **「ページ翻訳」**をクリックして一括翻訳
3. 必要に応じて手動で翻訳を編集
4. 用語集を使用して一貫した用語翻訳を定義
5. 完了したら**「CSV出力」**をクリック

**CSV形式の例：**
```csv
Hello,こんにちは
Attack,攻撃
HP: {value},HP: {value}
Welcome to @TOWN@,@TOWN@へようこそ
```

### 💰 コスト見積もり

Gemini 2.0 Flash Lite使用時（推奨）：
- **1000行あたり約$0.02**（非常に安価）
- **10,000行 ≈ $0.60 USD**（入力+出力）
- 無料枠で中小規模のインディーゲームをカバー可能

### 💵 コスト監視（v6.9+）

トークン使用量に基づく**おおよそのコスト推定機能**を搭載。

**⚠️ 重要：**
- これは**推定値のみ**です
- 入力と出力のトークン価格は異なります
- 実際のコストは大きく異なる場合があります
- 必ずGoogleの公式請求を確認してください
- 請求額の相違について一切責任を負いません

**使用方法：**
1. Gemini公式価格を確認：https://ai.google.dev/gemini-api/docs/pricing
2. コストモニターパネルに価格を入力
3. 翻訳中に推定使用量を監視
4. Google Cloud Consoleで実際のコストを確認

**参考価格（2025年1月時点）：**
- Gemini 2.0 Flash Lite: $0.075/100万入力, $0.30/100万出力
- Gemini 1.5 Pro: $3.50/100万入力, $10.50/100万出力

### 💝 サポート

インディーゲーム開発者として**The Sheepdog**（羊飼いの犬）- 心温まる戦術ゲームを制作中です。

このツールが役立ったら：
- ⭐ このリポジトリにスターを
- ☕ [Ko-fiでコーヒーを奢る](https://ko-fi.com/gardenatdesk)
- 🐦 [TikTok @GardenAtDeskをフォロー](https://www.tiktok.com/@gardenatdesk)

### 📝 ライセンス

MITライセンス - 自由に使ってください、訴えないでください。

---

**Made with 🐑 by a game dev who values efficiency over perfection**

**効率を完璧さより重視するゲーム開発者によって作成 🐑**

**完璧さより効率を重視するゲーム開発者が作成 🐑**
