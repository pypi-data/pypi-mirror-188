"""
An MkDocs plugin to remove 3rd party assets and download them locally
"""
import hashlib
import os
from typing import Dict, Optional, Tuple
from urllib.request import urlopen

import mkdocs.config.config_options
from bs4 import BeautifulSoup
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page


class No3rdPartyPlugin(BasePlugin):
    """Custom MkDocs plugin to remove 3rd party assets and download them locally."""

    config_scheme: Tuple = (
        ("download_js", mkdocs.config.config_options.Type(bool, default=True)),
        ("download_css", mkdocs.config.config_options.Type(bool, default=True)),
        ("directory", mkdocs.config.config_options.Type(str, default="3rd_party")),
    )

    def _is_relative_url(self, url: str) -> bool:
        """Check if a URL is relative."""
        return not (url.startswith("http://") or url.startswith("https://"))

    def _download(self, url: str, file_path: str) -> None:
        """Download a file from a URL and save it to disk."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with urlopen(url) as response:
            with open(file_path, "wb") as file:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    file.write(chunk)

    def _find_rel_path(self, file_name: str, *, page: Optional[Page]) -> str:
        """Find the relative path to a file."""
        path_part = self.config["directory"] + "/" + file_name
        if not page:
            return "/" + path_part

        drop_down_times = len(page.url.split("/")) - 1
        return "../" * drop_down_times + path_part

    def _html_proc(
        self, content: str, *, config: MkDocsConfig, page: Optional[Page]
    ) -> Optional[str]:
        # Parse HTML content
        soup = BeautifulSoup(content, "html.parser")

        # Files to download
        urls: Dict[str, str] = {}

        # Download JS files
        if self.config["download_js"]:
            for script in soup.find_all("script"):
                src = script.get("src")
                if src and not self._is_relative_url(src):
                    file_name = hashlib.sha256(src.encode()).hexdigest() + ".js"
                    file_path = os.path.join(
                        config["site_dir"], self.config["directory"], file_name
                    )
                    script["src"] = self._find_rel_path(file_name, page=page)
                    urls[src] = file_path

        # Download CSS files
        rel_to_ext_map = {"stylesheet": ".css"}
        if self.config["download_css"]:
            for link in soup.find_all("link"):
                href = link.get("href")
                rel = link.get("rel")
                if not rel or not href or self._is_relative_url(href):
                    continue

                rel = rel[0]
                ext = rel_to_ext_map.get(rel)
                if not ext:
                    continue

                file_name = hashlib.sha256(href.encode()).hexdigest() + ext
                file_path = os.path.join(
                    config["site_dir"], self.config["directory"], file_name
                )
                link["href"] = self._find_rel_path(file_name, page=page)
                urls[href] = file_path

        # Download files but ensure they are not downloaded twice
        for url, file_path in urls.items():
            if not os.path.exists(file_path):
                self._download(url, file_path)

        # Return HTML
        return str(soup)

    def on_post_page(
        self, output: str, *, page: Page, config: MkDocsConfig
    ) -> Optional[str]:
        """Remove 3rd party assets from HTML pages, before saving to disk."""
        return self._html_proc(output, config=config, page=page)

    def on_post_template(
        self, output: str, *, template_name: str, config: MkDocsConfig
    ) -> Optional[str]:
        """Remove 3rd party assets from HTML templates, before saving to disk."""
        if template_name.endswith(".html"):
            return self._html_proc(output, config=config, page=None)

        return output
