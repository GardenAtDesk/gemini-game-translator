# GameTranslator v7.6.1 Changelog / 更新日志 / 変更履歴

> **📖 This file is available in three languages / 本文档提供三种语言版本 / このファイルは3つの言語で利用可能です**
> 
> - [English](#english-version) 
> - [中文](#中文版本) 
> - [日本語](#日本語版)

**Release Date / 发布日期 / リリース日**: 2025-01-14

---

# English Version

## 🐛 Bug Fixes

### 0. **Fixed Config File Path Issue** ⭐ NEW
- **Problem**: Used relative path for config_v7.json, couldn't find config when starting from different directories
- **Fix**: Changed to use absolute path in program's directory, added detailed debug logging
- **Impact**: Config file can now always be correctly read and saved, regardless of startup directory

### 1. **Fixed Duplicate Save Issue**
- **Problem**: `append_row_to_disk` was appending data each time, causing potential duplicate records
- **Fix**: Changed to read-update-rewrite mode, ensuring each index is saved only once
- **Impact**: Improved data integrity, reduced file size

### 2. **Enhanced Newline Handling**
- **Problem**: Visual QA window only replaced `\n`, potentially missing `\r\n` on Windows
- **Fix**: Now handles `\r\n`, `\r`, and `\n` line breaks
- **Impact**: Better cross-platform compatibility

### 3. **Added Import Translation Feedback**
- **Problem**: When importing CSV, mismatched rows were silently skipped
- **Fix**: Now counts and displays the number of skipped rows
- **Impact**: Users have clearer feedback on import results

### 4. **Price Input Validation**
- **Problem**: Cost estimation didn't validate user input, could cause errors
- **Fix**: Added input validation, ensuring prices are non-negative
- **Impact**: More stable cost estimation

### 5. **Batch Translation 429 Retry Logic**
- **Problem**: When hitting API rate limit (429 error), requests were skipped without retry
- **Fix**: Added smart retry mechanism, up to 3 retries with wait times (15s, 30s, 45s)
- **Impact**: More reliable batch translation

### 6. **Visual QA Font Fallback**
- **Problem**: Font configuration failure could cause width detection errors
- **Fix**: Added default font fallback (Microsoft YaHei 12pt)
- **Impact**: More stable Visual QA

## 📊 Technical Details

### Modified Functions:
- `CONFIG_FILE`, `save_config()`, `load_config()`
- `append_row_to_disk()`, `VisualQAWindow.on_target_edit()`
- `get_max_line_width()`, `update_cost_display()`
- `import_translations_csv()`, `_fetch_ai_sync_batch()`

## 🔄 Upgrading from v7.6

**Fully Compatible** - Config and CSV files work directly. Just replace the .py file.

---
---

# 中文版本

## 🐛 Bug修复

### 0. **修复配置文件路径问题** ⭐ 新增
- **问题**: 使用相对路径查找config_v7.json，从不同目录启动程序时找不到配置文件
- **修复**: 改为使用程序所在目录的绝对路径，并添加详细的调试日志
- **影响**: 配置文件现在总能被正确读取和保存，无论从哪个目录启动程序

### 1. **修复重复保存问题**
- **问题**: `append_row_to_disk`每次都追加数据，导致working_csv中可能出现重复记录
- **修复**: 改为读取-更新-重写模式，确保每个索引只保存一次
- **影响**: 提高数据完整性，减少文件体积

### 2. **改进换行符处理**
- **问题**: Visual QA窗口只替换`\n`，在Windows系统可能遗漏`\r\n`
- **修复**: 现在同时处理`\r\n`、`\r`和`\n`三种换行符
- **影响**: 跨平台兼容性更好

### 3. **增加导入译文反馈**
- **问题**: 导入CSV时，格式不匹配的行被静默跳过，用户不知情
- **修复**: 现在会统计并显示跳过的行数
- **影响**: 用户能更清楚地了解导入结果

### 4. **价格输入验证**
- **问题**: 成本估算没有验证用户输入，可能导致错误
- **修复**: 添加输入验证，确保价格为非负数
- **影响**: 更稳定的成本估算

### 5. **批量翻译429错误重试**
- **问题**: 遇到API rate limit (429错误)时直接跳过，不重试
- **修复**: 添加智能重试机制，最多重试3次，等待时间递增(15s, 30s, 45s)
- **影响**: 批量翻译更可靠

### 6. **Visual QA字体fallback**
- **问题**: 如果字体配置失败可能导致宽度检测出错
- **修复**: 添加默认字体fallback (Microsoft YaHei 12pt)
- **影响**: Visual QA更稳定

## 📊 技术细节

### 改动的函数:
- `CONFIG_FILE`, `save_config()`, `load_config()`
- `append_row_to_disk()`, `VisualQAWindow.on_target_edit()`
- `get_max_line_width()`, `update_cost_display()`
- `import_translations_csv()`, `_fetch_ai_sync_batch()`

## 🔄 从v7.6升级

**完全兼容** - 配置文件和CSV文件可直接使用。只需替换.py文件。

---
---

# 日本語版

## 🐛 バグ修正

### 0. **設定ファイルパスの問題を修正** ⭐ 新機能
- **問題**: config_v7.jsonに相対パスを使用し、異なるディレクトリから起動すると設定が見つからない
- **修正**: プログラムのディレクトリの絶対パスを使用するように変更、詳細なデバッグログを追加
- **影響**: 起動ディレクトリに関係なく、設定ファイルが常に正しく読み込まれ保存される

### 1. **重複保存の問題を修正**
- **問題**: `append_row_to_disk`が毎回データを追加し、重複レコードが発生する可能性
- **修正**: 読み取り-更新-書き直しモードに変更、各インデックスが一度だけ保存される
- **影響**: データ整合性の向上、ファイルサイズの削減

### 2. **改行処理の強化**
- **問題**: Visual QAウィンドウが`\n`のみを置換し、Windowsで`\r\n`を見逃す可能性
- **修正**: `\r\n`、`\r`、`\n`の改行を処理
- **影響**: クロスプラットフォーム互換性の向上

### 3. **翻訳インポートフィードバックの追加**
- **問題**: CSV読み込み時、一致しない行が静かにスキップされる
- **修正**: スキップされた行数をカウントして表示
- **影響**: ユーザーがインポート結果をより明確に把握できる

### 4. **価格入力検証**
- **問題**: コスト推定がユーザー入力を検証せず、エラーの原因になる可能性
- **修正**: 入力検証を追加、価格が非負であることを確認
- **影響**: より安定したコスト推定

### 5. **バッチ翻訳429リトライロジック**
- **問題**: APIレート制限（429エラー）に達すると、リトライせずにスキップ
- **修正**: スマートリトライメカニズムを追加、最大3回リトライ（15秒、30秒、45秒待機）
- **影響**: より信頼性の高いバッチ翻訳

### 6. **Visual QAフォントフォールバック**
- **問題**: フォント設定の失敗が幅検出エラーを引き起こす可能性
- **修正**: デフォルトフォントフォールバックを追加（Microsoft YaHei 12pt）
- **影響**: より安定したVisual QA

## 📊 技術的詳細

### 変更された関数:
- `CONFIG_FILE`, `save_config()`, `load_config()`
- `append_row_to_disk()`, `VisualQAWindow.on_target_edit()`
- `get_max_line_width()`, `update_cost_display()`
- `import_translations_csv()`, `_fetch_ai_sync_batch()`

## 🔄 v7.6からのアップグレード

**完全互換** - 設定ファイルとCSVファイルは直接使用可能。.pyファイルを置き換えるだけ。
