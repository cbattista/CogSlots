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

WEIGHTS_TEXT = "The controls below control the the weighting of each symbol on each reel.  A value of '1' indicates that the symbol appears once per reel, a value of '10' indicates that the symbol appears 10 times, and so on.  This affects the odds of winning combinations in two ways.  First, increasing the weight of a symbol INCREASES the winning odds of combinations containing that symbol.  Second, increasing the weight of a symbol DESCREASES the winning odds of combinations not containing that symbol."

COMBOS_TEXT = "The controls below determine the winning combinations.  Each row features contains a payout, a winning combination, and the odds of that winning combination.  You can adjust the payout and the symbols making up a combo, but the odds are determined by the settings in the weights table above, and the combos you create.  The 'any' symbol can be used as a wildcard symbol, so that whatever symbol comes up is considered a winner."