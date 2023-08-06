import re
from abc import ABC, abstractmethod
from typing import List, Union, Tuple

from pykotor.resource.formats.ssf import SSF, SSFSound
from pykotor.tslpatcher.logger import PatchLogger
from pykotor.tslpatcher.memory import PatcherMemory, TokenUsage


class ModificationsNSS:
    def __init__(self, filename: str, replace_file: bool):
        self.filename: str = filename
        self.destination: str = "override"
        self.replace_file: bool = replace_file

    def apply(self, nss: List[str], memory: PatcherMemory, logger: PatchLogger) -> None:
        source = nss[0]

        while match := re.search(r"#2DAMEMORY\d+#", source):
            token_id = int(source[match.start() + 10:match.end() - 1])
            value = memory.memory_2da[token_id]
            source = source[0:match.start()] + str(value) + source[match.end():len(source)]

        while match := re.search(r"#StrRef\d+#", source):
            token_id = int(source[match.start() + 7:match.end() - 1])
            value = memory.memory_str[token_id]
            source = source[0:match.start()] + str(value) + source[match.end():len(source)]

        nss[0] = source
