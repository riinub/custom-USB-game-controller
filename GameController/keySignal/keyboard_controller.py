#!/usr/bin/env python3
"""
🎮 Arduino Game Controller 🎮

CONTROLS MAPPING:
- Left Joystick: WASD keys (movement)
- Right Joystick: Arrow keys (camera/look)
- Buttons: Space, Shift, Ctrl, etc.
"""

import serial
import time
import sys
import re
import glob
from pynput.keyboard import Key, Listener
from pynput import keyboard
import threading

# Configuration
BAUD_RATE = 115200
UPDATE_RATE = 60

class ArduinoKeyboardController:
    def __init__(self):
        self.serial_conn = None
        self.running = False
        self.controller = keyboard.Controller()
        
        # Current key states (to avoid repeated presses)
        self.pressed_keys = set()
        
        # Joystick deadzone (ignore small movements)
        self.deadzone = 0.2
        
        print("⌨️  Arduino Keyboard Controller v1.0")
        print("=" * 50)
    
    def find_arduino_port(self):
        """Auto-detect Arduino port"""
        print("🔍 Searching for GAM3BO1...")
        patterns = ['/dev/tty.usbmodem*', '/dev/tty.usbserial*']
        
        ports = []
        for pattern in patterns:
            ports.extend(glob.glob(pattern))
        
        if not ports:
            print("❌ No GAM3BO1 found!")
            return None
        
        print(f"✅ Found GAM3BO1 at: {ports[0]}")
        return ports[0]
    
    def connect_to_arduino(self):
        """Connect to GAM3BO1"""
        port = self.find_arduino_port()
        if not port:
            return False
        
        try:
            self.serial_conn = serial.Serial(port, BAUD_RATE, timeout=1)
            time.sleep(2)
            print("✅ Connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def parse_arduino_data(self, line):
        """Parse Arduino data and convert to keyboard inputs"""
        try:
            matches = re.findall(r'(\w+):(\d+)', line.strip())
            data = {key: int(value) for key, value in matches}
            
            # Clear all currently pressed keys
            keys_to_release = self.pressed_keys.copy()
            new_keys = set()
            
            # LEFT JOYSTICK -> WASD (Movement)
            if 'LX' in data:
                lx = (data['LX'] - 512) / 512.0
                if lx < -self.deadzone:  # Left
                    new_keys.add('a')
                elif lx > self.deadzone:  # Right
                    new_keys.add('d')
            
            if 'LY' in data:
                ly = (data['LY'] - 512) / 512.0
                if ly < -self.deadzone:  # Forward
                    new_keys.add('w')
                elif ly > self.deadzone:  # Backward
                    new_keys.add('s')
            
            # RIGHT JOYSTICK -> Arrow Keys (Camera)
            if 'RX' in data:
                rx = (data['RX'] - 512) / 512.0
                if rx > self.deadzone:  # Look Left
                    new_keys.add('left')
                elif rx < -self.deadzone:  # Look Right
                    new_keys.add('right')
            
            if 'RY' in data:
                ry = (data['RY'] - 512) / 512.0
                if ry > self.deadzone:  # Look Up
                    new_keys.add('up')
                elif ry < -self.deadzone:  # Look Down
                    new_keys.add('down')
            
            # BUTTONS -> Various Keys
            if data.get('LS', 0):  # Left stick click
                new_keys.add('shift')
            if data.get('RS', 0):  # Right stick click
                new_keys.add('ctrl')
            if data.get('B1', 0):  # Button 1
                new_keys.add('space')  # Jump/Nitro
            if data.get('B2', 0):  # Button 2
                new_keys.add('c')      # Brake
            if data.get('B3', 0):  # Button 3  
                new_keys.add('x')      # Action
            if data.get('B4', 0):  # Button 4
                new_keys.add('y')      # Look back
            
            # Release keys that are no longer pressed
            for key in keys_to_release - new_keys:
                self.release_key(key)
            
            # Press new keys
            for key in new_keys - self.pressed_keys:
                self.press_key(key)
            
            # Update pressed keys
            self.pressed_keys = new_keys
            
            return True
            
        except Exception as e:
            return False
    
    def press_key(self, key_name):
        """Press a key"""
        try:
            if key_name in ['up', 'down', 'left', 'right']:
                key = getattr(Key, key_name)
            elif key_name == 'space':
                key = Key.space
            elif key_name == 'shift':
                key = Key.shift
            elif key_name == 'ctrl':
                key = Key.ctrl
            else:
                key = key_name
            
            self.controller.press(key)
            
        except Exception as e:
            pass
    
    def release_key(self, key_name):
        """Release a key"""
        try:
            if key_name in ['up', 'down', 'left', 'right']:
                key = getattr(Key, key_name)
            elif key_name == 'space':
                key = Key.space
            elif key_name == 'shift':
                key = Key.shift
            elif key_name == 'ctrl':
                key = Key.ctrl
            else:
                key = key_name
            
            self.controller.release(key)
            
        except Exception as e:
            pass
    
    def display_status(self):
        """Show current status"""
        keys_list = list(self.pressed_keys)
        status = f"\r⌨️  Active keys: {keys_list}"
        print(status, end="", flush=True)
    
    def run(self):
        """Main loop"""
        print("🚀 Starting GAM3BO1...")
        
        if not self.connect_to_arduino():
            return
        
        print("\n⌨️  GAM3BO1 READY!")
        print("🎮 Control Mapping:")
        print("   Left Stick: WASD (movement)")
        print("   Right Stick: Arrow Keys (camera)")
        print("   Button 1: SPACE (jump/nitro)")
        print("   Button 2: C (brake)")
        print("   Left Click: SHIFT")
        print("   Right Click: CTRL")
        print("⚡ Press Ctrl+C to exit\n")
        
        self.running = True
        
        try:
            while self.running:
                if self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore')
                    if self.parse_arduino_data(line):
                        self.display_status()
                
                time.sleep(1 / UPDATE_RATE)
                
        except KeyboardInterrupt:
            print("\n\n👋 GAM3BO1 stopped!")
        finally:
            # Release all keys
            for key in self.pressed_keys:
                self.release_key(key)
            if self.serial_conn:
                self.serial_conn.close()

def main():
    # Check if pynput is installed
    try:
        import pynput
    except ImportError:
        print("❌ pynput not installed!")
        print("📦 Install it with: pip3 install pynput")
        return
    
    controller = ArduinoKeyboardController()
    controller.run()

if __name__ == "__main__":
    main()