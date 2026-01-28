from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import json
import threading
import time

class WeatherPlugin(BasePlugin):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Weather"
        try:
            self.font_temp = ImageFont.truetype("arialbd.ttf", 28)
            self.font_detail = ImageFont.truetype("arial.ttf", 10)
        except:
            self.font_temp = ImageFont.load_default()
            self.font_detail = ImageFont.load_default()
            
        self.weather_data = None
        self.last_fetch = 0
        self.fetching = False
        self.error_msg = ""
        
        # Default to a safe coordinate (London) if auto-IP fails
        # Users can edit this in source for now
        self.lat = 51.5074
        self.lon = -0.1278

    def _fetch_weather(self):
        self.fetching = True
        try:
            # 1. Get Location (Auto-IP)
            # Using ip-api.com (Free, no key)
            try:
                with urllib.request.urlopen("http://ip-api.com/json/", timeout=3) as url:
                    loc_data = json.loads(url.read().decode())
                    if loc_data['status'] == 'success':
                        self.lat = loc_data['lat']
                        self.lon = loc_data['lon']
            except:
                pass # Fallback to default/previous coordinates

            # 2. Get Weather
            url = f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}&current_weather=true"
            
            req = urllib.request.Request(url, headers={'User-Agent': 'Z10LCD/1.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                self.weather_data = data['current_weather']
                self.error_msg = ""
                
        except Exception as e:
            self.error_msg = "Conn Error"
            print(f"Weather Error: {e}")
        finally:
            self.fetching = False
            self.last_fetch = time.time()

    def update(self):
        # Fetch every 15 mins (900s)
        if time.time() - self.last_fetch > 900 and not self.fetching:
            threading.Thread(target=self._fetch_weather, daemon=True).start()

        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)
        
        if self.weather_data:
            # Temp
            temp = self.weather_data['temperature']
            draw.text((5, 5), f"{temp:.1f}°C", font=self.font_temp, fill=1)
            
            # WMO Code Parse
            code = self.weather_data['weathercode']
            cond = self.get_wmo_desc(code)
            
            draw.text((90, 10), cond, font=self.font_detail, fill=1)
            draw.text((90, 25), f"Wind: {self.weather_data['windspeed']}km/h", font=self.font_detail, fill=1)
        
        elif self.error_msg:
             draw.text((10, 15), self.error_msg, font=self.font_detail, fill=1)
        else:
             draw.text((10, 15), "Loading...", font=self.font_detail, fill=1)
             
        # Force refresh info
        if self.fetching:
            draw.rectangle([155, 0, 158, 3], fill=1)

        return img
        
    def get_wmo_desc(self, code):
        # Simple WMO code lookup
        if code == 0: return "Clear Sky"
        if code in [1,2,3]: return "Partly Cloud"
        if code in [45,48]: return "Fog"
        if code in [51,53,55]: return "Drizzle"
        if code in [61,63,65]: return "Rain"
        if code in [71,73,75]: return "Snow"
        if code in [80,81,82]: return "Rain Showers"
        if code in [95,96,99]: return "Thunderstorm"
        return "Unknown"

    def handle_input(self, btn_id):
        # Button 1 forces refresh
        if btn_id == 1:
            self.last_fetch = 0 
            return True
        return True
