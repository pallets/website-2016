# -*- coding: utf-8 -*-
import hashlib
import posixpath
import uuid
from datetime import datetime

from feedgen.feed import FeedGenerator
from lektor.build_programs import BuildProgram
from lektor.context import get_ctx, url_to
from lektor.pluginsystem import Plugin
from lektor.sourceobj import VirtualSourceObject

FEED_NAME = 'feed.xml'


class BlogFeedSource(VirtualSourceObject):
    def __init__(self, parent, plugin):
        VirtualSourceObject.__init__(self, parent)
        self.plugin = plugin

    @property
    def path(self):
        return self.parent.path + '@blog-feed'

    @property
    def url_path(self):
        return posixpath.join(self.parent.url_path, FEED_NAME)


def get_id(s):
    return uuid.UUID(bytes=hashlib.md5(s.encode('utf8')).digest(), version=3).urn


class AtomFeedBuilderProgram(BuildProgram):
    def produce_artifacts(self):
        self.declare_artifact(
            self.source.url_path,
            sources=list(self.source.iter_source_filenames()))

    def build_artifact(self, artifact):
        ctx = get_ctx()
        feed_source = self.source
        page = feed_source.parent

        fg = FeedGenerator()
        fg.id(get_id(ctx.env.project.id))
        fg.title(page.record_label + u" — Pallets Project")
        fg.link(href=url_to("/blog", external=True))
        fg.link(href=url_to(feed_source, external=True), rel="self")

        for item in page.children.order_by(
            '-pub_date', '-pub_order', 'title'
        ).limit(10):
            fe = fg.add_entry()
            fe.title(item["title"])
            fe.content(str(item["body"]), type="html")
            fe.link(href=url_to(item, external=True))
            fe.id(
                get_id(
                    u"{}/{}".format(ctx.env.project.id, item["_path"].encode("utf-8"))
                )
            )
            fe.author(name=item["author"])
            updated = datetime(*item["pub_date"].timetuple()[:3])
            updated = updated.isoformat() + "Z" if not updated.tzinfo else ""
            fe.updated(updated)

        with artifact.open('wb') as f:
            f.write(fg.atom_str(pretty=True))


class LektorBlogFeedPlugin(Plugin):
    name = 'Lektor Blog Feeds'

    def has_blog_feed(self, node):
        path = getattr(node, 'path', node)
        if not path or '@' in path:
            return False
        path = path.strip('/').split('/')
        return path == ['blog'] or \
            (len(path) == 2 and path[0] == 'blog-categories')

    def on_setup_env(self, **extra):
        self.env.add_build_program(BlogFeedSource, AtomFeedBuilderProgram)

        @self.env.virtualpathresolver('blog-feed')
        def feed_path_resolver(node, pieces):
            if not pieces and self.has_blog_feed(node):
                return BlogFeedSource(node, self)

        @self.env.generator
        def generate_feeds(source):
            if self.has_blog_feed(source):
                yield BlogFeedSource(source, self)
