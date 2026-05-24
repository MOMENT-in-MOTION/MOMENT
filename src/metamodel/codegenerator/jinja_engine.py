from jinja2 import Environment, FileSystemLoader, StrictUndefined


def build_engine(template_dir: str) -> Environment:
    """
    Create and configure a Jinja2 Environment for template rendering.

    Loads templates from the given directory and applies the following settings:
        - StrictUndefined: raises an error on any undefined variable reference
          instead of silently rendering an empty string.
        - trim_blocks: strips the first newline after a block tag ({% ... %}).
        - lstrip_blocks: strips leading whitespace from lines that begin with
          a block tag, keeping rendered output cleanly indented.

    Args:
        template_dir: Path to the directory containing the Jinja2 templates.
    """
    env = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def render(env: Environment, template_name: str, context: dict) -> str:
    """
    Render a single Jinja2 template against a given context.

    Looks up the named template inside the template directory and renders 
    it by unpacking the context dictionary as keyword arguments, making 
    every key available as a top-level variable inside the template.

    Args:
        env:           The Jinja2 Environment used to locate the template.
        template_name: Filename of the template to render.
        context:       Dictionary of variables to expose to the template.
    """
    template = env.get_template(template_name)
    return template.render(**context)
