import os

def speak(text):
    command = (
        'PowerShell -Command "'
        'Add-Type -AssemblyName System.Speech; '
        '(New-Object System.Speech.Synthesis.SpeechSynthesizer)'
        f'.Speak(\'{text}\')"'
    )
    os.system(command)
