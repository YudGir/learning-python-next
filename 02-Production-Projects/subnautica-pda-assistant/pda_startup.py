import asyncio
import edge_tts
import os
import time
import pygame
import soundfile as sf
import psutil
from datetime import datetime
from pedalboard import Pedalboard, Delay, Phaser, Gain

VOICE = "en-GB-SoniaNeural"
TITLE = "Fleet Admiral Yudha"

# KAMUS NOTIFIKASI V9.7
ALERTS = {
    "startup_morning": f"System reboot complete. Good morning, {TITLE}! All internal core modules are stable.",
    "startup_afternoon": f"Welcome back, {TITLE}! Please resume active operations at your earliest convenience.",
    "startup_evening": f"Welcome back, {TITLE}! Please resume active operations at your earliest convenience.",
    "startup_weekend": f"System reboot complete. Welcome back, {TITLE}! Standard duty protocols are suspended for the weekend cycle. Enjoy your rest.",
    "low_battery": "Warning! Power efficiency decreasing. Terminal battery capacity critical. Connect to an external power source immediately.",
    "charging": "External power grid connected. Initiating battery replenishment protocol.",
    "discharging": "External power disconnected. System is now operating on internal battery cells.",
    "sleep_warning": f"Attention, {TITLE}! It is now 10 PM. Biological scans detect elevated fatigue levels. It is highly recommended to log off and initiate rest protocols.",
    "lunch_warning": "Attention! Midday threshold reached. Data synchronization paused for biological replenishment.",
    "wifi_lost": "Alert! Local data network signal lost. System is now operating on offline database redundancy.",
    "wifi_connected": "Network signal restored. Synchronizing localized telemetry.",
    "ram_full": "Warning! Volatile memory capacity saturated. High risk of processing latency.",
    "storage_low": "Alert! Main storage matrix critical. Available sector space is insufficient.",
    "cpu_hot": "Emergency! Core temperature critical. Hardware thermal limits reached. Please optimize active processing tasks.",
    "hydrate": "Hydrate.",
    "time_1h": "Warning! Passing 1 hour of continuous operation. Mental stamina efficiency decreasing.",
    "time_2h": "Caution! Passing 2 hours of continuous operation. The local ecosystem features multiple academic hazards. Are you certain whatever you are doing is worth it?",
    "time_3h": "Emergency! Passing 3 hours of continuous operation. Critical cognitive overload detected. Surface immediately, Commander."
}

async def generate_and_apply_fx(text, output_filename):
    temp_mp3 = "temp_raw.mp3"
    communicate = edge_tts.Communicate(text, VOICE, rate="-3%", pitch="-3Hz")
    await communicate.save(temp_mp3)
    
    audio_data, sample_rate = sf.read(temp_mp3)
    board = Pedalboard([
        Phaser(rate_hz=1.0, depth=0.8, centre_frequency_hz=1000.0, feedback=0.4),
        Delay(delay_seconds=0.02, feedback=0.3, mix=0.3),
        Gain(gain_db=3.0)
    ])
    effected_audio = board(audio_data, sample_rate)
    sf.write(output_filename, effected_audio, sample_rate)
    
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

def play_alert(filename):
    if not os.path.exists(filename):
        return
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()
    pygame.mixer.quit()

def check_internet():
    try:
        gateways = psutil.net_if_stats()
        for interface, stats in gateways.items():
            if stats.isup and "loopback" not in interface.lower():
                return True
        return False
    except:
        return False

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(BASE_DIR)

    print(f"Mempersiapkan Master Audio v9.7 untuk {TITLE}...")
    for key, text in ALERTS.items():
        file_path = f"pda_{key}.wav"
        if not os.path.exists(file_path):
            print(f"Membuat audio untuk event: {key}")
            asyncio.run(generate_and_apply_fx(text, file_path))

    print(f"\n[AIE ENGINE v9.7 ONLINE] Selamat bertugas, {TITLE}!")
    
    # LOGIKA STARTUP
    now = datetime.now()
    current_hour = now.hour
    day_of_week = now.weekday()

    if day_of_week >= 5:
        play_alert("pda_startup_weekend.wav")
    else:
        if 5 <= current_hour < 12: play_alert("pda_startup_morning.wav")
        elif 12 <= current_hour < 18: play_alert("pda_startup_afternoon.wav")
        else: play_alert("pda_startup_evening.wav")
    
    # Setup Status Monitor
    last_plugged = psutil.sensors_battery().power_plugged
    last_internet = check_internet()
    low_battery_warned = False
    sleep_warning_played = False
    lunch_warning_played = False
    cpu_warned = False
    ram_warned = False
    storage_warned = False
    
    # TRACKING DURASI KERJA LAPTOP
    start_work_time = time.time()
    time_1h_played = False
    time_2h_played = False
    time_3h_played = False
    
    # Timer Pengingat Minum (Setiap 2 Jam = 7200 detik)
    start_hydration_timer = time.time()

    while True:
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = battery.power_plugged
        
        now = datetime.now()
        hour = now.hour
        minute = now.minute

        elapsed_time = time.time() - start_work_time

        # 1. PENGINGAT DURASI JAM NYATA
        if elapsed_time >= 3600 and not time_1h_played:
            play_alert("pda_time_1h.wav")
            time_1h_played = True
            
        if elapsed_time >= 7200 and not time_2h_played:
            play_alert("pda_time_2h.wav")
            time_2h_played = True
            
        if elapsed_time >= 10800 and not time_3h_played:
            play_alert("pda_time_3h.wav")
            time_3h_played = True

        # 2. PENGINGAT HARIAN
        if hour == 12 and minute == 0 and not lunch_warning_played:
            play_alert("pda_lunch_warning.wav")
            lunch_warning_played = True
        if hour == 12 and minute == 1: lunch_warning_played = False

        if hour == 22 and minute == 0 and not sleep_warning_played:
            play_alert("pda_sleep_warning.wav")
            sleep_warning_played = True
        if hour == 22 and minute == 1: sleep_warning_played = False 

        # 3. MONITOR BATTERY & CHARGER
        if plugged != last_plugged:
            if plugged:
                play_alert("pda_charging.wav")
                low_battery_warned = False
            else:
                play_alert("pda_discharging.wav")
            last_plugged = plugged

        if percent <= 20 and not plugged and not low_battery_warned:
            play_alert("pda_low_battery.wav")
            low_battery_warned = True

        # 4. MONITOR NETWORK
        current_internet = check_internet()
        if current_internet != last_internet:
            if current_internet: play_alert("pda_wifi_connected.wav")
            else: play_alert("pda_wifi_lost.wav")
            last_internet = current_internet

        # 5. MONITOR HARDWARE (CPU OVERHEAT > 85%)
        if psutil.cpu_percent(interval=None) > 85.0:
            if not cpu_warned:
                play_alert("pda_cpu_hot.wav")
                cpu_warned = True
        else: cpu_warned = False

        if psutil.virtual_memory().percent > 90.0:
            if not ram_warned:
                play_alert("pda_ram_full.wav")
                ram_warned = True
        else: ram_warned = False

        # 6. MONITOR STORAGE
        free_storage = psutil.disk_usage('C:\\').free
        if free_storage < (10 * 1024 * 1024 * 1024):
            if not storage_warned:
                play_alert("pda_storage_low.wav")
                storage_warned = True
        else: storage_warned = False

        # 7. LOGIKA MINUM AIR (Pemberitahuan "Drink." Tiap 2 Jam)
        if time.time() - start_hydration_timer > 7200:
            play_alert("pda_hydrate.wav")
            start_hydration_timer = time.time()

        time.sleep(5)