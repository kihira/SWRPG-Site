const watch = require("node-watch");
const SVGO = require("svgo");
const fs = require("fs");
const path = require("path");
const exec = require("child_process").exec;

const svgo = new SVGO();

watch('./assets/svg', {filter: /\.svg$/, recursive: true}, (evt, name) => {
    fs.readFile(name, (err, data) => {
        if (err) {
            console.error(err)
        }
        svgo.optimize(data).then(result => {
            if (result.error) {
                console.error(result.error)
            }
            else {
                const basename = path.basename(name);
                fs.writeFile(path.resolve(__dirname, 'static', 'img', basename), result.data, (err, data) => {
                    if (result.error) console.error(result.error);
                    else console.log("Optimised " + basename)
                });
            }
        })
    });
});

watch('./assets/less/style.less', (evt, name) => {
    const less = exec("npm run less");
    less.stderr.pipe(process.stderr);
    less.stdout.pipe(process.stdout);
});