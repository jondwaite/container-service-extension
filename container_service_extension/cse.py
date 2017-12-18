#!/usr/bin/env python

# container-service-extension
# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import click
from container_service_extension.config import check_config
from container_service_extension.config import generate_sample_config
from container_service_extension.config import install_cse
from container_service_extension.config import uninstall_cse
from container_service_extension.service import Service
import logging
import pkg_resources
import platform
from vcd_cli.utils import stdout

LOGGER = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Container Service Extension for VMware vCloud Director.

\b
    Manages CSE.
\b
    Examples
        cse sample
            Generate sample config.
\b
        cse sample > config1.yaml
            Save sample config.
\b
        cse check
            Validate configuration.
\b
        cse version
            Display version.
\b
    Environment Variables
        CSE_CONFIG
            If this environment variable is set, the commands will use the file
            indicated in the variable as the config file. The file indicated
            with the \'--config\' option will have preference over the
            environment variable. If both are omitted, it defaults to file
            \'config.yaml\' in the current directory.

    """

    if ctx.invoked_subcommand is None:
        click.secho(ctx.get_help())
        return


@cli.command(short_help='show version')
@click.pass_context
def version(ctx):
    """Show CSE version"""

    ver = pkg_resources.require('container-service-extension')[0].version
    ver_obj = {
        'product': 'cse',
        'description':
        'Container Service Extension for VMware vCloud Director',
        'version': ver,
        'python': platform.python_version()
    }
    ver_str = '%s, %s, version %s' % (ver_obj['product'],
                                      ver_obj['description'],
                                      ver_obj['version'])
    stdout(ver_obj, ctx, ver_str)


@cli.command('sample', short_help='generate sample configuration')
@click.pass_context
def sample(ctx):
    """Generate sample CSE configuration"""
    click.secho(generate_sample_config())


@cli.command(short_help='check configuration')
@click.pass_context
@click.option(
    '-c',
    '--config',
    'config',
    type=click.Path(exists=True),
    metavar='<config-file>',
    envvar='CSE_CONFIG',
    default='config.yaml',
    help='Config file to use.')
def check(ctx, config):
    """Validate CSE configuration"""
    check_config(config)
    click.secho('The configuration is valid.')


@cli.command(short_help='install CSE on vCD')
@click.pass_context
@click.option(
    '-c',
    '--config',
    'config',
    type=click.Path(exists=True),
    metavar='<config-file>',
    envvar='CSE_CONFIG',
    default='config.yaml',
    help='Config file to use.')
@click.option(
    '-t',
    '--template',
    'template',
    required=False,
    default='*',
    metavar='<template>',
    help='template')
@click.option(
    '-n',
    '--no-capture',
    is_flag=True,
    required=False,
    default=False,
    help='no capture')
def install(ctx, config, template, no_capture):
    """Install CSE on vCloud Director"""
    install_cse(ctx, config, template, no_capture)


@cli.command(short_help='uninstall CSE from vCD')
@click.pass_context
@click.option(
    '-c',
    '--config',
    'config',
    type=click.Path(exists=True),
    metavar='<config-file>',
    envvar='CSE_CONFIG',
    default='config.yaml',
    help='Config file to use.')
@click.option(
    '-t',
    '--template',
    'template',
    required=False,
    default='photon-custom-hw11-2.0-304b817.ova',
    metavar='<template>',
    help='template')
def uninstall(ctx, config, template):
    """Uninstall CSE from vCloud Director"""
    uninstall_cse(ctx, config, template)


@cli.command(short_help='run service')
@click.pass_context
@click.option(
    '-c',
    '--config',
    'config',
    type=click.Path(exists=True),
    metavar='<config-file>',
    envvar='CSE_CONFIG',
    default='config.yaml',
    help='Config file to use.')
@click.option(
    '-s',
    '--skip-check',
    is_flag=True,
    default=False,
    required=False,
    help='Skip check')
def run(ctx, config, skip_check):
    """Run CSE service"""
    service = Service(config, check_config=not skip_check)
    service.run()


if __name__ == '__main__':
    cli()
