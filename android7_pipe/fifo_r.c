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
	int fd, rc;
	char r_buf[100];

	rc = mkfifo(FIFO,O_CREAT|O_RDWR);
	printf("rc:%d\n",rc);

	if((fd = open(FIFO,O_RDONLY))<0)
	{ 
		printf("open error\n");
		exit(1);
	}

	if((read(fd,r_buf,100))<0)
	{
		printf("read error\n");
		exit(1);
	}
	printf("buf:%s\n",r_buf);
	memset(r_buf,0,sizeof(r_buf));

	printf("clear buf:%s\n",r_buf);
	return 0;
}

