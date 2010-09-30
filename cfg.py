import wx

# slot machine images
SLOT_SIZE = (16,16)
CTRL_SIZE = (50, -1)
IM_BAR = "bar.png"
IM_BELL = "bell.png"
IM_CHERRIES = "cherries.png"
IM_CLOVER = "clover.png"
IM_GOLDBARS = "gold_bullion.png"
IM_TREASURECHEST = "chest.png"
IM_BLANK = "spacer.png"
IM_EMPTY = "any.png"

# pack them in to a tuple to make things easier
symbols = [IM_BAR, IM_BELL, IM_CHERRIES, IM_CLOVER, IM_GOLDBARS, IM_TREASURECHEST, IM_EMPTY]
symbolnames = ["bar", "bell", "cherries", "clover", "gold bars", "treasure", "blank"]

# interface button images
IM_BACKGROUND = wx.ART_MISSING_IMAGE
IM_ORNAMENT_LEFT = "money_photo.png"
IM_ORNAMENT_RIGHT = "money_photo.png"
IM_DECREASEWAGER = wx.ART_MISSING_IMAGE
IM_DECREASEWAGER_DOWN = wx.ART_MISSING_IMAGE
IM_SPIN = wx.ART_MISSING_IMAGE
IM_SPIN_DOWN = wx.ART_MISSING_IMAGE
IM_INCREASEWAGER = wx.ART_MISSING_IMAGE
IM_INCREASEWAGER_DOWN = wx.ART_MISSING_IMAGE

#COLORS
FELT_GREEN = (0,153,0)
WINNING_GOLD = (255, 150, 0)

WEIGHTS_TEXT = "Values indicate how often symbols appear on reels."

COMBOS_TEXT = "The controls below determine the winning combinations.  Adjust the payout and the symbols making up a combo.  Odds are determined by the settings in the weights table above."
