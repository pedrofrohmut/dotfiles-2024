local wezterm = require("wezterm")
local config = wezterm.config_builder()
local mykeys = require("./mykeys")

config.default_prog = { "/usr/bin/zsh" }
config.enable_tab_bar = false

-- Font
config.font = wezterm.font("FiraMono Nerd Font", { weight = "Regular", italic = false })
config.font_size = 10.0
config.line_height = 1.10

-- Colors
config.color_scheme = "Sonokai (Gogh)"
config.colors = {
    background = "#1a1b2c", -- Tokyo night bg
}
config.window_background_opacity = 0.9

-- Keys
config.disable_default_key_bindings = true
mykeys.mapkeys(config)

return config
