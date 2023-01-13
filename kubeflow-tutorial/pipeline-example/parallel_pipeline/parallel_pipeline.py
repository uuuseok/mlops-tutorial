import kfp
from kfp import dsl
from kfp.components import create_component_from_func


@create_component_from_func
def generate_random_list_op() -> list:
    import random

    total = random.randint(5, 10)
    result = [i for i in range(1, total)]

    return result


@create_component_from_func
def print_op(num: int):
    print(f"{num} is Generated!")


@dsl.pipeline(
    name='Parallel pipeline',
)
def parallel_pipeline():
    random_list = generate_random_list_op().output

    with dsl.ParallelFor(random_list) as item:
        print_op(item)


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        parallel_pipeline,
        "./parallel_pipeline.yaml"
    )
