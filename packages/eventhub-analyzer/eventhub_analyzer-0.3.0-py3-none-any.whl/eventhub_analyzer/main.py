import os
import datetime

import click
import jsonpickle
from azure.storage.blob import BlobServiceClient
import itertools
from dotenv import load_dotenv
from texttable import Texttable

load_dotenv()


class CheckpointData:
    def __init__(self, timestamp, event_hubs):
        self.timestamp = timestamp
        self.event_hubs = event_hubs


class Checkpoint:
    def __init__(self, sequence_number, offset):
        self.offset = offset
        self.sequence_number = sequence_number


class RawCheckpoint:
    def __init__(self, event_hub, consumer_group, partition_id, sequence_number, offset):
        self.event_hub = event_hub
        self.consumer_group = consumer_group
        self.offset = offset
        self.sequence_number = sequence_number
        self.partition_id = partition_id


class Ownership:
    def __init__(self, event_hub, consumer_group, partition_id, owner_id):
        self.owner_id = owner_id
        self.partition_id = partition_id
        self.consumer_group = consumer_group
        self.event_hub = event_hub


def run_checkpoint_analysis(current_timestamp, current_event_hubs, previous_timestamp, previous_event_hubs):
    difference_in_seconds = (current_timestamp - previous_timestamp).total_seconds()
    for event_hub_name in current_event_hubs:
        for consumer_group_name in current_event_hubs[event_hub_name]:

            click.echo(f"Event Hub: {event_hub_name}, Consumer Group: {consumer_group_name}")

            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_dtype(['t',
                                  't',
                                  't',
                                  'f'])
            table.set_cols_align(["l", "l", "l", "r"])
            table.add_row(["Event Hub", "Consumer Group", "Partition", "Events per second"])
            for partition_id in current_event_hubs[event_hub_name][consumer_group_name]:
                current_checkpoint = current_event_hubs[event_hub_name][consumer_group_name][partition_id]
                try:
                    previous_checkpoint = previous_event_hubs[event_hub_name][consumer_group_name][partition_id]
                    sequence_delta = current_checkpoint.sequence_number - previous_checkpoint.sequence_number
                    events_per_second = sequence_delta / difference_in_seconds
                except KeyError:
                    events_per_second = -1

                table.add_row([event_hub_name, consumer_group_name, partition_id, events_per_second])

            click.echo(table.draw())
            click.echo()


def offset_analysis():
    previous_data = load_persisted_data()

    raw_checkpoints = get_data_from_container('checkpoint')

    event_hubs = {}
    raw_checkpoints_by_event_hub = itertools.groupby(raw_checkpoints, lambda c: c.event_hub)
    for event_hub_name, raw_checkpoints_of_event_hub in raw_checkpoints_by_event_hub:
        if event_hub_name not in event_hubs:
            event_hubs[event_hub_name] = {}

        raw_checkpoints_by_consumer_group = itertools.groupby(raw_checkpoints_of_event_hub, lambda c: c.consumer_group)
        for consumer_group_name, raw_checkpoints_of_consumer_group in raw_checkpoints_by_consumer_group:

            checkpoints_by_partition_id = {}
            for raw_checkpoint in raw_checkpoints_of_consumer_group:
                checkpoints_by_partition_id[raw_checkpoint.partition_id] = Checkpoint(offset=raw_checkpoint.offset,
                                                                                      sequence_number=raw_checkpoint.sequence_number)

            event_hubs[event_hub_name][consumer_group_name] = checkpoints_by_partition_id

    persist_data(event_hubs)
    if previous_data is None:
        click.echo("No previous run found, cannot perform analysis. Wait a minute and run this command again.")
    else:
        previous_timestamp = datetime.datetime.fromisoformat(previous_data.timestamp)
        run_checkpoint_analysis(now(), event_hubs, previous_timestamp, previous_data.event_hubs)


def get_data_from_container(entity_to_get):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    offset_container_name = os.getenv('CONTAINER_NAME')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container=offset_container_name)
    blob_list = container_client.list_blobs(include='metadata')
    result = []
    for blob in blob_list:
        name = blob.name
        _, event_hub_name, consumer_group_name, entity, partition_id = name.split('/')

        if entity_to_get == entity == 'checkpoint':
            sequence_number = int(blob.metadata['sequencenumber'])
            offset = int(blob.metadata['offset'])
            checkpoint = RawCheckpoint(event_hub_name, consumer_group_name, partition_id, sequence_number, offset)
            result.append(checkpoint)

        if entity_to_get == entity == 'ownership':
            ownership = Ownership(event_hub_name, consumer_group_name, partition_id, blob.metadata['ownerid'])
            result.append(ownership)
    return result


def persist_data(event_hubs):
    timestamp = now().isoformat()
    persisted_data = CheckpointData(timestamp=timestamp, event_hubs=event_hubs)
    with open('data.json', 'w') as f:
        f.write(jsonpickle.encode(persisted_data, indent=2))


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def load_persisted_data():
    if not os.path.isfile('data.json'):
        return None
    with open('data.json', 'r') as f:
        return jsonpickle.decode(f.read())


def owner_analysis():
    ownerships = get_data_from_container('ownership')

    event_hubs = {}
    ownerships_by_event_hub = itertools.groupby(ownerships, lambda c: c.event_hub)
    for event_hub_name, ownerships_of_event_hub in ownerships_by_event_hub:
        if event_hub_name not in event_hubs:
            event_hubs[event_hub_name] = {}

        ownerships_by_consumer_group = itertools.groupby(ownerships_of_event_hub, lambda c: c.consumer_group)
        for consumer_group_name, ownerships_of_consumer_group in ownerships_by_consumer_group:

            click.echo(f"Event Hub: {event_hub_name}, Consumer Group: {consumer_group_name}")

            ownerships_by_owner_id = itertools.groupby(ownerships_of_consumer_group, lambda o: o.owner_id)
            owner_count = 0
            for owner_id, ownerships_of_owner in ownerships_by_owner_id:
                click.echo(f"{owner_id} owns {len(list(ownerships_of_owner))} partitions")
                owner_count += 1

            click.echo(f"{owner_count} owners in total")
            click.echo()


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
def offsets():
    offset_analysis()


@cli.command()
def owners():
    owner_analysis()


cli()
