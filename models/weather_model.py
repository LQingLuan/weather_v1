import requests
from typing import Dict, Any, Optional

from config import Config


class WeatherModel:
    """天气数据模型"""

    # 天气代码映射
    WEATHER_CODES = {
        0: {"description": "晴朗", "icon": "sun", "color": "#FFD700"},
        1: {"description": "主要晴朗", "icon": "sun-cloud", "color": "#87CEEB"},
        2: {"description": "部分多云", "icon": "cloud-sun", "color": "#B0C4DE"},
        3: {"description": "阴天", "icon": "cloud", "color": "#808080"},
        45: {"description": "有雾", "icon": "fog", "color": "#D3D3D3"},
        48: {"description": "有雾", "icon": "fog", "color": "#D3D3D3"},
        51: {"description": "小雨", "icon": "drizzle", "color": "#4682B4"},
        53: {"description": "中雨", "icon": "rain", "color": "#4169E1"},
        55: {"description": "大雨", "icon": "rain-heavy", "color": "#00008B"},
        56: {"description": "冻雨", "icon": "sleet", "color": "#B0E0E6"},
        57: {"description": "冻雨", "icon": "sleet", "color": "#B0E0E6"},
        61: {"description": "小雨", "icon": "rain", "color": "#4682B4"},
        63: {"description": "中雨", "icon": "rain-heavy", "color": "#4169E1"},
        65: {"description": "大雨", "icon": "rain-heavy", "color": "#00008B"},
        66: {"description": "冻雨", "icon": "sleet", "color": "#B0E0E6"},
        67: {"description": "冻雨", "icon": "sleet", "color": "#B0E0E6"},
        71: {"description": "小雪", "icon": "snow", "color": "#F0F8FF"},
        73: {"description": "中雪", "icon": "snow", "color": "#E6E6FA"},
        75: {"description": "大雪", "icon": "snow-heavy", "color": "#ADD8E6"},
        77: {"description": "雪粒", "icon": "snow", "color": "#E6E6FA"},
        80: {"description": "阵雨", "icon": "showers", "color": "#4682B4"},
        81: {"description": "强阵雨", "icon": "showers-heavy", "color": "#4169E1"},
        82: {"description": "暴雨", "icon": "thunderstorm", "color": "#00008B"},
        85: {"description": "阵雪", "icon": "snow", "color": "#F0F8FF"},
        86: {"description": "强阵雪", "icon": "snow-heavy", "color": "#ADD8E6"},
        95: {"description": "雷暴", "icon": "thunderstorm", "color": "#4B0082"},
        96: {"description": "雷暴", "icon": "thunderstorm", "color": "#4B0082"},
        99: {"description": "强雷暴", "icon": "thunderstorm-heavy", "color": "#191970"},
    }

    @staticmethod
    def fetch_weather_data(latitude: float, longitude: float, city_name: str = "北京") -> Optional[Dict[str, Any]]:
        """从Open-Meteo API获取天气数据"""
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,sunrise,sunset",
                "current_weather": "true",
                "timezone": "auto",
                "forecast_days": 7
            }

            response = requests.get(Config.OPEN_METEO_URL, params=params, timeout=10)
            response.raise_for_status()

            weather_data = response.json()

            # 处理数据
            processed_data = {
                "city": city_name,
                "current": {
                    "temperature": weather_data.get("current_weather", {}).get("temperature"),
                    "weathercode": weather_data.get("current_weather", {}).get("weathercode"),
                    "windspeed": weather_data.get("current_weather", {}).get("windspeed"),
                    "winddirection": weather_data.get("current_weather", {}).get("winddirection"),
                    "is_day": weather_data.get("current_weather", {}).get("is_day") == 1,
                    "time": weather_data.get("current_weather", {}).get("time")
                },
                "daily": {
                    "time": weather_data.get("daily", {}).get("time", []),
                    "weathercode": weather_data.get("daily", {}).get("weathercode", []),
                    "temperature_2m_max": weather_data.get("daily", {}).get("temperature_2m_max", []),
                    "temperature_2m_min": weather_data.get("daily", {}).get("temperature_2m_min", []),
                    "sunrise": weather_data.get("daily", {}).get("sunrise", []),
                    "sunset": weather_data.get("daily", {}).get("sunset", [])
                },
                "units": weather_data.get("daily_units", {})
            }

            # 计算平均温度
            if processed_data["daily"]["temperature_2m_max"] and processed_data["daily"]["temperature_2m_min"]:
                temps_max = processed_data["daily"]["temperature_2m_max"]
                temps_min = processed_data["daily"]["temperature_2m_min"]
                processed_data["average_temp"] = sum(
                    (max_t + min_t) / 2 for max_t, min_t in zip(temps_max, temps_min)) / len(temps_max)
            else:
                processed_data["average_temp"] = None

            return processed_data

        except requests.exceptions.RequestException as e:
            print(f"获取天气数据时出错: {e}")
            return None
        except Exception as e:
            print(f"处理天气数据时出错: {e}")
            return None

    @classmethod
    def get_weather_icon(cls, weather_code: int, is_day: bool = True) -> str:
        """根据天气代码和时间获取图标类名"""
        weather_info = cls.WEATHER_CODES.get(weather_code, {"icon": "question", "color": "#808080"})
        icon_name = weather_info["icon"]

        # 如果是夜晚，调整图标
        if not is_day:
            if icon_name == "sun":
                icon_name = "moon"
            elif icon_name == "sun-cloud":
                icon_name = "cloud-moon"
            elif icon_name == "cloud-sun":
                icon_name = "cloud-moon"

        return f"wi wi-{icon_name}"

    @classmethod
    def get_weather_color(cls, weather_code: int) -> str:
        """根据天气代码获取颜色"""
        return cls.WEATHER_CODES.get(weather_code, {"color": "#808080"})["color"]

    @classmethod
    def get_weather_description(cls, weather_code: int) -> str:
        """根据天气代码获取中文描述"""
        return cls.WEATHER_CODES.get(weather_code, {"description": "未知天气"})["description"]