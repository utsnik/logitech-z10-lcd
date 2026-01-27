from .base import BasePlugin
from PIL import Image, ImageDraw, ImageFont
import psutil
import time
from datetime import datetime
import subprocess

class EnhancedMonitorPlugin(BasePlugin):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.name = "Pro Stats"
        self.page = 1 # 1=Overall, 2=Thermal, 3=Fans(IO), 4=Info
        
        # GPU Stats
        self.gpu_temp = "N/A"
        self.gpu_util = "0"
        self.gpu_freq = "0"
        self.gpu_mem_freq = "0"
        self.gpu_power = "0"
        
        # CPU Stats
        self.cpu_temp = "N/A"
        
        self.last_gpu_check = 0
        self.last_cpu_check = 0

        # Load Fonts
        try:
            self.font_big = ImageFont.truetype("arialbd.ttf", 18)
            self.font_med = ImageFont.truetype("arial.ttf", 12)
            self.font_small = ImageFont.truetype("arial.ttf", 9)
        except:
            self.font_big = ImageFont.load_default()
            self.font_med = ImageFont.load_default()
            self.font_small = ImageFont.load_default()

    def get_gpu_info(self):
        if time.time() - self.last_gpu_check < 2.0:
            return
        try:
            # Query: Temp, Util, Graphics Clock, Memory Clock, Power Draw
            cmd = "nvidia-smi --query-gpu=temperature.gpu,utilization.gpu,clocks.gr,clocks.mem,power.draw --format=csv,noheader,nounits"
            output = subprocess.check_output(cmd, shell=True).decode().strip()
            parts = output.split(',')
            if len(parts) >= 5:
                self.gpu_temp = parts[0].strip()
                self.gpu_util = parts[1].strip()
                self.gpu_freq = parts[2].strip()
                self.gpu_mem_freq = parts[3].strip()
                self.gpu_power = parts[4].strip()
        except:
            pass
        self.last_gpu_check = time.time()

    def get_cpu_temp(self):
        if time.time() - self.last_cpu_check < 4.0:
            return
        try:
            # Attempt to get CPU Temp via WMI (Requires Admin)
            # This is the most common one that works on some systems without external tools
            cmd = "powershell -WindowStyle Hidden -Command \"(Get-WmiObject -Namespace root/wmi -Class MSAcpi_ThermalZoneTemperature).CurrentTemperature\""
            out = subprocess.check_output(cmd, shell=True).decode().strip()
            if out:
                # Convert from tenths of Kelvin to Celsius
                temp = (float(out) / 10.0) - 273.15
                self.cpu_temp = f"{temp:.0f}"
        except:
            self.cpu_temp = "N/A"
        self.last_cpu_check = time.time()

    def handle_input(self, btn_id):
        # Buttons 1-4 switch pages
        if btn_id in [1, 2, 3, 4]:
            self.page = btn_id
            return True
        return False

    def update(self):
        img = Image.new('1', (self.width, self.height), 0)
        draw = ImageDraw.Draw(img)

        # Header (Minimal)
        titles = {1: "SYS", 2: "THERM", 3: "NET/IO", 4: "CLOCKS"}
        title = titles.get(self.page, "STATS")
        draw.line([0, 7, 160, 7], fill=1)
        draw.text((2, -2), f"{title}", font=self.font_small, fill=1)
        draw.text((120, -2), f"P:{self.page}/4", font=self.font_small, fill=1)

        if self.page == 1: # OVERALL
            self.get_gpu_info()
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            procs = len(psutil.pids())
            draw.text((2, 10), f"CPU: {cpu}%", font=self.font_med, fill=1)
            draw.text((80, 10), f"RAM: {ram}%", font=self.font_med, fill=1)
            
            draw.text((2, 25), f"Procs: {procs}", font=self.font_med, fill=1)
            draw.text((80, 25), f"GPU: {self.gpu_util}%", font=self.font_med, fill=1)
            
        elif self.page == 2: # THERMAL
            self.get_gpu_info()
            self.get_cpu_temp()
            cpu_load = psutil.cpu_percent()
            
            draw.text((2, 10), f"GPU: {self.gpu_temp}°C  ({self.gpu_util}%)", font=self.font_med, fill=1)
            draw.text((2, 25), f"CPU: {self.cpu_temp}°C  ({cpu_load}%)", font=self.font_med, fill=1)
            
        elif self.page == 3: # NETWORK / DISK
            net = psutil.net_io_counters()
            sent = net.bytes_sent / (1024**2) 
            recv = net.bytes_recv / (1024**2) 
            draw.text((2, 10), f"In: {recv:.0f} MB", font=self.font_small, fill=1)
            draw.text((2, 20), f"Out: {sent:.0f} MB", font=self.font_small, fill=1)
            try:
                d = psutil.disk_usage('C:\\')
                free_gb = int(d.free / (1024**3))
                draw.text((80, 10), f"C: Free", font=self.font_small, fill=1)
                draw.text((80, 20), f"{free_gb} GB", font=self.font_med, fill=1)
            except: pass

        elif self.page == 4: # CLOCKS / POWER
            self.get_gpu_info()
            cpu_freq = psutil.cpu_freq().current
            
            draw.text((2, 8), f"CPU: {cpu_freq:.0f} MHz", font=self.font_small, fill=1)
            draw.text((2, 18), f"GPU: {self.gpu_freq} / {self.gpu_mem_freq} MHz", font=self.font_small, fill=1)
            # Power
            draw.text((2, 28), f"GPU Power: {self.gpu_power}W", font=self.font_small, fill=1)
            
            boot = datetime.fromtimestamp(psutil.boot_time())
            up = str(datetime.now() - boot).split('.')[0]
            draw.text((85, 28), f"Up: {up}", font=self.font_small, fill=1)

        return img
