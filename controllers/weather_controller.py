from datetime import datetime
from flask import render_template, request, jsonify

from config import Config
from models import WeatherModel
from utils import Helpers


class WeatherController:
    """天气控制器"""

    def __init__(self):
        self.model = WeatherModel()
        self.helpers = Helpers()

    def index(self):
        """首页"""
        city_name = "北京"
        city_data = Config.CITIES.get(city_name)

        if city_data:
            weather_data = self.model.fetch_weather_data(
                city_data["lat"], city_data["lon"], city_name)
        else:
            weather_data = None

        return render_template(
            'index.html',
            weather_data=weather_data,
            cities=Config.CITIES,
            current_city=city_name,
            get_weather_icon=self.model.get_weather_icon,
            get_weather_color=self.model.get_weather_color,
            get_weather_description=self.model.get_weather_description,
            format_date=self.helpers.format_date,
            format_time=self.helpers.format_time,
            now=datetime.now()
        )

    def get_city_weather(self, city_name: str):
        """获取指定城市的天气"""
        city_data = Config.CITIES.get(city_name)

        if not city_data:
            return jsonify({"error": "城市不存在"}), 404

        weather_data = self.model.fetch_weather_data(
            city_data["lat"], city_data["lon"], city_name)

        if not weather_data:
            return jsonify({"error": "获取天气数据失败"}), 500

        # 转换为JSON响应
        response_data = {
            "city": weather_data["city"],
            "current": weather_data["current"],
            "daily": weather_data["daily"],
            "average_temp": weather_data.get("average_temp"),
            "units": weather_data.get("units", {})
        }

        return jsonify(response_data)

    def get_weather_by_param(self):
        """通过参数获取天气"""
        city_name = request.args.get('city', '北京')
        city_data = Config.CITIES.get(city_name)

        if not city_data:
            return jsonify({"error": "城市不存在"}), 404

        weather_data = self.model.fetch_weather_data(
            city_data["lat"], city_data["lon"], city_name)

        if not weather_data:
            return jsonify({"error": "获取天气数据失败"}), 500

        return render_template(
            'index.html',
            weather_data=weather_data,
            current_city=city_name,
            get_weather_icon=self.model.get_weather_icon,
            get_weather_color=self.model.get_weather_color,
            get_weather_description=self.model.get_weather_description,
            format_date=self.helpers.format_date,
            format_time=self.helpers.format_time,
            now=datetime.now()
        )