import kfp
from kfp.components import InputPath, OutputPath, create_component_from_func


@create_component_from_func
def write_file_op(
    data_output_path: OutputPath("dict")
):
    import json

    data = {
        "a": 300,
        "b": 10,
    }

    with open(data_output_path, "w") as f:
        json.dump(data, f)


@create_component_from_func
def read_file_and_multiply_op(
    data_input_path: InputPath("dict")
) -> float:
    import json

    with open(data_input_path, "r") as f:
        data = json.load(f)

    result = data["a"] * data["b"]

    print(f"Result: {result}")

    return result


@kfp.dsl.pipeline(name="Data Passing by File Example")
def data_passing_file_pipeline():
    write_file_task = write_file_op()
    _ = read_file_and_multiply_op(write_file_task.outputs["data_output"])


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        data_passing_file_pipeline,
        "./data_passing_file_pipeline.yaml"
    )
