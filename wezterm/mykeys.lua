local wezterm = require("wezterm")
local act = wezterm.action

local M = {}

local keys = {
    { key = "Enter", mods = "ALT", action = act.ToggleFullScreen },
    { key = "Enter", mods = "CTRL|SHIFT", action = act.SpawnWindow },

    -- Modes
    { key = "f", mods = "SHIFT|CTRL", action = act.Search("CurrentSelectionOrEmptyString") },
    { key = "x", mods = "SHIFT|CTRL", action = act.ActivateCopyMode },

    -- Font Size
    { key = "=", mods = "CTRL", action = act.IncreaseFontSize },
    { key = "-", mods = "CTRL", action = act.DecreaseFontSize },
    { key = "0", mods = "CTRL", action = act.ResetFontSize },

    -- Clipboard
    { key = "C", mods = "SHIFT|CTRL", action = act.CopyTo("Clipboard") },
    { key = "V", mods = "SHIFT|CTRL", action = act.PasteFrom("Clipboard") },
}

local key_tables = {
    copy_mode = {
        -- Custom
        { key = "l", mods = "SHIFT", action = act.CopyMode("MoveToEndOfLineContent") },
        { key = "h", mods = "SHIFT", action = act.CopyMode("MoveToStartOfLineContent") },

        -- Default
        { key = "v", mods = "NONE", action = act.CopyMode({ SetSelectionMode = "Cell" }) },
        { key = "v", mods = "CTRL", action = act.CopyMode({ SetSelectionMode = "Block" }) },
        { key = "V", mods = "NONE", action = act.CopyMode({ SetSelectionMode = "Line" }) },

        { key = "$", mods = "NONE", action = act.CopyMode("MoveToEndOfLineContent") },
        { key = "^", mods = "NONE", action = act.CopyMode("MoveToStartOfLineContent") },
        { key = "0", mods = "NONE", action = act.CopyMode("MoveToStartOfLine") },
        { key = "O", mods = "NONE", action = act.CopyMode("MoveToSelectionOtherEndHoriz") },

        { key = "g", mods = "NONE", action = act.CopyMode("MoveToScrollbackTop") },
        { key = "G", mods = "NONE", action = act.CopyMode("MoveToScrollbackBottom") },

        { key = "h", mods = "NONE", action = act.CopyMode("MoveLeft") },
        { key = "j", mods = "NONE", action = act.CopyMode("MoveDown") },
        { key = "k", mods = "NONE", action = act.CopyMode("MoveUp") },
        { key = "l", mods = "NONE", action = act.CopyMode("MoveRight") },
        { key = "b", mods = "NONE", action = act.CopyMode("MoveBackwardWord") },
        { key = "w", mods = "NONE", action = act.CopyMode("MoveForwardWord") },
        { key = "e", mods = "NONE", action = act.CopyMode("MoveForwardWordEnd") },

        { key = "u", mods = "CTRL", action = act.CopyMode({ MoveByPage = -0.5 }) },
        { key = "d", mods = "CTRL", action = act.CopyMode({ MoveByPage = 0.5 }) },
        { key = "b", mods = "CTRL", action = act.CopyMode("PageUp") },
        { key = "f", mods = "CTRL", action = act.CopyMode("PageDown") },
        { key = "PageUp", mods = "NONE", action = act.CopyMode("PageUp") },
        { key = "PageDown", mods = "NONE", action = act.CopyMode("PageDown") },

        {
            key = "y",
            mods = "NONE",
            action = act.Multiple({ { CopyTo = "ClipboardAndPrimarySelection" }, { CopyMode = "Close" } }),
        },
        {
            key = "Enter",
            mods = "NONE",
            action = act.Multiple({ { CopyTo = "ClipboardAndPrimarySelection" }, { CopyMode = "Close" } }),
        },

        { key = "q", mods = "NONE", action = act.CopyMode("Close") },
    },

    search_mode = {
        { key = "Escape", mods = "NONE", action = act.CopyMode("Close") },
        { key = "n", mods = "CTRL", action = act.CopyMode("NextMatch") },
        { key = "p", mods = "CTRL", action = act.CopyMode("PriorMatch") },
        { key = "r", mods = "CTRL", action = act.CopyMode("CycleMatchType") },
        { key = "u", mods = "CTRL", action = act.CopyMode("ClearPattern") },
    },
}

M.mapkeys = function(config)
    config.keys = keys
    config.key_tables = key_tables
end

return M
