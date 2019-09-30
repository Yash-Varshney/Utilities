# Terminal proxy
echo '' | sudo tee /etc/apt/apt.conf >/dev/null
echo 'Terminal proxy removed'

# System proxy
gsettings set org.gnome.system.proxy mode 'none'
echo 'System proxy removed'

# git proxy
X="$(git --version)" 
if [[ ${X:11:1} -eq $2 ]]; then
	git config --global --unset http.proxy
	git config --global --unset https.proxy
	git config --global --unset core.gitproxy
	echo 'Git proxy removed'
fi

# Terminal env proxy
file=~/.bashrc
echo "$file" | \
while IFS= read -r cmd; do
	if [[ $cmd != "export"*"proxy"* ]]; then
		echo ${cmd} ;
	fi
done < ~/.bashrc > ~/.bashrc.t
mv ~/.bashrc{.t,}
echo 'Terminal-env proxy removed'
echo '****** Restart Terminal ******'