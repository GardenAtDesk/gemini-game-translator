# Config File Guide & Troubleshooting / 配置文件指南与故障排除 / 設定ファイルガイドとトラブルシューティング

> **📖 This file is available in three languages / 本文档提供三种语言版本 / このファイルは3つの言語で利用可能です**
> 
> - [English](#english-version) 
> - [中文](#中文版本) 
> - [日本語](#日本語版)

---

# English Version

## 📝 What is config_v7.json?

`config_v7.json` stores all your settings including:
- API key
- Model selection
- UI language
- Target translation language
- Glossary
- Custom instructions
- And more...

## 🤔 Do I need to create it manually?

### New users
**No need!** The program will automatically create this file when you close it for the first time.

### Existing users (upgrading from v7.6 or earlier)
**Yes, copy it!** Copy your old `config_v7.json` to the same folder as the new program.

## 📂 File Location

### v7.6.1 (New version)
Config file **must** be in the same folder as the main program:

```
YourFolder/
├── GameTranslator7_6_1.py         or GameTranslatorHelper.exe
└── config_v7.json                 ← Here
```

The program will show the config file path at startup:
```
[Config] Looking for: C:\full\path\config_v7.json
```

## ✅ How to verify config loading?

### Method 1: Check Console Output

When running the program, open console/terminal window, you'll see:

```
[Config] Looking for: /full/path/config_v7.json
[Config] Successfully loaded config with 17 keys
[Config] API Key loaded: Yes
[Config] UI Language: English
[Config] Glossary items: 5
```

**If you see "File not found"** → Config file doesn't exist
**If you see "Load failed: ..."** → Config file format error

### Method 2: Test Config Saving

1. Start program
2. Enter API Key
3. Select UI language as "中文"
4. Close program
5. Start again

**Expected result:**
- API Key should still be there
- UI language should be 中文
- All settings preserved

## 🐛 Common Issues & Solutions

### Issue 1: Config not loading

**Check:**
1. Is `config_v7.json` in the same folder as .py file?
2. Check console for `[Config] Looking for:` message
3. Is filename exactly `config_v7.json` (not `config_v7.json.txt`)?
4. Is JSON format correct? (Use online JSON validator)

**Solution:**
Delete corrupted `config_v7.json` and let program regenerate it.

### Issue 2: Settings not saved

**Check:**
1. Does the folder have write permission?
2. Check console for `[Config] Saved to:` message

**Solution:**
Run program with administrator rights (Windows) or check folder permissions.

### Issue 3: My glossary/regex/instructions disappeared

**Reason:** Config file not being loaded

**Solution:** Follow Method 1 above to verify config file location.

## 📄 Config File Fields

```json
{
  "api_key": "",                              // Your Google Gemini API key
  "model_std": "models/gemini-2.0-flash-lite", // Standard model (fast, cheap)
  "model_adv": "models/gemini-1.5-pro",        // Advanced model (accurate, expensive)
  "ui_lang": "English",                        // UI language: "English", "中文", "日本語"
  "target_lang": "Simplified Chinese",         // Target translation language
  "custom_target": "",                         // Custom target (if selecting "Custom")
  "newline_code": "{换行}",                    // Newline code
  "safety_unlock": false,                      // Disable safety filters (use carefully)
  "auto_translate": false,                     // Auto-translate next line after save
  "price_std_in": 0.075,                       // Standard model input price (per 1M tokens)
  "price_std_out": 0.30,                       // Standard model output price
  "price_adv_in": 3.50,                        // Advanced model input price
  "price_adv_out": 10.50,                      // Advanced model output price
  "glossary": [],                              // Glossary ["source=translation", ...]
  "regex": ["\\{.*?\\}", "<.*?>", "\\@.*?\\@"], // Regex protection patterns
  "extra_instruction": ""                      // Extra translation instructions
}
```

## ⚠️ Important Notes

### 1. API Key Security
- ❌ Don't share config files containing API keys
- ❌ Don't upload to public GitHub/platforms
- ✅ Delete `"api_key"` value before sharing

### 2. File Encoding
- Must be UTF-8 encoding
- Use UTF-8 compatible text editors (VS Code, Notepad++, etc.)
- Don't use Windows Notepad (encoding issues)

### 3. JSON Format
- Pay attention to commas and quotes
- No comma after the last field
- Boolean values: `true`/`false` (lowercase, no quotes)
- Numbers: no quotes

## 🔄 Version Compatibility

### v7.6 → v7.6.1
✅ Fully compatible! Just copy and use.

### v7.5 or earlier → v7.6.1
✅ Mostly compatible, may miss new fields (program uses defaults).

## 📝 Manually Create Config File

If needed, you can manually create a minimal config file:

**config_v7.json:**
```json
{
  "api_key": "your-api-key-here",
  "model_std": "models/gemini-2.0-flash-lite",
  "model_adv": "models/gemini-1.5-pro",
  "ui_lang": "English",
  "target_lang": "Simplified Chinese",
  "custom_target": "",
  "newline_code": "{换行}",
  "safety_unlock": false,
  "auto_translate": false,
  "price_std_in": 0.075,
  "price_std_out": 0.30,
  "price_adv_in": 3.50,
  "price_adv_out": 10.50,
  "glossary": [],
  "regex": ["\\{.*?\\}", "<.*?>", "\\@.*?\\@"],
  "extra_instruction": ""
}
```

Save to the same directory as the program.

---
---

# 中文版本

## 📝 config_v7.json是什么？

`config_v7.json` 保存你的所有设置，包括：
- API密钥
- 模型选择
- UI语言
- 目标翻译语言
- 术语表
- 自定义指令
- 等等...

## 🤔 需要手动创建吗？

### 新用户
**不需要！** 程序第一次关闭时会自动创建这个文件。

### 老用户（从v7.6或更早版本升级）
**需要复制！** 把你旧的 `config_v7.json` 复制到新程序的同一文件夹。

## 📂 文件位置

### v7.6.1 (新版本)
配置文件**必须**和主程序在同一文件夹：

```
你的文件夹/
├── GameTranslator7_6_1.py         或 GameTranslatorHelper.exe
└── config_v7.json                 ← 这里
```

程序启动时会显示配置文件路径：
```
[Config] Looking for: C:\完整路径\config_v7.json
```

## ✅ 如何验证配置文件是否被读取？

### 方法1: 查看控制台输出

运行程序时，打开控制台/终端窗口，你会看到：

```
[Config] Looking for: /完整/路径/config_v7.json
[Config] Successfully loaded config with 17 keys
[Config] API Key loaded: Yes
[Config] UI Language: 中文
[Config] Glossary items: 5
```

**如果看到 "File not found"** → 配置文件不存在
**如果看到 "Load failed: ..."** → 配置文件格式错误

### 方法2: 测试配置保存

1. 启动程序
2. 输入API Key
3. 选择UI语言为"中文"
4. 关闭程序
5. 再次启动

**预期结果:**
- API Key应该还在
- UI语言应该是中文
- 所有设置都被保留

## 🐛 常见问题与解决方案

### 问题1: 配置没有加载

**检查:**
1. `config_v7.json`是否在.py文件同目录？
2. 查看控制台的`[Config] Looking for:`消息
3. 文件名是否完全正确：`config_v7.json`（不是 `config_v7.json.txt`）？
4. JSON格式是否正确？（可以用在线JSON验证器检查）

**解决:**
删除损坏的`config_v7.json`，让程序重新生成。

### 问题2: 配置没有保存

**检查:**
1. 文件夹是否有写入权限？
2. 查看控制台的`[Config] Saved to:`消息

**解决:**
以管理员权限运行程序（Windows）或检查文件夹权限。

### 问题3: 我的术语表/正则/额外指令都消失了

**原因:** 配置文件没有被读取

**解决:** 按照上面的方法1验证配置文件位置。

## 📄 配置文件字段说明

```json
{
  "api_key": "",                              // 你的Google Gemini API密钥
  "model_std": "models/gemini-2.0-flash-lite", // 标准模型（快速、便宜）
  "model_adv": "models/gemini-1.5-pro",        // 高级模型（准确、贵）
  "ui_lang": "English",                        // UI语言: "English", "中文", "日本語"
  "target_lang": "Simplified Chinese",         // 目标翻译语言
  "custom_target": "",                         // 自定义目标语言（如果选"Custom"）
  "newline_code": "{换行}",                    // 换行符代码
  "safety_unlock": false,                      // 是否解除安全过滤器（谨慎使用）
  "auto_translate": false,                     // 保存后自动翻译下一行
  "price_std_in": 0.075,                       // 标准模型输入价格（每百万token）
  "price_std_out": 0.30,                       // 标准模型输出价格
  "price_adv_in": 3.50,                        // 高级模型输入价格
  "price_adv_out": 10.50,                      // 高级模型输出价格
  "glossary": [],                              // 术语表 ["原文=译文", ...]
  "regex": ["\\{.*?\\}", "<.*?>", "\\@.*?\\@"], // 正则保护模式
  "extra_instruction": ""                      // 额外翻译指令
}
```

## ⚠️ 重要提示

### 1. API密钥安全
- ❌ 不要分享包含API密钥的配置文件
- ❌ 不要上传到公开的GitHub等平台
- ✅ 如果需要分享，先删除 `"api_key"` 的值

### 2. 文件编码
- 必须是UTF-8编码
- 使用支持UTF-8的文本编辑器（VS Code、Notepad++等）
- 不要用Windows记事本（可能编码有问题）

### 3. JSON格式
- 注意逗号和引号
- 最后一个字段后面不要有逗号
- 布尔值用 `true`/`false`（小写，无引号）
- 数字不要加引号

## 🔄 配置文件版本兼容性

### v7.6 → v7.6.1
✅ 完全兼容！直接复制使用即可。

### v7.5 或更早 → v7.6.1
✅ 大部分兼容，可能缺少新字段（程序会使用默认值）。

## 📝 手动创建配置文件

如果需要，你可以手动创建一个最小配置文件：

**config_v7.json:**
```json
{
  "api_key": "你的API密钥",
  "model_std": "models/gemini-2.0-flash-lite",
  "model_adv": "models/gemini-1.5-pro",
  "ui_lang": "中文",
  "target_lang": "Simplified Chinese",
  "custom_target": "",
  "newline_code": "{换行}",
  "safety_unlock": false,
  "auto_translate": false,
  "price_std_in": 0.075,
  "price_std_out": 0.30,
  "price_adv_in": 3.50,
  "price_adv_out": 10.50,
  "glossary": [],
  "regex": ["\\{.*?\\}", "<.*?>", "\\@.*?\\@"],
  "extra_instruction": ""
}
```

保存到与程序相同的目录。

---
---

# 日本語版

## 📝 config_v7.jsonとは？

`config_v7.json` はすべての設定を保存します：
- APIキー
- モデル選択
- UI言語
- ターゲット翻訳言語
- 用語集
- カスタム指示
- その他...

## 🤔 手動で作成する必要がありますか？

### 新規ユーザー
**不要です！** プログラムを初めて閉じたときに自動的に作成されます。

### 既存ユーザー（v7.6以前からのアップグレード）
**コピーが必要です！** 古い `config_v7.json` を新しいプログラムと同じフォルダにコピーしてください。

## 📂 ファイルの場所

### v7.6.1 (新バージョン)
設定ファイルはメインプログラムと**同じフォルダ**に必要です：

```
あなたのフォルダ/
├── GameTranslator7_6_1.py         または GameTranslatorHelper.exe
└── config_v7.json                 ← ここ
```

プログラム起動時に設定ファイルパスが表示されます：
```
[Config] Looking for: C:\完全なパス\config_v7.json
```

## ✅ 設定の読み込みを確認する方法

### 方法1: コンソール出力を確認

プログラム実行時、コンソール/ターミナルウィンドウを開くと以下が表示されます：

```
[Config] Looking for: /完全なパス/config_v7.json
[Config] Successfully loaded config with 17 keys
[Config] API Key loaded: Yes
[Config] UI Language: 日本語
[Config] Glossary items: 5
```

**"File not found"が表示される** → 設定ファイルが存在しない
**"Load failed: ..."が表示される** → 設定ファイルの形式エラー

### 方法2: 設定保存をテスト

1. プログラムを起動
2. APIキーを入力
3. UI言語として「日本語」を選択
4. プログラムを閉じる
5. 再度起動

**期待される結果:**
- APIキーがまだある
- UI言語が日本語
- すべての設定が保持されている

## 🐛 一般的な問題と解決策

### 問題1: 設定が読み込まれない

**確認:**
1. `config_v7.json`は.pyファイルと同じフォルダにありますか？
2. コンソールで`[Config] Looking for:`メッセージを確認
3. ファイル名は正確に`config_v7.json`ですか（`config_v7.json.txt`ではない）？
4. JSON形式は正しいですか？（オンラインJSONバリデーターで確認）

**解決:**
破損した`config_v7.json`を削除し、プログラムに再生成させる。

### 問題2: 設定が保存されない

**確認:**
1. フォルダに書き込み権限がありますか？
2. コンソールで`[Config] Saved to:`メッセージを確認

**解決:**
管理者権限でプログラムを実行（Windows）またはフォルダの権限を確認。

### 問題3: 用語集/正規表現/追加指示が消えた

**原因:** 設定ファイルが読み込まれていない

**解決:** 上記の方法1で設定ファイルの場所を確認。

## 📄 設定ファイルフィールドの説明

```json
{
  "api_key": "",                              // Google Gemini APIキー
  "model_std": "models/gemini-2.0-flash-lite", // 標準モデル（高速、安価）
  "model_adv": "models/gemini-1.5-pro",        // 高度なモデル（正確、高価）
  "ui_lang": "English",                        // UI言語: "English", "中文", "日本語"
  "target_lang": "Simplified Chinese",         // ターゲット翻訳言語
  "custom_target": "",                         // カスタムターゲット（「Custom」を選択した場合）
  "newline_code": "{换行}",                    // 改行コード
  "safety_unlock": false,                      // 安全フィルターを無効化（慎重に使用）
  "auto_translate": false,                     // 保存後に次の行を自動翻訳
  "price_std_in": 0.075,                       // 標準モデル入力価格（100万トークンあたり）
  "price_std_out": 0.30,                       // 標準モデル出力価格
  "price_adv_in": 3.50,                        // 高度なモデル入力価格
  "price_adv_out": 10.50,                      // 高度なモデル出力価格
  "glossary": [],                              // 用語集 ["原文=訳文", ...]
  "regex": ["\\{.*?\\}", "<.*?>", "\\@.*?\\@"], // 正規表現保護パターン
  "extra_instruction": ""                      // 追加の翻訳指示
}
```

## ⚠️ 重要な注意事項

### 1. APIキーのセキュリティ
- ❌ APIキーを含む設定ファイルを共有しない
- ❌ 公開GitHub/プラットフォームにアップロードしない
- ✅ 共有する前に`"api_key"`の値を削除

### 2. ファイルエンコーディング
- UTF-8エンコーディングでなければならない
- UTF-8互換のテキストエディタを使用（VS Code、Notepad++など）
- Windowsメモ帳は使用しない（エンコーディングの問題）

### 3. JSON形式
- カンマと引用符に注意
- 最後のフィールドの後にカンマなし
- ブール値：`true`/`false`（小文字、引用符なし）
- 数値：引用符なし

## 🔄 バージョン互換性

### v7.6 → v7.6.1
✅ 完全互換！コピーして使用するだけ。

### v7.5以前 → v7.6.1
✅ ほぼ互換、新しいフィールドがない可能性（プログラムはデフォルトを使用）。

## 📝 設定ファイルを手動で作成

必要に応じて、最小限の設定ファイルを手動で作成できます：

**config_v7.json:**
```json
{
  "api_key": "あなたのAPIキー",
  "model_std": "models/gemini-2.0-flash-lite",
  "model_adv": "models/gemini-1.5-pro",
  "ui_lang": "日本語",
  "target_lang": "Simplified Chinese",
  "custom_target": "",
  "newline_code": "{换行}",
  "safety_unlock": false,
  "auto_translate": false,
  "price_std_in": 0.075,
  "price_std_out": 0.30,
  "price_adv_in": 3.50,
  "price_adv_out": 10.50,
  "glossary": [],
  "regex": ["\\{.*?\\}", "<.*?>", "\\@.*?\\@"],
  "extra_instruction": ""
}
```

プログラムと同じディレクトリに保存してください。
