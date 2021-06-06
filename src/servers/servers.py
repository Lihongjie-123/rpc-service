import json
import sys
sys.path.append('grpc_base_models')
import grpc
import time
from concurrent import futures
from src.proto import grpcdatabase_pb2
from src.proto import grpcdatabase_pb2_grpc
# from grpc_base_models import grpcdatabase_pb2
# from grpc_base_models import grpcdatabase_pb2_grpc

_SLEEP_TIME = 60
_HOST = "0.0.0.0"
_PORT = "19999"


class RpcServer(grpcdatabase_pb2_grpc.GreeterServicer):
    def GetContent(self, request, context):
        """
        获取文章摘要
        :param request:
        :param context:
        :return:
        """
        try:
            _content = request.content
            input_dict = json.loads(_content)
            print(input_dict.keys())
            print(input_dict.values())
            print(input_dict.items())
            code = 0
        except Exception as e:
            _content = str(e)
            code=1
        return grpcdatabase_pb2.Return(message=_content,code=code)


def server():
    global _PORT
    if sys.argv.__len__()>=2:
        _PORT = sys.argv[1]
    else:
        _PORT = "19999"
    grpcServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpcdatabase_pb2_grpc.add_GreeterServicer_to_server(RpcServer(), grpcServer)
    grpcServer.add_insecure_port("{0}:{1}".format(_HOST, _PORT))
    grpcServer.start()
    try:
        while True:
            time.sleep(_SLEEP_TIME)
    except KeyboardInterrupt:
        grpcServer.stop(0)


if __name__ == '__main__':
    server()
