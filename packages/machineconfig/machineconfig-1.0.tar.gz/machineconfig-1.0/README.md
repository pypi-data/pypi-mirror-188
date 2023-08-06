
# Welcome to machineconfig
Machineconfig is a package for managing configuration files (aka dotfiles). The idea is to collect those critical, time-consuming-files-to-setup in one directory and reference them via symbolic links from their original locations. Thus, when a new machine is to be setup, all that is required is to clone the repo in that machine and create the symbolic links.
Dotfiles include, but are not limited to:
* `~/.gitconfig`
* `~/.ssh`
* `~/.aws`
* `~/.bash_profile`
* `~/.bashrc`
* `~/.config`
* `$profile` in Windows Powershell
* etc

Additionally, files that contain data, sensitive information that should not be pushed to a repository are contained in a directory `~/dotfiles`. The files therein are encrypted before backedup.
Additionally, scripts to perform setup of new machines and perform mundane tasks are maintained here in `scripts`. The repo uses Python to perform the tasks.

# Shortcuts
* `bit.ly/configroot` is a shortcut to this repo.
* Use `curl bit.ly/readconfig -L | bat -l md` to get the readme file.


## Windows Setup
With elevated `PowerShell`, run the following:
```powershell
# apps
Invoke-WebRequest https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_windows/apps.ps1 | Invoke-Expression
# virtual enviornment
Invoke-WebRequest https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_windows/ve.ps1 | Invoke-Expression
# dev repos
Invoke-WebRequest https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_windows/repos.ps1 | Invoke-Expression
# symlinks: locally, run: `ftpsx username@hostname[:port] ~/dotfiles -z`, then, on the remote:
. ~/code/machineconfig/src/machineconfig/setup_windows/symlinks.ps1
# pwsh profile
# ~/code/machineconfig/src/machineconfig/setup_windows/wt_and_pwsh.ps1  # experimental
# devapps:
~/code/machineconfig/src/machineconfig/setup_windows/devapps.ps1
```

###### Setup SSH connection (CHANGE APPROPRIATELY):
```powershell
Invoke-WebRequest https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_windows/openssh_all.ps1 | Invoke-Expression  # https://github.com/thisismygitrepo.keys
```

###### Install Croshell Terminal Directly,
```powershell
Invoke-WebRequest https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_windows/croshell.ps1 | Invoke-Expression
```

# Linux Setup
With `sudo` access, run the following:
```bash
# apps
# sudo -s
curl https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_linux/apps.sh | bash
# virtual enviornment
curl https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_linux/ve.sh | bash
# repos
curl https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_linux/repos.sh | bash
# symlinks and bash profile.
# locally, run: `ftpsx username@hostname[:port] ~/dotfiles -z`
# for wsl: wsl_server.ps1; ftpsx $env:USERNAME@localhost:2222 ~/dotfiles -z # OR: ln -s /mnt/c/Users/$(whoami)/dotfiles ~/dotfiles
source ~/code/machineconfig/src/machineconfig/setup_linux/symlinks.sh  # requires sudo since it invloves chmod of dotfiles/.ssh, however sudo doesn't work with source. best to have sudo -s earlier.
# devapps
source <(sudo cat ~/code/machineconfig/src/machineconfig/setup_linux/devapps.sh)
```

###### Setup SSH connection (CHANGE APPROPRIATELY):
```bash
curl https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_linux/openssh_all.sh | sudo bash  # https://github.com/thisismygitrepo.keys
# For WSL only, also run the following:
curl https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_linux/openssh_wsl.sh | sudo bash  # "https://github.com/thisismygitrepo.keys"
```

###### Install Croshell Terminal Directly,
```bash
curl https://raw.githubusercontent.com/thisismygitrepo/machineconfig/main/src/machineconfig/setup_linux/croshell.sh | sudo bash
```

# Author
Alex Al-Saffar. [email](mailto:programmer@usa.com)
