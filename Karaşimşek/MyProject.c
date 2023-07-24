unsigned short deger;
void main() {
TRISB = 0X00;
PORTB = 0X00;
deger = 0x01;
PORTB = deger;
 
 sol: delay_ms(300);
      deger=deger << 1;
      PORTB=deger;
      if(deger<128) goto sol;
 sag: delay_ms(300);
      deger=deger>>1;
      PORTB=deger;
      if(deger>1) goto sag;
goto sol;
}