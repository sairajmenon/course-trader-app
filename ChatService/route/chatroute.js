const express = require("express");
const con = require("./../dbconnect");

const router = express.Router();

router.route("/").get((req, res, next) => {
  res.setHeader("Content-Type", "application/json");
  res.statusCode = 200;

    con.query("SELECT * FROM chat_tbl", function (err, result, fields) {
      if (err) throw err;
      res.json(JSON.stringify(result));
    });
  });

module.exports = router;
