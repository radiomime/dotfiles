#include <unistd.h>
#include <sys/types.h>
#include <stdio.h>
#include <pwd.h>
#include <linux/limits.h>

int main(int argc, char *argv[]){
    struct passwd *pws;
    pws = getpwuid(getuid());

    printf("The user id is: %s\n", pws->pw_name);

    return 1;
    }
