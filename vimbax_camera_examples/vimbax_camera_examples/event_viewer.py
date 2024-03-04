# Copyright 2024 Allied Vision Technologies GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
import argparse

from vimbax_camera_events.event_subscriber import EventSubscriber
from vimbax_camera_msgs.msg import EventData


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("node_name")
    parser.add_argument("events", nargs="+")

    (args, rosargs) = parser.parse_known_args()

    rclpy.init(args=rosargs)

    node = Node("_feature_command_execute")

    event_subscriber = EventSubscriber(EventData, node, f"/{args.node_name}/events")

    def print_event_data(event):
        for entry in event.entries:
            print(f"  {entry.name}: {entry.value}")

    event_subscribtions = []

    for event_name in args.events:

        def event_callback(event):
            print(f"Got event {event_name}")
            print_event_data(event)

        event_subscribtions.append(event_subscriber.subscribe_event(event_name, event_callback))

    rclpy.spin(node)

    for event_subscribtion in event_subscribtions:
        event_subscribtion.destory()