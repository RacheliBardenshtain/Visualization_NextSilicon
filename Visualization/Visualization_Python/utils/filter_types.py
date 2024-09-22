import filter_factory_module
filter_types = filter_factory_module.FilterType

TIME = "Time"
THREADID = "ThreadId"
CLUSTER = "Cluster"
TIMERANGE = "TimeRange"
IO = "Io"
QUAD = "Quad"
UNIT = "Unit"
AREA = "Area"


FILTER_TYPES = {
    TIME: filter_types.Time,
    THREADID: filter_types.ThreadId,
    CLUSTER: filter_types.Cluster,
    TIMERANGE: filter_types.TimeRange,
    IO: filter_types.Io,
    QUAD: filter_types.Quad,
    UNIT: filter_types.Unit,
    AREA: filter_types.Area
}

FILTER_TYPES_NAMES = {
    TIME: filter_types.Time.name,
    THREADID: filter_types.ThreadId.name,
    CLUSTER: filter_types.Cluster.name,
    TIMERANGE: filter_types.TimeRange.name,
    IO: filter_types.Io.name,
    QUAD: filter_types.Quad.name,
    UNIT: filter_types.Unit.name,
    AREA: filter_types.Area.name
}