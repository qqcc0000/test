#include <unistd.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdlib.h>

int main(int argc,char * argv [ ])
{
	int pipe_fd[2];
	int sun1,sun2,father;
	char buf_r[20];
	memset(buf_r,0,sizeof(buf_r));
	memcpy(buf_r,"helloworld\n",strlen("helloworld\n"));
	if(pipe(pipe_fd)<0)
	{
		perror("pipe_fd:");
	}
	else
	{
		printf("creat pipe success\n");
		//return 1;
	}

	if((sun1=fork())<0)
	{
		perror("sun1:");
		return 1;
	}
	else
	{
		close(pipe(pipe_fd[0]));
		write(pipe_fd[1],buf_r,5);
		printf("sun1 ok\n");
	}
	
	if((sun2=fork())<0)
	{
		perror("sun2:");
		return 1;
	}
	else
	{
		close(pipe(pipe_fd[1]));
		read(pipe_fd[0],buf_r,5);
		printf("sun2 ok\n");
	}
	
	
	return 0;
}
