#include <stdio.h>
#include <stdlib.h>
#include <string.h>
 
main()
{
  int pipefd[2];
  int pid;
  int i, line;
  char s[100]={0};
 
  if (pipe(pipefd) < 0) {
    perror("pipe");
    exit(1);
  }
 
  pid = fork();
 
  if (pid > 0)//父进程
   {
      printf("pipefd[1]:%d fater writing....\n", pipefd[1]);
      memcpy(s,"helloworld\n",strlen("helloworld\n"));
      write(pipefd[1], s, strlen(s));
      close(pipefd[1]);
  }
  else//子进程
  {
        printf("pipefd[0]:%d, child reading....\n", pipefd[0]);
        read(pipefd[0],s,1000);
        printf("read result: %s\n",s);
        close(pipefd[0]);
  }
}

