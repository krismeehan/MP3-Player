# *****************************************************************************
# ***************************  Python Source Code  ****************************
# *****************************************************************************
# 
#   DESIGNER NAME:  Kris Meehan
# 
#       FILE NAME:  Project 3
#  
#            DATE:  12/15/2021
#
# DESCRIPTION
#   This file is an MP3 player. The user can load MP3 files from a folder, or from
#   a saved playlist. The program will automatically sort out only the mp3 files 
#   from a folder, which can then be saved to a playlist. The user can choose for
#   songs to play randomly, or sequentially. The user also controls volume, skipping
#   of songs, pausing, playing, and stopping. Opening a folder or playlist of songs
#   will display the folder path to the user, as well as the current song playing
#   and the status of the MP3 player (playing, paused, stopped).
#
# *****************************************************************************

# modules used by this file
import os
import random
import pickle
from os.path import join
import tkinter as TK
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
from pygame import mixer

#---------------------------------------------------
# Global constants to be used in program
#---------------------------------------------------

# max/min volume and volume scale and first song constants
MIN_VOLUME = 0.0
MID_VOLUME = 5.0
MAX_VOLUME = 10.0
VOLUME_SCALE = 0.1
FIRST_SONG = 0
LIMIT_SET = 1
MIN_SONGS = 2
CALLBACK_DELAY = 500
MP3_SUFFIX = '.mp3'

# dimensions and padding
FRAME_PAD = 5
WIDTH = 300
HEIGHT = 25

# song column and path/location column constant
SONG_COLUMN = 1
PATH_COLUMN = 0

# random box constants
RANDOM = 1
NOT_RAND = 0
EMPTY = 0

# icon constants
PLAY_BTN_ICON   = u"\u25B6"
PAUSE_BTN_ICON  = u"\u23F8"
STOP_BTN_ICON   = u"\u23F9"
NEXT_BTN_ICON   = u"\u23E9"
PREV_BTN_ICON   = u"\u23EA"
QUIT_BTN_ICON   = u"\u274C"
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will create and display the GUI window to the user for 
#   the mp3 player
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def create_gui_window():

  # create main window with title "MP3 Player"
  root = TK.Tk()
  root.geometry("450x200")
  root.title("Python MP3 Player")
  mp3_list = []

  # dynamic variables for random box, song index and volume
  random_var         = tkinter.IntVar()
  song_index         = tkinter.IntVar()
  vol_var            = tkinter.DoubleVar()

  # dynamic boolean variables for paused and stopped
  pause_boolean      = tkinter.BooleanVar()
  stop_boolean       = tkinter.BooleanVar()

  # dynamic variables for folder path, now playing, and MP3 status
  display_path       = tkinter.StringVar(value='Select folder to load') 
  playing_var        = tkinter.StringVar(value='*** NONE ***')
  player_status_info = tkinter.StringVar(value='STOPPED')

  # set initial index, volume, and pause/stop booleans
  song_index.set(FIRST_SONG)
  vol_var.set(MID_VOLUME)
  pause_boolean.set(False)
  stop_boolean.set(True)

  # initialize mixer and set volume to mid
  mixer.init()
  mixer.music.set_volume(MID_VOLUME*VOLUME_SCALE) 

  # create bold font type
  bold_font = tkinter.font.Font(family='Helvetica', size='8', weight='bold')

  # create 2 frames (mp3 status and mp3 controls)
  mp3_status_frame  = tkinter.LabelFrame(root, text="MP3 Status", fg="blue", 
                                         padx = FRAME_PAD, pady = FRAME_PAD)                                    
                                       
  mp3_control_frame = tkinter.LabelFrame(root, text="MP3 Controls", fg="blue", 
                                         padx = FRAME_PAD, pady = FRAME_PAD)                                      

  # create label frames for folder path, now playing, mp3 status
  labels_frame       = tkinter.Label(mp3_status_frame)
  info_frame         = tkinter.Label(mp3_status_frame)
  folder_name_frame  = tkinter.LabelFrame(info_frame, width=WIDTH, height = HEIGHT)
  playing_info_frame = tkinter.LabelFrame(info_frame, width=WIDTH, height = HEIGHT)
  status_info_frame  = tkinter.LabelFrame(info_frame, width=WIDTH, height = HEIGHT)

  # pack info frames with equal dimensions
  folder_name_frame.pack_propagate(EMPTY)
  playing_info_frame.pack_propagate(EMPTY)
  status_info_frame.pack_propagate(EMPTY)

  # create button for opening folder and labels for "now playing" and mp3 status
  folder_button = tkinter.Button(labels_frame, text = 'FOLDER', fg='black', font=bold_font,
                                 command = lambda: [open_folder(mp3_list, display_path, playing_var), 
                                 stop_audio(pause_play, player_status_info, pause_boolean, stop_boolean)])
  playing_label = tkinter.Label(labels_frame, text = 'Now Playing:', font=bold_font)
  status_label  = tkinter.Label(labels_frame, text = 'MP3 Player Status:', font=bold_font)

  # create frames for dynamic variables of folder path, now playing, and mp3 status
  folder_var_frame   = tkinter.Label(folder_name_frame, textvariable=display_path)
  playing_var_frame  = tkinter.Label(playing_info_frame, textvariable=playing_var)
  status_var_frame   = tkinter.Label(status_info_frame, textvariable=player_status_info)

  # create random button for deciding if songs will play sequentially of randomly
  random_button = tkinter.Checkbutton(mp3_control_frame, text="Random ", variable=random_var)
  
  # create volume control spinbox and label for volume
  volume_control = tkinter.Spinbox(mp3_control_frame, from_=MIN_VOLUME, to=MAX_VOLUME,
                                   width=2, textvariable = vol_var, state='readonly',
                                   command= lambda: adjust_volume(vol_var))  
  volume_label = tkinter.Label(mp3_control_frame, text = 'Volume  ') 

  # create button for going back a song
  last_song = tkinter.Button(mp3_control_frame, text = PREV_BTN_ICON, fg='black',
                             command = lambda: last_song_func(mp3_list, song_index,
                             playing_var, random_var, pause_boolean, stop_boolean,
                             pause_play, player_status_info)) 

  # create button for going forwards a song
  next_song = tkinter.Button(mp3_control_frame, text = NEXT_BTN_ICON, fg='black',
                             command = lambda: next_song_func(mp3_list, song_index,
                             playing_var, random_var, pause_boolean, stop_boolean,
                             pause_play, player_status_info))

  # create a button for pausing/playing
  pause_play = tkinter.Button(mp3_control_frame, text = PLAY_BTN_ICON, fg='black',
                             command = lambda: pause_play_func(pause_play, player_status_info,
                                                               pause_boolean, stop_boolean))
  
  # create a button for stopping the music
  stop_song = tkinter.Button(mp3_control_frame, text = STOP_BTN_ICON, fg='black',
                             command = lambda: stop_audio(pause_play, player_status_info, 
                                                          pause_boolean, stop_boolean))

  # create a button for stopping the program
  quit_prog = tkinter.Button(mp3_control_frame, text = QUIT_BTN_ICON, fg='red',
                             command = root.destroy)                                                                                                                                                  
  
  # pack folder button, "now playing" and mp3 status labels
  mp3_status_frame.pack()
  folder_button.pack(side = 'top')
  playing_label.pack(side = 'top')
  status_label.pack(side = 'top')

  # pack dynamic variables for folder path, "now playing" and mp3 status
  folder_var_frame.pack(side = 'top', expand='yes')
  playing_var_frame.pack(side = 'top')
  status_var_frame.pack(side = 'top')

  # pack frames for dynamic variables
  folder_name_frame.pack(side = 'top')
  playing_info_frame.pack(side = 'top')
  status_info_frame.pack(side = 'top')

  # pack labels frame and info frame to the left side
  labels_frame.pack(side = 'left')
  info_frame.pack(side = 'right')

  # pack mp3 control frame
  mp3_control_frame.pack()
  random_button.pack(side = 'left')
  volume_control.pack(side = 'left')
  volume_label.pack(side = 'left')

  # pack mp3 controls 
  last_song.pack(side = 'left')
  next_song.pack(side = 'left')
  pause_play.pack(side = 'left')
  stop_song.pack(side = 'left')
  quit_prog.pack(side = 'left')

  # create an options/help menu attached to the main window
  menu = tkinter.Menu(root)
  root.config(menu=menu)
  options_menu = tkinter.Menu(menu, tearoff=False)
  help_menu = tkinter.Menu(menu, tearoff=False)

  # add the options and help drop-down labels to the menu
  menu.add_cascade(label="Options", menu=options_menu)
  menu.add_cascade(label="Help", menu=help_menu)

  # add "Open playlist", "Save playlist", and "Clear playlist" drop down options
  options_menu.add_command(label="Open Playlist", command=lambda: [open_playlist(
                           mp3_list, playing_var, display_path, song_index), 
                           stop_audio(pause_play, player_status_info, pause_boolean,
                           stop_boolean)])
  options_menu.add_command(label="Save Playlist", command=lambda: save_playlist(
                           mp3_list))
  options_menu.add_command(label="Clear Playlist", command=lambda: clear_playlist(
                           display_path, playing_var, player_status_info, mp3_list, 
                           pause_play))

  # add a "help" and "about" info dialogue box within the help drop-down
  help_menu.add_command(label="Help", command=help_info)
  help_menu.add_command(label="About", command=about_info)

  # enter the tkinter main loop
  check_event(root, mp3_list, song_index, playing_var, random_var, pause_boolean, 
              stop_boolean, pause_play, player_status_info)

  root.mainloop()

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function opens a folder of the user's choice and appends the mp3 files
#   to a list
#
# INPUT PARAMETERS:
#   mp3_list - the list of mp3 files
#   display_path - the path displayed in the GUI
#   playing_var - the song displayed in the GUI
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def open_folder(mp3_list, display_path, playing_var):

  # clear list incase it had contents before opening folder
  mp3_list.clear()

  # have user browse directory and choose folder to open. join path together
  folder_name = tkinter.filedialog.askdirectory()
  os.path.join(folder_name)

  # if file is an MP3, append the path and song name to the mp3 list
  for file in os.listdir(folder_name):

    if file.endswith(MP3_SUFFIX):
      song_info = [folder_name, file]
      mp3_list.append(song_info)      

  # clear list and display error if less than two mp3 files
  if len(mp3_list) < MIN_SONGS:
    mp3_list.clear()
    tkinter.messagebox.showinfo('ERROR', 'Please choose a folder or ' +
    'playlist with at least two songs in it.')
  
  # load first song and display on GUI if there are two or more mp3 files in folder
  else:
    display_path.set(folder_name)
    mixer.music.load(mp3_list[FIRST_SONG][PATH_COLUMN] + "/" + mp3_list[FIRST_SONG][SONG_COLUMN])
    playing_var.set(mp3_list[FIRST_SONG][SONG_COLUMN])

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function pauses or plays the mixer depending on the variables passed in
#
# INPUT PARAMETERS:
#   pause_play - button for pausing and playing
#   player_status_info - status of if mixer is playing, stopped, or paused
#   pause_boolean - returns true if mixer is paused
#   stop_boolean - returns true if mixer is stopped
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def pause_play_func(pause_play, player_status_info, pause_boolean, stop_boolean):

  # local variables. Set stop to False, get pause boolean result 
  stop_boolean.set(False)
  pause_bool = pause_boolean.get()

  try: # might throw exception

    # if mixer is paused, unpause, set pause bool to false and change icon to pause
    if pause_bool == True:
      mixer.music.unpause()
      pause_boolean.set(False)
      pause_play['text'] = PAUSE_BTN_ICON
      player_status_info.set('PLAYING')  
    
    # if mixer is playing, pause, set pause bool to true and change icon to play
    elif mixer.music.get_busy() == True:
      mixer.music.pause()
      pause_boolean.set(True)
      pause_play['text'] = PLAY_BTN_ICON
      player_status_info.set('PAUSED') 
    
    # if neither the above... play mixer, set pause bool to false and change icon to pause
    else:
      mixer.music.play() 
      pause_play['text'] = PAUSE_BTN_ICON 
      player_status_info.set('PLAYING')
      pause_boolean.set(False)

  # print error message if there is not a song loaded in to play
  except:
    tkinter.messagebox.showinfo('No song to play', 'Please choose a folder or ' +
    'playlist with at least two songs in it.')  

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function stops audio when called
#
# INPUT PARAMETERS:
#   pause_play - button for pausing and playing
#   player_status_info - status of if mixer is playing, stopped, or paused
#   pause_boolean - returns true if mixer is paused
#   stop_boolean - returns true if mixer is stopped
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def stop_audio(pause_play, player_status_info, pause_boolean, stop_boolean):
  
  # stop mixer, change pause bool to false, stop bool to true and change icons
  mixer.music.stop()
  pause_boolean.set(False)
  stop_boolean.set(True)
  player_status_info.set('STOPPED')
  pause_play['text'] = PLAY_BTN_ICON 

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function opens a playlist that has been previously saved on your computer
#
# INPUT PARAMETERS:
#   mp3_list - the list of mp3 files
#   playing_var - the song displayed in the GUI
#   display_path - the path displayed in the GUI
#   song_index - index of current song being played
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def open_playlist(mp3_list, playing_var, display_path, song_index):

  # local variables
  playlist_open = ''
  written_list = []

  # clear mp3 list when opening a new playlist
  mp3_list.clear()

  # have user browse directory for file to open
  playlist_name = tkinter.filedialog.askopenfilename()

  try: # code might throw exception...
  
    # if file has at least two songs, open for reading and load to list
    if os.path.getsize(playlist_name) > LIMIT_SET:
      playlist_open = open(playlist_name, 'rb')
      written_list = pickle.load(playlist_open)

      # append each item to the mp3 list
      for item in written_list:
        mp3_list.append(item)

      # close file
      playlist_open.close()

      # set song index to first song, change displays of folder path and song playing
      song_index.set(FIRST_SONG)
      playing_var.set(mp3_list[FIRST_SONG][SONG_COLUMN])
      display_path.set(playlist_name)

      # load first song into the mixer
      mixer.music.load(mp3_list[FIRST_SONG][PATH_COLUMN] + "/" + mp3_list[FIRST_SONG][SONG_COLUMN])

    # if not at least two songs in file, print error message
    else:
      tkinter.messagebox.showinfo('Empty Playlist', 'Please choose a playlist with ' +
      'at least two songs in it.')  
  
  # print error message if invalid file
  except:
    tkinter.messagebox.showinfo('Invalid File', 'Choose a valid playlist with mp3 files.')

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function saves the current playlist when called
#
# INPUT PARAMETERS:
#   mp3_list - the list of mp3 files
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def save_playlist(mp3_list):

  # local variables
  playlist_save = ''

  # if at least two songs, ask user where to save and what to name file
  if len(mp3_list) > LIMIT_SET:
    playlist_name = tkinter.filedialog.asksaveasfilename()

    # if filename is NOT empty
    if len(playlist_name) > EMPTY:

      # open file for writing and dump mp3 filenames into file
      playlist_save = open(playlist_name, 'wb')
      pickle.dump(mp3_list, playlist_save)

      # close file
      playlist_save.close()

    # if name is empty, print error message requiring name
    else:
      tkinter.messagebox.showinfo('Name Required', 'Filename required before saving') 

  # if less than two songs, print error message 
  else:
    tkinter.messagebox.showinfo('MP3 Required', 'Please choose a folder with at ' +
    'least two MP3 files before saving a playlist.')  

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function clears the current loaded songs when called
#
# INPUT PARAMETERS:
#   display_path - the path displayed in the GUI
#   playing_var - the song displayed in the GUI
#   player_status_info - status of whether mixer is playing, stopped, or paused
#   mp3_list - the list of mp3 files
#   pause_play - button for pausing/playing mixer
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def clear_playlist(display_path, playing_var, player_status_info, mp3_list, pause_play):

  # unload current song and clear mp3 list of songs. set dynamic variables back to default
  mixer.music.unload()
  mp3_list.clear()
  display_path.set('Select folder to load') 
  playing_var.set('*** NONE ***')
  player_status_info.set('STOPPED')
  pause_play['text'] = PLAY_BTN_ICON

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function goes to the next song when called
#
# INPUT PARAMETERS:
#   mp3_list - the list of mp3 files
#   song_index - index of current song
#   playing_var - the song displayed in the GUI
#   random_var - variable to tell if random box is checked or not
#   pause_boolean - true if mixer is paused
#   stop_boolean - true if mixer is stopped
#   pause_play - button for pausing/playing mixer
#   player_status_info - status of player (playing, paused, stopped)
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def next_song_func(mp3_list, song_index, playing_var, random_var, pause_boolean, stop_boolean,
                   pause_play, player_status_info):

  # check random and stop boolean
  random_box = random_var.get()
  stop_bool = stop_boolean.get()
   
  # set random number limit to length of mp3 list 
  random_limit =len(mp3_list)

  try: # might throw exception...

    # if random box is checked, randomly assign index number in range 
    if random_box == RANDOM:
      index = random.randint(FIRST_SONG, (random_limit -LIMIT_SET))

    # if random box NOT checked, index goes up by one
    else:
      index = (song_index.get() + LIMIT_SET) 

      # stops index from being more than list length
      if index >= len(mp3_list):
        index -= LIMIT_SET

      else:
        index = index

    # load song based on index calculated
    mixer.music.load(mp3_list[index][PATH_COLUMN] + "/" + mp3_list[index][SONG_COLUMN])

    # set new song index and change "now playing" dynamic var
    song_index.set(index)
    playing_var.set(mp3_list[index][SONG_COLUMN])

    # if mixer is stopped, play, change play button to pause, and set pause bool to False
    if stop_bool == False:

      mixer.music.play()
      pause_play['text'] = PAUSE_BTN_ICON
      player_status_info.set('PLAYING')
      pause_boolean.set(False)

  # print error if exception is thrown    
  except:
    tkinter.messagebox.showinfo('MP3 Required', 'Load a playlist or folder of ' +
    'MP3 files in order to switch song.') 

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function goes to the last song when called
#
# INPUT PARAMETERS:
#   mp3_list - the list of mp3 files
#   song_index - index of current song
#   playing_var - the song displayed in the GUI
#   random_var - variable to tell if random box is checked or not
#   pause_boolean - true if mixer is paused
#   stop_boolean - true if mixer is stopped
#   pause_play - button for pausing/playing mixer
#   player_status_info - status of player (playing, paused, stopped)
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def last_song_func(mp3_list, song_index, playing_var, random_var, pause_boolean, stop_boolean,
                   pause_play, player_status_info):

  # check random and stop boolean
  random_box = random_var.get()
  stop_bool = stop_boolean.get() 

  # set random number limit to length of mp3 list 
  random_limit =len(mp3_list)

  try: # might throw exception...

    # if random box is checked, randomly assign index number in range 
    if random_box == RANDOM:
      index = random.randint(FIRST_SONG, (random_limit -LIMIT_SET))
    
    # if random box NOT checked, index goes down by one
    else:
      index = (song_index.get() - LIMIT_SET) 

      # stops index from being less than list length
      if index < FIRST_SONG:
        index += LIMIT_SET

      else:
        index = index

    # load song based on index calculated
    mixer.music.load(mp3_list[index][PATH_COLUMN] + "/" + mp3_list[index][SONG_COLUMN])

    # set new song index and change "now playing" dynamic var
    song_index.set(index)
    playing_var.set(mp3_list[index][SONG_COLUMN])

    # if mixer is stopped, play, change play button to pause, and set pause bool to False
    if stop_bool == False:

      mixer.music.play()
      pause_play['text'] = PAUSE_BTN_ICON
      player_status_info.set('PLAYING')
      pause_boolean.set(False)

  # print error if exception is thrown 
  except: 
    tkinter.messagebox.showinfo('MP3 Required', 'Load a playlist or folder of ' +
    'MP3 files in order to switch song.')  

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function adjusts volume when called
#
# INPUT PARAMETERS:
#   vol_var - dynamic variable of volume setting
# RETURN:
#   none
#
# -----------------------------------------------------------------------------
def adjust_volume(vol_var):
  
  # retrieve current volume
  volume = vol_var.get()

  # set volume to number multiplied by vol scale (range is 0.0-1.0)
  mixer.music.set_volume(volume*VOLUME_SCALE)

  return
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function checks whether a song has ended or not
#
# INPUT PARAMETERS:
#   mp3_list - the list of mp3 files
#   song_index - index of current song
#   playing_var - the song displayed in the GUI
#   random_var - variable to tell if random box is checked or not
#   pause_boolean - true if mixer is paused
#   stop_boolean - true if mixer is stopped
#   pause_play - button for pausing/playing mixer
#   player_status_info - status of player (playing, paused, stopped)
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def check_event(root, mp3_list, song_index, playing_var, random_var, pause_boolean, stop_boolean,
                pause_play, player_status_info):

  # local boolean variables
  stop_bool = stop_boolean.get()
  pause_bool = pause_boolean.get()

  # if length of list isn't empty, if stop and pause are both false, and if mixer isn't
  # playing, start next song
  if len(mp3_list) > EMPTY:
    if (stop_bool == False and pause_bool == False):
      if mixer.music.get_busy() == False:

        next_song_func(mp3_list, song_index, playing_var, random_var, pause_boolean, stop_boolean,
                       pause_play, player_status_info)

  # check again in 500 ms
  root.after(CALLBACK_DELAY, check_event, root, mp3_list, song_index, playing_var, random_var, pause_boolean, 
              stop_boolean, pause_play, player_status_info)

  return
    
# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will display a "help" dialog box when called
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def help_info():
  
  tkinter.messagebox.showinfo('Help', 'First, you must open a folder containing at ' +
  'least two MP3 files by clicking on the \"FOLDER\" button. This opens your computer ' +
  'directory and allows you to browse for any folder. The \"Random\" box allows you ' +
  'to choose whether the next song will be sequential or randomized. There is volume ' +
  'control (1-10), as well as buttons for skipping backwards or forwards a song, ' +
  'pausing, stopping, and quitting the program. Once a folder has been opened, the ' +
  'will display the path to the folder/playlist, the current song loaded, and the status ' +
  'stopped, playing, or paused. Playlists can be saved, loaded, or cleared from the MP3 ' +
  'under the options tab in the top left.')

  return

# -----------------------------------------------------------------------------
# DESCRIPTION
#   This function will display an "about" dialog box explaining the program
#   and showing the programmer's name
#
# RETURN:
#   none
# -----------------------------------------------------------------------------
def about_info():
  
  tkinter.messagebox.showinfo('About', 'Kris Meehan, 12/15/2021, MP3 Player\n' +
  'This program is an MP3 player that can save and load playlists.')

  return
#---------------------------------------------------------------------
# main function of program
#---------------------------------------------------------------------
def main():

  # call create GUI window function
  create_gui_window()

# Call the main function.
if __name__ == '__main__':
  main()