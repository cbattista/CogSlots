import wx

# slot machine images
SLOT_SIZE = (16,16)
CTRL_SIZE = (50, -1)
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
IM_ORNAMENT_LEFT = "images/money_photo.png"
IM_ORNAMENT_RIGHT = "images/money_photo.png"
IM_DECREASEWAGER = wx.ART_MISSING_IMAGE
IM_DECREASEWAGER_DOWN = wx.ART_MISSING_IMAGE
IM_SPIN = wx.ART_MISSING_IMAGE
IM_SPIN_DOWN = wx.ART_MISSING_IMAGE
IM_INCREASEWAGER = wx.ART_MISSING_IMAGE
IM_INCREASEWAGER_DOWN = wx.ART_MISSING_IMAGE

#COLORS
FELT_GREEN = (0,153,0)
WINNING_GOLD = (255, 150, 0)

WEIGHTS_TEXT = "The controls below change the weighting of each symbol on each reel.  Values indicate how often symbols appear on reels.  Increasing the weight of a symbol increases the win odds of combinations containing that symbol, and decreases the win odds of combinations not containing that symbol."

COMBOS_TEXT = "The controls below determine the winning combinations.  Adjust the payout and the symbols making up a combo.  Odds are determined by the settings in the weights table above."
