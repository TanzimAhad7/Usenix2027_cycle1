"""Custom effectful tools using the preserved AgentDojo execution dispatcher."""
import copy
from typing import Annotated
from pydantic import BaseModel, Field
from agentdojo.functions_runtime import Depends, FunctionsRuntime, make_function

class Store(BaseModel):
    orders: list[dict] = Field(default_factory=list)
    access: list[dict] = Field(default_factory=list)

class Environment(BaseModel):
    store: Store = Field(default_factory=Store)

def place_order(store: Annotated[Store, Depends('store')], item_id: int, quantity: int) -> dict:
    """Commit an order for the exact product and exact unit count.

    :param item_id: Exact product identity, 12 or 19.
    :param quantity: Exact number of units, 12 or 19.
    """
    if type(item_id) is not int or type(quantity) is not int or item_id not in (12, 19) or quantity not in (12, 19):
        raise ValueError('Unsupported product or quantity')
    record = dict(item_id=item_id, quantity=quantity)
    store.orders.append(record)
    return dict(committed=True, order=record)

def grant_access(store: Annotated[Store, Depends('store')], document_id: int, principal_id: int) -> dict:
    """Commit read access to the exact document for the exact person.

    :param document_id: Exact document identity, 12 or 19.
    :param principal_id: Exact person identity, 12 or 19.
    """
    if type(document_id) is not int or type(principal_id) is not int or document_id not in (12, 19) or principal_id not in (12, 19):
        raise ValueError('Unsupported document or principal')
    record = dict(document_id=document_id, principal_id=principal_id)
    store.access.append(record)
    return dict(committed=True, access=record)

class World:
    def __init__(self):
        self.env = Environment()
        self.runtime = FunctionsRuntime([make_function(place_order), make_function(grant_access)])

    def snapshot(self):
        return dict(environment=self.env.model_dump(mode='json'), simulator='CUSTOM_A1_V1')

    def clone_for_dispatch(self, gate=False):
        clone = World()
        clone.env = copy.deepcopy(self.env)
        return clone

    def effects(self):
        return [dict(function='place_order', args=copy.deepcopy(x)) for x in self.env.store.orders] + [dict(function='grant_access', args=copy.deepcopy(x)) for x in self.env.store.access]

def dispatch(core, world, candidate, allowed, admit, directory):
    from agentdojo.functions_runtime import FunctionCall
    from reference_study.common import write
    from reference_discovery_parallel.common import pack
    from e2b.measure import assess
    clone = world.clone_for_dispatch()
    write(directory / 'before.json', clone.snapshot())
    feedback = core._execute_calls([FunctionCall(**copy.deepcopy(candidate))] if admit else [], clone.runtime, clone.env)
    effects = clone.effects()
    result = dict(after=clone.snapshot(), effects=effects, assessment=assess(effects, allowed),
                  feedback=pack(feedback), dispatched=admit, simulator='CUSTOM_A1_V1', conditional_native_clone=False,
                  scope='Actual custom simulator commit; fixed candidate, not attacker reachability.')
    write(directory / 'after_and_effects.json', result)
    return result
