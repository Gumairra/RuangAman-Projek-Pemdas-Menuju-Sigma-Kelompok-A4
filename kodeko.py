import time
import spidev
import RPi.GPIO as GPIO
import Adafruit_DHT
from Adafruit_DHT import Raspberry_Pi
import requests   

# ===== KONFIGURASI PIN =====
DHT_PIN = 4
DHT_TYPE = Adafruit_DHT.DHT22

LED_HIJAU = 17
LED_KUNING = 27
LED_MERAH = 22
BUZZER = 23
FAN_PIN = 18

MCP_CHANNEL = 0

# ===== PARAMETER =====
BATAS_SUHU = 30.0
BATAS_ASAP = 600

FLASK_URL = "http://127.0.0.1:5000/update"  

# ===== SETUP GPIO =====
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_HIJAU, GPIO.OUT)
GPIO.setup(LED_KUNING, GPIO.OUT)
GPIO.setup(LED_MERAH, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

# ===== SETUP SPI =====
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_mcp3002(channel=0):
    if channel == 0:
        command = [0b11010000, 0x00]
    else:
        command = [0b11110000, 0x00]

    resp = spi.xfer2(command)
    value = ((resp[0] & 0x03) << 8) | resp[1]
    return value

def reset_output():
    GPIO.output(LED_HIJAU, GPIO.LOW)
    GPIO.output(LED_KUNING, GPIO.LOW)
    GPIO.output(LED_MERAH, GPIO.LOW)
    GPIO.output(BUZZER, GPIO.LOW)
    GPIO.output(FAN_PIN, GPIO.LOW)

print("Sistem Monitoring Suhu & Asap - Raspberry Pi Ready")

try:
    while True:
        
        humidity, temperature = Adafruit_DHT.read_retry(
            DHT_TYPE, DHT_PIN, platform=Raspberry_Pi
        )

        suhu = temperature
        asap = read_mcp3002(MCP_CHANNEL)

        suhuTinggi = (suhu is not None) and (suhu > BATAS_SUHU)
        adaAsap = asap > BATAS_ASAP

        reset_output()

        
        if suhuTinggi and adaAsap:
            GPIO.output(LED_MERAH, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.HIGH)
            GPIO.output(FAN_PIN, GPIO.HIGH)
        elif suhuTinggi and not adaAsap:
            GPIO.output(LED_KUNING, GPIO.HIGH)
            GPIO.output(FAN_PIN, GPIO.HIGH)
        elif (not suhuTinggi) and adaAsap:
            GPIO.output(LED_MERAH, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.HIGH)
        else:
            GPIO.output(LED_HIJAU, GPIO.HIGH)

        # ===== KIRIM KE FLASK (REALTIME WEB) =====
        payload = {
            "suhu": float(suhu) if suhu is not None else 0.0,
            "asap": int(asap)
        }

        try:
            requests.post(FLASK_URL, json=payload, timeout=2)
        except Exception as e:
            print("⚠️ Gagal kirim ke Flask:", e)

        # ===== DEBUG TERMINAL =====
        if suhu is None:
            print(f"Suhu: N/A | Asap (ADC): {asap}")
        else:
            print(f"Suhu: {suhu:.1f} °C | Asap (ADC): {asap}")

        time.sleep(2)   

except KeyboardInterrupt:
    print("Program dihentikan.")

finally:
    reset_output()
    GPIO.cleanup()
    spi.close()