


import os
import typing

import jk_typing

from .DirEntryX import DirEntryX
from .StdEmitFilter import StdEmitFilter





#
# This emit filter will return only regular files that have one of the specified file extensions.
#
class FileExtEmitFilter(StdEmitFilter):

	def __init__(self, *extensions:str):
		super().__init__(
			emitWalkRoot=False,
			emitDirectories=False,
			emitRegularFiles=True,
			emitSymLinks=False,
			emitBlockDevices=False,
			emitCharacterDevices=False,
			emitSockets=False,
			emitFIFOs=False,
			emitOthers=False,
			emitErrors=True,
		)

		self.__extensions = []
		for ext in extensions:
			assert isinstance(ext, str)
			assert ext
			if not ext.startswith("."):
				ext = "." + ext
			self.__extensions.append(ext)
	#

	def checkEmit(self, entry:DirEntryX) -> bool:
		b = super().checkEmit(entry)
		if not b:
			return False

		for ext in self.__extensions:
			if entry.name.endswith(ext):
				return True

		return False
	#

#



