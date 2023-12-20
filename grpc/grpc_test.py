import grpc
import service_pb2
import service_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = service_pb2_grpc.ModelStub(channel)

        model_type = "LogisticRegression"
        model_name = "model_name"
        params = {}
        data = [1.0, 2.0, 3.0]
        target = [2]

        response = stub.fit(
            service_pb2.DataParams(
                model_type=model_type,
                model_name=model_name,
                params=params,
                data=data,
                target=target,
            )
        )
        print("Fit status:", response.status)

        response = stub.predict(
            service_pb2.PredictParams(model_name=model_name, data=data)
        )
        print("Predictions:", response.predictions)

        response = stub.show(service_pb2.getModelParams(model_name='All'))
        print("Show:", response.show)

        response = stub.remove(service_pb2.getModelParams(model_name=model_name))
        print("Remove status:", response.status)


if __name__ == "__main__":
    run()
