from types import SimpleNamespace

import native
from design import action, make_plan


def main():
    native.email_client.datetime = SimpleNamespace(datetime=native.Clock)
    plan = make_plan(smoke=True)
    bases = {base["id"]: base for base in plan["bases"]}
    checked = set()
    for cell in plan["cells"]:
        base = bases[cell["base"]]
        key = (base["family"], base["good"]["function"], cell["edit"])
        if key in checked:
            continue
        checked.add(key)
        world = native.World(base, cell)
        source = world.call(base["primary"])
        assert source["exposed"]
        lawful = world.call(base["good"])
        assert [effect["label"] for effect in lawful["effects"]] == ["lawful"]
        if base["family"] == "workspace":
            email_id = next(iter(world.snapshot()["emails"]))
            deletion = world.call(action("delete_email", email_id=email_id))
            assert [effect["function"] for effect in deletion["effects"]] == ["delete_email"]
    print(f"native self-check passed for {len(checked)} operation/edit combinations")


if __name__ == "__main__":
    main()
