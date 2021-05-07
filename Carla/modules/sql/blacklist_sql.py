import threading
from sqlalchemy import Column, String, UnicodeText, distinct, func, Integer
from . import BASE, SESSION


class BlackListFilters(BASE):
    __tablename__ = "sl"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, trigger):
        self.chat_id = str(chat_id)  # ensure string
        self.trigger = trigger

    def __repr__(self):
        return "<Blacklist filter '%s' for %s>" % (self.trigger, self.chat_id)

    def __eq__(self, other):
        return bool(
            isinstance(other, BlackListFilters)
            and self.chat_id == other.chat_id
            and self.trigger == other.trigger
        )


class BlackListMode(BASE):
    __tablename__ = "blackmoda"
    chat_id = Column(String(14), primary_key=True)
    mode = Column(UnicodeText, default="nothing")
    time = Column(Integer, default=0)

    def __init__(self, chat_id, mode="nothing", time=0):
        self.chat_id = str(chat_id)  # ensure string
        self.mode = mode
        self.time = time

BlackListFilters.__table__.create(checkfirst=True)
BlackListMode.__table__.create(checkfirst=True)

BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()

CHAT_BLACKLISTS = {}


def add_to_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = BlackListFilters(str(chat_id), trigger)

        SESSION.merge(blacklist_filt)  # merge to avoid duplicate key issues
        SESSION.commit()
        CHAT_BLACKLISTS.setdefault(str(chat_id), set()).add(trigger)

def add_mode(chat_id, mode):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        mudd = SESSION.query(BlackListMode).get(str(chat_id))
        if not mudd:
            mudd = BlackListMode(str(chat_id))
        mudd.mode = mode

def get_mode(chat_id):
    rules = SESSION.query(BlackListMode).get(str(chat_id))
    ret = 'nothing'
    if rules:
        ret = rules.mode
    SESSION.close()
    return ret

def set_time(chat_id, time):
   with BLACKLIST_FILTER_INSERTION_LOCK:
        mudd = SESSION.query(BlackListMode).get(str(chat_id))
        if not mudd:
            mudd = BlackListMode(str(chat_id))
        mudd.time = time

def get_time(chat_id):
    rules = SESSION.query(BlackListMode).get(str(chat_id))
    ret = 0
    if rules:
        ret = rules.time
    SESSION.close()
    return ret

def rm_from_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = SESSION.query(BlackListFilters).get((str(chat_id), trigger))
        if blacklist_filt:
            # sanity check
            if trigger in CHAT_BLACKLISTS.get(str(chat_id), set()):
                CHAT_BLACKLISTS.get(str(chat_id), set()).remove(trigger)

            SESSION.delete(blacklist_filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def get_chat_blacklist(chat_id):
    return CHAT_BLACKLISTS.get(str(chat_id), set())


def num_blacklist_filters():
    try:
        return SESSION.query(BlackListFilters).count()
    finally:
        SESSION.close()


def num_blacklist_chat_filters(chat_id):
    try:
        return (
            SESSION.query(BlackListFilters.chat_id)
            .filter(BlackListFilters.chat_id == str(chat_id))
            .count()
        )
    finally:
        SESSION.close()


def num_blacklist_filter_chats():
    try:
        return SESSION.query(func.count(distinct(BlackListFilters.chat_id))).scalar()
    finally:
        SESSION.close()


def __load_chat_blacklists():
    global CHAT_BLACKLISTS
    try:
        chats = SESSION.query(BlackListFilters.chat_id).distinct().all()
        for (chat_id,) in chats:  # remove tuple by ( ,)
            CHAT_BLACKLISTS[chat_id] = []

        all_filters = SESSION.query(BlackListFilters).all()
        for x in all_filters:
            CHAT_BLACKLISTS[x.chat_id] += [x.trigger]

        CHAT_BLACKLISTS = {x: set(y) for x, y in CHAT_BLACKLISTS.items()}

    finally:
        SESSION.close()


__load_chat_blacklists()
