var mysql = require('mysql');

var con = mysql.createConnection({
  host: "upbeat-stratum-310102:us-central1:cloudmysql",
  user: "root",
  password: "cloudmysql",
  database: "cloudproject"
});

// con.connect(function(err) {
//   if (err) throw err;
//   console.log("Connected mysql!");
// });

// const createTcpPool = async config => {
//   // Extract host and port from socket address
//   // Establish a connection to the database
//   return await mysql.createPool({
//     user: "root", // e.g. 'my-db-user'
//     password: "clousmysql", // e.g. 'my-db-password'
//     database: "chat", // e.g. 'my-database'
//     host: "upbeat-stratum-310102:us-central1:cloudmysql", // e.g. '127.0.0.1'
//     port: 3306, // e.g. '3306'
//   });
// };


module.exports = con;
