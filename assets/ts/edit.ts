interface KeyDict {
  [key: string]: any;
}

class RepeatableSection {
  private readonly container: JQuery;
  private template: JQuery;
  private sectionsCount: number = 0;

  constructor(fieldset: HTMLElement) {
    this.template = $(fieldset).clone();

    const $addNew = $("<div>Add New</div>")
      .on("click", this.addNew);
    this.container = $("<div></div>", { class: "repeatable_container" })
      .append($addNew);

    $(fieldset)
      .after(this.container)
      .hide();
  }

  // todo add support for more nested documents (specifically if something has 2 of the same weapon)
  public addExisting(data: number[] | string[] | boolean[]) {
    for (const value of data) {
      const section = this.addNew();
      if (typeof value === "number") {
        section.find(":input").val(value);
      }
      else if (typeof value === "string") {
        section.find(":input").val(value);
      }
      else if (typeof value === "boolean") {
        section.find(":input").prop("checked", value);
      }
    }
  }

  private remove = () => {
    $(this).parent().remove();
  };

  private addNew = () => {
    this.sectionsCount += 1;
    return this.template
      .clone()
      .find(":input")
      .each((index: number, element: HTMLElement) => {
        const newId = element.id + this.sectionsCount;
        $(element).prev().attr("for", newId);
        element.id = newId;
      })
      .end()
      .appendTo(this.container);
  };
}

const repeatableSections: { [key: string]: RepeatableSection } = {};

$(() => {
  $("fieldset")
    .each(function(this: HTMLElement) {
      repeatableSections[this.id] = new RepeatableSection(this);
    });
});
