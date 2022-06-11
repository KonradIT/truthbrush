from dataclasses import dataclass
from dataclasses_json import dataclass_json

from typing import List, Any, Optional


@dataclass
@dataclass_json
class Account:
    id: str
    username: str
    acct: str
    display_name: str
    locked: bool
    bot: bool
    discoverable: bool
    group: bool
    created_at: str
    note: str
    url: str
    avatar: str
    avatar_static: str
    header: str
    header_static: str
    followers_count: int
    following_count: int
    statuses_count: int
    last_status_at: str
    verified: bool
    location: str
    website: str
    emojis: List[Any]
    fields: List[Any]

    def __init__(self, id: str, username: str, acct: str, display_name: str, locked: bool, bot: bool, discoverable: bool, group: bool, created_at: str, note: str, url: str, avatar: str, avatar_static: str, header: str, header_static: str, followers_count: int, following_count: int, statuses_count: int, last_status_at: str, verified: bool, location: str, website: str, emojis: List[Any], fields: List[Any]) -> None:
        self.id = id
        self.username = username
        self.acct = acct
        self.display_name = display_name
        self.locked = locked
        self.bot = bot
        self.discoverable = discoverable
        self.group = group
        self.created_at = created_at
        self.note = note
        self.url = url
        self.avatar = avatar
        self.avatar_static = avatar_static
        self.header = header
        self.header_static = header_static
        self.followers_count = followers_count
        self.following_count = following_count
        self.statuses_count = statuses_count
        self.last_status_at = last_status_at
        self.verified = verified
        self.location = location
        self.website = website
        self.emojis = emojis
        self.fields = fields


@dataclass
@dataclass_json
class Card:
    url: str
    title: str
    description: str
    type: str
    author_name: str
    author_url: str
    provider_name: str
    provider_url: str
    html: str
    width: int
    height: int
    image: str
    embed_url: str
    blurhash: str

    def __init__(self, url: str, title: str, description: str, type: str, author_name: str, author_url: str, provider_name: str, provider_url: str, html: str, width: int, height: int, image: str, embed_url: str, blurhash: str) -> None:
        self.url = url
        self.title = title
        self.description = description
        self.type = type
        self.author_name = author_name
        self.author_url = author_url
        self.provider_name = provider_name
        self.provider_url = provider_url
        self.html = html
        self.width = width
        self.height = height
        self.image = image
        self.embed_url = embed_url
        self.blurhash = blurhash


@dataclass
@dataclass_json
class Original:
    width: int
    height: int
    size: Optional[str] = None
    aspect: Optional[float] = None
    duration: Optional[float] = None
    bitrate: Optional[int] = None
    frame_rate: Optional[str] = None

    def __init__(self, width: int, height: int, size: Optional[str], aspect: Optional[float], frame_rate: Optional[str], duration: Optional[float], bitrate: Optional[int]) -> None:
        self.width = width
        self.height = height
        self.size = size
        self.aspect = aspect
        self.frame_rate = frame_rate
        self.duration = duration
        self.bitrate = bitrate


@dataclass
@dataclass_json
class Small:
    width: int
    height: int
    size: str
    aspect: float

    def __init__(self, width: int, height: int, size: str, aspect: float) -> None:
        self.width = width
        self.height = height
        self.size = size
        self.aspect = aspect


@dataclass
@dataclass_json
class Meta:
    original: Original
    small: Optional[Small] = None

    def __init__(self, original: Original, small: Optional[Small]) -> None:
        self.original = original
        self.small = small


@dataclass
@dataclass_json
class PostMediaAttachment:
    id: str
    type: str
    url: str
    preview_url: str
    text_url: str
    meta: Meta
    external_video_id: Optional[str] = None
    preview_remote_url: Optional[Any] = None
    remote_url: Optional[Any] = None
    description: Optional[Any] = None
    blurhash: Optional[str] = None

    def __init__(self, id: str, type: str, url: str, preview_url: str, external_video_id: Optional[str], remote_url: Optional[Any], preview_remote_url: Optional[Any], text_url: str, meta: Meta, description: Optional[Any], blurhash: Optional[str]) -> None:
        self.id = id
        self.type = type
        self.url = url
        self.preview_url = preview_url
        self.external_video_id = external_video_id
        self.remote_url = remote_url
        self.preview_remote_url = preview_remote_url
        self.text_url = text_url
        self.meta = meta
        self.description = description
        self.blurhash = blurhash


@dataclass
@dataclass_json
class ReblogMediaAttachment:
    id: str
    type: str
    url: str
    preview_url: str
    text_url: str
    meta: Meta
    blurhash: str
    external_video_id: Optional[Any] = None
    description: Optional[Any] = None
    preview_remote_url: Optional[Any] = None
    remote_url: Optional[Any] = None

    def __init__(self, id: str, type: str, url: str, preview_url: str, external_video_id: Optional[Any], remote_url: Optional[Any], preview_remote_url: Optional[Any], text_url: str, meta: Meta, description: Optional[Any], blurhash: str) -> None:
        self.id = id
        self.type = type
        self.url = url
        self.preview_url = preview_url
        self.external_video_id = external_video_id
        self.remote_url = remote_url
        self.preview_remote_url = preview_remote_url
        self.text_url = text_url
        self.meta = meta
        self.description = description
        self.blurhash = blurhash


@dataclass
@dataclass_json
class Reblog:
    id: str
    created_at: str
    sensitive: bool
    spoiler_text: str
    visibility: str
    language: str
    uri: str
    url: str
    replies_count: int
    reblogs_count: int
    favourites_count: int
    favourited: bool
    reblogged: bool
    muted: bool
    bookmarked: bool
    content: str
    account: Account
    media_attachments: List[ReblogMediaAttachment]
    mentions: List[Any]
    tags: List[Any]
    emojis: List[Any]
    card: Optional[Any] = None
    poll: Optional[Any] = None
    quote: Optional[Any] = None
    in_reply_to: Optional[Any] = None
    in_reply_to_id: Optional[Any] = None
    reblog: Optional[Any] = None
    in_reply_to_account_id: Optional[Any] = None

    def __init__(self, id: str, created_at: str, in_reply_to_id: Optional[Any], in_reply_to_account_id: Optional[Any], sensitive: bool, spoiler_text: str, visibility: str, language: str, uri: str, url: str, replies_count: int, reblogs_count: int, favourites_count: int, favourited: bool, reblogged: bool, muted: bool, bookmarked: bool, content: str, reblog: Optional[Any], account: Account, media_attachments: List[ReblogMediaAttachment], mentions: List[Any], tags: List[Any], emojis: List[Any], card: Optional[Any], poll: Optional[Any], quote: Optional[Any], in_reply_to: Optional[Any]) -> None:
        self.id = id
        self.created_at = created_at
        self.in_reply_to_id = in_reply_to_id
        self.in_reply_to_account_id = in_reply_to_account_id
        self.sensitive = sensitive
        self.spoiler_text = spoiler_text
        self.visibility = visibility
        self.language = language
        self.uri = uri
        self.url = url
        self.replies_count = replies_count
        self.reblogs_count = reblogs_count
        self.favourites_count = favourites_count
        self.favourited = favourited
        self.reblogged = reblogged
        self.muted = muted
        self.bookmarked = bookmarked
        self.content = content
        self.reblog = reblog
        self.account = account
        self.media_attachments = media_attachments
        self.mentions = mentions
        self.tags = tags
        self.emojis = emojis
        self.card = card
        self.poll = poll
        self.quote = quote
        self.in_reply_to = in_reply_to


@dataclass
@dataclass_json
class Post:
    id: str
    created_at: str
    sensitive: bool
    spoiler_text: str
    visibility: str
    uri: str
    url: str
    replies_count: int
    reblogs_count: int
    favourites_count: int
    favourited: bool
    reblogged: bool
    muted: bool
    bookmarked: bool
    content: str
    account: Account
    media_attachments: List[PostMediaAttachment]
    mentions: List[Any]
    tags: List[Any]
    emojis: List[Any]
    _pulled: str
    language: Optional[str] = None
    reblog: Optional[Reblog] = None
    card: Optional[Card] = None
    poll: Optional[Any] = None
    quote: Optional[Any] = None
    in_reply_to: Optional[Any] = None
    in_reply_to_id: Optional[Any] = None
    in_reply_to_account_id: Optional[Any] = None

    def __init__(self, id: str, created_at: str, in_reply_to_id: Optional[Any], in_reply_to_account_id: Optional[Any], sensitive: bool, spoiler_text: str, visibility: str, language: Optional[str], uri: str, url: str, replies_count: int, reblogs_count: int, favourites_count: int, favourited: bool, reblogged: bool, muted: bool, bookmarked: bool, content: str, reblog: Optional[Reblog], account: Account, media_attachments: List[PostMediaAttachment], mentions: List[Any], tags: List[Any], emojis: List[Any], card: Optional[Card], poll: Optional[Any], quote: Optional[Any], in_reply_to: Optional[Any], _pulled: str) -> None:
        self.id = id
        self.created_at = created_at
        self.in_reply_to_id = in_reply_to_id
        self.in_reply_to_account_id = in_reply_to_account_id
        self.sensitive = sensitive
        self.spoiler_text = spoiler_text
        self.visibility = visibility
        self.language = language
        self.uri = uri
        self.url = url
        self.replies_count = replies_count
        self.reblogs_count = reblogs_count
        self.favourites_count = favourites_count
        self.favourited = favourited
        self.reblogged = reblogged
        self.muted = muted
        self.bookmarked = bookmarked
        self.content = content
        self.reblog = reblog
        self.account = account
        self.media_attachments = media_attachments
        self.mentions = mentions
        self.tags = tags
        self.emojis = emojis
        self.card = card
        self.poll = poll
        self.quote = quote
        self.in_reply_to = in_reply_to
        self.pulled = _pulled
