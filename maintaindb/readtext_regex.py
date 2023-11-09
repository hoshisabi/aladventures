import re

def get_patt_first_group(regex, text):
    if matches := re.search(regex, text, re.MULTILINE | re.IGNORECASE):
        return matches[1]


text = """CAN YOU SURVIVE WATERDEEP'S MOST INFAMOUS DEATHTRAP?

Blue Alley lies hidden in the heart of Waterdeep. Built by a secretive wizard, it is a magic maze full of tricks, traps, strange monsters, and rich treasure. Countless adventurers have ventured inside to test their bravery and skill, yet few have returned. And now it is your turn…

Blue Alley is a 3-4 hour Dungeons & Dragons adventure for characters of 1st to 4th level. It expands upon the material presented in Waterdeep: Dragon Heist, but can be played on its own or as part of any D&D campaign.

This product is a DMs Guild Adepts adventure! The Dungeon Masters Guild Adept program brings highly talented individuals together for creative development. Guild Adept products are identified with the golden ampersand and logo.

This adventure is Adventurers League legal and uses the code DDHC-WDH-03.

This product includes:

An all-new, high-resolution map.
A MOD file to play this adventure on Fantasy Grounds!
*Note: This title is NOT for Roll20 VTT"""

# text = """
# Friendly Vampirate Captain is looking for people to participate in dragon boat festival.
# Nothing is what it seems.
#
# A Four-Hour Adventure for Tier 2 Characters. Optimized for APL 9.
#
# CONTENT WARNING: Imprisonment, Flooding.
#
# This adventure is based on Dragon Boat Festival and "Legend of the White Snake".
#
# Part of SJ-DC-TTUC series. """

#
# text = """
# You and your crew have arrived in Planet Kurion in the Busigra Wildspace to restock supplies. As soon as you've arrived, locals have rumors about the wilderness and it's natural treasures.
#
#
# A two-hour adventure for 1st to 4th level characters.
#
# Includes:
#
# Maps (Colored, Black & White)
# Statblocks of encounters
# """

# text = """
# When a nefarious bounty has the Kyriakos stymied, they approach you with an offer you
# can ill refuse.
# The hunt is on in The Prime’s fog shrouded streets, but there is also danger at every turn.
# Can you win through?
#
# A Heroic Four-Hour Adventure for Tier 2 Characters. Optimized for APL 8.
#
# Content Warning: Abuse (Charm/Mind Control), Alcohol, Hospital (Injuries from Terrorism), Possible Phobia Triggers (Clowns, Rodents, Spelljammer Crash)
#
# From veteran authors Michelle Churchill and Luís Ricardo comes a metropolitan adventure set in the Artificium system, where film noir, science fiction, and high fantasy collides and are underscored by an unsettling circus vibe. Episode 6 of Ad Astra.
# Ad Astra is a series of loosely connected Spelljammer adventures for D&D Adventurers League.
# Traverse the stars in an ancient, arcane locomotive, and experience 12 fresh takes on the spacefaring genre written and produced by bestselling Dungeon Masters Guild authors and international talents from the Dungeon Designers Discord community. Uncover the secrets of the Monad, explore unique and unconventional worlds, and unravel a mystery that spans a millennium!
# This product includes:
#
# a 61-page adventure that brings the Artificium Wildspace system to life
# a metropolis and space clowns
# custom battle maps
# custom NPC images and handouts
# standard and printer-friendly PDFs"""

# text = "A 4 Hour Adventure for Tier 2 Characters. Optimised for APL 8. Suitable for Adventurers League games."


print(get_patt_first_group(r"([0-9-]+|(two|four))[ -]hour", text))
print(get_patt_first_group(r"Tier ?([1-4])", text))
print(get_patt_first_group(r"APL ?(\d+)", text))
print(get_patt_first_group(r"Levels (\d+ ?-\d+)", text))

