from concurrent import futures
import grpc
import service_pb2
import service_pb2_grpc
from functions import (
    model_fit,
    model_refit,
    model_remove,
    predict,
    show,
)


class ModelServicer(service_pb2_grpc.ModelServicer):

    def fit(self, request, context):
        model_fit(request.model_type, request.model_name, request.params, request.data, request.target)
        return service_pb2.FitResponse(status="success")

    def refit(self, request, context):
        model_refit(request.model_name, request.params, request.data, request.target)
        return service_pb2.RefitResponse(status="success")

    def remove(self, request, context):
        model_remove(request.model_name)
        return service_pb2.RemoveResponse(status="success")

    def predict(self, request, context):
        predictions = predict(request.model_name, request.data)
        return service_pb2.PredictResponse(predictions=predictions)

    def show(self, request, context):
        return service_pb2.ShowResponse(show=show(request.model_name)))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ModelServicer_to_server(ModelServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()