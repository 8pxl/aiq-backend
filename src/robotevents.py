import logging
from typing import Any
import requests
from enum import Enum
import db
from tables import Qualification, Teams

class RobotEvents:
    token: str
    header: dict[str, str]
    base: str
    season: int
    logger: logging.Logger = logging.getLogger(__name__)

    def __init__(self, token: str):
        self.token = token
        self.base = "https://www.robotevents.com/api/v2"
        self.season = 197
        self.header = {
            "Authorization": f"Bearer {token}"
        }

    def request(self, path: str) -> Any | None:  # pyright: ignore[reportExplicitAny, reportAny]
        if path[0] != "/":
            self.logger.exception("path needs to start with a blackslash")
            return (None)
        url = self.base + path
        res = requests.get(url, headers=self.header)
        try:
            res.raise_for_status()
        except requests.RequestException as exc:
            self.logger.exception("API request failed: %s %s", url, exc)
            return None
        return res.json()  # pyright: ignore[reportAny]

    def get_qualifications(self, robotevents_id: int) -> Qualification:
        awards = self.request(f"/teams/{str(robotevents_id)}/awards?season%5B%5D={self.season}")
        if not awards:
            return Qualification.NONE
        awards = awards["data"]
        highest = Qualification.NONE
        for award in awards:
            # print(award)
            if (award["qualifications"]):
                for qual in award["qualifications"]:
                    new = Qualification.from_string(qual)
                    if new.value > highest.value:
                        highest = new
        return highest


    def create_team(self, robotevents_id: int, score: tuple[int, int, int]):
        res = self.request(f"/teams/{robotevents_id}")
        if not res:
            return None
        team = Teams(
            id=res['id'],  # pyright: ignore[reportAny] 
            number=res['number'],  # pyright: ignore[reportAny]
            organization = res['organization'],   # pyright: ignore[reportAny]
            country= res['location']['country'],  # pyright: ignore[reportAny]
            registered = res['registered'],  # pyright: ignore[reportAny]
            grade = res['grade'],  # pyright: ignore[reportAny]
            qualification =  self.get_qualifications(res['id']),  # pyright: ignore[reportAny]
            score = score[0],
            programming = score[1],
            driver = score[2],
        )
        return team

