from adapters.mapping_adapter import MappingBasedAdapter
from core.engine import RCAEngine


if __name__ == "__main__":
    adapter = MappingBasedAdapter(
        config_path="adapters/configs/synthetic.yaml"
    )

    engine = RCAEngine(adapter=adapter)
    result = engine.run()

    print("\n================ RCA RESULT ================")
    print(f"Incident ID: {result['incident_id']}\n")

    print("Ranked Root Causes:")
    for rank, hypothesis, score in result["ranked_root_causes"]:
        print(f"{rank}. {hypothesis.category} | {hypothesis.description} | score={score}")

    print("\nExplanation:")
    print(result["explanation"])
    print("============================================")
