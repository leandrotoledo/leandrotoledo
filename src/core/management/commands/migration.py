from django.core.management import BaseCommand
from django.contrib.auth.models import User
from core.models import Post
from xml.dom import minidom

"""
mysql -D leandrotoledo -u root -p -e "select post_title AS title, post_excerpt AS excerpt, post_content AS content, post_date AS created_date, post_modified AS updated_date from wp_posts where post_type = 'post' order by post_date;" -X > dump.xml
"""

class Command(BaseCommand):
    args = '<xml-file>'
    help = 'Import posts from WordPress XML dumped table (wp_posts)'

    requires_model_validation = True

    def handle(self, *args, **kwargs):
        with open(args[0]) as file:
            xml = minidom.parseString(file.read())

            for row in xml.getElementsByTagName('row'):
                post = Post()
                for node in row.childNodes:
                    if node.nodeType != node.TEXT_NODE:
                        attr = node.getAttribute('name')
                        try:
                            post.__dict__[attr] = node.firstChild.data
                        except AttributeError:
                            post.__dict__[attr] = ''

                print 'Post:', repr(post.title)
                post.published_date = post.created_date
                post.user = User.objects.get(username='leandrotoledo')

                post.save()
