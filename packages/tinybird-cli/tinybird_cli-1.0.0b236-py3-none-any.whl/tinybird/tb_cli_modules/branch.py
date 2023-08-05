
# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

import click
from click import Context

from tinybird.client import TinyB
from tinybird.tb_cli_modules.cli import cli
from tinybird.tb_cli_modules.common import coro, get_config_and_hosts, \
    create_workspace_branch, switch_workspace, switch_to_workspace_by_user_workspace_data, \
    print_current_workspace, _get_config, print_data_branch_summary, echo_safe_humanfriendly_tables_format_smart_table, \
    get_current_main_workspace
from tinybird.feedback_manager import FeedbackManager
from tinybird.datafile import wait_job
from tinybird.config import VERSION


@cli.group(hidden=True)
@click.pass_context
def branch(ctx):
    '''Branch commands'''


@branch.command(name="ls", hidden=True)
@click.pass_context
@coro
async def branch_ls(ctx):
    """List all the branches from the workspace token
    """
    client = ctx.obj['client']
    config = ctx.obj['config']

    if 'id' not in config:
        config = await _get_config(config['host'], config['token'], load_tb_file=False)

    current_main_workspace = await get_current_main_workspace(client, config)

    if current_main_workspace['id'] != config['id']:
        client = TinyB(current_main_workspace['token'], config['host'], version=VERSION)

    response = await client.branches()

    columns = ['name', 'id']
    table = []

    for branch in response['branches']:
        table.append([branch['name'], branch['id']])

    await print_current_workspace(ctx)

    click.echo(FeedbackManager.info_branches())
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@branch.command(name='use', hidden=True)
@click.argument('branch_name_or_id')
@click.pass_context
@coro
async def branch_use(ctx: Context, branch_name_or_id: str):
    """Switch to another branch. Use 'tb branch ls' to list the branches you have access to.
    """
    await switch_workspace(ctx, branch_name_or_id, only_branches=True)


@branch.command(name='current', hidden=True)
@click.pass_context
@coro
async def branch_current(ctx: Context):
    """Show the branch you're currently authenticated to
    """
    await print_current_workspace(ctx)


@branch.command(name='create', short_help="Create a new Branch from the Workspace you are authenticated", hidden=True)
@click.argument('branch_name', required=False)
@click.option('--last-partition', is_flag=True, default=False, help="When enabled, last modified partition is attached from the origin Workspace to the Branch")
@click.option('--all', is_flag=True, default=False, help="When enabled, all data from the origin Workspace is attached to the Branch. Use only if you actually need all the data in the branch.")
@click.option('--wait', is_flag=True, default=False, help="Waits for data branch jobs to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def create_branch(ctx: Context, branch_name: str, last_partition: bool, all: bool, wait: bool):
    if last_partition and all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all but not both"))
        return

    await create_workspace_branch(ctx, branch_name, last_partition, all, wait)


@branch.command(name='rm', short_help="Removes a Branch for your Tinybird user and it can't be recovered.", hidden=True)
@click.argument('branch_name_or_id')
@click.option('--yes', is_flag=True, default=False, help="Do not ask for confirmation")
@click.pass_context
@coro
async def delete_branch(ctx: Context, branch_name_or_id: str, yes: bool):
    """Remove a branch where you are admin"""

    client: TinyB = ctx.ensure_object(dict)['client']
    config, host, ui_host = await get_config_and_hosts(ctx)

    try:
        workspaces = (await client.user_workspace_branches()).get('workspaces', [])
        workspace_to_delete = next((workspace for workspace in workspaces if
                                    workspace['name'] == branch_name_or_id or workspace['id'] == branch_name_or_id), None)
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return

    if not workspace_to_delete:
        raise click.ClickException(FeedbackManager.error_branch(branch=branch_name_or_id))

    if yes or click.confirm(FeedbackManager.warning_confirm_delete_branch(branch=workspace_to_delete['name'])):
        need_to_switch_to_main = workspace_to_delete.get('main') and config['id'] == workspace_to_delete['id']
        # get origin workspace if deleting current branch
        if need_to_switch_to_main:
            try:
                workspaces = (await client.user_workspaces()).get('workspaces', [])
                workspace_main = next((workspace for workspace in workspaces if
                                       workspace['id'] == workspace_to_delete['main']), None)
            except Exception:
                workspace_main = None
        try:
            await client.delete_branch(workspace_to_delete['id'])
            click.echo(FeedbackManager.success_branch_deleted(branch_name=workspace_to_delete['name']))
        except Exception as e:
            click.echo(FeedbackManager.error_exception(error=str(e)))
            return
        else:
            if need_to_switch_to_main:
                if workspace_main:
                    await switch_to_workspace_by_user_workspace_data(ctx, workspace_main)
                else:
                    click.echo(FeedbackManager.error_switching_to_main())


@branch.command(name='data', short_help="Perform a data branch operation, see flags for details", hidden=True)
@click.option('--last-partition', is_flag=True, default=False, help="When enabled, last modified partition is attached from the origin Workspace to the Branch")
@click.option('--all', is_flag=True, default=False, help="When enabled, all data from the origin Workspace is attached to the Branch. Use only if you actually need all the data in the branch.")
@click.option('--wait', is_flag=True, default=False, help="Waits for data branch jobs to finish, showing a progress bar. Disabled by default.")
@click.pass_context
@coro
async def data_branch(ctx, last_partition, all, wait):
    if last_partition and all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all but not both"))
        return

    if not last_partition and not all:
        click.echo(FeedbackManager.error_exception(error="Use --last-partition or --all"))
        return

    client = ctx.obj['client']
    config = ctx.ensure_object(dict)['config']

    try:
        response = await client.branch_workspace_data(config['id'], last_partition, all)
        if all:
            if 'job' not in response:
                raise click.ClickException(response)
            job_id = response['job']['job_id']
            job_url = response['job']['job_url']
            click.echo(FeedbackManager.info_data_branch_job_url(url=job_url))
            if wait:
                await wait_job(client, job_id, job_url, 'Data branching')
                await print_data_branch_summary(client, job_id)
        else:
            await print_data_branch_summary(client, None, response)
            click.echo(FeedbackManager.success_workspace_data_branch())
    except Exception as e:
        click.echo(FeedbackManager.error_exception(error=str(e)))
        return
