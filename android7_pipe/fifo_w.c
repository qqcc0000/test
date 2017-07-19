#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#define FIFO "/home/q/wfifo"

int main(int argc,char * argv [ ])
{
	int fd;
	char w_buf[100];
	if((fd = open(FIFO, O_WRONLY,0666))<0)
	{
		printf("/data/wfifo open error\n");
		exit(1);
	}
	strcpy(w_buf,argv[1]);

	if((write(fd,w_buf,100))<0)
		exit(1);
	
	return 0;
}
