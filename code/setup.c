#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <sys/utsname.h>
#define PATH_MAX 1024

/* Prototypes  */
int copy(char* from, char* to);
char* get_home_dir(int OS);
int make_file(char *home_path, char* file_name);
void make_vim_color(char *color_file, char *home_path);
void make_vim(char *home_path);
void check_arg(char* homedir, char* arg);


int copy(char* from, char* to){
   char ch, source_file[PATH_MAX], target_file[PATH_MAX];
   FILE *source, *target;
 
   source = fopen(from, "r");
 
   if( source == NULL )
   {
     printf("Could not locate file to copy: %s\n", from);
     return -1;

     
   }
   
   /* Set to w+ because we want to overwrite the contents of the file   */
   target = fopen(to, "w+");
 
   if( target == NULL )
   {
     printf("Could not locate destination at: %s\n", to);
     fclose(source);
     return -1;
   }
 
   while( ( ch = fgetc(source) ) != EOF )
      fputc(ch, target);


   fclose(source);
   fclose(target);
   return 0;

}

char* get_home_dir(int OS){
  char *user = malloc(PATH_MAX * sizeof(char));
  struct passwd *pws;
  /* Secure method for getting username to build file path */
  pws = getpwuid(getuid());
  strcpy(user, pws->pw_name);
  char *homedir = malloc(PATH_MAX * sizeof(char)); // Free in main
  char *home;
  if(OS == 0){
    /* Home Directory for mac_os  */
    home = "/Users/";
  }
  else{
    /* Home Directory for Linux  */
    home = "/home/";
  }
  /* Build the proper path  */
  strcpy(homedir, home);
  strcat(homedir, user);

  /* Return a pointer to the path to be used by other functions */
  char* get_home;
  get_home = homedir;
  free(user);
  return get_home;
}


/*  Add a new dotfile using a file from conf folder */
int make_file(char *home_path, char* file_name){
  /* add the new file */ 
  char *file_path = malloc(PATH_MAX * sizeof(char));
  strcpy(file_path, home_path);

  /* Add the prefix to create the dot file */
  char *add_dot = "/.";
  strcat(file_path, add_dot);
  /* Add the name of the file to the new path */
  strcat(file_path, file_name);

  /* Build the path to file to be coppied */ 
  char *conf_file_path = "conf/";
  char *local_new = malloc(PATH_MAX * sizeof(char));
  strcpy(local_new, conf_file_path);
  strcat(local_new, file_name);
  /* Try to copy the file to the new path */
  if(copy(local_new, file_path) != 0){
    printf("%s not coppied, the horror... blood everywhere...\n", local_new);
    free(local_new);
    free(file_path);
    return -1;
  }

  else{
  free(local_new);
  free(file_path);
  return 0;
  }
}


void make_vim_color(char *color_file, char *home_path){
  /* Create given color scheme   */
   char *color= malloc(PATH_MAX * sizeof(char));
   strcpy(color, home_path);
   /* Account for formatting of slash in added color scheme */
   char *addSlash = "/";
   strcat(color, addSlash);
   strcat(color, color_file);
   /* Add the relative path to the configuration file  */
   char *local = malloc(PATH_MAX * sizeof(char));
   /* Add the route to the vim color files  */
   char *conf = "conf/";
   strcpy(local, conf);
   strcat(local, color_file);
   if(copy(local, color) != 0){
    printf("It's not good... something happened and now crashing is happening \n");
  }
   free(color);
   free(local);
}


void make_vim(char *home_path){
  /* Add the vimrc file */
  char *file_name = "vimrc";
  if(make_file(home_path, file_name) != 0){
    printf("Error Copying vimrc\n");
  }

  /* Make directory for .vim */
  char *vim = "/.vim";
  strcat(home_path, vim);
  mkdir(home_path, 0777);

  /* Make directory for colors */
  char *colors = "/colors";
  strcat(home_path, colors);
  mkdir(home_path, 0777);

  /* Add different color schemes   */
  char *color = "badwolf.vim";
  make_vim_color(color, home_path);

  color = "goodwolf.vim";
  make_vim_color(color, home_path);

  color = "onedark.vim";
  make_vim_color(color, home_path);
}


void check_arg(char* homedir, char* arg){
  /*  Add vim files  */
  if(!strcmp(arg, "-v") || !strcmp(arg, "-a")){
   make_vim(homedir);
   printf("Added vim files\n");
  }

  /* Add the bashrc   */
  if(!strcmp(arg, "-b") || !strcmp(arg, "-a")){
   char* file_name = "bashrc";
   char* ip_name = "getIP.sh";
   if(make_file(homedir, file_name) != 0){
     printf("Couldn't copy the bashrc\n");
   }
   else{
     printf("Added bashrc file\n");
   }
   if(make_file(homedir, ip_name) != 0){
     printf("Couldn't copy the getIP\n");
   }
   else{
     printf("Added getIP file\n");
   }
  }
  
  /* Add tmux file  */
  if(!strcmp(arg, "-t") || !strcmp(arg, "-a")){
  char* file_name = "tmux.conf";
  if(make_file(homedir, file_name) != 0){
      printf("Couldn't copy tmux \n");
      }
  else{
    printf("Added tmux.conf file\n");
    }
  }
}

int main(int argc ,char *argv[]){  
  /* Get info about OS  */
   struct utsname unameData;
   uname(&unameData);

   /*  Set OS to 0 for  mac, 1 for linux */ 
   char *mac_os = "Darwin";
   char *linux_os = "Linux";
   int OS;
   if(!strcmp(unameData.sysname, mac_os)){
     OS = 0;
   }
   if(!strcmp(unameData.sysname, linux_os)){
     OS = 1;
   }
   char *homedir = get_home_dir(OS);

   for(int i = 0; i < argc; i++){
     check_arg(homedir, argv[i]);
   }

   free(homedir);
   return 0;
}
