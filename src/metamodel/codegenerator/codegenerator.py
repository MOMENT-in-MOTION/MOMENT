from .mapper import create_view
from .jinja_engine import build_engine, render
from metameta.api.m_m_m_classes import MetaModel
import os


def generate_Code(meta_model: MetaModel) -> dict[str, str]:

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, "templates/")

    j2_engine = build_engine(template_dir)
    context = create_view(meta_model=meta_model)
    
    dataclass_code = render(j2_engine, "dataclass_template.py.j2", context)
    enum_code = render(j2_engine, "enum_template.py.j2", context)
    
    generated_Code = {
        "dataclass_code"   : dataclass_code,
        "enum_code"         : enum_code
    }
    
    return generated_Code

