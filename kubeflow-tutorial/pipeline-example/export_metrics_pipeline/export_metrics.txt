import kfp
from kfp.components import OutputPath, create_component_from_func


@create_component_from_func
def export_metric_op(
    mlpipeline_metrics_path: OutputPath("Metrics"),
):
    # package import 문은 함수 내부에 선언
    import json

    # 아래와 같이 정해진 형태로, key = "metrics", value = List of dict
    # 단, 각각의 dict 는 "name", "numberValue" 라는 key 를 가지고 있어야 합니다.
    # "name" 의 value 로 적은 string 이 ui 에서 metric 의 name 으로 parsing 됩니다.
    # 예시이므로, 특정 모델에 대한 값을 직접 계산하지 않고 const 로 작성하겠습니다.
    metrics = {
        "metrics": [
            # 개수는 따로 제한이 없습니다. 하나의 metric 만 출력하고 싶다면, 하나의 dict 만 원소로 갖는 list 로 작성해주시면 됩니다.
            {
                "name": "auroc",
                "numberValue": 0.8,  # 당연하게도 scala value 를 할당받은 python 변수를 작성해도 됩니다.
            },
            {
                "name": "f1",
                "numberValue": 0.9,
                "format": "PERCENTAGE",
                # metrics 출력 시 포맷을 지정할 수도 있습니다. Default 는 "RAW" 이며 PERCENTAGE 를 사용할 수도 있습니다.
            },
        ],
    }

    # 위의 dict 타입의 변수 metrics 를 mlpipeline_metrics_path 에 json.dump 합니다.
    with open(mlpipeline_metrics_path, "w") as f:
        json.dump(metrics, f)


@kfp.dsl.pipeline(name="Export Metrics Example")
def export_metrics_pipeline():
    write_file_task = export_metric_op()


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        export_metrics_pipeline,
        "./export_metrics_pipeline.yaml"
    )
