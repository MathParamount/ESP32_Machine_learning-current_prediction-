#include <Arduino.h>
#include <WiFi.h>

#define ADC_PIN 34
#define ADC_Max 4095.0
#define volt_ref 3.3
#define n 2000          // number of iterations
#define current_ref 5       //reference current informed at datasheet

#define Vrms_rede 127.0      // grid voltage

float rms_current;

float offset = 0;
float acumulator;
float potency_estim;

void setup()
{
   Serial.begin(115200);
   analogSetAttenuation(ADC_11db);

   //Shotting down the wifi
   
   WiFi.mode(WIFI_OFF);
   Serial.println("Wifi disabled")

float h = 3000;

   for (int i = 0; i < h; i++)
    {
        float adc = analogRead(ADC_PIN);

        offset += adc;

        delayMicroseconds(300);
    }

    offset = (offset/h) * (3.3/ADC_Max);
}

void loop()
{

acumulator = 0;
potency_estim = 0;

    for( int i =0; i< n; i++)
    {
        float adc = analogRead(ADC_PIN);
        float voltage_adc = (adc * volt_ref)/ ADC_Max;
        float current_adc = (voltage_adc - offset) / 0.185;      // Exemplo (ACS712 – 5A): Sensibilidade ≈ 66 mV/A , Offset ≈ 2.5 V

        acumulator += current_adc * current_adc;

        delayMicroseconds(300);
    }    

    rms_current = sqrt(acumulator / n);

    potency_estim = Vrms_rede * rms_current;     // estimated without (Voltage sensor)

    Serial.print(" rms_A: ");
    Serial.print(rms_current, 2);
    Serial.print(" W: ");
    Serial.println(potency_estim, 2);
}  
