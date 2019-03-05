interface KeyDict {
    [key: string]: any;
}

class RepeatableSection {
    private readonly container: JQuery;
    private readonly template: JQuery;
    private sectionsCount: number = 0;

    constructor(template: HTMLElement) {
        this.template = $(template);

        const $addNew = $("<div>Add New</div>")
            .on("click", this.addNew);
        this.container = $("<div></div>", { class: "repeatable_container" })
            .appendTo("#repeatables")
            .append($addNew);
    }

    // todo add support for more nested documents (specifically if something has 2 of the same weapon)
    public addExisting(data: number[] | string[] | boolean[]) {
        for (const value of data) {
            const section = this.addNew();
            const input = section.get()[0].querySelector("input") as HTMLInputElement;

            if (typeof value === "number") {
                input.value = value.toString();
            }
            else if (typeof value === "string") {
                input.value = value;
            }
            else if (typeof value === "boolean") {
                input.checked = value;
            }
        }
    }

    private remove = () => {
        $(this).parent().remove();
    }

    private addNew = () => {
        this.sectionsCount += 1;
        return this.template
            .clone()
            .appendTo(this.container)
            .show()
            .find(":input")
            .each((index, element) => {
                const newId = element.id + this.sectionsCount;
                $(element).prev().attr("for", newId);
                element.id = newId;
                console.log("yay");
            })
            .end();
    }
}

const repeatableSections: { [key: string]: RepeatableSection } = {};

$(() => {
    $("fieldset")
        .each(function(this: HTMLElement) {
            repeatableSections[this.id] = new RepeatableSection(this as HTMLElement);
        });
});
