#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <pwd.h>

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
 
   target = fopen(to, "ab+");
 
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

char* get_home_dir(){
  char *user = malloc(PATH_MAX * sizeof(char));
  struct passwd *pws;
  pws = getpwuid(getuid());
  strcpy(user, pws->pw_name);
  /* The user name (for mac use) is stored in user  */
  char *homedir = malloc(PATH_MAX * sizeof(char)); // Free in main
  /* Adding /Users/ instead of /home/ for mac  */
  char *home = "/Users/";
  /* Build the proper path  */
  strcpy(homedir, home);
  strcat(homedir, user);

  /* Return a pointer to the path to be used by other functions */
  char* get_home;
  get_home = homedir;
  free(user);
  return get_home;
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


  /* Create badwolf color scheme   */
   char *badwolf_file = malloc(PATH_MAX * sizeof(char));
   strcpy(badwolf_file, home_path);
   char *badwolf = "/badwolf.vim";
   strcat(badwolf_file, badwolf);
   char *local_badwolf = "../conf/badwolf.vim";
   if(cp(local_badwolf, badwolf_file) != 1){
    printf("It's not good... something happened and I'mma just crash now\n");
  } 

  /* create goodwolf color scheme  */
  char *goodwolf_file = malloc(PATH_MAX * sizeof(char));
  strcpy(goodwolf_file, home_path);
  char *goodwolf = "/goodwolf.vim";
  strcat(goodwolf_file, goodwolf);
  char *local_goodwolf = "../conf/goodwolf.vim";
  /* Copy the local version of the file to the correct path */
  if(cp(local_goodwolf, goodwolf_file) != 1){
    printf("It's not good... something happened and I'mma just crash now\n");
  }

  /* create onedark color scheme  */
  char *onedark_file = malloc(PATH_MAX * sizeof(char));
  strcpy(onedark_file, home_path);
  char *onedark = "/onedark.vim";
  strcat(onedark_file, onedark);
  char *local_onedark = "../conf/onedark.vim";
  /* Copy the local version of the file to the correct path */
  if(cp(local_onedark, onedark_file) != 1){
    printf("It's not good... something happened and I'mma just crash now\n");
  } 
  free(onedark_file);
  free(goodwolf_file);
  free(badwolf_file);
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
   char *homedir = get_home_dir();

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
