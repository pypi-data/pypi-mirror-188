import logging
import pathlib
import pdb
import shutil
from collections import defaultdict
from functools import partial

import pluggy
from jinja2 import Environment
from rich.progress import Progress

from .collection import Collection
from .engine import engine, url_for
from .hookspecs import SiteSpecs
from .page import Page

_PROJECT_NAME = "render_engine"


class Site:
    """
    The site stores your pages and collections to be rendered.

    Attributes:
        output_path: str to write rendered content. **Default**: `output`
        static: Output str Path for the static folder. This will get copied to the output folder. **Default**: `static`
        site_vars: Vars that will be passed into the render functions

            Default `site_vars`:

            - SITE_TITLE: "Untitled Site"
            - SITE_URL: "http://example.com"
    """

    output_path: str = "output"
    static_path: str = "static"

    site_vars: dict = {
        "SITE_TITLE": "Untitled Site",
        "SITE_URL": "http://localhost:8000/",
    }
    plugins: list

    def __init__(
        self,
        plugins=None,
    ) -> None:
        self._pm = pluggy.PluginManager(project_name=_PROJECT_NAME)
        self._pm.add_hookspecs(SiteSpecs)
        self.route_list: defaultdict = defaultdict(list)
        self.subcollections: defaultdict = defaultdict(lambda: {"pages": []})
        self.engine.filters["url_for"] = partial(url_for, site=self)

        if not hasattr(self, "plugins"):
            setattr(self, "plugins", [])

        if plugins:
            self.plugins.extend(plugins)

        self._register_plugins()

    def _register_plugins(self):
        for plugin in self.plugins:
            self._pm.register(plugin)

    def post_build_page(self, page: Page):
        """Parse the content of the page using the plugins"""
        _page = page
        self._pm.hook.post_build_page(page=_page)
        return _page

    @property
    def engine(self) -> Environment:
        env = engine
        env.globals.update(self.site_vars)
        return env

    def add_to_route_list(self, page: Page) -> None:
        """Add a page to the route list"""
        self.route_list[page.slug] = page

    def collection(self, collection: Collection) -> Collection:
        """Create the pages in the collection including the archive"""
        _collection = collection()
        self._pm.hook.pre_build_collection(collection=_collection)
        logging.debug("Adding Collection: %s", _collection.__class__.__name__)

        for page in _collection.pages:
            logging.debug("Adding Page: %s", page.__class__.__name__)
            self._pm.hook.pre_build_collection_pages(page=page)
            self.add_to_route_list(page)
            self._pm.hook.post_build_collection_pages(site=self)

        for archive in _collection.archives:
            logging.debug("Adding Archive: %s", archive.__class__.__name__)
            self.add_to_route_list(archive)

        if feed := _collection._feed:
            self.add_to_route_list(feed)
        self._pm.hook.post_build_collection(site=self)

        return _collection

    def page(self, page: type[Page]) -> Page:
        """Create a Page object and add it to self.routes"""
        _page = self.post_build_page(page())
        self.add_to_route_list(_page)
        return _page

    def render_static(self, directory) -> None:
        """Copies a Static Directory to the output folder"""
        shutil.copytree(
            directory, pathlib.Path(self.output_path) / directory, dirs_exist_ok=True
        )

    def render_output(self, route: str, page: Page):
        """writes the page object to disk"""
        if page._extension == ".xml":
            logging.debug("%s, %s", page.content, page.pages)
        path = (
            pathlib.Path(self.output_path)
            / pathlib.Path(route)
            / pathlib.Path(page.url)
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        return path.write_text(page._render_content(engine=self.engine))

    def build_subcollections(self, page) -> None:
        if subcollections := getattr(page, "subcollections", []):
            logging.debug("Adding subcollections: %s", subcollections)

            for attr in subcollections:
                logging.debug("Adding attr: %s", attr)

                for page_attr in getattr(page, attr, []):
                    logging.debug("Adding page_attr: %s", page_attr)
                    self.subcollections[page_attr]
                    self.subcollections[page_attr]["pages"].append(page)
                    self.subcollections[page_attr]["route"] = attr

                    if "template" not in self.subcollections[page_attr]:
                        self.subcollections[page_attr][
                            "template"
                        ] = page.subcollection_template

    def render(self) -> None:
        """Render all pages and collections"""

        with Progress() as progress:
            pre_build_task = progress.add_task("Loading Pre-Build Plugins", total=1)
            self._pm.hook.pre_build_site(site=self)

            # Parse Route List
            task_add_route = progress.add_task(
                "[blue]Adding Routes", total=len(self.route_list)
            )
            engine.globals["site"] = self
            for page in self.route_list.values():
                progress.update(
                    task_add_route,
                    description=f"[blue]Adding[grey]Route: [blue]{page.slug}",
                )
                self.build_subcollections(page)
                progress.update(task_add_route, advance=1)

                for route in page.routes:
                    self.render_output(route, page)

            # Parse SubCollection
            task_render_subcollection = progress.add_task(
                "[blue]Rendering SubCollections", total=len(self.subcollections)
            )
            for tag, subcollection in self.subcollections.items():
                progress.update(
                    task_render_subcollection,
                    description=f"[blue]Rendering[grey]SubCollection: [blue]{tag}",
                )
                page = Page()
                page.title = tag
                page.template = subcollection["template"]
                page.pages = subcollection["pages"]

                self.render_output(
                    pathlib.Path(page.routes[0]).joinpath(subcollection["route"]), page
                )

            if pathlib.Path(self.static_path).is_dir():
                task = progress.add_task("copying static directory", total=1)
                self.render_static(pathlib.Path(self.static_path).name)

            post_build_task = progress.add_task("Loading Post-Build Plugins", total=1)
            self._pm.hook.post_build_site(site=self)
            progress.update(pre_build_task, advance=1)
