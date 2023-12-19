import grpc
import service_pb2
import service_pb2_grpc

def run():
    # Подключение к серверу
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.ModelServiceStub(channel)

        # Пример использования сервиса
        response = stub.Fit(service_pb2.FitRequest(model_type='Catboost', model_name='model_name', params=None, train_data=[1.0, 2.0, 3.0], train_target=[4.0, 5.0, 6.0]))
        print("Fit:", response.status)

if __name__ == '__main__':
    run()