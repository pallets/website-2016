from setuptools import setup

setup(
    name='lektor-blog-feed',
    version='0.1',
    author=u'Armin Ronacher',
    author_email='armin@ronacher.eu',
    license='MIT',
    py_modules=['lektor_blog_feed'],
    install_requires=['feedgen', 'MarkupSafe'],
    entry_points={
        'lektor.plugins': [
            'blog-feed = lektor_blog_feed:LektorBlogFeedPlugin',
        ]
    }
)
