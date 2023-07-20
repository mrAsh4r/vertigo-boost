import hashlib
import random

alnum = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
ralnum = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
    'J': 8,
    'K': 9,
    'L': 10,
    'M': 11,
    'N': 12,
    'P': 13,
    'Q': 14,
    'R': 15,
    'S': 16,
    'T': 17,
    'U': 18,
    'V': 19,
    'W': 20,
    'X': 21,
    'Y': 22,
    'Z': 23,
    '2': 24,
    '3': 25,
    '4': 26,
    '5': 27,
    '6': 28,
    '7': 29,
    '8': 30,
    '9': 31,
}

default_steam_id = 0x110000100000000
default_group_id = 0x170000000000000

def b32(input):
    res = ""
    input = input.to_bytes(8, 'big')
    input = int.from_bytes(input, 'little')

    for i in range(13):
        if i == 4 or i == 9:
            res += "-"
        res += alnum[input & 0x1F]
        input >>= 5

    return res

def rb32(input):
    res = 0

    for i in range(13):
        if i == 4 or i == 9:
            input = input[1:]
        res |= ralnum[input[0]] << (5 * i)
        input = input[1:]

    res = res.to_bytes(8, 'big')
    res = int.from_bytes(res, 'little')
    return res

def hash_steam_id(id):
    account_id = id & 0xFFFFFFFF
    strange_steam_id = account_id | 0x4353474F00000000

    bytes = strange_steam_id.to_bytes(8, 'little')

    hash = hashlib.md5(bytes).digest()
    buf = hash[:4]

    buf = int.from_bytes(buf, 'little')
    return buf

def make_u64(hi, lo):
    return (hi << 32) | lo

class FriendCode:
    @staticmethod
    def encode(steamid):
        steamid = int(steamid)

        h = hash_steam_id(steamid)

        r = 0
        for i in range(8):
            id_nibble = steamid & 0xF
            steamid >>= 4

            hash_nibble = (h >> i) & 1

            a = (r << 4) | id_nibble

            r = make_u64(r >> 28, a)
            r = make_u64(r >> 31, a << 1 | hash_nibble)
        res = b32(r)

        if res[:4] == "AAAA":
            res = res[5:]

        return res

    @staticmethod
    def __decode(friend_code):
        if len(friend_code) != 10:
            return None

        if friend_code[:5] != "AAAA-":
            friend_code = "AAAA-" + friend_code

        val = rb32(friend_code)
        id = 0

        for i in range(8):
            val >>= 1
            id_nibble = val & 0xF
            val >>= 4

            id <<= 4
            id |= id_nibble

        return id

    @staticmethod
    def decode(friend_code):
        id = FriendCode.__decode(friend_code)

        if id:
            return str(id | default_steam_id)

        return ""

    @staticmethod
    def encode_direct_challenge(account_id):
        account_id = int(account_id)
        r = random.randint(0, 0x7fff) << 16
        part1 = FriendCode.encode(r | (account_id & 0x0000FFFF))
        part2 = FriendCode.encode(r | ((account_id & 0xFFFF0000) >> 16))

        return f"{part1}-{part2}"

    @staticmethod
    def encode_direct_group_challenge(group_id):
        group_id = int(group_id)
        part1 = FriendCode.encode((0x10000) | (group_id & 0x0000FFFF))
        part2 = FriendCode.encode((0x10000) | ((group_id & 0xFFFF0000) >> 16))

        return f"{part1}-{part2}"

    @staticmethod
    def decode_direct_challenge(challenge_code):
        if len(challenge_code) != 21:
            return ""

        part1 = int(FriendCode.__decode(challenge_code[:10]))
        part2 = int(FriendCode.__decode(challenge_code[11:]))

        type = "u"
        id = (part1 & 0x0000FFFF) | ((part2 & 0x0000FFFF) << 16)

        if (part1 & 0xFFFF0000) == 0x10000 and (part2 & 0xFFFF0000) == 0x10000:
            type = "g"
            id = id | default_group_id
        else:
            id = id | default_steam_id

        return f"{part1},{part2},{type},{id}"
