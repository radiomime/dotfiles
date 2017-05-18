#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>
#include <sys/utsname.h>

#define PATH_MAX 1024

int cp(char* from, char* to){
   char ch, source_file[PATH_MAX], target_file[PATH_MAX];
   FILE *source, *target;
 
   source = fopen(from, "r");
 
   if( source == NULL )
   {
      printf("Exiting from as null\n");
      exit(EXIT_FAILURE);
   }
   
   /* Set to w+ because we want to overwrite the contents of the file   */
   target = fopen(to, "w+");
 
   if( target == NULL )
   {
      fclose(source);
      printf("Exiting to as null\n");
      exit(EXIT_FAILURE);
   }
 
   while( ( ch = fgetc(source) ) != EOF )
      fputc(ch, target);


   fclose(source);
   fclose(target);
   return 1;

}

char* get_home_dir(int OS){
  char *user = malloc(PATH_MAX * sizeof(char));
  struct passwd *pws;
  pws = getpwuid(getuid());
  strcpy(user, pws->pw_name);
  /* The user name (for mac use) is stored in user  */
  char *homedir = malloc(PATH_MAX * sizeof(char)); // Free in main
  /* Adding /Users/ instead of /home/ for mac  */
  char *home;
  if(OS == 0){
    /* Home Directory for Mac  */
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


void make_vim_color(char *color_file, char *home_path){
  /* Create given color scheme   */
   char *color= malloc(PATH_MAX * sizeof(char));
   strcpy(color, home_path);
   /* Account for formatting of slash in added color scheme */
   char *addSlash = "/";
   strcat(color, addSlash);
   strcat(color, color_file);
   char *local = malloc(PATH_MAX * sizeof(char));
   char *conf = "../conf/";
   strcpy(local, conf);
   strcat(local, color_file);
   if(cp(local, color) != 1){
    printf("It's not good... something happened and I'mma just crash now\n");
  }
   free(color);
   free(local);

}



void make_vim(char *home_path){
  /* The home directory is passed in home_path */
  /* add the vimrc */ 
  char *vimrc_file = malloc(PATH_MAX * sizeof(char));
  strcpy(vimrc_file, home_path);
  char *vimrc = "/.vimrc";
  strcat(vimrc_file, vimrc);
  /* The path to make the vimrc is stored in vimrc_file */
  char *local_vimrc = "../conf/vimrc";
  /* Try to copy the vim to /.vimrc */
  if(cp(local_vimrc, vimrc_file) != 1){
    printf("vimrc not coppied, the horror... blood everywhere...\n");
  }

  /* Make directory for .vim */
  char *vim = "/.vim";
  strcat(home_path, vim);
  mkdir(home_path, 0777);

  /* Make directory for colors */
  char *colors = "/colors";
  strcat(home_path, colors);
  mkdir(home_path, 0777);


  /* Create different color schemes   */
  char *color = "badwolf.vim";
  make_vim_color(color, home_path);

  color = "goodwolf.vim";
  make_vim_color(color, home_path);

  color = "onedark.vim";
  make_vim_color(color, home_path);

  free(vimrc_file);
}

void make_tmux(char *home_path){
  /* add the tmux.conf */ 
  char *tmux_file = malloc(PATH_MAX * sizeof(char));
  strcpy(tmux_file, home_path);
  char *tmux = "/.tmux.conf";
  strcat(tmux_file, tmux);
  /* Path to new tmux is stored in tmux_file */
  char *local_tmux = "../conf/tmux.conf";
  /* Try to copy the tmux to /.tmux */
  if(cp(local_tmux, tmux_file) != 1){
    printf("tmux.conf not coppied, the horror... blood everywhere...\n");
  }
  free(tmux_file);
}

void make_bash(char *home_path){
  /* add the tmux.conf */ 
  char *bash_file = malloc(PATH_MAX * sizeof(char));
  strcpy(bash_file, home_path);
  char *bash = "/.bashrc";
  strcat(bash_file, bash);
  /* Path to new bashrc is stored in bash_file  */
  char *local_bashrc = "../conf/bashrc";
  /* Try to copy the bashrc to .bashrc */
  if(cp(local_bashrc, bash_file) != 1){
    printf("bashrc not coppied, the horror... blood everywhere...\n");
  }
  free(bash_file);
}


int one_arg(char* arg, char* homedir){
   char *vim = malloc(PATH_MAX * sizeof(char));
   strcpy(vim, homedir);

   char *tmux = malloc(PATH_MAX * sizeof(char));
   strcpy(tmux, homedir);

   char *bash = malloc(PATH_MAX * sizeof(char));
   strcpy(bash, homedir);
  
  /* All Flag is set  */
  if(!strcmp(arg, "-a")){
    make_vim(vim);
    make_tmux(tmux);
    make_bash(bash);
  }

  /* Vim Flag is set  */
  if(!strcmp(arg, "-v")){
    make_vim(vim);
}
  /* Bash Flag is set  */
  if(!strcmp(arg, "-b")){
    make_bash(bash);
}

  /* Tmux Flag is set  */

  if(!strcmp(arg, "-t")){
    make_tmux(tmux);
}
 free(bash);
 free(tmux);
 free(vim);
 return 0;
}


int two_args(char* arg_one, char* arg_two, char *homedir){
  /* If a flag is set for vim  */
  if(!strcmp(arg_one, "-v") || !strcmp(arg_two, "-v")){
    char *vim = malloc(PATH_MAX * sizeof(char)); 
    strcpy(vim, homedir);
    make_vim(vim);
    int check = cp("from.txt", "to.txt");
    free(vim);
  }
  /* If a flag is set for bash  */
  if(!strcmp(arg_one, "-b") || !strcmp(arg_two, "-b")){
    char *bash = malloc(PATH_MAX * sizeof(char));
    strcpy(bash, homedir);
    make_bash(bash);
    free(bash);
  }
  /* If a flag is set for tmux  */
  if(!strcmp(arg_one, "-t") || !strcmp(arg_two, "-t")){
    char *tmux = malloc(PATH_MAX * sizeof(char));
    strcpy(tmux, homedir);
    make_tmux(tmux);
    free(tmux);
  }
  return 1;
}

int main(int argc ,char *argv[])
{  
   struct utsname unameData;
   uname(&unameData);

   /*  Set OS to 0 for  mac, 1 for linux */ 
   char *mac = "Darwin";
   char *linux_os = "Linux";
   int OS;
   if(!strcmp(unameData.sysname, mac)){
     OS = 0;
   }
   if(!strcmp(unameData.sysname, linux_os)){
     OS = 1;
   }

   char *homedir = get_home_dir(OS);

   int check;
   if(argc == 2){
    check = one_arg(argv[1], homedir);
   }
   if(argc == 3){
     check = two_args(argv[1], argv[2], homedir);
   }

   free(homedir);
   return 0;
}
