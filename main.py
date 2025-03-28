import threading

from agent_network.graph.graph import Graph
from flask import Flask, request
from agent_network.constant import network
import json

app = Flask(__name__)


@app.route('/service', methods=['POST'])
def service():
    context = request.json
    assert context['flowId'] is not None, "智能体流程节点未找到"
    assert context['task'] is not None, "智能体任务未找到"
    graph = Graph()
    result = graph.execute(network, context['task'], context['flowId'], context.get("params"), context.get("results", ["result"]))
    graph.release()
    return result


@app.route('/service/graph', methods=['POST'])
def service_graph():
    context = request.json
    assert context['graph'] is not None, "智能体执行图未找到"
    assert context['vertex'] is not None, "智能体流程节点未找到"
    assert context['parameterList'] is not None, "智能体流程参数未找到"
    assert context['organizeId'] is not None, "智能体流程组织架构参数未找到"
    assert context['taskId'] is not None, "智能体流程任务ID参数未找到"
    assert context['subtaskId'] is not None, "智能体流程子任务ID参数未找到"
    assert context['subtask'] is not None, "智能体流程子任务参数未找到"
    if "trace_id" not in context['graph']:
        Exception(f"task error: {context['graph']}")
    graph_dict = json.loads(context['graph'])
    graph = Graph(id=graph_dict["trace_id"])
    graph.organizeId = context['organizeId']
    graph.subtaskId = context['subtaskId']
    graph.taskId = context['taskId']
    result = graph.execute_task_call(context['subtask'], graph_dict, network, context['vertex'],
                                     context["parameterList"], context['organizeId'])
    graph.release()
    return result


@app.route('/service/summary', methods=['POST'])
def service_summary():
    context = request.json
    assert context['graph'] is not None, "智能体执行图未找到"
    assert context['vertex'] is not None, "智能体流程节点未找到"
    assert context['parameterList'] is not None, "智能体流程参数未找到"
    assert context['organizeId'] is not None, "智能体流程组织架构参数未找到"
    assert context['taskId'] is not None, "智能体流程任务ID参数未找到"
    assert context['subtaskId'] is not None, "智能体流程子任务ID参数未找到"
    assert context['subtask'] is not None, "智能体流程子任务参数未找到"
    if "trace_id" not in context['graph']:
        Exception(f"task error: {context['graph']}")
    graph_dict = json.loads(context['graph'])
    graph = Graph(id=graph_dict["trace_id"])
    graph.organizeId = context['organizeId']
    graph.subtaskId = context['subtaskId']
    graph.taskId = context['taskId']
    result = graph.execute_task_summary(context['subtask'], graph_dict, network, context['vertex'],
                                        context["parameterList"], context['organizeId'])
    graph.release()
    return result


def run_web(debug=False):
    app.run(host='0.0.0.0', port=18080, debug=debug)


if __name__ == '__main__':
    web_thread = threading.Thread(target=run_web)
    web_thread.start()
