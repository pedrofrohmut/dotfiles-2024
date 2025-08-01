# --- Aliases/Functions --------------------------------------------------------

alias src-rc='source ~/.zshrc'

alias vim='nvim'
alias hx='helix'

alias gits='git status'
alias gitp='git push'
alias gitac='git add . && git commit -m'
alias git-ops='git reset --soft HEAD^'

# Git diff
gitd() {
    if [ $1 ]; then
        git diff "$1" | bat
    else
        git diff . | bat
    fi
}

# Git logging
gitl() {
    if [ $1 ]; then
        git log -n "$1" | bat
    else
        git log -n 5 | bat
    fi
}

alias ls='ls --color=auto'
alias ll='ls -lAFh'
alias la='ls -1 -AFh'

alias tree='tree -C'
alias gtree='tree --gitignore'

alias ..='cd ..'
alias cp='cp --verbose'
alias mv='mv --verbose'
alias rm='rm --verbose'

alias jj='jobs'

# Depends on X11 and XClip
alias c-path='pwd | xclip -selection clipboard'

alias du-here='du -h -d 1 | sort -hr | head --lines 20'
alias dh='du-here'

# Tar easy of use
tar_to() {
    if [ ! $1 ]; then
        echo "Missing file input"
        echo "Usage: tar-to <input-path> <output-path>"
    elif [ ! $2 ]; then
        tar -xzvf $1
    else
        tar -xzvf $1 -C $2
    fi
}

alias last-installed='cat /var/log/pacman.log | grep "ALPM] installed" | tail -n 30'
alias installed="cat /var/log/pacman.log | grep 'ALPM] installed'"

alias update-grub='sudo grub-mkconfig -o /boot/grub/grub.cfg'

alias update-mirrors='sudo reflector --country "Brazil" --age 12 --protocol https \
    --sort rate --save /etc/pacman.d/mirrorlist && echo "Mirror list updated successfully!"'

alias update-arch='sudo pacman -Syu && echo "System updated successfully!"'

alias update-system='update-mirrors && update-arch'

# Setup Ocaml env
alias opam-env='eval $(opam env)'

# Setup Dotnet8 env based on file
alias dotnet8-env="source $HOME/opt/dotnet-8.0.201/dotnet8.env"

# Compile the qtile configuration for any errors
alias compile-qtile="python -m py_compile ~/.config/qtile/config.py"

# Run or flatpak
run_or_flatpak() {
    cmd_path=$(command -v $1)
    if [ $cmd_path ]; then
        $1
    else
        $2
    fi
}

# --- ENV ----------------------------------------------------------------------

# # Fcitx5
# export GTK_IM_MODULE=fcitx5
# export QT_IM_MODULE=fcitx5
# export XMODIFIERS="@im=fcitx5"
# export DefaultIMModule=fcitx5
# export SDL_IM_MODULE=fcitx5
#
# export EDITOR=/usr/bin/nvim
# export SHELL=/usr/bin/zsh
# export GIT_EDITOR=/usr/bin/nvim
#
# # Java
# export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
#
# # My local bin (my symlinks)
# export LOCAL_BIN=$HOME/.local/bin # For endeavourOS
#
# export PATH=$PATH:$LOCAL_BIN

# --- Keybinds -----------------------------------------------------------------

# \e, \E, = Escape
# ^[      = Alt key (on some keyboards this is the same as escape)
# ^?      = Delete
# ^X, ^   = Control

bindkey -v # Enables vi mode (Very good but have to rebind some stuff because of it)

# Adding minimal keybinds (using vi mode for the rest)
bindkey "^P" history-search-backward
bindkey "^N" history-search-forward
bindkey "^A" beginning-of-line
bindkey "^E" end-of-line

# Removing keys
bindkey -r '^J' # accept-line

# --- Completion ---------------------------------------------------------------

# init completion
autoload -U compinit; compinit

# Case-insensitive completion
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'

# Show completion menu if more than one option is available
zstyle ':completion:*' menu select

# Ignore completion duplicates
zstyle ':completion:*' unique

# Autocomplete from history
zstyle ':completion:*' history 1

# Colored completion (different colors for dirs/files/etc)
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"

# automatically find new executables in path
zstyle ':completion:*' rehash true

# --- Options ------------------------------------------------------------------

setopt nobeep

# --- Evals --------------------------------------------------------------------

# Starship Prompt
eval "$(starship init zsh)"

# Opam (OCaml package manager)
#eval "$(opam env)"

# Zoxide
# eval "$(zoxide init zsh)"
