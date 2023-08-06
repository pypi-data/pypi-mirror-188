"""Exec module for managing Network Routes"""

__func_alias__ = {"list_": "list"}

from typing import Dict
from collections import OrderedDict


async def get(hub, ctx, resource_id: str) -> Dict:
    """Gets network Routes from azure account.

    Args:
        resource_id(str):
            The resource id of the resource group.

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.network.routes.get resource_id="test-route1"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path:  aws.network.routes.get
                - kwargs:
                    resource_id: test-route1
    """

    result = dict(comment=[], ret=None, result=True)
    response_get = await hub.exec.request.json.get(
        ctx,
        url=f"{ctx.acct.endpoint_url}{resource_id}?api-version=2022-07-01",
        success_codes=[200],
    )

    if not response_get["result"]:
        result["comment"] = response_get["comment"]
        result["result"] = False
        result["ret"] = {"status": response_get["status"]}
        return result

    result["ret"] = response_get["ret"]

    return result


async def list_(
    hub,
    ctx,
) -> Dict:
    """Lists all Network Routes.

    Returns:
        Dict[str, Any]

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec azure.network.routes.list

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: azure.network.routes.list

    """

    result = dict(comment=[], ret=[], result=True)

    subscription_id = ctx.acct.subscription_id
    uri_parameters = OrderedDict(
        {
            "subscriptions": "subscription_id",
            "resourceGroups": "resource_group_name",
            "routeTables": "route_table_name",
            "routes": "route_name",
        }
    )
    async for page_result in hub.tool.azure.request.paginate(
        ctx,
        url=f"{ctx.acct.endpoint_url}/subscriptions/{subscription_id}/providers/Microsoft.Network/routeTables?api-version=2022-07-01",
        success_codes=[200],
    ):
        route_table_list = page_result.get("value", None)
        if route_table_list:
            for route_table in route_table_list:
                if route_table.get("properties") and route_table.get("properties").get(
                    "routes"
                ):
                    routes_list = route_table["properties"]["routes"]
                    for resource in routes_list:
                        resource_id = resource["id"]
                        uri_parameter_values = (
                            hub.tool.azure.uri.get_parameter_value_in_dict(
                                resource_id, uri_parameters
                            )
                        )
                        result["ret"].append(
                            hub.tool.azure.network.routes.convert_raw_routes_to_present(
                                resource=resource,
                                idem_resource_name=resource_id,
                                resource_id=resource_id,
                                **uri_parameter_values,
                            )
                        )

    return result
