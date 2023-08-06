from typing import Optional, List

import click
from imagination import container

from dnastack.alpha.client.ewes.client import EWesClient
from dnastack.alpha.client.ewes.models import ExtendedRunListOptions
from dnastack.cli.helpers.client_factory import ConfigurationBasedClientFactory
from dnastack.cli.helpers.command.decorator import command
from dnastack.cli.helpers.command.spec import ArgumentSpec
from dnastack.cli.helpers.exporter import to_json, normalize
from dnastack.cli.helpers.iterator_printer import show_iterator, OutputFormat


def _get(context_name: Optional[str] = None,
         endpoint_id: Optional[str] = None,
         namespace: Optional[str] = None) -> EWesClient:
    factory: ConfigurationBasedClientFactory = container.get(ConfigurationBasedClientFactory)
    return factory.get(EWesClient, endpoint_id=endpoint_id, context_name=context_name, namespace=namespace)


def _parse_to_datetime_iso_format(date: str, start_of_day: bool = False, end_of_day: bool = False) -> str:
    if (date is not None) and ("T" not in date):
        if start_of_day:
            return f'{date}T00:00:00.000Z'
        if end_of_day:
            return f'{date}T23:59:59.999Z'
    return date


@click.group('workbench')
def alpha_workbench_command_group():
    """ Interact with Workbench """


@click.group('runs')
def runs_command_group():
    """ EWES Runs API """


@command(runs_command_group,
         'list',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='Namespace',
                 as_option=True,
                 required=True
             ),
             ArgumentSpec(
                 name='max_results',
                 arg_names=['--max-results'],
                 help='An optional flag to limit the total number of results.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='page',
                 arg_names=['--page'],
                 help='An optional flag to set the offset page number. '
                      'This allows for jumping into an arbitrary page of results.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='page_size',
                 arg_names=['--page-size'],
                 help='An optional flag to set the page size returned by the server.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='order',
                 arg_names=['--order'],
                 help='An optional flag to define the ordering of the results. '
                      'The value should return to the attribute name to order the results by. '
                      'By default, results are returned in descending order. '
                      'To change the direction of ordering include the "ASC" or "DESC" string after the column. '
                      'e.g.: --O "end_time", --O "end_time ASC"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='states',
                 arg_names=['--state'],
                 help='An optional flag to filter the results by their state. '
                      'This flag can be defined multiple times, with the result being any of the states.',
                 as_option=True
             ),
             ArgumentSpec(
                 name='submitted_since',
                 arg_names=['--submitted-since'],
                 help='An optional flag to filter the results with their start_time '
                      'greater or equal to the since timestamp. '
                      'The timestamp can be in iso date, or datetime format. '
                      'e.g.: -f "2022-11-23", -f "2022-11-23T00:00:00.000Z"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='submitted_until',
                 arg_names=['--submitted-until'],
                 help='An optional flag to filter the results with their start_time '
                      'strictly less than the since timestamp. '
                      'The timestamp can be in iso date, or datetime format. '
                      'e.g.: -t "2022-11-23", -t "2022-11-23T23:59:59.999Z"',
                 as_option=True
             ),
             ArgumentSpec(
                 name='engine',
                 arg_names=['--engine'],
                 help='An optional flag to filter the results to runs with the given engine ID',
                 as_option=True
             ),
             ArgumentSpec(
                 name='search',
                 arg_names=['--search'],
                 help='An optional flag to perform a full text search across various fields using the search value',
                 as_option=True
             ),
         ])
def list_runs(context: Optional[str],
              endpoint_id: Optional[str],
              namespace: Optional[str],
              max_results: Optional[int],
              page: Optional[int],
              page_size: Optional[int],
              order: Optional[str],
              submitted_since: Optional[str],
              submitted_until: Optional[str],
              engine: Optional[str],
              search: Optional[str],
              states: List[str] = None):
    """ List workflow runs """
    order_direction = None
    if order:
        order_and_direction = order.split()
        if len(order_and_direction) > 1:
            order = order_and_direction[0]
            order_direction = order_and_direction[1]

    client = _get(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    list_options: ExtendedRunListOptions = ExtendedRunListOptions(
        page=page,
        page_size=page_size,
        order=order,
        direction=order_direction,
        state=states,
        since=_parse_to_datetime_iso_format(date=submitted_since, start_of_day=True),
        until=_parse_to_datetime_iso_format(date=submitted_until, end_of_day=True),
        engineId=engine,
        search=search,
    )
    show_iterator(output_format=OutputFormat.JSON, iterator=client.list_runs(list_options, max_results))


@command(runs_command_group,
         'describe',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='Namespace',
                 as_option=True,
                 required=True
             ),
             ArgumentSpec(
                 name='status',
                 arg_names=['--status'],
                 help='Output a minimal response, only showing the status id, current state, start and stop times.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='inputs',
                 arg_names=['--inputs'],
                 help='Display only the run\'s inputs as json.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='outputs',
                 arg_names=['--outputs'],
                 help='Display only the run\'s outputs as json.',
                 as_option=True,
                 default=False
             ),
             ArgumentSpec(
                 name='include_tasks',
                 arg_names=['--include-tasks'],
                 help='Include the tasks in the output.',
                 as_option=True,
                 default=False
             ),
         ])
def describe_runs(context: Optional[str],
                  endpoint_id: Optional[str],
                  namespace: Optional[str],
                  status: Optional[bool],
                  inputs: Optional[bool],
                  outputs: Optional[bool],
                  include_tasks: Optional[bool],
                  runs: List[str] = None):
    """ Describe workflow run """
    client = _get(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    described_runs = [client.get_run(run_id=run, include_tasks=include_tasks) for run in runs]
    if status:
        described_runs = [
            {
                'run_id': described_run.run_id,
                'external_id': described_run.external_id,
                'state': described_run.state,
                'tasks': described_run.task_logs
            } for described_run in described_runs
        ]
    elif inputs:
        described_runs = [
            {
                'run_id': described_run.run_id,
                'inputs': described_run.request.workflow_params,
            } for described_run in described_runs
        ]
    elif outputs:
        described_runs = [
            {
                'run_id': described_run.run_id,
                'outputs': described_run.outputs
            } for described_run in described_runs
        ]
    click.echo(to_json(normalize(described_runs)))


@command(runs_command_group,
         'cancel',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='Namespace',
                 as_option=True,
                 required=True
             )
         ])
def cancel_runs(context: Optional[str],
                endpoint_id: Optional[str],
                namespace: Optional[str],
                runs: List[str] = None):
    """Cancel one or more workflow runs"""
    client = _get(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    result = client.cancel_runs(runs)
    click.echo(to_json(normalize(result)))


@command(runs_command_group,
         'delete',
         specs=[
             ArgumentSpec(
                 name='namespace',
                 arg_names=['--namespace', '-n'],
                 help='Namespace',
                 as_option=True,
                 required=True
             ),
             ArgumentSpec(
                 name='force',
                 arg_names=['--force'],
                 help='Force the deletion without prompting for confirmation.',
                 as_option=True,
                 default=False
             )
         ])
def delete_runs(context: Optional[str],
                endpoint_id: Optional[str],
                namespace: Optional[str],
                force: Optional[bool] = False,
                runs: List[str] = None):
    """Delete one or more workflow runs"""
    client = _get(context_name=context, endpoint_id=endpoint_id, namespace=namespace)
    if not force and not click.confirm('Do you want to proceed?'):
        return
    result = client.delete_runs(runs)
    click.echo(to_json(normalize(result)))


alpha_workbench_command_group.add_command(runs_command_group)
