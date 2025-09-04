// Arduino Mega 2560 Serial Game Controller
// Wire your components like this:
// LEFT JOYSTICK: VCC->5V, GND->GND, VRX->A0, VRY->A1, SW->Pin 2
// RIGHT JOYSTICK: VCC->5V, GND->GND, VRX->A2, VRY->A3, SW->Pin 3  
// BUTTONS: One leg to pin, other leg to GND (pins 4,5,6,7)

// Pin definitions for LEFT joystick (movement)
const int leftJoystickX = A0;
const int leftJoystickY = A1;
const int leftJoystickButton = 2;

// Pin definitions for RIGHT joystick (camera/aiming)
const int rightJoystickX = A2;
const int rightJoystickY = A3;
const int rightJoystickButton = 3;

// Additional face buttons
const int button1 = 4;  // Face button A/X
const int button2 = 5;  // Face button B/Circle  
const int button3 = 6;  // Face button X/Square
const int button4 = 7;  // Face button Y/Triangle

void setup() {
  // Initialize serial communication at high speed
  Serial.begin(115200);
  
  // Set button pins as inputs with pull-up resistors
  pinMode(leftJoystickButton, INPUT_PULLUP);
  pinMode(rightJoystickButton, INPUT_PULLUP);
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(button3, INPUT_PULLUP);
  pinMode(button4, INPUT_PULLUP);
  
  Serial.println("Arduino Mega Serial Controller Ready!");
}us

void loop() {
  // Read joystick values
  int leftX = analogRead(leftJoystickX);
  int leftY = analogRead(leftJoystickY);
  int rightX = analogRead(rightJoystickX);
  int rightY = analogRead(rightJoystickY);
  
  // Read button states (invert because of pull-up resistors)
  bool leftStick = !digitalRead(leftJoystickButton);
  bool rightStick = !digitalRead(rightJoystickButton);
  bool btn1 = !digitalRead(button1);
  bool btn2 = !digitalRead(button2);
  bool btn3 = !digitalRead(button3);
  bool btn4 = !digitalRead(button4);
  
  // Send data in a structured format
  // Format: LX:value,LY:value,RX:value,RY:value,LS:0/1,RS:0/1,B1:0/1,B2:0/1,B3:0/1,B4:0/1
  Serial.print("LX:");
  Serial.print(leftX);
  Serial.print(",LY:");
  Serial.print(leftY);
  Serial.print(",RX:");
  Serial.print(rightX);
  Serial.print(",RY:");
  Serial.print(rightY);
  Serial.print(",LS:");
  Serial.print(leftStick ? 1 : 0);
  Serial.print(",RS:");
  Serial.print(rightStick ? 1 : 0);
  Serial.print(",B1:");
  Serial.print(btn1 ? 1 : 0);
  Serial.print(",B2:");
  Serial.print(btn2 ? 1 : 0);
  Serial.print(",B3:");
  Serial.print(btn3 ? 1 : 0);
  Serial.print(",B4:");
  Serial.print(btn4 ? 1 : 0);
  Serial.println(); // End line
  
  delay(20); // Send updates 50 times per second
}