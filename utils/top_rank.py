from typing import Generator, Optional

import aiohttp
import asyncio
import collections
import csv
import dataclasses
import datetime
import dateutil.relativedelta
import enum
import itertools
import logging
import os
import pydantic


logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG") else logging.INFO,
    format="[%(levelname)7s] %(message)s",
)
logger = logging.getLogger()
VEKN_LOGIN = os.getenv("VEKN_LOGIN")
VEKN_PASSWORD = os.getenv("VEKN_PASSWORD")


class RankingType(enum.IntEnum):
    OFFLINE_CONSTRUCTED = 1
    ONLINE_CONSTRUCTED = 2


RANKING_TYPE = RankingType.OFFLINE_CONSTRUCTED
REFRESH = False
MAX_EVENT_ID = 10700

# liga RTPs (manual addition from Igor)
MANUAL_ADDITION = {
    datetime.date(2020, 11, 28): {
        "1004065": 158,
        "6060012": 150,
        "8500048": 176,
        "3040004": 148,
        "2150015": 311,
        "1002979": 55,
        "7400050": 9,
        "1003214": 65,
        "4550009": 17,
        "1800007": 13,
        "5230002": 17,
        "7400007": 31,
        "1800008": 9,
        "6060015": 71,
        "1003217": 53,
        "1005186": 71,
        "4440049": 31,
        "3040009": 57,
        "3540410": 25,
        "5950005": 17,
        "7400021": 5,
        "7630001": 49,
        "1002308": 29,
        "6110002": 17,
        "8580039": 31,
        "5810002": 13,
        "1820002": 71,
        "1000565": 7,
        "4200008": 15,
        "1820011": 5,
        "5850007": 37,
        "6060020": 5,
        "6060009": 5,
        "6110000": 11,
        "2570010": 35,
        "4550004": 29,
        "1003221": 35,
        "1000317": 23,
        "3200246": 35,
        "5940017": 19,
        "6060005": 25,
        "7630037": 11,
        "9670004": 33,
        "1006065": 35,
        "5110005": 5,
        "6010157": 73,
        "9098134": 5,
        "6010151": 33,
        "7060055": 43,
        "7240009": 31,
        "9098137": 33,
        "6230002": 25,
        "8500050": 5,
        "3080036": 9,
        "9098159": 27,
        "3080035": 5,
        "3190087": 13,
        "1004066": 25,
        "9200002": 5,
        "7060071": 23,
        "1004064": 57,
        "9098136": 15,
    }
}


class EventType(enum.IntEnum):
    DEMO = 1
    STANDARD_CONSTRUCTED = 2
    LIMITED = 3
    MINI_QUALIFIER = 4
    CONTINENTAL_QUALIFIER = 5
    CONTINENTAL_CHAMPIONSHIP = 6
    NATIONAL_QUALIFIER = 7
    NATIONAL_CHAMPIONSHIP = 8
    STORYLINE = 9
    LAUNCH = 10
    CUSTOM_STORYLINE = 11
    UNSANCTIONED = 12
    LIMITED_NATIONAL_CHAMPIONSHIP = 13
    LIMITED_CONTINENTAL_CHAMPIONSHIP = 14
    GRAND_PRIX = 15


class PlayerResult(pydantic.BaseModel):
    pos: int
    wd: Optional[bool] = 0
    dq: Optional[bool] = 0
    veknid: str
    firstname: str
    lastname: str
    gw: int
    vp: float
    tp: int
    tie: Optional[int] = 0
    vpf: float
    rtp: int


class Event(pydantic.BaseModel):
    event_id: str
    event_name: str
    event_startdate: datetime.date
    # event_starttime: Optional[datetime.time] -- ignore because bad 24:00:00 format
    event_enddate: datetime.date
    # event_endtime: Optional[datetime.time] -- ignore because bad 24:00:00 format
    event_isonline: bool
    venue_id: Optional[int]
    venue_name: Optional[str]
    venue_city: Optional[str]
    venue_country: Optional[str]
    eventtype_id: Optional[EventType]
    eventtype_name: Optional[str]
    rounds: Optional[str]
    attendance: int
    players: list[PlayerResult]

    @property
    def date(self):
        return self.event_enddate or self.event_startdate

    @property
    def constructed(self):
        return (
            self.eventtype_id
            in {
                EventType.STANDARD_CONSTRUCTED,
                EventType.CONTINENTAL_CHAMPIONSHIP,
                EventType.CONTINENTAL_QUALIFIER,
                EventType.NATIONAL_CHAMPIONSHIP,
                EventType.NATIONAL_QUALIFIER,
                EventType.MINI_QUALIFIER,
                EventType.GRAND_PRIX,
            }
            and self.attendance > 9
        )

    @property
    def online(self):
        return self.event_isonline


class Events(pydantic.BaseModel):
    __root__: list[Event]


class IgnoreError(RuntimeError):
    pass


async def _get_event(session, token, event_num) -> Event:
    async with session.get(
        f"https://www.vekn.net/api/vekn/event/{event_num}",
        headers={"Authorization": f"Bearer {token}"},
    ) as response:
        result = await response.json()
        data = result["data"]
        if not data:
            raise IgnoreError(f"No data for event #{event_num}: {result}")
        events = data.get("events")
        if not events:
            raise IgnoreError(f"No data.events for event #{event_num}: {result}")
        if len(events) > 1:
            raise RuntimeError(f"Multiple events for event #{event_num}: {result}")
        try:
            event = Event(**events[0])
        except pydantic.ValidationError as e:
            raise RuntimeError(
                f"Validation error for event #{event_num} ({result}): "
                + str(e).replace("\n", " ")
            )
        if not event.eventtype_id:
            raise IgnoreError(f"No event type for event #{event_num}: {result}")
        if not event.date:
            raise RuntimeError(f"No date for event #{event_num}: {result}")
        return event


def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


async def _get_events() -> list[Event]:
    logger.info("Authenticating...")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://www.vekn.net/api/vekn/login",
            data={"username": VEKN_LOGIN, "password": VEKN_PASSWORD},
        ) as response:
            result = await response.json()
            token = result.get("data", {}).get("auth", None)
            if not token:
                raise RuntimeError(f"Unable to authentify to VEKN: {result}")

        logger.info("Getting events...")
        results = []
        for event_ids in batched(range(1, MAX_EVENT_ID), 50):
            executed = await asyncio.gather(
                *(_get_event(session, token, i) for i in event_ids),
                return_exceptions=True,
            )
            print(".", end="", flush=True)
            for result in executed:
                if isinstance(result, Event):
                    results.append(result)
                elif isinstance(result, IgnoreError):
                    continue
                else:
                    print(result)
        return results


async def _get_vekns(vekns) -> dict:
    players = {}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://www.vekn.net/api/vekn/login",
            data={"username": VEKN_LOGIN, "password": VEKN_PASSWORD},
        ) as response:
            result = await response.json()
            token = result.get("data", {}).get("auth", None)
            if not token:
                raise RuntimeError(f"Unable to authentify to VEKN: {result}")
        for vekn in vekns:
            vekn = str(vekn)
            async with session.get(
                f"https://www.vekn.net/api/vekn/registry?filter={vekn}",
                headers={"Authorization": f"Bearer {token}"},
            ) as response:
                result = await response.json()
                result = result["data"]
                if isinstance(result, str):
                    raise RuntimeError(f"VEKN returned an error: {result}")
                result = result["players"]
                if len(result) > 1:
                    raise RuntimeError("Incomplete VEKN ID#")
                if len(result) < 1:
                    raise RuntimeError("VEKN ID# not found")
                result = result[0]
                if result["veknid"] != vekn:
                    raise RuntimeError("VEKN ID# not found")
                players[vekn] = (
                    result["firstname"] + " " + result["lastname"],
                    result["countryname"],
                )
    return players


@dataclasses.dataclass
class Performance:
    event_id: str
    rtp: int

    def __repr__(self):
        return f"<{self.event_id}: {self.rtp}>"


class Ranking:
    window = dateutil.relativedelta.relativedelta(months=+18)
    out_of_window = dateutil.relativedelta.relativedelta(months=+18, days=+1)

    def __init__(self):
        self.events: list[Event] = []
        self.performances: dict[str, list[Performance]] = collections.defaultdict(list)
        self.current: list[tuple[datetime.date, list[Event]]] = []

    def rank(self):
        return sorted(
            [
                (vekn, sorted(performance, reverse=True, key=lambda p: p.rtp)[:8])
                for vekn, performance in self.performances.items()
            ],
            key=lambda a: sum(p.rtp for p in a[1]),
            reverse=True,
        )

    def adjust_for_date(self, date: datetime.date):
        while self.current and self.current[0][0] + self.window < date:
            for event in self.current[0][1]:
                logger.debug("Removing %s event#%s", event.date, event.event_id)
                for player in event.players:
                    self.performances[player.veknid].pop(0)
            yield self.current[0][0] + self.out_of_window, self.rank()
            self.current.pop(0)

    def add(self, date: datetime.date, events: list[Event]):
        for event in events:
            logger.debug("Adding %s event#%s", event.date, event.event_id)
            for player in event.players:
                self.performances[player.veknid].append(
                    Performance(event_id=event.event_id, rtp=player.rtp)
                )
        self.current.append((date, events))
        return date, self.rank()

    @classmethod
    def load_from_vekn(cls):
        ret = cls()
        ret.events = sorted(asyncio.run(_get_events()), key=lambda e: e.date)
        with open("tournament_points.json", "w") as fp:
            fp.write(Events(__root__=ret.events).json())
        return ret

    @classmethod
    def load_from_cache(cls):
        ret = cls()
        ret.events = Events.parse_file("tournament_points.json").__root__
        return ret

    def filter(self, type: RankingType):
        if type == RankingType.OFFLINE_CONSTRUCTED:
            self.events = [e for e in self.events if e.constructed and not e.online]
        elif type == RankingType.ONLINE_CONSTRUCTED:
            self.events = [e for e in self.events if e.constructed and e.online]

    def yield_rankings(self):
        for date, events_on_date in itertools.groupby(
            self.events, key=lambda e: e.date
        ):
            events_on_date = list(events_on_date)
            yield from self.adjust_for_date(date)
            yield self.add(date, events_on_date)
        yield from self.adjust_for_date(datetime.date.today())


def main():
    if REFRESH:
        ranking = Ranking.load_from_vekn()
    else:
        ranking = Ranking.load_from_cache()

    ranking.filter(RANKING_TYPE)
    if RANKING_TYPE == RankingType.ONLINE_CONSTRUCTED:
        for date, players in MANUAL_ADDITION.items():
            event = Event.construct(
                event_id=f"manual-{date}",
                event_name=f"manual-{date}",
                event_enddate=date,
                event_isonline=True,
                attendance=len(players),
                players=[
                    PlayerResult.construct(
                        veknid=veknid,
                        rtp=rtp,
                    )
                    for veknid, rtp in players.items()
                ],
            )
            logging.debug("Adding manual event: %s", event)
            ranking.events.append(event)
        ranking.events.sort(key=lambda e: e.date)
    top_players = []
    points_records = []
    top_player, top_score, max_score, top_start_date = None, 0, 0, None
    for date, rank in ranking.yield_rankings():
        new_top_player, new_top_performance = rank[0]
        new_top_score = sum(p.rtp for p in new_top_performance)
        if new_top_player != top_player:
            if top_player:
                print(
                    f"{top_player} from {top_start_date} to {date} reached {top_score}"
                )
                top_players.append([top_player, top_start_date, date, top_score])
            top_start_date = date
            top_player = new_top_player
            top_score = new_top_score
        elif new_top_score > top_score:
            top_score = new_top_score
        if top_score > max_score:
            max_score = top_score
            print(f"New max score on {date}: {top_player} with {max_score}")
            points_records.append([top_player, date, max_score])

    print(f"{len(ranking.events)} tournaments taken into account (VEKN)")
    top50 = ranking.rank()[:50]
    players = asyncio.run(
        _get_vekns({p[0] for p in top_players} | {p[0] for p in top50})
    )
    with open("top_players.csv", "w") as fp:
        w = csv.writer(fp)
        w.writerows(
            [
                players.get(vekn, "N/A")[0],
                vekn,
                players.get(vekn, "N/A")[1],
                start.isoformat(),
                end.isoformat(),
                str(score),
            ]
            for vekn, start, end, score in top_players
        )
    with open("score_records.csv", "w") as fp:
        w = csv.writer(fp)
        w.writerows(
            [players.get(vekn, "N/A"), vekn, dat.isoformat(), str(score)]
            for vekn, dat, score in points_records
        )
    print("Current ranking")
    for player, score in top50:
        print(player, players.get(player, "N/A"), sum(s.rtp for s in score), score)


if __name__ == "__main__":
    main()
