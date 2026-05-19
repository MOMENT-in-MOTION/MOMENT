from jinja2 import Environment, FileSystemLoader, StrictUndefined


def build_engine(template_dir: str) -> Environment:
    env = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def render(env: Environment, template_name: str, context: dict) -> str:
    template = env.get_template(template_name)
    return template.render(**context)
