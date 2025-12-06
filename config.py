import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'weather-app-secret-key')
    DEBUG = True

    # 城市坐标数据
    CITIES = {
        "北京": {"lat": 39.9042, "lon": 116.4074},
        "上海": {"lat": 31.2304, "lon": 121.4737},
        "广州": {"lat": 23.1291, "lon": 113.2644},
        "深圳": {"lat": 22.5431, "lon": 114.0579},
        "成都": {"lat": 30.5728, "lon": 104.0668},
        "杭州": {"lat": 30.2741, "lon": 120.1551},
        "西安": {"lat": 34.3416, "lon": 108.9398},
        "武汉": {"lat": 30.5928, "lon": 114.3055},
        "南京": {"lat": 32.0603, "lon": 118.7969},
        "重庆": {"lat": 29.5630, "lon": 106.5516},
    }

    # API配置
    OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"