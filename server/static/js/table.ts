import ColumnSettings = DataTables.ColumnSettings;

function init(fields: string[], hasIndex: boolean, categories: boolean) {
    const params: {[key: string]: string} = {};
    location.search.substr(1).split("&").forEach((value) => { params[value.split("=")[0]] = value.split("=")[1]; });

    const settings: DataTables.Settings = {
        paging: false,
        search: {
            search: params.search || "",
        },
    };

    const columns: ColumnSettings[] = [];
    if (categories) {
        columns.push({data: "category", visible: false});
        settings.orderFixed = [0, "asc"];
        settings.rowGroup = {dataSrc: "category"};
    }
    columns.push({data: "name"});
    fields.forEach((value) => { columns.push({data: value}); });
    if (hasIndex) {
        columns.push({data: "index"});
    }
    settings.columns = columns;

    const table = $("#data").DataTable(settings);

    const buildUrl = () => {
        const url = window.location.href.split("?")[0] + "?";
        const newParams: any = {};
        table.order().forEach((col) => {
            newParams[col[0]] = col[1];
        });
        if (table.search()) {
            newParams.search = table.search();
        }
        window.history.pushState(null, "", url + $.param(newParams));
    };

    table.on("order.dt", buildUrl);
    table.on("search.dt", buildUrl);
}
