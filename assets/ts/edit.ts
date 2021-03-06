interface KeyDict {
    [key: string]: any;
}

function insertText(symbol: string)
{
    if (lastActiveElement == null) { return; }
    const selected = $(lastActiveElement as HTMLInputElement).get(0);
    const caret = selected.selectionStart as number;
    const text = selected.value;

    selected.value = text.substr(0, caret) + symbol + text.substr(caret);
    (lastActiveElement as HTMLElement).focus();
}

class RepeatableSection {
    private readonly container: JQuery;
    private readonly template: JQuery;

    constructor(template: HTMLElement) {
        this.template = $(template);

        const $addNew = $("<div>Add New</div>")
            .on("click", this.addNew);
        this.container = $("<div></div>", { class: "repeatable_container" })
            .appendTo("#repeatables")
            .append($addNew);
    }

    // todo add support for more nested documents (specifically if something has 2 of the same weapon)
    public addExisting(data: string[]) {
        for (const value of data) {
            const section = this.addNew();
            const input = section.find("input");
            input.val(value);
        }
    }

    private remove = () => {
        $(this).parent().remove();
    }

    private addNew = () => {
        const clone = this.template.clone();
        // clone.removeUniqueId();
        clone.attr("id", null);
        clone.find("input").removeAttr("disabled");
        clone.show().appendTo(this.container);

        return clone;
    }
}

const repeatableSections: { [key: string]: RepeatableSection } = {};
let lastActiveElement: Element | null = null;

$(() => {
    $("fieldset")
        .each(function(this: HTMLElement) {
            repeatableSections[this.id] = new RepeatableSection(this as HTMLElement);
        });

    $("textarea")
        .each(function(this: HTMLElement) {
            this.onmousedown = () => lastActiveElement = this;
        });
});
