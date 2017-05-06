#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <linux/limits.h>


int cp(char* from, char* to){
   char ch, source_file[1024], target_file[1024];
   FILE *source, *target;
 
   source = fopen(from, "r");
 
   if( source == NULL )
   {
      printf("Press any key to exit...\n");
      exit(EXIT_FAILURE);
   }
 


 
   target = fopen(to, "ab+");
 
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
   return 1;

}



char* get_home_dir(){
  char user[PATH_MAX+1];
  int check = getlogin_r(user, sizeof(user));

  char homedir[PATH_MAX+1];
  char *home = "/home/";
//  char *adding = "/.vim";

  strcpy(homedir, home);
  strcat(homedir, user);
//  strcat(homedir, adding);
  char* get_home;
  get_home = homedir;
  return get_home;
}

void make_vim(char *home_path){
  
  /* add the vimrc */ 
  char vimrc_file[PATH_MAX+1];
  strcpy(vimrc_file, home_path);
  char *vimrc = "/.vimrc";
  strcat(vimrc_file, vimrc);
  printf("Path to vimrc is: %s\n", vimrc_file);
  /* Try to copy the vim to /.vimrc */
  if(cp("vimrc", vimrc_file) != 1){
    printf("vimrc not coppied, the horror... blood everywhere...\n");
  }

  /* Make directory for .vim */
  char *vim = "/.vim";
  strcat(home_path, vim);
  printf("The home dir is %s\n", home_path);
  mkdir(home_path, 0777);

  /* Make directory for colors */
  char *colors = "/colors";
  strcat(home_path, colors);
  mkdir(home_path, 0777);


  /* Create badwolf color scheme   */
  char badwolf_file[PATH_MAX+1];
  strcpy(badwolf_file, home_path);
  char *badwolf = "/badwolf.vim";
   strcat(badwolf_file, badwolf);
   if(cp("badwolf.vim", badwolf_file) != 1){
    printf("It's not good... something happened and I'mma just crash now\n");
  } 


  /* create goodwolf color scheme  */
  char goodwolf_file[PATH_MAX+1];
  strcpy(goodwolf_file, home_path);
  printf("home_path is: %s\n", home_path);
  char *goodwolf = "/goodwolf.vim";
  strcat(goodwolf_file, goodwolf);
  if(cp("goodwolf.vim", goodwolf_file) != 1){
    printf("It's not good... something happened and I'mma just crash now\n");
  }


  /* create onedark color scheme  */
  char onedark_file[PATH_MAX+1];
  strcpy(onedark_file, home_path);
  char *onedark = "/onedark.vim";
  strcat(onedark_file, onedark);
  if(cp("goodwolf.vim", onedark_file) != 1){
    printf("It's not good... something happened and I'mma just crash now\n");
  } 
}

void make_tmux(char *home_path){
  /* add the tmux.conf */ 
  char tmux_file[PATH_MAX+1];
  strcpy(tmux_file, home_path);
  char *tmux = "/.tmux.conf";
  strcat(tmux_file, tmux);
  printf("Path to tmux.conf is: %s\n", tmux_file);
  /* Try to copy the tmux to /.tmux */
  if(cp("tmux.conf", tmux_file) != 1){
    printf("tmux.conf not coppied, the horror... blood everywhere...\n");
  }
}

void make_bash(char *home_path){
  /* add the tmux.conf */ 
  char bash_file[PATH_MAX+1];
  strcpy(bash_file, home_path);
  char *bash = "/.bashrc";
  strcat(bash_file, bash);
  printf("Path to bashrc is: %s\n", bash_file);
  /* Try to copy the bashrc to .bashrc */
  if(cp("bashrc", bash_file) != 1){
    printf("bashrc not coppied, the horror... blood everywhere...\n");
  }
}


int one_arg(char* arg, char* homedir){
   char vim[PATH_MAX+1];
   strcpy(vim, homedir);


   char tmux[PATH_MAX+1];
   strcpy(tmux, homedir);

   char bash[PATH_MAX+1];
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
}


int two_args(char* arg_one, char* arg_two, char *homedir){
  /* If a flag is set for vim  */
  if(!strcmp(arg_one, "-v") || !strcmp(arg_two, "-v")){
    char vim[PATH_MAX+1];
    strcpy(vim, homedir);
    make_vim(vim);
    int check = cp("from.txt", "to.txt");
  }
  /* If a flag is set for bash  */
  if(!strcmp(arg_one, "-b") || !strcmp(arg_two, "-b")){
    char bash[PATH_MAX+1];
    strcpy(bash, homedir);
    make_bash(bash);
  }
  /* If a flag is set for tmux  */
  if(!strcmp(arg_one, "-t") || !strcmp(arg_two, "-t")){
    char tmux[PATH_MAX+1];
    strcpy(tmux, homedir);
    make_tmux(tmux);
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

   return 0;
}
