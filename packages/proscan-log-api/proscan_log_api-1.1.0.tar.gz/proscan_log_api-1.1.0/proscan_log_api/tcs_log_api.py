import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Optional, Union

from proscan_log_api.utils import get_files


@dataclass
class TcsLog:
    data: List[dict]
    metadata: Optional[List[dict]] = None


class SlowControlClient:
    def __init__(
        self, root_dir: str = "/mnt/TCSlogs/", folders: List[str] | str = []
    ) -> None:
        self.root_dir = root_dir
        self.folders = folders
        self.units_re = re.compile(
            r"(# (?P<title>(?!Title|Description|PROSCAN_TCS|Logging)[\S]+) +(?P<key>[\S]*) +(?P<description>.+)\n)"
        )

    def _get_units(self, text: str) -> List[dict]:
        units = []
        for row in self.units_re.finditer(text):
            units.append(row.groupdict())
        return units

    def _create_pattern(self, unit_names: List[str]) -> re.Pattern:
        pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
        for i, _ in enumerate(unit_names):
            pattern = pattern + r"(?P<%s>\S+)\s+" % f"g{i}"
        return re.compile(pattern)

    def get(
        self,
        system: Literal["tvs", "tds"],
        folders: List[str] | str = [],
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
        area: Literal["G2", "G3", "O2"] | None = None,
    ) -> Optional[TcsLog]:
        data_list = []

        if not folders:
            if self.folders:
                folders = self.folders
            else:
                raise Exception("Please provide the folders to be searched!")

        for file in get_files(
            root_dir=self.root_dir,
            folders=folders,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            area=area,
            tcs_type="SlowControl",
            system=system,
        ):
            with open(file, mode="r", encoding="utf-8") as file_obj:
                text = file_obj.read()
                units = self._get_units(text)
                pattern = self._create_pattern(
                    [unit["title"] for unit in self._get_units(text)]
                )
                for row in pattern.finditer(text):
                    row_dict = {}
                    group_values = list(row.groupdict().values())
                    row_dict["timestamp"] = group_values.pop(0)
                    row_dict = {
                        units[i]["title"]: value for i, value in enumerate(group_values)
                    }
                    data_list.append(row_dict)
        return data_list


class TcsTraceClient:
    def __init__(
        self, root_dir: str = "/mnt/TCSlogs/", folders: List[str] | str = []
    ) -> None:
        self.root_dir = root_dir
        self.folders = folders

    def _create_pattern(
        _,
        timestamp: Union[int, float, datetime, None] = None,
        source: Optional[str] = None,
        signal_type: Optional[str] = None,
        message_regex: Optional[str] = None,
    ) -> re.Pattern:
        if timestamp:
            if timestamp.isinstance(int):
                time_str = datetime.strftime(
                    datetime.fromtimestamp(timestamp / 1000000), "%d.%m.%y %H:%M:%S.%f"
                )
            elif timestamp.isinstance(float):
                time_str = datetime.strftime(
                    datetime.fromtimestamp(timestamp), "%d.%m.%y %H:%M:%S.%f"
                )
            elif timestamp.isinstance(datetime):
                time_str = datetime.strftime(timestamp, "%d.%m.%y %H:%M:%S.%f")
            time_str = time_str[:21]
        else:
            time_str = r"\d{2}\.\d{2}\.\d{2}\s\d{2}\:\d{2}\:\d{2}.\d+"
        if not source:
            source = r"\w+"
        if not signal_type:
            signal_type = r"[^:]+"
        if not message_regex:
            message_regex = r"[^\n]+"
        if message_regex:
            message_regex = message_regex + r"[^\n]+"

        pattern = re.compile(
            r"(?P<timestamp>%s)\s(?P<source>%s)\s(?P<signal_type>%s):\s(?P<message>%s)"
            % (time_str, source, signal_type, message_regex)
        )
        return pattern

    def get(
        self,
        system: Literal["tds", "tvs"],
        area: Optional[Literal["G2", "G3", "O2"]],
        folders: List[str] | str = [],
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        timestamp: Union[int, float, datetime, None] = None,
        source: Optional[str] = None,
        signal_type: Optional[str] = None,
        message_regex: Optional[str] = None,
    ) -> Optional[TcsLog]:
        data_list = []
        pattern = self._create_pattern(timestamp, source, signal_type, message_regex)
        if not folders:
            if self.folders:
                folders = self.folders
            else:
                raise Exception("Please provide the folders to be searched!")

        for file in get_files(
            system=system,
            folders=folders,
            root_dir=self.root_dir,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            area=area,
            tcs_type="TcsTrace",
        ):
            with open(file, mode="r", encoding="utf-8") as file_obj:
                for row in pattern.finditer(file_obj.read()):
                    row_dict = row.groupdict()
                    row_datetime = datetime.strptime(
                        row_dict["timestamp"],
                        "%d.%m.%y %H:%M:%S.%f",
                    )
                    if (row_datetime >= start_datetime or not start_datetime) and (
                        row_datetime <= end_datetime or not end_datetime
                    ):
                        data_list.append(row_dict)

        if not data_list:
            raise Exception("No data found!")
        return data_list
