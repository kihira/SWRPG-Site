const watch = require("node-watch");
const SVGO = require("svgo");
const fs = require("fs");
const path = require("path");
const less = require("less");
const uglify = require("uglify-js");
const csso = require("csso");
const SourceMapConsumer = require("source-map").SourceMapConsumer;

const svgo = new SVGO();

function writeFile(directory, fileName, data) {
    fs.writeFile(path.resolve(__dirname, directory, fileName), data, (err) => {
        if (err) throw err;
    })
}

function minifyCss(data, filename, sourceMap) {
    const result = csso.minify(data, {filename: filename, sourceMap: true, comments: false});
    if (sourceMap) {
        result.map.applySourceMap(new SourceMapConsumer(sourceMap), filename)
    }
    result.css += `\n/*# sourceMappingURL=${path.parse(filename).name}.css.map */`;
    return result
}

watch('./assets/svg', {filter: /\.svg$/, recursive: true}, (evt, name) => {
    fs.readFile(name, (err, data) => {
        if (err) {
            console.error(err);
            return;
        }
        svgo.optimize(data)
            .then(result => {
                if (result.error) {
                    console.error(result.error)
                }
                else {
                    const basename = path.basename(name);
                    writeFile("static/img", basename, result.data);
                    console.log("Optimised " + basename);
                }
            })
            .catch((err) => {
                console.error(err.stack);
            })
    });
});

watch(["./assets/less/style.less", "./assets/less/edit.less"], (evt, name) => {
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
});

watch("./assets/css", {filter: /\.css$/}, (evt, name) => {
    if (!fs.existsSync(name)) return;
    fs.readFile(name, "utf8", (err, data) => {
        const pathData = path.parse(name);
        const result = minifyCss(data, name);
        writeFile("static/css", `${pathData.name}.css`, result.css);
        writeFile("static/css", `${pathData.name}.css.map`, result.map);
        console.info(`Minified ${pathData.base}`)
    });
});

// todo shouldn't watch ./static/js in the future, just parse the typescript output
watch(["./assets/js", "./static/js"], {filter: /(?<!\.min)\.js$/, recursive: true}, (evt, name) => {
    if (!fs.existsSync(name)) return;
    fs.readFile(name, "utf8", (err, data) => {
        const pathData = path.parse(name);
        const options = {sourceMap: {filename: pathData.name + "min.js", url: `${pathData.name}.min.js.map`}};
        if (fs.existsSync(name + ".map")) {
            options.sourceMap.content = fs.readFileSync(name + ".map", "utf8");
        }
        const files = {};
        files[pathData.base] = data;
        const result = uglify.minify(files, options);
        if (result.error) {
            console.error(result.error.stack);
            return;
        }
        writeFile("static/js", `${pathData.name}.min.js`, result.code);
        writeFile("static/js", `${pathData.name}.min.js.map`, result.map);
        console.info(`Minified ${pathData.base}`)
    })
});

watch("./assets/images", {recursive: true}, (evt, name) => {
    if (!fs.existsSync(name)) return;
    const pathData = path.parse(name);
    fs.copyFileSync(name, "./static/img/" + pathData.base);
});