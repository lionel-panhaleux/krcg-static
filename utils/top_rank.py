from typing import Generator, Optional

import aiohttp
import asyncio
import collections
import datetime
import dateutil.relativedelta
import enum
import itertools
import json
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

IGNORE_ONLINE = False
REFRESH = False
MAX_EVENT_ID = 10680
ONLINE_EVENTS = {
    9611,
    9612,
    9614,
    9619,
    9622,
    9630,
    9633,
    9636,
    9648,
    9654,
    9657,
    9661,
    9664,
    9666,
    9694,
    9706,
    9710,
    9713,
    9714,
    9719,
    9720,
    9721,
    9723,
    9724,
    9740,
    9743,
    9745,
    9753,
    9754,
    9755,
    9759,
    9760,
    9761,
    9762,
    9763,
    9767,
    9768,
    9769,
    9770,
    9771,
    9772,
    9773,
    9774,
    9775,
    9777,
    9780,
    9782,
    9783,
    9784,
    9788,
    9790,
    9794,
    9802,
    9810,
    9813,
    9815,
    9828,
    9831,
    9832,
    9834,
    9837,
    9842,
    9852,
    9856,
    9861,
    9872,
    9879,
    9885,
    9888,
    9891,
    9897,
    9898,
    9899,
    9930,
    9931,
    9932,
    9946,
    9960,
    9976,
    9984,
    9996,
    9997,
    10008,
    10012,
    10021,
    10044,
    10046,
    10047,
    10058,
    10064,
    10068,
    10073,
    10077,
    10099,
    10190,
    10209,
    10232,
    10240,
    10273,
    10285,
    10455,
    10458,
    10476,
    10508,
    10522,
    10527,
    10528,
    10576,
    10591,
}

ONLINE_VENUES = {
    (3845, "Online"),
    (3876, "Campina Grande Online"),
    (3866, "Lackey Online"),
    (3839, "Lackey"),
    (3853, "Lackey"),
    (3859, "Lackey"),
    (3905, "Lackey"),
    (3856, "Lackey "),
    (3867, "Lackey via Discord"),
    (3842, "Lackey via Discord"),
    (3858, "Lackey via Discord"),
    (3841, "SchreckNET"),
    (3908, "Table Top Simulator"),
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
                players[vekn] = result["firstname"] + " " + result["lastname"]
    return players


def main():
    if REFRESH:
        events = asyncio.run(_get_events())
        events = Events(__root__=sorted(events, key=lambda e: e.date))
        with open("tournament_points.json", "w") as fp:
            fp.write(events.json())
    else:
        events = Events.parse_file("tournament_points.json")

    months_18 = dateutil.relativedelta.relativedelta(months=+18)
    players_scores = collections.defaultdict(list)
    top_players = []
    points_records = []
    top_player, top_score, max_score, top_start_date = None, 0, 0, None
    events = [
        e
        for e in events.__root__
        if e.eventtype_id
        in {
            EventType.STANDARD_CONSTRUCTED,
            EventType.CONTINENTAL_CHAMPIONSHIP,
            EventType.CONTINENTAL_QUALIFIER,
            EventType.NATIONAL_CHAMPIONSHIP,
            EventType.NATIONAL_QUALIFIER,
            EventType.MINI_QUALIFIER,
            EventType.GRAND_PRIX,
        }
        and datetime.date(2020, 1, 1) <= e.event_startdate <= datetime.date.today()
        and int(e.event_id) in ONLINE_EVENTS
        and e.attendance > 9
    ]
    past = itertools.groupby(events, key=lambda e: e.date)
    current = itertools.groupby(events, key=lambda e: e.date)
    begin_date, begin_events = next(past)
    for date, events_on_date in current:
        top_start_date = top_start_date or date
        for event in events_on_date:
            logger.debug("Adding %s event#%s", date, event.event_id)
            for player in event.players:
                players_scores[player.veknid].append(player.rtp)
        while begin_date + months_18 < date:
            for event in begin_events:
                logger.debug("Removing %s event#%s", date, event.event_id)
                for player in event.players:
                    players_scores[player.veknid].pop(0)
            begin_date, begin_events = next(past)
        if not players_scores:
            continue
        new_top_player, new_top_score = max(
            [
                (vekn, sum(sorted(points, reverse=True)[:8]))
                for vekn, points in players_scores.items()
            ],
            key=lambda a: a[1],
        )
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

    print(f"{top_player} from {date} until today reached {top_score}")
    top_players.append([top_player, top_start_date, datetime.date.today(), top_score])
    print(f"{len(events)} tournaments taken into account (VEKN)")
    players = asyncio.run(_get_vekns({p[0] for p in top_players}))
    print("\n\n===================================================================\n")
    print("TOP PLAYERS")
    for vekn, start, end, score in top_players:
        print(
            ",".join(
                [
                    players.get(vekn, "N/A"),
                    vekn,
                    start.isoformat(),
                    end.isoformat(),
                    str(score),
                ]
            )
        )
    print("\n\n===================================================================\n")
    print("SCORE RECORDS")
    for vekn, dat, score in points_records:
        print(",".join([players.get(vekn, "N/A"), vekn, dat.isoformat(), str(score)]))


if __name__ == "__main__":
    main()
