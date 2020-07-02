#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main()
{
    printf("1\r");
    fflush(stdout);
    sleep(1);
    printf("2\r");
    fflush(stdout);
    sleep(1);
    printf("3\r");
    fflush(stdout);
    sleep(1);
    printf("over\n");

    return 0;
}



