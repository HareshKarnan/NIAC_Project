#include <CheapStepper.h>
CheapStepper m1 (53,51,49,47); 
CheapStepper m2 (4,5,6,7); 
CheapStepper m3 (22,24,26,28); 
CheapStepper m4 (30,32,34,36); 
CheapStepper m5 (38,40,42,44); 
void setup() {
  // put your setup code here, to run once:

  m1.setRpm(20);
  m2.setRpm(20);
  m3.setRpm(20);
  m4.setRpm(20);
  m5.setRpm(20);
  Serial.begin(115200); 
}
String input;
String temp;
int motor;
int val;
int i;
void loop() {

  while(Serial.available()>0)
{
  input = Serial.readStringUntil(';');
  
  for (i=0;input[i]!=':';i++)
  {
      temp+=input[i];    
  }
  i=i+1;
  motor = temp.toInt();
  Serial.println(motor);
  temp="";
  for (i;i<input.length();i++)
  {
        temp+=input[i];
  }
  
  val = temp.toInt();
  Serial.println(val);
  temp="";
  
  if(motor==1)
  {
                Serial.println("yessss");
                if (val<0)
                { 
                m1.newMoveDegrees (0, int(abs(val)));
                }
                else if (val>0)
                { 
                m1.newMoveDegrees (1, int(val));
                }  
  } 
    else if(motor==2)
    {
                if (val<0)
                { 
                m2.newMoveDegrees (0, int(abs(val)));
                }
                else if (val>0)
                { 
                m2.newMoveDegrees (1, int(val));
                }  
    }
    if(motor==3)
    {
                if (val<0)
                { 
                m3.newMoveDegrees (0, int(abs(val)));
                }
                else if (val>0)
                { 
                m3.newMoveDegrees (1, int(val));
                }
    }  
    if(motor==4)
    {
                if (val<0)
                { 
                m4.newMoveDegrees (0, int(abs(val)));
                }
                else if (val>0)
                { 
                m4.newMoveDegrees (1, int(val));
                }  
    }
    if(motor==5)
    {
                if (val<0)
                { 
                m5.newMoveDegrees (0, int(abs(val)));
                }
                else if (val>0)
                { 
                m5.newMoveDegrees (1, int(val));
                }
    }                                     
  }
 m1.run();
 m2.run();
 m3.run();
 m4.run();
 m5.run();
  
}
  
