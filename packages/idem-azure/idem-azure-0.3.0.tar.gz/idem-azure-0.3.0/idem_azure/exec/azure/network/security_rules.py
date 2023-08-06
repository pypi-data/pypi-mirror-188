"""Exec module for managing network security_rules."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Get network security rule resource from resource_id.

    Args:
        name(str):
            The name of the Idem state.
        resource_id(str):
            The resource_id of security rule

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id:

        .. code-block:: bash

            idem exec azure.network.security_rules.get name="value" resource_id="value"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path:  azure.network.security_rules.get
                - kwargs:
                    name: "sr-1"
                    resource_id: "/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Network/networkSecurityGroups/{network_security_group_name}/securityRules/{security_rule_name}"

    """
    result = dict(comment=[], result=True, ret=None)

    response_get = await hub.exec.request.json.get(
        ctx,
        url=f"{hub.exec.azure.URL}{resource_id}?api-version=2022-07-01",
        success_codes=[200],
    )
    if not response_get["result"]:
        result["comment"] = response_get["comment"]
        result["result"] = False
        result["ret"] = {"status": response_get["status"]}
        return result

    result[
        "ret"
    ] = hub.tool.azure.network.security_rules.convert_raw_security_rules_to_present(
        resource=response_get["ret"], idem_resource_name=name
    )

    return result


async def list_(hub, ctx) -> Dict:
    """List of network security rules

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id:

        .. code-block:: bash

            idem exec azure.network.security_rules.list

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: azure.network.security_rules.list


    """
    result = dict(comment=[], result=True, ret=[])
    subscription_id = ctx.acct.subscription_id
    async for nsg_page_result in hub.tool.azure.request.paginate(
        ctx,
        url=f"{hub.exec.azure.URL}/subscriptions/{subscription_id}/providers/Microsoft.Network/networkSecurityGroups?api-version=2021-03-01",
        success_codes=[200],
    ):
        nsg_resource_list = nsg_page_result.get("value")
        if nsg_resource_list:
            for nsg_resource in nsg_resource_list:
                if nsg_resource.get("properties") and nsg_resource.get(
                    "properties"
                ).get("securityRules"):
                    for resource in nsg_resource.get("properties").get("securityRules"):
                        resource_id = resource["id"]
                        result["ret"].append(
                            hub.tool.azure.network.security_rules.convert_raw_security_rules_to_present(
                                resource=resource,
                                idem_resource_name=resource_id,
                            )
                        )
    return result
