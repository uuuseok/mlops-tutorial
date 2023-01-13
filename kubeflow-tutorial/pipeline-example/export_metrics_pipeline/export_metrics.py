import kfp
from kfp.components import OutputPath, create_component_from_func


@create_component_from_func
def export_metric_op(
    mlpipeline_metrics_path: OutputPath("Metrics"),
):
    import json
    metrics = {
        "metrics": [
            {
                "name": "auroc",
                "numberValue": 0.8,  
            },
            {
                "name": "f1",
                "numberValue": 0.9,
                "format": "PERCENTAGE",
            },
        ],
    }

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
