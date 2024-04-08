from typing import TypedDict


# Contains all the key-value pairs meaningful in a config file.
# Added LambdaAddress and APIKey to ConfigValues for syntax errors
class ConfigValues(TypedDict):
    CmpDomain: bool
    EqWildcard: bool
    ImpliedExpression: bool
    InconsistentExpression: bool
    StrangeHaving: bool
    SubqueryOrderBy: bool
    SubquerySelect: bool
    SumDistinct: bool
    LambdaAddress: str
    APIKey: str