from datetime import datetime


class Helpers:
    """工具类"""

    @staticmethod
    def format_date(date_str: str) -> str:
        """格式化日期"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # 转换为中文星期
            weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
            weekday = weekdays[date_obj.weekday()]

            # 如果是今天或明天
            today = datetime.now().date()
            if date_obj.date() == today:
                return "今天"
            elif date_obj.date() == today.replace(day=today.day + 1):
                return "明天"
            else:
                return f"{date_obj.month}/{date_obj.day} {weekday}"
        except:
            return date_str

    @staticmethod
    def format_time(time_str: str) -> str:
        """格式化时间"""
        try:
            time_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
            return time_obj.strftime("%H:%M")
        except:
            return time_str