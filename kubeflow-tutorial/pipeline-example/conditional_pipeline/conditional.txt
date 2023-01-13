import kfp
from kfp import dsl
from kfp.components import create_component_from_func


@create_component_from_func
def generate_random_op(minimum: int, maximum: int) -> int:
    import random

    result = random.randint(minimum, maximum)

    print(f"Random Integer is : {result}")
    return result


@create_component_from_func
def small_num_op(num: int):
    print(f"{num} is Small!")


@create_component_from_func
def large_num_op(num: int):
    print(f"{num} is Large!")


@dsl.pipeline(
    name='Conditional pipeline',
    description='Small or Large'
)
def conditional_pipeline():
    # generate_random_op 의 결과를 number 변수에 할당
    number = generate_random_op(0, 100).output

    # if number < 30, execute small_num_op
    with dsl.Condition(number < 30):
        small_num_op(number)
    # if number >= 30, execute large_num_op
    with dsl.Condition(number >= 30):
        large_num_op(number)


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        conditional_pipeline,
        "./conditional_pipeline.yaml"
    )
