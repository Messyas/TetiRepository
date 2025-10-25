# MANTEM SOMENTE OS DADOS RECEBIDOS, SIMILAR AO MQTT

import serial #pip install pyserial
import time

# Configuração da porta serial
porta = 'COM2'  # Altere conforme necessário
baud_rate = 9600

try:
    ser = serial.Serial(porta, baud_rate, timeout=1)
    time.sleep(2)
    print(f"[INFO] Lendo dados da porta {porta}...")

    while True:
        if ser.in_waiting:
            linha = ser.readline().decode('utf-8', errors='ignore').strip()
            if linha:
                print(f"[RECEBIDO] {linha}")
                # Sobrescreve o conteúdo anterior com a nova linha
                with open("alarme.txt", "w") as arquivo:
                    arquivo.write(linha + "\n")

        time.sleep(0.2)  # Evita leitura excessiva da porta

except serial.SerialException as e:
    print(f"[ERRO] Problema na porta serial: {e}")

except KeyboardInterrupt:
    print("\n[INFO] Leitura interrompida pelo usuário.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"[INFO] Porta {porta} fechada.")
