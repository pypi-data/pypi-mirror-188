"""Custom scrapy extensions."""
import logging
import re

from scrapy.extensions.throttle import AutoThrottle
from scrapy.http import Response


class CustomDelayThrottle(AutoThrottle):
    """Set custom `DOWNLOAD_DELAY`for different url regex."""

    def __init__(self, crawler):
        """Initialize the custom delay throttle."""
        self.urlRegex_delays: dict = crawler.settings.getdict('DOMAIN_DELAYS')
        logging.debug('Using Custom delay for each url regex')
        super().__init__(crawler)

    def _adjust_delay(self, slot, latency: float, response: Response):
        """Override AutoThrottle._adjust_delay()."""
        for regex, delay in self.urlRegex_delays.items():
            if re.match(regex, response.url):
                slot.delay = delay
                break
