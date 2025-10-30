from ruamel.yaml import YAML
from model import PatchrightConfig

yaml = YAML(typ="safe")
yaml.default_flow_style = False
yaml.allow_unicode = True
yaml.encoding = "utf-8"


class Config:
    patchright: PatchrightConfig

    def __init__(self):
        with open("./assets/config.yaml", "r", encoding="utf-8") as file:
            config: dict = yaml.load(file)

        self.patchright = PatchrightConfig(**config.get("patchright", {}))
