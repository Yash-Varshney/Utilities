# Copying Alias files to a Given Folder
sudo mkdir ~/.Ubuntu_Set_up
sudo cp ./*prxy.sh ~/.Ubuntu_Set_up/

# Creating proxy aliases
aliasFile=~/.bash_aliases
echo "$aliasFile" | \
while IFS= read -r cmd; do
	if [[ $cmd != *"prxy.sh" ]]; then
		echo ${cmd} ;
	fi
done < ~/.bash_aliases > ~/.bash_aliases.t
mv ~/.bash_aliases{.t,}
echo 'alias set_prxy=". ~/.Ubuntu_Set_up/prxy.sh"
alias rmv_prxy=". ~/.Ubuntu_Set_up/no_prxy.sh"' >> $aliasFile

# Setting-up Touchpad Gestures
sudo gpasswd -a $USER input
sudo apt-get install gem
sudo apt-get install libinput-tools
sudo apt-get install xdotool
sudo apt-get install ruby
sudo -E gem install fusuma
cd ~/.config
mkdir fusuma
cd fusuma
touch config.yml
cat <<EOF > ~/.config/fusuma/config.yml
swipe:
  3: 
    left: 
      command: 'xdotool key alt+Left'
    right: 
      command: 'xdotool key alt+Right'
    up: 
      command: 'xdotool key super'
    down: 
      command: 'xdotool key super'
  4:
    left: 
      command: 'xdotool key ctrl+alt+Down'
    right: 
      command: 'xdotool key ctrl+alt+Up'
    up: 
      command: 'xdotool key ctrl+alt+Down'
    down: 
      command: 'xdotool key ctrl+alt+Up'
pinch:
  in:
    command: 'xdotool key ctrl+plus'
  out:
     command: 'xdotool key ctrl+minus'

threshold:
  swipe: 0.4
  pinch: 0.03

interval:
  swipe: 0.8
  pinch: 0.05
EOF

# Adding Fusuma(Touchpad-Gestures) to start-up 
touch ~/.gnomerc
cat <<EOF > ~/.gnomerc
'sudo fusuma'
EOF

sudo apt auto-remove

echo "Gnome Environment has been Set-Up"

echo "To Set Proxy run set_prxy in Comand Line and to remove run rmv_prxy."

echo "Touchpad Gestures have been configured similar to that of windows. Edit ~/.config/fusuma/config.yml for futher customization !!"

# Running Fusuma
sudo fusuma