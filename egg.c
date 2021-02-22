// egg.c
// this program is used to create the bot as its own process,
// so that it can be controlled better

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <errno.h>
#include <string.h>
#include <signal.h>

int main() {

  char *cmd = "python3";
  char *args[2];
  args[0] = "python3";
  args[1] = "./ProctorPhil.py";

  pid_t pid = fork();

  if (pid < 0) printf("fork failed.\n\n");

  else if (pid == 0) {

    printf("[egg] starting ProctorPhil at PID %d\n", getpid());

    if (execvp(cmd, args)) {
      printf("failed to run ProctorPhil\n");
      exit(1);
    }
    
  } else {

    // run bot for 59m 55s
    sleep(3600 - 5);
    kill(pid, SIGTERM);
    printf("[egg] PID %d terminated.\n", pid);
    exit(0);

  }
}
