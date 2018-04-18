import ColumnSettings = DataTables.ColumnSettings;
import ColumnMethods = DataTables.ColumnMethods;

interface Query {
    search?: string;
    asc?: number[];
    desc?: number[];
}

interface Column {
    header: string;
    field: string;
    filter?: { type: "select" | "number", data: string[] | Array<{ display: string, value: string }> };
    hidden?: boolean;
}

interface Entry {
    display: string;
    value: string;
}

let numberFilters: [{ min: JQuery; max: JQuery; dataField: string}];

function numberSearch(settings: DataTables.Api, searchData: any[], index: number, dataSrc: any): boolean {
    let success = true;
    numberFilters.forEach((filter) => {
        const min = parseInt(filter.min.val() as string, 10) || 0;
        const max = parseInt(filter.max.val() as string, 10) || 0;
        const value = dataSrc[filter.dataField] as number;
        if ( value < min || value > max) {
            success = false;
            return;
        }
    });
    return success;
}

function createNumberFilter(column: ColumnMethods) {
    // Find min/max values for column
    // @ts-ignore: Bad typing definition for column.index()
    const data = {min: 0, max: 0, column: column.index() as number};
    column.data().each((value: string) => {
        const num = parseInt(value, 10);
        if (num < data.min) { data.min = num; }
        else if (num > data.max) { data.max = num; }
    });

    // Create elements
    const name = column.header().textContent || "";
    const minElem = $("<input>", {
        class: "number-filter",
        id: name + "_min",
        max: data.max,
        min: data.min,
        title: "Min",
        type: "number",
        value: data.min,
    });
    const maxElem = minElem.clone().attr("value", data.max).attr("id", name + "_max").attr("title", "Max");
    const div = $("<div/>", {class: "filter"}).appendTo($(".filters")).text(name).append("<br>");
    minElem.appendTo(div);
    div.append("-");
    maxElem.appendTo(div);

    if (!numberFilters) { numberFilters = [{min: minElem, max: maxElem, dataField: column.dataSrc() as string}]; }
    else { numberFilters.push({min: minElem, max: maxElem, dataField: column.dataSrc() as string}); }
}

function createSelectFilter(column: ColumnMethods, options?: Array<Entry | string>) {
    if (!options) {
        // Build list of options from data that is used for search
        options = [];
        column.cache("search").each((value: string) => {  // gets the data that is used when searching (ie without html)
            value.split(", ").forEach((item: string) => options!.push(item.split(":")[0]));
        });
        options = options.filter((value, index, arr) => arr.indexOf(value) === index);
    }

    // Create the select and option elements
    const name = column.header().textContent || "";
    const select = $("<select>", {
        multiple: "multiple",
        title: name,
    });
    options.sort().forEach((value) => {
        select.append($("<option>")
            .attr("value", typeof value === "string" ? value : value.value)
            .text(typeof value === "string" ? value : value.display));
    });

    // Add filter to filters section
    const div = $("<div/>", {class: "filter"}).appendTo($(".filters")).text(name).append("<br>");
    select.appendTo(div);

    // Init chosen library on it and register handler for change
    select.chosen({width: "210px"}).on("change", function (this: HTMLElement) {
        column.search(($(this).val() as string[]).join(" ")).draw();
    });
}

function init(columns: Column[], hasIndex: boolean, categories: boolean) {
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

    const columnSettings: ColumnSettings[] = [{name: "name", data: "name"}];
    const settings: DataTables.Settings = {
        fixedHeader: true,
        paging: false,
        search: {
            search: params.search || "",
        },
    };

    if (categories) {
        columnSettings.push({name: "category", data: "category", visible: false});
        settings.orderFixed = {pre: [1, "asc"]};
        settings.rowGroup = {dataSrc: "category"};

        $("#categories").on("change", function(this: HTMLElement) {
            const checked = $(this).prop("checked");
            table.rowGroup().enable(checked);
            table.column("category:name").visible(!checked);
            table.order.fixed(checked ? {pre: [1, "asc"]} : {});
            table.draw();
        });
    }

    columns.forEach((value) => {
        const cs: ColumnSettings = {name: value.field, data: value.field, visible: !value.hidden};
        if (value.field === "price") {
            cs.render = (data: string, type: any, row: any) => {
                let out = "<td>";
                if (row.restricted) {
                    out += "(R) ";
                }
                out += parseInt(data, 10).toLocaleString() + "</td>";
                return out;
            };
            cs.type = "num";
        }
        columnSettings.push(cs);
    });
    if (hasIndex) {
        columnSettings.push({name: "index", data: "index"});
    }

    settings.columns = columnSettings;

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

    // Setup filters
    columns.forEach((column) => {
        if (!column.filter) { return; }
        switch (column.filter.type) {
            case "select":
                createSelectFilter(table.column(`${column.field}:name`), column.filter.data);
                break;
            case "number":
                createNumberFilter(table.column(`${column.field}:name`));
                break;
        }
    });

    // If number filters is defined, it means we have a number filter
    if (numberFilters) {
        $.fn.dataTable.ext.search.push(numberSearch);
        $(".number-filter").on("keyup change", () => table.draw());
    }
}
