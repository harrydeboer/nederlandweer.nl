from django.contrib.sitemaps import Sitemap
from nederland_weer.models import Page

class PageSitemap(Sitemap):
    changefreq = "never"

    def items(self):
        return [Page()]

    def lastmod(self, obj):
        return obj.lastedit_date