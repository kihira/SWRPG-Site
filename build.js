const fs = require("fs-extra");
const path = require("path");
const csso = require("csso");
const SourceMapConsumer = require("source-map").SourceMapConsumer;
const svgo = new require("svgo")();

function buildImages() {
    fs.ensureDirSync("./static/img");

    // PNG images
    fs.copy("./assets/images", "./static/img/", (err) => {
        if (err) console.log(err);
    });

    // SVG
    fs.readdir("./assets/svg", (err, files) => {
        files.forEach((file) => {
            const data = fs.readFileSync(file);
            svgo.optimize(data)
                .then(result => {
                    if (result.error) {
                        console.error(result.error);
                    }
                    else {
                        writeFile("static/img", path.parse(name).name, result.data);
                    }
                })
                .catch((err) => console.error(err.stack));
        })
    });
}

function minifyCss(data, filename, sourceMap) {
    const result = csso.minify(data, {filename: filename, sourceMap: true, comments: false});
    if (sourceMap) {
        result.map.applySourceMap(new SourceMapConsumer(sourceMap), filename)
    }
    result.css += `\n/*# sourceMappingURL=${path.parse(filename).name}.css.map */`;
    return result
}

function buildCss() {
    fs.readFile(name, 'utf8', (err, data) => {
        const pathData = path.parse(name);
        less.render(data, {
            sourceMap: {},
            paths: [pathData.dir],
            filename: name // need to pass full path to ensure it works with @import
        })
            .then((result) => {
                result = minifyCss(result.css, pathData.base, result.map);
                writeFile("static/css", `${pathData.name}.css`, result.css);
                writeFile("static/css", `${pathData.name}.css.map`, result.map);
                console.info(`Compiled ${pathData.base}`)
            })
            .catch((err) => {
                console.error(err.stack);
            })
    });
    fs.readFile(name, "utf8", (err, data) => {
        const pathData = path.parse(name);
        const result = minifyCss(data, name);
        writeFile("static/css", `${pathData.name}.css`, result.css);
        writeFile("static/css", `${pathData.name}.css.map`, result.map);
        console.info(`Minified ${pathData.base}`)
    });
}