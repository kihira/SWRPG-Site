import ColumnSettings = DataTables.ColumnSettings;
import * as $ from "jquery";

import "datatables.net";
import "datatables.net-fixedheader";
import "datatables.net-rowgroup";

interface Query {
    search?: string;
    asc?: number[];
    desc?: number[];
}

interface InitParams {
    fields: string[];
    has_index: boolean;
    categories: boolean;
}

declare var initParams: InitParams;

function init(fields: string[], hasIndex: boolean, categories: boolean) {
    const params: Query = {};
    location.search.substr(1).split("&").forEach((value) => {
        const data = value.split("=");
        if (data[0] === "search") {
            params.search = data[1];
        }
        switch (data[0]) {
            case "search":
                params.search = data[1];
                break;
            case "asc":
                params.asc = data[1].split(/_/).map((value2) => parseInt(value2, 10));
                break;
            case "desc":
                params.desc = data[1].split(/_/).map((value2) => parseInt(value2, 10));
                break;
        }
    });

    const columns: ColumnSettings[] = [{data: "name"}];
    const settings: DataTables.Settings = {
        fixedHeader: true,
        paging: false,
        search: {
            search: params.search || "",
        },
    };

    if (categories) {
        columns.push({data: "category", visible: false});
        settings.orderFixed = [1, "asc"];
        settings.rowGroup = {dataSrc: "category"};
    }

    fields.forEach((value) => { columns.push({data: value}); });
    if (hasIndex) {
        columns.push({data: "index"});
    }

    settings.columns = columns;

    // Set default order based on query string
    const order: Array<Array<(number | string)>> = [];
    if (params.desc) {
        params.desc.forEach((value) => {
            order.push([value, "desc"]);
        });
    }
    if (params.asc) {
        params.asc.forEach((value) => {
            order.push([value, "asc"]);
        });
    }
    settings.order = order;

    const table = $("#data").DataTable(settings);

    const buildUrl = () => {
        const url = window.location.href.split("?")[0] + "?";
        const newParams: { search?: string, asc?: string, desc?: string } = {};

        const asc: number[] = [];
        const desc: number[] = [];
        table.order().forEach((col: Array<(string | number)>) => {
            if (col[1] === "asc") {
                asc.push(col[0] as number);
            }
            else if (col[1] === "desc") {
                desc.push(col[0] as number);
            }
        });
        if (asc.length > 0) {
            newParams.asc = asc.join("_");
        }
        if (desc.length > 0) {
            newParams.desc = desc.join("_");
        }

        if (table.search()) {
            newParams.search = table.search();
        }

        window.history.pushState(null, "", url + $.param(newParams));
    };

    table.on("order.dt", buildUrl);
    table.on("search.dt", buildUrl);
}

// Gotta get an object defined in a <script> from the html as webpack causes stuff to lazy load if CommonsChunk
$(() => {
    init(initParams.fields, initParams.has_index, initParams.categories);
});
