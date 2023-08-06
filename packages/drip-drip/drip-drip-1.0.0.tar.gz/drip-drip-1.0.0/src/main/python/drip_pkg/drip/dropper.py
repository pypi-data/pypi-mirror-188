"""Define the Dropper class"""

from typing import Any, List, Tuple


class Dropper:
    """
    This class provides the concrete implementation use by a Feeder
    instance to execute a particular type of drip-feed.
    """

    def __init__(self, config_file: str, section: str):
        """
        Creates an instance of this class.

        :param config_file: the name of the file containing the configuration information.
        :param threshold: the maximum number of files allowed in the destination directory.
        """

    def assess_condition(self) -> Tuple[int, str]:
        """
        Assess whether a drip should be executed or not.

        :return maximum number if items that can be dropped and
        explanation of any limitations.
        """

    def drop(self, item: Any) -> None:
        """
        "Drops" the supplied item, i.e. acts on that item.

        :param item: the item to be dropped.
        """

    def fill_cache(self) -> List[Any]:
        """
        Fills internal list of files to be moved.
        """
