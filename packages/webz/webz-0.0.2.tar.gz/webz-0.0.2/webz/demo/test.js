[
    //(url前缀, 类, 是否静态类, 初始化参数)
    ("func/", servers.test.Test)
    ("page/", webz.Static, 0, ["page", "pages"])
    ("js/webz/", webz.Static, 0, ["js/webz", "webz.js"])
    ("css/webz/", webz.Static, 0, ["css/webz", "webz.css"])
]