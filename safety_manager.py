"""
Safety Manager Module for Game Translator Helper
Handles API safety protections, daily quotas, and cost limits
Version: 7.7
"""

import os
import json
from datetime import datetime, date
import time


class SafetyManager:
    """管理 API 安全保护的类"""

    def __init__(self, config_file="safety_config.json"):
        self.config_file = config_file

        # 默认设置
        self.daily_translation_limit = 1000  # 每日翻译条数上限
        self.daily_cost_limit = 5.0  # 每日费用上限（美元）
        self.batch_confirm_threshold = 50  # 批量翻译确认阈值
        self.translation_interval = 4.0  # 翻译间隔（秒）
        self.max_consecutive_errors = 3  # 最大连续错误次数
        self.limits_enabled = True  # 是否启用限制

        # 运行时数据
        self.today_date = str(date.today())
        self.today_translation_count = 0
        self.today_cost = 0.0
        self.consecutive_errors = 0
        self.last_translation_time = 0

        # 加载配置
        self.load_config()

    def load_config(self):
        """从配置文件加载设置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 加载设置
                self.daily_translation_limit = data.get('daily_translation_limit', 1000)
                self.daily_cost_limit = data.get('daily_cost_limit', 5.0)
                self.batch_confirm_threshold = data.get('batch_confirm_threshold', 50)
                self.translation_interval = data.get('translation_interval', 4.0)
                self.max_consecutive_errors = data.get('max_consecutive_errors', 3)
                self.limits_enabled = data.get('limits_enabled', True)

                # 加载今日统计
                saved_date = data.get('today_date', str(date.today()))
                if saved_date == str(date.today()):
                    # 同一天，继续累计
                    self.today_translation_count = data.get('today_translation_count', 0)
                    self.today_cost = data.get('today_cost', 0.0)
                else:
                    # 新的一天，重置计数
                    self.today_translation_count = 0
                    self.today_cost = 0.0
                    self.today_date = str(date.today())
                    self.save_config()  # 保存新日期

        except Exception as e:
            print(f"Failed to load safety config: {e}")
            self.save_config()  # 创建默认配置

    def save_config(self):
        """保存配置到文件"""
        try:
            data = {
                'daily_translation_limit': self.daily_translation_limit,
                'daily_cost_limit': self.daily_cost_limit,
                'batch_confirm_threshold': self.batch_confirm_threshold,
                'translation_interval': self.translation_interval,
                'max_consecutive_errors': self.max_consecutive_errors,
                'limits_enabled': self.limits_enabled,
                'today_date': self.today_date,
                'today_translation_count': self.today_translation_count,
                'today_cost': self.today_cost
            }

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save safety config: {e}")

    def check_can_translate(self, count=1, estimated_cost=0.0):
        """
        检查是否可以继续翻译

        Args:
            count: 要翻译的条数
            estimated_cost: 预估费用

        Returns:
            (can_translate: bool, reason: str)
        """
        if not self.limits_enabled:
            return True, ""

        # 检查日期是否变更
        if self.today_date != str(date.today()):
            self.reset_daily_stats()

        # 检查翻译条数上限
        if self.today_translation_count + count > self.daily_translation_limit:
            remaining = self.daily_translation_limit - self.today_translation_count
            return False, f"Daily translation limit reached ({self.today_translation_count}/{self.daily_translation_limit}). Remaining: {remaining}"

        # 检查费用上限
        if self.today_cost + estimated_cost > self.daily_cost_limit:
            remaining = self.daily_cost_limit - self.today_cost
            return False, f"Daily cost limit reached (${self.today_cost:.4f}/${self.daily_cost_limit:.2f}). Remaining: ${remaining:.4f}"

        return True, ""

    def check_translation_interval(self):
        """
        检查翻译间隔，如果太快则等待

        Returns:
            wait_time: 需要等待的时间（秒）
        """
        current_time = time.time()
        elapsed = current_time - self.last_translation_time

        if elapsed < self.translation_interval:
            wait_time = self.translation_interval - elapsed
            return wait_time

        return 0

    def record_translation(self, cost=0.0):
        """
        记录一次翻译

        Args:
            cost: 本次翻译的费用
        """
        # 检查日期是否变更
        if self.today_date != str(date.today()):
            self.reset_daily_stats()

        self.today_translation_count += 1
        self.today_cost += cost
        self.last_translation_time = time.time()
        self.consecutive_errors = 0  # 成功后重置错误计数

        # 自动保存
        self.save_config()

    def record_error(self):
        """记录一次错误"""
        self.consecutive_errors += 1

    def should_stop_on_error(self):
        """检查是否应该因为连续错误而停止"""
        return self.consecutive_errors >= self.max_consecutive_errors

    def reset_daily_stats(self):
        """重置每日统计"""
        self.today_date = str(date.today())
        self.today_translation_count = 0
        self.today_cost = 0.0
        self.consecutive_errors = 0
        self.save_config()

    def get_daily_stats(self):
        """
        获取今日统计信息

        Returns:
            dict: 包含各项统计数据
        """
        # 检查日期是否变更
        if self.today_date != str(date.today()):
            self.reset_daily_stats()

        translation_percent = (self.today_translation_count / self.daily_translation_limit * 100) if self.limits_enabled else 0
        cost_percent = (self.today_cost / self.daily_cost_limit * 100) if self.limits_enabled else 0

        return {
            'date': self.today_date,
            'translation_count': self.today_translation_count,
            'translation_limit': self.daily_translation_limit,
            'translation_remaining': max(0, self.daily_translation_limit - self.today_translation_count),
            'translation_percent': min(100, translation_percent),
            'cost': self.today_cost,
            'cost_limit': self.daily_cost_limit,
            'cost_remaining': max(0, self.daily_cost_limit - self.today_cost),
            'cost_percent': min(100, cost_percent),
            'limits_enabled': self.limits_enabled
        }

    def disable_limits(self):
        """临时解除限制"""
        self.limits_enabled = False
        self.save_config()

    def enable_limits(self):
        """启用限制"""
        self.limits_enabled = True
        self.save_config()

    def update_settings(self, daily_limit=None, cost_limit=None, batch_threshold=None,
                       interval=None, max_errors=None):
        """
        更新设置

        Args:
            daily_limit: 每日翻译上限
            cost_limit: 每日费用上限
            batch_threshold: 批量确认阈值
            interval: 翻译间隔
            max_errors: 最大连续错误数
        """
        if daily_limit is not None:
            self.daily_translation_limit = daily_limit
        if cost_limit is not None:
            self.daily_cost_limit = cost_limit
        if batch_threshold is not None:
            self.batch_confirm_threshold = batch_threshold
        if interval is not None:
            self.translation_interval = interval
        if max_errors is not None:
            self.max_consecutive_errors = max_errors

        self.save_config()
