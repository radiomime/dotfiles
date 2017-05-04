#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int cp(char* from, char* to){
   char ch, source_file[1024], target_file[1024];
   FILE *source, *target;
 
   source = fopen(from, "r");
 
   if( source == NULL )
   {
      printf("Press any key to exit...\n");
      exit(EXIT_FAILURE);
   }
 


 
   target = fopen(to, "w");
 
   if( target == NULL )
   {
      fclose(source);
      printf("Press any key to exit...\n");
      exit(EXIT_FAILURE);
   }
 
   while( ( ch = fgetc(source) ) != EOF )
      fputc(ch, target);
 
   printf("File copied successfully.\n");
 
   fclose(source);
   fclose(target);

}

int one_arg(char* arg){
      if(!strcmp(arg, "-a")){
       int check = cp("from", "../to.txt");
     }
     if(!strcmp(arg, "-v")){
       int check = cp("from.txt", "to.txt");
   }
     if(!strcmp(arg, "-b")){
       int check = cp("from.txt", "to.txt");
   }
     if(!strcmp(arg, "-t")){
       int check = cp("from.txt", "to.txt");
   }
}


int two_args(char* arg_one, char* arg_two){
     if(!strcmp(arg_one, "-v") || !strcmp(arg_two, "-v")){
       int check = cp("from.txt", "to.txt");
   }
     if(!strcmp(arg_one, "-b") || !strcmp(arg_two, "-b")){
       int check = cp("from.txt", "to.txt");
   }
     if(!strcmp(arg_one, "-t") || !strcmp(arg_two, "-t")){
       int check = cp("from.txt", "to.txt");
   }

}

char* get_home_dir(){
  char user[1024];
  int check = getlogin_r(user, sizeof(user));

  char homedir[1024];
  char *home = "/home/";
//  char *adding = "/.vim";

  strcpy(homedir, home);
  strcat(homedir, user);
//  strcat(homedir, adding);
  char* get_home;
  printf("Also printing: %s\n", homedir);
  get_home = homedir;
  return get_home;
}

int main(int argc ,char *argv[])
{  

   char *homedir = get_home_dir();
   printf("The home dir is: %s\n", homedir);
   int check;
   if(argc == 2){
    check = one_arg(argv[1]);
   }
   if(argc == 3){
     check = two_args(argv[1], argv[2]);
   }

   return 0;
}
