const fs = require("fs-extra");

fs.copy("./assets/images", "./static/img/", (err) => {
    if (err) console.log(err);
});