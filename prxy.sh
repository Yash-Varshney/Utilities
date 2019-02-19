#	setting terminal proxy
echo 'Acquire::http::Proxy "http://gateway.iitmandi.ac.in:8080";
Acquire::https::Proxy "https://gateway.iitmandi.ac.in:8080";
Acquire::ftp::Proxy "ftp://gateway.iitmandi.ac.in:8080";' | sudo tee /etc/apt/apt.conf >/dev/null
echo 'Terminal proxy configured'

#	Setting system proxy
gsettings set org.gnome.system.proxy mode 'manual'
gsettings set org.gnome.system.proxy.http host "http://gateway.iitmandi.ac.in"
gsettings set org.gnome.system.proxy.http port "8080"
gsettings set org.gnome.system.proxy.https host "https://gateway.iitmandi.ac.in"
gsettings set org.gnome.system.proxy.https port "8080"
gsettings set org.gnome.system.proxy.ftp host "ftp://gateway.iitmandi.ac.in"
gsettings set org.gnome.system.proxy.ftp port "8080"
gsettings set org.gnome.system.proxy ignore-hosts "['localhost', '127.0.0.0/8', '::1', '*.some.domain', '10.0.0.0/8']"
echo 'System proxy configured'

#	Git proxy set-up
X="$(git --version)"
if [[ ${X:11:1} -eq $2 ]]; then
	git config --global http.proxy http://gateway.iitmandi.ac.in:8080
	git config --global https.proxy https://gateway.iitmandi.ac.in:8080
	echo 'Git proxy configured'
fi

#	Terminal env proxy set-up
file=~/.bashrc
echo "$file" | \
while IFS= read -r cmd; do
	if [[ $cmd != "export"*"proxy"* ]]; then
		echo ${cmd} ;
	fi
done < ~/.bashrc > ~/.bashrc.t
mv ~/.bashrc{.t,}
echo 'export https_proxy=https://gateway.iitmandi.ac.in:8080
export http_proxy=http://gateway.iitmandi.ac.in:8080
export all_proxy=http://gateway.iitmandi.ac.in:8080' >> ~/.bashrc
echo 'Terminal-env proxy configured'

echo '****** Restart Terminal ******'