from abc import ABC, abstractmethod

from .extraction_result import ExtractionResult


class Extractor(ABC):
    @abstractmethod
    def extract_timetable(self, group_id: str) -> ExtractionResult:
        """
        Extracts object of :class:`common.timetable_objects.Timetable` using id of group.

        Examples of group ids:

        21203

        23717

        22710.1

        23402м

        23402m

        20401с

        20401s

        Note: group ids 23402м and 23402m are the ids of the same group.

        :param group_id: id of group, can contain any number of spaces at the beginning and at the end.
        """

        pass

    @abstractmethod
    def extract_room(self, room_name: str) -> ExtractionResult:
        """
        Extracts object of :class:`common.timetable_objects.Room` using name of room.

        Examples of valid names:

        3107

        402 ГК

        433 ЛК

        118а ЛК

        т2221

        т212 ГК

        т531 ЛК

        МА

        БА

        1216 студия

        :param room_name: name of room, can contain any positive number of spaces between words, any number of spaces at
        the beginning and at the end, case doesn't matter.
        """

        pass

    @abstractmethod
    def extract_tutor(self, tutor_name: str) -> ExtractionResult:
        """
        Extracts object of :class:`common.timetable_objects.Tutor` by name (short or full). It can contain any number of spaces
        at the beginning and at the end.


        **Format of short name**

        "<last name> <shortened first name>.<shortened patronymic>."

        *Examples of valid short names*

        Доманова Е.Д.

        Валишев А.И.


        **Format of full name**

        "<last name> <first name> <patronymic>"

        *Examples of valid full names*

        Доманова Елена Дмитриевна

        Валишев Абрик Ибрагимович

        :param tutor_name: name of tutor in correct format.
        """

        pass

    @abstractmethod
    def extract_times(self) -> ExtractionResult:
        """
        Extracts times of :class:`common.timetable_objects.Times` (timestamps when lessons begin).
        """

        pass
