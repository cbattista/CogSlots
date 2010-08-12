import wx

# slot machine images
SLOT_SIZE = (24,24)
IM_BAR = "images/bar.png"
IM_BELL = "images/bell.png"
IM_CHERRIES = "images/cherries.png"
IM_CLOVER = "images/clover.png"
IM_GOLDBARS = "images/gold_bullion.png"
IM_TREASURECHEST = "images/chest.png"
IM_BLANK = "images/spacer.gif"
IM_EMPTY = "images/any.png"

# pack them in to a tuple to make things easier
symbols = [IM_BAR, IM_BELL, IM_CHERRIES, IM_CLOVER, IM_GOLDBARS, IM_TREASURECHEST, IM_EMPTY]
symbolnames = ["bar", "bell", "cherries", "clover", "gold bars", "treasure", "any"]

# interface button images
IM_BACKGROUND = wx.ART_MISSING_IMAGE
IM_ORNAMENT_LEFT = wx.ART_MISSING_IMAGE
IM_ORNAMENT_RIGHT = wx.ART_MISSING_IMAGE
IM_DECREASEWAGER = wx.ART_MISSING_IMAGE
IM_DECREASEWAGER_DOWN = wx.ART_MISSING_IMAGE
IM_SPIN = wx.ART_MISSING_IMAGE
IM_SPIN_DOWN = wx.ART_MISSING_IMAGE
IM_INCREASEWAGER = wx.ART_MISSING_IMAGE
IM_INCREASEWAGER_DOWN = wx.ART_MISSING_IMAGE

#COLORS
FELT_GREEN = (0,153,0)
WINNING_GOLD = (255, 150, 0)
