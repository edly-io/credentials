""" Copy catalog data from Discovery. """

import logging

from django.contrib.sites.models import Site
from django.core.management import BaseCommand, CommandError

from credentials.apps.catalog.utils import parse_pathway, parse_program
from credentials.apps.core.models import SiteConfiguration


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Copy catalog data from Discovery'

    def add_arguments(self, parser):
        """
        Add arguments to the command parser.
        """
        parser.add_argument(
            '--page-size',
            action='store',
            type=int,
            default=None,
            help='The maximum number of catalog items to request at once.'
        )

    def handle(self, *args, **options):
        page_size = options.get('page_size')
        failure_count = 0

        for site in Site.objects.all():
            success = True
            site_configs = SiteConfiguration.objects.filter(site=site)
            site_config = site_configs.get() if site_configs.exists() else None

            # We skip the site if records_enabled is false - remember to remove that check once we start
            # using the catalog data for certificates too.
            if not site_config or not site_config.catalog_api_url or not site_config.records_enabled:
                logger.info(f'Skipping site {site.domain}. No configuration.')
                continue

            logger.info(f'Copying catalog data for site {site.domain}')
            client = site_config.catalog_api_client
            try:
                Command.fetch_programs(site, client, page_size=page_size)
                logger.info('Finished copying programs.')
            except Exception as error:
                success = False
                logger.exception('Failed to copy programs for site: {}.'.format(site.domain))

            try:
                Command.fetch_pathways(site, client, page_size=page_size)
                logger.info('Finished copying pathways.')
            except Exception as error:
                success = False
                logger.exception('Failed to copy pathways for site: {}.'.format(site.domain))

            if not success:
                failure_count += 1

        if failure_count:
            raise CommandError(
                'Programs / Pathways copying for {failure_for_sites} out of {total_sites} sites have failed. '
                'Please check the configuration.'.format(
                    failure_for_sites=failure_count,
                    total_sites=Site.objects.count(),
                )
            )

    @staticmethod
    def fetch_programs(site, client, page_size=None):
        next_page = 1
        while next_page:
            programs = client.programs.get(exclude_utm=1, page=next_page, page_size=page_size)
            for program in programs['results']:
                logger.info('Copying program "{}"'.format(program['title']))
                parse_program(site, program)
            next_page = next_page + 1 if programs['next'] else None

    @staticmethod
    def fetch_pathways(site, client, page_size=None):
        next_page = 1
        while next_page:
            pathways = client.pathways.get(exclude_utm=1, page=next_page, page_size=page_size)
            for pathway in pathways['results']:
                logger.info('Copying pathway "{}"'.format(pathway['name']))
                parse_pathway(site, pathway)
            next_page = next_page + 1 if pathways['next'] else None
