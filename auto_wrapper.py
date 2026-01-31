"""
Auto Wrapper Module v2.1
自动换行模块 - 用于 Game Translator Helper

核心逻辑：
  1. 以原文行数作为目标行数
  2. 优先在句末标点（。！？）处换行
  3. 其次在句中标点（，、；：）处换行
  4. 尽量平均分配每行长度
  5. 绝不在特殊代码内部断开

作者：Claude Code Assistant
版本：v2.1 (2026-01-29)

更新日志：
  v2.1 - 修复中日文合并时产生多余空格的问题
         原因：之前使用 " ".join() 连接各行，对 CJK 语言不适用
         修复：添加 _should_add_space() 智能判断是否需要空格
"""

import re
from tkinter import font
import tkinter as tk


class AutoWrapper:
    """自动换行处理器 v2.1"""

    def __init__(self,
                 newline_code="{换行}",
                 filter_regex=r"[<＜].*?[：:](.*?)[>＞]",
                 filter_repl=r"\1",
                 filter_enabled=True,
                 font_family="Microsoft YaHei",
                 font_size=12):
        """
        初始化自动换行器

        Args:
            newline_code: 换行符代码，如 "{换行}"
            filter_regex: 视觉过滤器正则表达式
            filter_repl: 过滤器替换字符串
            filter_enabled: 是否启用过滤器
            font_family: 字体名称
            font_size: 字体大小
        """
        self.newline_code = newline_code
        self.filter_regex = filter_regex
        self.filter_repl = filter_repl
        self.filter_enabled = filter_enabled
        self.font_family = font_family
        self.font_size = font_size
        self._font = None

    def _ensure_font(self):
        """确保字体对象已创建"""
        if self._font is None:
            try:
                self._font = font.Font(family=self.font_family, size=self.font_size)
            except:
                pass

    def get_visual_text(self, raw_text):
        """获取视觉文本（过滤特殊代码后）"""
        if not raw_text:
            return raw_text
        if not self.filter_enabled or not self.filter_regex:
            return raw_text
        try:
            filtered = re.sub(self.filter_regex, self.filter_repl, raw_text)
            return filtered
        except:
            return raw_text

    def measure_width(self, text):
        """测量文本宽度（像素）"""
        self._ensure_font()
        if self._font:
            try:
                return self._font.measure(text)
            except:
                pass
        # 回退估算
        width = 0
        for char in text:
            width += self.font_size if ord(char) > 127 else self.font_size // 2
        return width

    def find_special_code_ranges(self, text):
        """找出所有特殊代码的位置范围"""
        ranges = []
        patterns = [
            r"[<＜][^>＞]*[>＞]",  # Ruby/HTML 标签
            r"\{[^}]+\}",          # 变量标记
            r"\[[^\]]+\]",         # 方括号标记
        ]
        for pattern in patterns:
            try:
                for match in re.finditer(pattern, text):
                    ranges.append((match.start(), match.end()))
            except:
                pass
        ranges.sort(key=lambda x: x[0])
        # 合并重叠范围
        merged = []
        for start, end in ranges:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        return merged

    def is_in_code(self, pos, code_ranges):
        """检查位置是否在特殊代码内"""
        for start, end in code_ranges:
            if start <= pos < end:
                return True
        return False

    def find_break_candidates(self, text, code_ranges):
        """
        找出所有可能的断点位置，按优先级分类

        Returns:
            dict: {
                'sentence_end': [...],    # 句末标点后 (。！？!?)
                'clause_end': [...],      # 句中标点后 (，、；：,;:)
                'any_position': [...]     # 任意非代码位置
            }
        """
        sentence_end_chars = "。！？!?"
        clause_end_chars = "，、；：,;:"

        candidates = {
            'sentence_end': [],
            'clause_end': [],
            'any_position': []
        }

        for i in range(1, len(text)):
            # 跳过代码内部
            if self.is_in_code(i, code_ranges):
                continue

            prev_char = text[i - 1]

            if prev_char in sentence_end_chars:
                candidates['sentence_end'].append(i)
            elif prev_char in clause_end_chars:
                candidates['clause_end'].append(i)
            else:
                candidates['any_position'].append(i)

        return candidates

    def split_into_n_lines(self, text, target_lines, max_width):
        """
        将文本分成 n 行，尽量平均分配

        核心算法：
        1. 计算目标每行长度 = 总长度 / 目标行数
        2. 在目标位置附近寻找最佳断点（优先标点）
        3. 如果找不到好的断点，适当调整

        Args:
            text: 要分行的文本（不含换行符）
            target_lines: 目标行数
            max_width: 最大宽度限制

        Returns:
            list: 分行后的文本列表
        """
        if target_lines <= 1:
            return [text]

        code_ranges = self.find_special_code_ranges(text)
        candidates = self.find_break_candidates(text, code_ranges)

        # 合并所有候选断点，带优先级标记
        all_breaks = []
        for pos in candidates['sentence_end']:
            all_breaks.append((pos, 0))  # 优先级 0 最高
        for pos in candidates['clause_end']:
            all_breaks.append((pos, 1))
        for pos in candidates['any_position']:
            all_breaks.append((pos, 2))

        all_breaks.sort(key=lambda x: x[0])

        # 计算视觉文本的总长度
        visual_text = self.get_visual_text(text)
        total_width = self.measure_width(visual_text)

        # 目标每行宽度
        target_width_per_line = total_width / target_lines

        # 贪心算法：从前往后，在接近目标宽度的位置寻找最佳断点
        result_lines = []
        current_start = 0

        for line_num in range(target_lines - 1):  # 最后一行不需要找断点
            remaining_lines = target_lines - line_num
            remaining_text = text[current_start:]
            remaining_visual = self.get_visual_text(remaining_text)
            remaining_width = self.measure_width(remaining_visual)

            # 这一行的目标宽度
            this_line_target = remaining_width / remaining_lines

            # 在候选断点中找最接近目标的
            best_break = None
            best_score = float('inf')

            for pos, priority in all_breaks:
                if pos <= current_start:
                    continue

                # 计算到这个断点的宽度
                segment = text[current_start:pos]
                visual_segment = self.get_visual_text(segment)
                segment_width = self.measure_width(visual_segment)

                # 不能超过最大宽度太多
                if segment_width > max_width * 1.2:
                    continue

                # 计算与目标宽度的差距
                width_diff = abs(segment_width - this_line_target)

                # 综合评分：宽度差距 + 优先级惩罚
                # 标点断点有很大优势
                score = width_diff + priority * 50

                # 如果宽度差距很小，标点优势更大
                if width_diff < this_line_target * 0.3:
                    score = width_diff + priority * 100

                if score < best_score:
                    best_score = score
                    best_break = pos

            if best_break is None:
                # 找不到好的断点，取最接近目标宽度的任意位置
                for pos, priority in all_breaks:
                    if pos <= current_start:
                        continue
                    segment = text[current_start:pos]
                    visual_segment = self.get_visual_text(segment)
                    if self.measure_width(visual_segment) <= max_width:
                        best_break = pos

            if best_break is None:
                # 实在找不到，把剩余文本作为一行
                break

            # 添加这一行
            line = text[current_start:best_break].rstrip()
            result_lines.append(line)
            current_start = best_break

            # 跳过开头的空格
            while current_start < len(text) and text[current_start] == ' ':
                current_start += 1

        # 添加最后一行
        if current_start < len(text):
            result_lines.append(text[current_start:])

        return result_lines

    def _is_cjk_char(self, char):
        """判断字符是否为中日韩字符"""
        if not char:
            return False
        code = ord(char)
        return (0x4E00 <= code <= 0x9FFF or    # CJK 基本
                0x3040 <= code <= 0x30FF or    # 日文假名
                0x3400 <= code <= 0x4DBF or    # CJK 扩展A
                0xF900 <= code <= 0xFAFF or    # CJK 兼容
                0xFF00 <= code <= 0xFFEF or    # 全角字符
                0x20000 <= code <= 0x2A6DF)    # CJK 扩展B

    def _should_add_space(self, prev_char, next_char):
        """判断两个字符之间是否需要空格"""
        if not prev_char or not next_char:
            return False
        # 中日韩标点符号
        cjk_punct = "。，、！？；：""''（）《》【】・…—"
        # 如果两边都是 CJK 字符，不加空格
        if self._is_cjk_char(prev_char) and self._is_cjk_char(next_char):
            return False
        # 如果一边是 CJK 标点符号，不加空格
        if prev_char in cjk_punct or next_char in cjk_punct:
            return False
        # 如果一边是 CJK，另一边是英文，不加空格（保持原样）
        if self._is_cjk_char(prev_char) or self._is_cjk_char(next_char):
            return False
        # 英文之间加空格
        return True

    def auto_wrap(self, text, max_width, source_lines=None, max_lines=None):
        """
        自动换行处理

        Args:
            text: 原始译文（可能已包含换行符代码）
            max_width: 最大宽度限制（像素）
            source_lines: 原文行数（作为目标行数）
            max_lines: 最大行数限制

        Returns:
            dict: {
                'success': bool,
                'result': str,
                'lines': int,
                'message': str
            }
        """
        if not text or not text.strip():
            return {
                'success': True,
                'result': text,
                'lines': 0,
                'message': 'Empty text'
            }

        # 将现有换行符转为临时标记（同时处理真实换行和换行符代码）
        TEMP_NL = "\x00NL\x00"
        working = text.replace("\n", TEMP_NL)  # 先处理真实换行符
        working = working.replace(self.newline_code, TEMP_NL)  # 再处理换行符代码

        # 统计现有行数
        existing_lines = working.split(TEMP_NL)
        existing_line_count = len(existing_lines)

        # 确定目标行数
        if source_lines and source_lines > 0:
            target_lines = source_lines
        elif max_lines and max_lines > 0:
            target_lines = max_lines
        else:
            target_lines = existing_line_count

        # 将所有行合并成一个字符串（用于重新分配）
        # v2.1 修复: 中日文之间不加空格，避免产生多余空格
        lines_stripped = [line.strip() for line in existing_lines if line.strip()]
        merged_parts = []
        for i, line in enumerate(lines_stripped):
            merged_parts.append(line)
            if i < len(lines_stripped) - 1:
                next_line = lines_stripped[i + 1]
                if line and next_line:
                    if self._should_add_space(line[-1], next_line[0]):
                        merged_parts.append(' ')
        merged = ''.join(merged_parts)

        # 检查合并后的文本是否需要分行
        visual_merged = self.get_visual_text(merged)
        total_width = self.measure_width(visual_merged)

        if total_width <= max_width and target_lines <= 1:
            # 一行就够了
            return {
                'success': True,
                'result': merged,
                'lines': 1,
                'message': 'Single line sufficient'
            }

        # 分行处理
        result_lines = self.split_into_n_lines(merged, target_lines, max_width)

        # 检查结果
        final_line_count = len(result_lines)
        result = self.newline_code.join(result_lines)

        # 验证每行宽度
        all_ok = True
        for line in result_lines:
            visual = self.get_visual_text(line)
            if self.measure_width(visual) > max_width * 1.1:  # 允许 10% 误差
                all_ok = False
                break

        if max_lines and final_line_count > max_lines:
            return {
                'success': False,
                'result': result,
                'lines': final_line_count,
                'message': f'Exceeded max lines: {final_line_count} > {max_lines}'
            }

        return {
            'success': True,
            'result': result,
            'lines': final_line_count,
            'message': f'Wrapped into {final_line_count} lines'
        }


# 便捷函数
_wrapper = None

def get_wrapper():
    global _wrapper
    if _wrapper is None:
        _wrapper = AutoWrapper()
    return _wrapper

def auto_wrap_text(text, max_width, newline_code="{换行}",
                   filter_regex=None, filter_repl=None, filter_enabled=True,
                   font_size=12, source_lines=None, max_lines=None):
    """
    便捷函数：自动换行

    Args:
        text: 原始文本
        max_width: 最大宽度（像素）
        newline_code: 换行符代码
        filter_regex: 过滤器正则
        filter_repl: 过滤器替换
        filter_enabled: 是否启用过滤器
        font_size: 字体大小
        source_lines: 原文行数（目标行数）
        max_lines: 最大行数限制

    Returns:
        dict
    """
    w = get_wrapper()
    w.newline_code = newline_code
    w.font_size = font_size
    w.filter_enabled = filter_enabled
    w._font = None

    if filter_regex is not None:
        w.filter_regex = filter_regex
    if filter_repl is not None:
        w.filter_repl = filter_repl

    return w.auto_wrap(text, max_width, source_lines, max_lines)


# 测试
if __name__ == "__main__":
    wrapper = AutoWrapper(newline_code="{换行}", font_size=12)

    print("=" * 60)
    print("Auto Wrapper v2.0 Test")
    print("=" * 60)

    # 测试用例：用户提供的例子
    # 原文 4 行
    source = """それから僕の生活はジェーン中心に
なった。えさはもちろん欠かさず、
毎日仲良しブラシでブラッシング。
僕たちはどんどん仲良くなった。"""

    # 译文（需要换行成 4 行）
    target = "从那以后，我的生活就以简为中心了。喂食当然不能少，每天也都要用友好毛刷给它梳理毛发。我们的关系变得越来越亲密。"

    source_line_count = len(source.strip().split('\n'))
    print(f"\nSource lines: {source_line_count}")
    print(f"Target (raw): {target}")

    result = wrapper.auto_wrap(target, max_width=300, source_lines=source_line_count)
    print(f"\nWrapped result:")
    for i, line in enumerate(result['result'].split('{换行}'), 1):
        print(f"  Line {i}: {line}")
    print(f"Lines: {result['lines']}")
    print(f"Message: {result['message']}")

    # 测试不同宽度
    print("\n" + "=" * 60)
    print("Test with different widths:")
    for width in [200, 250, 300, 350, 400]:
        r = wrapper.auto_wrap(target, max_width=width, source_lines=4)
        lines = r['result'].split('{换行}')
        print(f"\nWidth={width}px, Lines={len(lines)}:")
        for line in lines:
            visual = wrapper.get_visual_text(line)
            w = wrapper.measure_width(visual)
            print(f"  [{w:3d}px] {line}")
