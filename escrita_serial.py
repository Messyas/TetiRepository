import serial
import time

# Configuração da porta serial
porta = 'COM3'  # Altere conforme seu sistema
baud_rate = 9600

try:
    ser = serial.Serial(porta, baud_rate, timeout=1)
    time.sleep(2)  # Aguarda estabilização da conexão
    print(f"[INFO] Conectado à porta {porta}. Pronto para enviar dados!")

    while True:
        mensagem = input(
            "[ENVIAR] Digite a mensagem (ou 'sair' para encerrar): ")
        if mensagem.lower() == 'sair':
            break
        ser.write((mensagem + '\n').encode('utf-8'))
        print(f"[INFO] Mensagem enviada: {mensagem}")

except serial.SerialException as e:
    print(f"[ERRO] Falha ao abrir a porta serial: {e}")

except KeyboardInterrupt:
    print("\n[INFO] Interrompido pelo usuário.")

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print(f"[INFO] Porta {porta} fechada.")
