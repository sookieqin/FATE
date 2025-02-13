#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from fate_flow.utils.api_utils import get_json_result
from fate_flow.settings import stat_logger
from arch.api.utils.dtable_utils import get_table_info
from arch.api import session
from flask import Flask, request

manager = Flask(__name__)


@manager.errorhandler(500)
def internal_server_error(e):
    stat_logger.exception(e)
    return get_json_result(retcode=100, retmsg=str(e))


@manager.route('/<table_func>', methods=['post'])
def dtable(table_func):
    config = request.json
    if table_func == 'table_info':
        table_name, namespace = get_table_info(config=config, create=config.get('create', False))
        if config.get('create', False):
            table_key_count = 0
        else:
            table = session.get_data_table(name=table_name, namespace=namespace)
            if table:
                table_key_count = table.count()
            else:
                table_key_count = 0
        return get_json_result(data={'table_name': table_name, 'namespace': namespace, 'count': table_key_count})
    else:
        return get_json_result()
