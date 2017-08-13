# -*- coding: utf-8 -*-
import uuid
import hashlib
import posixpath
from datetime import datetime

from lektor.build_programs import BuildProgram
from lektor.pluginsystem import Plugin
from lektor.context import get_ctx, url_to
from lektor.sourceobj import VirtualSourceObject
from werkzeug._compat import to_native, to_bytes, text_type

from werkzeug.contrib.atom import AtomFeed


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
    s = text_type(s).encode('utf8')
    return uuid.UUID(bytes=hashlib.md5(s).digest(), version=3).urn


class AtomFeedBuilderProgram(BuildProgram):

    def produce_artifacts(self):
        self.declare_artifact(
            self.source.url_path,
            sources=list(self.source.iter_source_filenames()))

    def build_artifact(self, artifact):
        ctx = get_ctx()
        feed_source = self.source
        page = feed_source.parent

        feed = AtomFeed(
            title=page.record_label + u' — Pallets Project',
            feed_url=url_to(feed_source, external=True),
            url=url_to('/blog', external=True),
            id=get_id(ctx.env.project.id)
        )

        for item in page.children.order_by('-pub_date').limit(10):
            item_author = item['author']

            feed.add(
                item['title'],
                text_type(item['body']),
                xml_base=url_to(item, external=True),
                url=url_to(item, external=True),
                content_type='html',
                id=get_id(u'%s/%s' % (
                    ctx.env.project.id,
                    item['_path'].encode('utf-8'))),
                author=item_author,
                updated=datetime(*item['pub_date'].timetuple()[:3]))

        with artifact.open('wb') as f:
            f.write(feed.to_string().encode('utf-8'))


class LektorBlogFeedPlugin(Plugin):
    name = u'Lektor Blog Feeds'

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
