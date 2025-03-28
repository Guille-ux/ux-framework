void putchar(int pos, char c) {
    char *cpt = (char *)0xB8000;
    cpt += pos * 2;
    *cpt = c;
}

char getchar() {
    unsigned char tecla;
    asm volatile ("inb $0x60, %0" : "=a"(tecla));
    return tecla;
}
