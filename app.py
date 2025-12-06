from flask import Flask
from config import Config
from controllers.weather_controller import WeatherController
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# 创建控制器实例
weather_controller = WeatherController()

@app.route('/')
def index():
    """首页"""
    return weather_controller.index()

@app.route('/weather/<city_name>')
def get_city_weather(city_name):
    """获取指定城市的天气"""
    return weather_controller.get_city_weather(city_name)

@app.route('/weather')
def get_weather():
    """通过参数获取天气"""
    return weather_controller.get_weather_by_param()

@app.context_processor
def inject_now():
    """注入当前时间到模板"""
    return {'now': datetime.now()}

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=5001)