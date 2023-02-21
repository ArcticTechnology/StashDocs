#!/usr/bin/python3 -B
from .stash import Stash
from .stashgui import StashGUI
from .utils.configloader import ConfigLoader

def main():
	configparser = ConfigLoader()
	stash = Stash.stash()
	stashgui = StashGUI()
	#stash.run()

if __name__ == "__main__":
	raise SystemExit(main())