from django.contrib.sitemaps import Sitemap
from dashboard_meet_je_stad.models import Page

class PageSitemap(Sitemap):
    changefreq = "never"

    def items(self):
        return [Page()]

    def lastmod(self, obj):
        return obj.lastedit_date
