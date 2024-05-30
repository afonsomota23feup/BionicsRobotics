#include <Servo.h>

// Definição dos pinos dos servos
const int SHOULDER_PIN = 4; // Pino do servo do ombro (eixo Y)
const int ELBOW_PIN = 5;    // Pino do servo do cotovelo (eixo Z)
const int WRIST_PIN = 6;    // Pino do servo do pulso (eixo X)
const int FINGERS_PIN = 7;  // Pino do servo dos dedos (força)

// Definição dos limites de movimento dos servos (em graus)
const int SHOULDER_MIN_ANGLE = 0;
const int SHOULDER_MAX_ANGLE = 180;

const int ELBOW_MIN_ANGLE = 0;
const int ELBOW_MAX_ANGLE = 180;

const int WRIST_MIN_ANGLE = 0;
const int WRIST_MAX_ANGLE = 180;

const int FINGERS_MIN_ANGLE = 0;
const int FINGERS_MAX_ANGLE = 180;

// Inicialização dos objetos Servo
Servo shoulderServo;
Servo elbowServo;
Servo wristServo;
Servo fingersServo;

// Posições iniciais dos servos
int shoulderAngle = 90;
int elbowAngle = 90;
int wristAngle = 90;
int fingersAngle = 90;

// Função para calcular o ângulo baseado na distância
int calculateAngleFromDistance(int distance_cm) {
  return (distance_cm ) * 5;
}

// Função para mover um servo a um ângulo específico com restrição de limites
void moveServo(Servo& servo, int& currentAngle, int angleChange, int minAngle, int maxAngle) {
  int newAngle = currentAngle + angleChange;
  newAngle = constrain(newAngle, minAngle, maxAngle);
  servo.write(newAngle);
  currentAngle = newAngle;
}

void setup() {
  // Associar os servos aos pinos
  shoulderServo.attach(SHOULDER_PIN);
  elbowServo.attach(ELBOW_PIN);
  wristServo.attach(WRIST_PIN);
  fingersServo.attach(FINGERS_PIN);

  // Posicionar os servos na posição inicial
  shoulderServo.write(shoulderAngle);
  elbowServo.write(elbowAngle);
  wristServo.write(wristAngle);
  fingersServo.write(fingersAngle);
  // Iniciar a comunicação serial
  Serial.begin(9600);
}

void loop() {
  // Verificar se há dados disponíveis na porta serial
  if (Serial.available() > 0) {
    // Ler os dados do vetor de movimento
    int xDistance = Serial.parseInt();
    int yDistance = Serial.parseInt();
    int zDistance = Serial.parseInt();
    int force = Serial.parseInt();
    // Calcular os incrementos de ângulo para cada servo
    int shoulderAngleChange = calculateAngleFromDistance(yDistance);
    int elbowAngleChange = calculateAngleFromDistance(zDistance);
    int wristAngleChange = calculateAngleFromDistance(xDistance);
    int fingersAngleChange = calculateAngleFromDistance(force);

    // Mover os servos
    moveServo(shoulderServo, shoulderAngle, shoulderAngleChange, SHOULDER_MIN_ANGLE, SHOULDER_MAX_ANGLE);
    moveServo(elbowServo, elbowAngle, elbowAngleChange, ELBOW_MIN_ANGLE, ELBOW_MAX_ANGLE);
    moveServo(wristServo, wristAngle, wristAngleChange, WRIST_MIN_ANGLE, WRIST_MAX_ANGLE);
    moveServo(fingersServo, fingersAngle, fingersAngleChange, FINGERS_MIN_ANGLE, FINGERS_MAX_ANGLE);

    // Limpar o buffer serial
    Serial.readString();
  }
}

