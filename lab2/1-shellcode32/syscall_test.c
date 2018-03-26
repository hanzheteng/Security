#include <stdio.h>
#include <fcntl.h>

int main(int argc, char **argv)
{
    int fd;

    fd = open("foo.txt", O_RDWR, 0777);
    if(fd == -1)
        perror("open");

    printf("%d\n", fd);
    
    char buffer[20];

    read(fd, buffer, 20);

    printf("%s\n", buffer);

    write(1, buffer, 10);   // 1 stands for stdout

    write(1, "\n", 1);

    close(fd);

    return 0;
}

