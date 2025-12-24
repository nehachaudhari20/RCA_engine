from adapters.mapping_adapter import MappingBasedAdapter
from core.engine import RCAEngine


if __name__ == "__main__":
    adapter = MappingBasedAdapter(
        config_path="adapters/configs/synthetic.yaml"
    )

    engine = RCAEngine(adapter=adapter)
    engine.run()
