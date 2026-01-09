import time
import requests
import spidev
import RPi.GPIO as GPIO
import Adafruit_DHT

# ===== KONFIGURASI PIN SESUAI FILE =====
DHT_PIN = 4              # GPIO4 untuk DHT22 DATA
DHT_TYPE = Adafruit_DHT.DHT22

LED_HIJAU = 17           # GPIO17
LED_KUNING = 27          # GPIO27
LED_MERAH = 22           # GPIO22
BUZZER = 23              # GPIO23
FAN_PIN = 18             # GPIO18 (MOSFET Gate)

MCP_CS = 8               # GPIO8 (CE0)
MCP_CHANNEL = 0          # MQ-2 di CH0 MCP3002

# ===== PARAMETER =====
BATAS_SUHU = 30.0
BATAS_ASAP = 600 

FLASK_URL = "http://127.0.0.1:5000/update"

# ===== SETUP GPIO =====
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_HIJAU, GPIO.OUT)
GPIO.setup(LED_KUNING, GPIO.OUT)
GPIO.setup(LED_MERAH, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device CE0 (GPIO8)
spi.max_speed_hz = 1350000

def read_mcp3002(channel=0):
    # MCP3002: 10-bit ADC
    # Command format: start bit + mode + channel
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
        suhu, _ = Adafruit_DHT.read_retry(DHT_TYPE, DHT_PIN)
        asap = read_mcp3002(MCP_CHANNEL)

        # Proteksi jika sensor gagal
        suhu = suhu if suhu is not None else 0.0
        asap = int(asap)

        reset_output()

        if suhu > BATAS_SUHU and asap > BATAS_ASAP:
            GPIO.output(LED_MERAH, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.HIGH)
            GPIO.output(FAN_PIN, GPIO.HIGH)

        elif suhu > BATAS_SUHU:
            GPIO.output(LED_KUNING, GPIO.HIGH)
            GPIO.output(FAN_PIN, GPIO.HIGH)

        elif asap > BATAS_ASAP:
            GPIO.output(LED_MERAH, GPIO.HIGH)
            GPIO.output(BUZZER, GPIO.HIGH)

        else:
            GPIO.output(LED_HIJAU, GPIO.HIGH)

        payload = {
            "suhu": round(suhu, 1),
            "asap": asap
        }

        try:
            requests.post(FLASK_URL, json=payload, timeout=2)
        except:
            print("Gagal kirim ke Flask")

        print(f"Suhu: {suhu:.1f}°C | Asap: {asap}")
        time.sleep(2)

except KeyboardInterrupt:
    print("Program dihentikan")

finally:
    GPIO.cleanup()
    spi.close()
