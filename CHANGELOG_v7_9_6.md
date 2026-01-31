# GameTranslator v7.9.6 Changelog | 更新日志 | 変更履歴

> **This file is available in three languages | 本文档提供三种语言版本 | このファイルは3つの言語で利用可能です**
>
> - [English](#english-version)
> - [中文](#中文版本)
> - [日本語](#日本語版)

**Release Date | 发布日期 | リリース日**: 2026-01-31

---

# English Version

## What's New in v7.9.6 (Visual QA Final Edition)

### Bug Fixes

#### 1. Auto-Wrap Adding Extra Lines
- **Problem**: Clicking "Auto Wrap" button would add an extra blank line each time
- **Cause**: `auto_wrap()` only processed `{换行}` code, not real `\n` newlines in Text widget
- **Fix**: Now processes both real newlines and newline codes

#### 2. Find Next Issue False Positives
- **Problem**: "Find Next Issue" would find lines that were actually OK after visual filtering
- **Cause**: `check_row_overflow()` used virtual line count calculation, inconsistent with Visual QA window
- **Fix**: Simplified logic to only use hard line breaks, matching Visual QA behavior

#### 3. max_lines Judgment Inconsistency
- **Problem**: Lines with fewer lines than source were still flagged as overflow
- **Cause**: `find_next_overflow` used fixed `max_lines`, while Visual QA auto-sets per source line
- **Fix**: Removed `max_lines` check, only checks "target lines > source lines"

#### 4. Visual QA Window Buttons Compressed
- **Problem**: When MaxLines increased, bottom buttons would be compressed or hidden
- **Cause**: `main_frame` using `expand=True` packed before `nav_frame`
- **Fix**: Added dynamic window height adjustment in `update_layout()` (500-1200px range)

### New Features (v7.9.x Series)

#### Visual QA Enhancements
- **Auto-Wrap** - Intelligently wrap text at punctuation marks (。！？，、etc.)
- **Find Next Issue** - Scan and jump to next overflow problem
- **Ignore Line** - Mark lines that don't need checking (saved to disk)
- **Visual Filter** - Filter Ruby text `<tag:text>` for accurate width measurement
- **Dynamic Window Height** - Window auto-resizes when content grows
- **Undo/Redo** - Ctrl+Z/Y support in Visual QA editor

#### API Safety Protection (v7.7+)
- Daily translation limit (default: 1000/day)
- Daily cost limit (default: $5/day)
- Batch confirmation dialog (>50 items)
- 4-second translation interval (prevents 429 errors)
- Auto-stop on consecutive errors

### Technical Details

#### Modified Files:
- `GameTranslator7_9_6.py` - Main program (~4000 lines)
- `auto_wrapper.py` - Auto-wrap module (v2.1)
- `safety_manager.py` - API safety manager

#### Key Methods Changed:
- `VisualQAWindow.update_layout()` - Dynamic height
- `VisualQAWindow.__init__()` - `nav_frame` → `self.nav_frame`
- `check_row_overflow()` - Simplified overflow logic
- `find_next_overflow()` - Consistent with Visual QA
- `auto_wrap()` - Handle both `\n` and newline codes

## Upgrading from v7.6.1

**Fully Compatible** - Config and CSV files work directly.

New files:
- `auto_wrapper.py` - Required module
- `safety_manager.py` - Required module
- `safety_config.json` - Auto-generated

Just copy all `.py` files to your folder and run.

---
---

# 中文版本

## v7.9.6 新功能 (Visual QA 最终版)

### Bug 修复

#### 1. 自动换行增加空行
- **问题**: 点击"自动换行"按钮每次会增加一个空行
- **原因**: `auto_wrap()` 只处理了 `{换行}` 代码，未处理 Text 控件中的真实 `\n`
- **修复**: 现在同时处理真实换行符和换行符代码

#### 2. 查找下一个问题误报
- **问题**: "查找下一个问题"会找到经视觉过滤后正常的行
- **原因**: `check_row_overflow()` 使用虚拟行数计算，与 Visual QA 窗口不一致
- **修复**: 简化逻辑，只使用硬换行数，与 Visual QA 保持一致

#### 3. max_lines 判断不一致
- **问题**: 译文行数少于原文时仍被误判为溢出
- **原因**: `find_next_overflow` 使用固定 `max_lines`，而 Visual QA 根据每行原文自动设置
- **修复**: 移除 `max_lines` 检查，只检查"译文行数 > 原文行数"

#### 4. Visual QA 窗口按钮被压缩
- **问题**: 当 MaxLines 增加时，底部按钮会被压缩或隐藏
- **原因**: `main_frame` 使用 `expand=True` 且在 `nav_frame` 之前 pack
- **修复**: 在 `update_layout()` 中添加动态窗口高度调整 (500-1200px)

### 新功能 (v7.9.x 系列)

#### Visual QA 增强
- **自动换行** - 智能在标点处换行（。！？，、等）
- **查找下一个问题** - 扫描并跳转到下一个溢出问题
- **忽略功能** - 标记不需要检查的行（保存到磁盘）
- **视觉过滤器** - 过滤注音 `<标签:文本>` 以准确测量宽度
- **动态窗口高度** - 内容增加时窗口自动调整大小
- **撤销/重做** - Visual QA 编辑器支持 Ctrl+Z/Y

#### API 安全保护 (v7.7+)
- 每日翻译限制（默认：1000条/天）
- 每日费用上限（默认：$5/天）
- 批量翻译确认对话框（>50条时）
- 4秒翻译间隔（防止429错误）
- 连续错误时自动停止

### 技术细节

#### 修改的文件:
- `GameTranslator7_9_6.py` - 主程序 (~4000行)
- `auto_wrapper.py` - 自动换行模块 (v2.1)
- `safety_manager.py` - API 安全管理器

#### 关键方法修改:
- `VisualQAWindow.update_layout()` - 动态高度
- `VisualQAWindow.__init__()` - `nav_frame` → `self.nav_frame`
- `check_row_overflow()` - 简化溢出逻辑
- `find_next_overflow()` - 与 Visual QA 保持一致
- `auto_wrap()` - 同时处理 `\n` 和换行符代码

## 从 v7.6.1 升级

**完全兼容** - 配置文件和 CSV 文件可直接使用。

新增文件：
- `auto_wrapper.py` - 必需模块
- `safety_manager.py` - 必需模块
- `safety_config.json` - 自动生成

只需将所有 `.py` 文件复制到你的文件夹并运行。

---
---

# 日本語版

## v7.9.6 の新機能 (Visual QA 最終版)

### バグ修正

#### 1. 自動改行で空行が追加される
- **問題**: 「自動改行」ボタンをクリックするたびに空行が追加される
- **原因**: `auto_wrap()` が `{换行}` コードのみを処理し、Textウィジェットの実際の `\n` を処理しなかった
- **修正**: 実際の改行と改行コードの両方を処理

#### 2. 次の問題検索の誤検出
- **問題**: 「次の問題を検索」が視覚フィルタ後は正常な行を検出する
- **原因**: `check_row_overflow()` が仮想行数計算を使用し、Visual QAウィンドウと一致しない
- **修正**: ハード改行のみを使用するロジックに簡素化、Visual QAの動作と一致

#### 3. max_lines 判定の不一致
- **問題**: 原文より行数が少ない行がオーバーフローと判定される
- **原因**: `find_next_overflow` が固定の `max_lines` を使用、Visual QAは原文ごとに自動設定
- **修正**: `max_lines` チェックを削除、「訳文行数 > 原文行数」のみをチェック

#### 4. Visual QAウィンドウのボタンが圧縮される
- **問題**: MaxLinesが増加すると、下部のボタンが圧縮または非表示になる
- **原因**: `main_frame` が `expand=True` で `nav_frame` より先にpack
- **修正**: `update_layout()` に動的ウィンドウ高さ調整を追加 (500-1200px)

### 新機能 (v7.9.x シリーズ)

#### Visual QA 強化
- **自動改行** - 句読点（。！？，、など）で賢く改行
- **次の問題を検索** - 次のオーバーフロー問題をスキャンしてジャンプ
- **無視機能** - チェック不要な行をマーク（ディスクに保存）
- **視覚フィルタ** - ルビテキスト `<タグ:テキスト>` をフィルタして正確な幅測定
- **動的ウィンドウ高さ** - コンテンツ増加時にウィンドウが自動リサイズ
- **元に戻す/やり直し** - Visual QAエディタでCtrl+Z/Yサポート

#### API安全保護 (v7.7+)
- 日次翻訳制限（デフォルト：1000件/日）
- 日次コスト上限（デフォルト：$5/日）
- 一括翻訳確認ダイアログ（50件超）
- 4秒の翻訳間隔（429エラー防止）
- 連続エラー時の自動停止

### 技術的詳細

#### 変更されたファイル:
- `GameTranslator7_9_6.py` - メインプログラム (~4000行)
- `auto_wrapper.py` - 自動改行モジュール (v2.1)
- `safety_manager.py` - API安全マネージャー

#### 変更された主要メソッド:
- `VisualQAWindow.update_layout()` - 動的高さ
- `VisualQAWindow.__init__()` - `nav_frame` → `self.nav_frame`
- `check_row_overflow()` - オーバーフローロジック簡素化
- `find_next_overflow()` - Visual QAと一致
- `auto_wrap()` - `\n` と改行コードの両方を処理

## v7.6.1からのアップグレード

**完全互換** - 設定ファイルとCSVファイルは直接使用可能。

新規ファイル：
- `auto_wrapper.py` - 必須モジュール
- `safety_manager.py` - 必須モジュール
- `safety_config.json` - 自動生成

すべての `.py` ファイルをフォルダにコピーして実行するだけ。
