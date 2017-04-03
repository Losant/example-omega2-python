import time
import onionGpio # See Library: https://github.com/OnionIoT/onion-gpio
from losantmqtt import Device

ledPin = 0 # GPIO 0
buttonPin = 1 # GPIO 1
lightStatus = 0

led = onionGpio.OnionGpio(ledPin)
led.setOutputDirection(0) # make LED output and init to 0

button = onionGpio.OnionGpio(buttonPin)
button.setInputDirection() # make Button input

# Construct device
device = Device("my-device-id", "my-access-key", "my-access-secret")

# Called when a Losant Device Command is received.
def on_command(device, command):
    global lightStatus
    print("Command received.")
    print(command["name"])
    print(command["payload"])
    if command["name"] == "toggle":
        lightStatus = int(not lightStatus)
        led.setValue(lightStatus)


# Listen for commands.
device.add_event_observer("command", on_command)

# Connect to Losant.
device.connect(blocking=False)

print("Here we go! Press CTRL+C to exit")
try:
    while 1:
        device.loop()
        if device.is_connected():
            if int(button.getValue()):
                print("Button pressed!")
                device.send_state({"button": 1})
                time.sleep(3) # Debounce button press
        time.sleep(0.03)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    led._freeGpio()
    button._freeGpio()# cleanup all GPIO
