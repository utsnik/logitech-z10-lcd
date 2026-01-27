"""
Z-10 System Monitor App
Displays CPU, RAM, and Time on the LCD
"""

import time
import psutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from z10_driver import Z10LCD, create_canvas

def main():
    print("Starting Z-10 Monitor...")
    print("Press Ctrl+C to stop.")
    
    lcd = Z10LCD()
    try:
        lcd.connect()
        print("[OK] Connected to Z-10 LCD")
        
        # Load Fonts
        try:
            # Try to load standard Windows fonts
            font_large = ImageFont.truetype("arial.ttf", 16)
            font_med = ImageFont.truetype("arialbd.ttf", 11) # Bold
            font_small = ImageFont.truetype("arial.ttf", 9)
        except IOError:
            print("Warning: Arial font not found, using default.")
            font_large = ImageFont.load_default()
            font_med = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        while True:
            # Create a new blank frame
            canvas = create_canvas()
            draw = ImageDraw.Draw(canvas)
            
            # --- Get System Info ---
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().percent
            current_time = datetime.now().strftime("%H:%M")
            date_str = datetime.now().strftime("%a %d %b")
            
            # --- Draw UI ---
            # Layout:
            # [TIME]      [CPU Graph]
            # [DATE]      CPU: XX% RAM: XX%
            
            # Draw Time (Left)
            # Offset x=1, y=-2 to center the large font vertically in the top half
            draw.text((1, -2), current_time, font=font_large, fill=1)
            draw.text((3, 22), date_str.upper(), font=font_small, fill=1)
            
            # Vertical Divider Line
            draw.line([55, 2, 55, 40], fill=1)
            
            # Stats (Right)
            draw.text((60, 2), f"CPU: {int(cpu_usage)}%", font=font_med, fill=1)
            draw.text((60, 14), f"RAM: {int(ram_usage)}%", font=font_med, fill=1)
            
            # Mini Graph (CPU History/Load Bar)
            # Box is at bottom right
            # Width available: 160 - 60 = 100 pixels.
            # Height: 30 to 40
            
            # Draw Outline
            draw.rectangle([60, 28, 156, 38], outline=1)
            
            # Draw Fill based on CPU
            fill_width = int((cpu_usage / 100.0) * 94) # 94 pixels max width inside
            if fill_width > 0:
                draw.rectangle([62, 30, 62 + fill_width, 36], fill=1)

            # Send to LCD
            lcd.display_image(canvas)
            
            # Wait 1 second
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        lcd.clear()
        lcd.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    main()
