echo 'Acquire::http::Proxy "http://gateway.iitmandi.ac.in:8080";
Acquire::https::Proxy "https://gateway.iitmandi.ac.in:8080";
Acquire::ftp::Proxy "ftp://gateway.iitmandi.ac.in:8080";' | sudo tee /etc/apt/apt.conf >/dev/null

gsettings set org.gnome.system.proxy.http host "http://gateway.iitmandi.ac.in"
gsettings set org.gnome.system.proxy.http port "8080"

gsettings set org.gnome.system.proxy.https host "https://gateway.iitmandi.ac.in"
gsettings set org.gnome.system.proxy.https port "8080"

gsettings set org.gnome.system.proxy.ftp host "ftp://gateway.iitmandi.ac.in"
gsettings set org.gnome.system.proxy.ftp port "8080"

gsettings set org.gnome.system.proxy ignore-hosts "['localhost', '127.0.0.0/8', '::1', '*.some.domain', '10.0.0.0/8']"