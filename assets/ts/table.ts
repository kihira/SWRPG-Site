import ColumnSettings = DataTables.ColumnSettings;
import ColumnMethods = DataTables.ColumnMethods;
import ColumnLegacy = DataTables.ColumnLegacy;

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

function createNumberFilter(column: ColumnMethods, name: string) {
    // Find min/max values for column
    const data = {min: 0, max: 0, column: column.index() as number};
    column.cache("search").each((value: string) => { // todo should look into why this is string and not numbers
        const num = parseInt(value, 10);
        if (num < data.min) { data.min = num; }
        else if (num > data.max) { data.max = num; }
    });

    // Create elements
    const minElem = $("<input>").addClass("number-filter")
        .attr("type", "number").attr("min", data.min).attr("max", data.max).attr("value", data.min);
    const maxElem = minElem.clone().attr("value", data.max);
    const div = $("<div>").appendTo($(".filters")).text(name);
    minElem.appendTo($("<label>").text("Min").appendTo(div));
    maxElem.appendTo($("<label>").text("Max").appendTo(div));

    // Register a new search function to handle this filter
    // todo should use one global one or create individual ones?
    $.fn.dataTable.ext.search.push((settings: DataTables.Api, searchData: any[]): boolean => {
        const min = parseInt(minElem.val() as string, 10);
        const max = parseInt(maxElem.val() as string, 10);
        const value = searchData[data.column] as number;

        return !isNaN(min) && !isNaN(max) && value >= min && value <= max;
    });
}

function createSelectFilter(column: ColumnMethods) {
    // Build list of options from data that is used for search
    const options: Set<string> = new Set();
    column.cache("search").each((value: string) => {  // gets the data that is used when searching (ie without html)
        value.split(", ").forEach((item: string) => options.add(item.split(":")[0]));
    });

    // Create the select and option elements
    const select = $("<select>")
        .attr("multiple", "multiple")
        .appendTo($(column.footer()).text(""));
    Array.from(options).sort().forEach((value: string) => {
        select.append($("<option>").attr("value", value).text(value));
    });

    // Add filter to filters section
    const label = $("<label>").text(column.header().textContent || "");
    select.appendTo(label);
    label.appendTo($(".filters"));

    // Init chosen library on it and register handler for change
    select.chosen({width: "30%"}).on("change", function(this: HTMLElement) {
        column.search(($(this).val() as string[]).join(" ")).draw();
    });
}

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

    const columns: ColumnSettings[] = [{name: "name", data: "name"}];
    const settings: DataTables.Settings = {
        fixedHeader: true,
        paging: false,
        search: {
            search: params.search || "",
        },
    };

    if (categories) {
        columns.push({name: "category", data: "category", visible: false});
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

    fields.forEach((value) => { columns.push({name: value, data: value}); });
    if (hasIndex) {
        columns.push({name: "index", data: "index"});
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

    // Technically internal APIs but can be used for auto creating
    table.settings()[0].aoColumns.forEach((column: ColumnLegacy) => {
        if (column.sType === "num") { createNumberFilter(table.column(column.idx), column.sTitle); }
        else if (column.sType === "html") { // Most likely to be a list of things that link elsewhere
            const data = table.column(column.idx).data();
            let commas = 0;
            data.each((value: string) => { commas += value.split(/,/g).length - 1; });
            if (commas > data.length / 4) { createSelectFilter(table.column(column.idx)); } // todo check ratio is good
        }
    });

    table.on("order.dt", buildUrl);
    table.on("search.dt", buildUrl);

    $(".number-filter").on("keyup change", () => table.draw());
}

// Gotta get an object defined in a <script> from the html as webpack causes stuff to lazy load if CommonsChunk
$(() => {
    init(initParams.fields, initParams.has_index, initParams.categories);
});
