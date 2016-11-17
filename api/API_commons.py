# -*- coding:Utf-8 -*-
# !/usr/bin/env python3.5

"""

"""
import json
import time

from cogs.utils import prefs, scores


async def init():
    from kyoukai import Kyoukai

    global kyk, API_VERSION
    kyk = Kyoukai("dh_api", debug=False)
    API_VERSION = "Duckhunt API, 0.0.1 ALPHA"


async def is_channel_activated(channel):
    servers = prefs.JSONloadFromDisk("channels.json")

    try:
        if channel.id in servers[channel.server.id]["channels"]:
            activated = True
        else:
            activated = False
    except KeyError:
        activated = False

    return activated


async def prepare_resp(resp_payload, code=200, error_msg="OK"):
    resp = {
        "generated_at": int(time.time()),
        "payload"     : resp_payload,
        "error"       : {
            "code"     : code,
            "error_msg": error_msg
        },
        "api_version" : API_VERSION
    }
    return json.dumps(resp), code, {
        "Content-Type": "application/json"
    }


async def get_user_scores(channel, member):
    return {
        "server_id"             : channel.server.id,
        "channel_id"            : channel.id,
        "user_id"               : member.id,
        "name"                  : member.name,
        "nick"                  : member.nick,
        "discriminator"         : member.discriminator,
        "avatar_url"            : member.avatar_url,
        "weapon_confiscated"    : scores.getStat(channel, member, "confique"),
        "weapon_jammed"         : scores.getStat(channel, member, "enrayee"),
        "weapon_sabotaged"      : scores.getStat(channel, member, "sabotee"),
        "exp"                   : scores.getStat(channel, member, "exp"),
        "bullets"               : scores.getStat(channel, member, "balles"),
        "shots_without_ducks"   : scores.getStat(channel, member, "tirsSansCanards"),
        "ducks_killed"          : scores.getStat(channel, member, "canardsTues"),
        "best_time"             : scores.getStat(channel, member, "meilleurTemps", default=prefs.getPref(channel.server, "time_before_ducks_leave")),
        "shoots_missed"         : scores.getStat(channel, member, "tirsManques"),
        "chargers"              : scores.getStat(channel, member, "chargeurs"),
        "banned"                : scores.getStat(channel, member, "banni"),
        "hunters_killed"        : scores.getStat(channel, member, "chasseursTues"),
        "super_ducks_killed"    : scores.getStat(channel, member, "superCanardsTues"),
        "last_giveback"         : scores.getStat(channel, member, "lastGiveback"),
        "wet"                   : scores.getStat(channel, member, "mouille"),
        "time_explosive_ammo"   : scores.getStat(channel, member, "munExplo"),
        "time_AP_ammo"          : scores.getStat(channel, member, "munAP_"),
        "time_grease"           : scores.getStat(channel, member, "graisse"),
        "time_life_insurence"   : scores.getStat(channel, member, "AssuranceVie"),
        "time_clover"           : scores.getStat(channel, member, "trefle"),
        "clover_exp"            : scores.getStat(channel, member, "trefle_exp"),
        "time_infrared_detector": scores.getStat(channel, member, "detecteurInfra"),
        "time_silencer"         : scores.getStat(channel, member, "silencieux")
    }
