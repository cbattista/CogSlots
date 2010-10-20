import wx

# slot machine images
SLOT_SIZE = (16,16)
CTRL_SIZE = (50, -1)
IM_BAR = "bar_tile.png"
IM_BELL = "bell_tile.png"
IM_CHERRIES = "cherry_tile.png"
IM_CLOVER = "clover_tile.png"
IM_GOLDBARS = "gold_tile.png"
IM_TREASURECHEST = "chest_tile.png"
IM_BLANK = "blank_tile.png"
IM_EMPTY = "any.png"

# pack them in to a tuple to make things easier
symbols = [IM_BAR, IM_BELL, IM_CHERRIES, IM_CLOVER, IM_GOLDBARS, IM_TREASURECHEST, IM_EMPTY]
symbolnames = ["bar", "bell", "cherries", "clover", "gold bars", "treasure", "blank"]

# interface button images
IM_BACKGROUND = wx.ART_MISSING_IMAGE
IM_ORNAMENT_LEFT = "ornament.png"
IM_ORNAMENT_RIGHT = "ornament.png"
IM_DECREASEWAGER = "decrease.png"
IM_DECREASEWAGER_HOVER = wx.ART_MISSING_IMAGE
IM_DECREASEWAGER_DEAC = "decrease_deac.png"
IM_SPIN = "spin.png"
IM_SPIN_HOVER = wx.ART_MISSING_IMAGE
IM_SPIN_DEAC = "spin_deac.png"
IM_INCREASEWAGER = "increase.png"
IM_INCREASEWAGER_HOVER = wx.ART_MISSING_IMAGE
IM_INCREASEWAGER_DEAC = "increase_deac.png"

#COLORS
FELT_GREEN = (0,153,0)
WINNING_GOLD = (255, 150, 0)
STEEL_BLUE = (51, 51, 102)
LIGHT_GREY =(204, 204, 204)

WEIGHTS_TEXT = "Values indicate how often symbols appear on reels."

COMBOS_TEXT = "Adjust the payout and the symbols making up a combo.  Odds are determined by the settings in the weights table above."

INSTRUCTIONS_HTML = """
<html>
<body>

<h1>Objective</h1>

<p>The objective is to get a winning combination of three objects along the red payoff line that runs across the reels. 
</p>

<h1>Payouts</h1>
<p>Different payouts are awarded depending on the size of the bet and the winning combination. Specific payout amounts are displayed in the Payout Table above the reels.
</p>
</body>
</html>
"""
